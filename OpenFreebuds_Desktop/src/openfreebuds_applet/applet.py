import logging
import os
from io import StringIO

import pystray

import openfreebuds.manager
import openfreebuds_backend
from openfreebuds import event_bus
from openfreebuds.events import EVENT_UI_UPDATE_REQUIRED, EVENT_DEVICE_PROP_CHANGED, EVENT_MANAGER_STATE_CHANGED
from openfreebuds_applet import tools, settings, icons, tool_server, tool_hotkeys, tool_update
from openfreebuds_applet.l18n import t
from openfreebuds_applet.ui.menu_device import DeviceMenu
from openfreebuds_applet.ui.menu_no_device import DeviceOfflineMenu, DeviceScanMenu
from openfreebuds_applet.ui.menu_app import ApplicationMenuPart
from openfreebuds_applet.ui.base import HeaderMenuPart, QuitingMenu

log = logging.getLogger("Applet")


class FreebudsApplet:
    def __init__(self):
        super().__init__()
        self.started = False
        self.allow_ui_update = False
        self.current_menu_hash = ""
        self.current_icon_hash = ""

        self.settings = settings.SettingsStorage()
        self.log = StringIO()

        self.manager = openfreebuds.manager.create()
        self.manager.safe_run_wrapper = tools.run_thread_safe

        self.menu_app = ApplicationMenuPart(self)
        self.menu_header = HeaderMenuPart(self)
        self.menu_offline = DeviceOfflineMenu(self)
        self.menu_scan = DeviceScanMenu(self)
        self.menu_device = DeviceMenu(self)

        self._tray = pystray.Icon(name="OpenFreebuds",
                                  title="OpenFreebuds",
                                  icon=icons.generate_icon(1),
                                  menu=pystray.Menu())

    def start(self):
        icons.set_theme(self.settings.theme)

        tool_hotkeys.start(self)
        tool_server.start(self)
        tool_update.start(self)

        if self.settings.enable_debug_features:
            self.start_debug()

        tools.run_thread_safe(self._ui_update_loop, "Applet", True)
        self._tray.run()

    def start_debug(self):
        log.debug("Setup log stram")
        handler = logging.StreamHandler(self.log)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(threadName)s  %(message)s"))
        for a in ["SPPDevice", "FreebudsManager"]:
            logging.getLogger(a).addHandler(handler)

    def exit(self):
        log.info("Exiting this app...")
        items = QuitingMenu().build()
        menu = pystray.Menu(*items)
        self._tray.menu = menu

        self.allow_ui_update = False
        self.started = False
        event_bus.invoke(EVENT_UI_UPDATE_REQUIRED)

    def update_icon(self):
        if not self.allow_ui_update:
            return

        mgr_state = self.manager.state
        battery = 0
        noise_mode = 0

        if mgr_state == self.manager.STATE_CONNECTED:
            dev = self.manager.device

            battery_left = dev.get_property("battery_left", 0)
            battery_right = dev.get_property("battery_right", 0)
            if battery_left == 0:
                battery_left = 100
            if battery_right == 0:
                battery_right = 100
            noise_mode = dev.get_property("noise_mode", 0)
            battery = min(battery_right, battery_left)

        new_hash = icons.get_hash(mgr_state, battery, noise_mode)
        if self.current_icon_hash == new_hash:
            return

        self._tray.icon = icons.generate_icon(mgr_state, battery, noise_mode)
        self.current_icon_hash = new_hash

    def apply_menu(self, menu):
        if not self.allow_ui_update:
            return

        items = self.menu_header.build()
        items += menu.build()
        items += self.menu_app.build()

        items_hash = tools.items_hash_string(items)

        if self.current_menu_hash != items_hash:
            menu = pystray.Menu(*items)

            self.current_menu_hash = items_hash
            self._tray.menu = menu

            log.debug("Menu updated, hash=" + items_hash)

    def _ui_update_loop(self):
        self.started = True
        self.allow_ui_update = True

        event_queue = event_bus.register([
            EVENT_UI_UPDATE_REQUIRED,
            EVENT_DEVICE_PROP_CHANGED,
            EVENT_MANAGER_STATE_CHANGED
        ])

        if self.settings.address != "":
            log.info("Using saved address: " + self.settings.address)
            self.manager.set_device(self.settings.address)
        else:
            openfreebuds_backend.show_message(t("first_run_message"))

        while self.started:
            self.update_icon()
            if self.manager.state == self.manager.STATE_NO_DEV:
                self.apply_menu(self.menu_scan)
            elif self.manager.state == self.manager.STATE_CONNECTED:
                self.apply_menu(self.menu_device)
            else:
                self.apply_menu(self.menu_offline)
            event_queue.wait()

        self.manager.close()
        self._tray.stop()
        log.info("Tray stopped, exiting...")

        # noinspection PyProtectedMember,PyUnresolvedReferences
        os._exit(0)
