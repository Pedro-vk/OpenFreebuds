import asyncio
import sys
from typing import Optional

from PyQt6.QtGui import QIcon, QKeySequence
from PyQt6.QtWidgets import QMenu
from qasync import asyncSlot

from openfreebuds import IOpenFreebuds, OfbEventKind
from openfreebuds.utils.logger import create_logger
from openfreebuds_qt.app.dialog.manual_connect import OfbQtManualConnectDialog
from openfreebuds_qt.app.helper import OfbQtSettingsTabHelper
from openfreebuds_qt.app.module import OfbQtAboutModule, OfbQtSoundQualityModule, OfbQtLinuxExtrasModule, \
    OfbQtHotkeysModule, OfbQtGesturesModule, OfbEmptyModule, OfbQtDualConnectModule, OfbQtDeviceOtherSettingsModule, \
    OfbQtDeviceInfoModule, OfbQtCommonModule, OfbQtChooseDeviceModule
from openfreebuds_qt.constants import ASSETS_PATH
from openfreebuds_qt.designer.main_window import Ui_OfbMainWindowDesign
from openfreebuds_qt.generic import IOfbQtApplication, IOfbMainWindow
from openfreebuds_qt.utils import qt_error_handler, OfbCoreEvent, OfbQtReportTool, get_qt_icon_colored

log = create_logger("OfbQtMainWindow")

WIN32_BODY_STYLE = "QPushButton, QComboBox { padding: 6px 12px; }"


class OfbQtMainWindow(Ui_OfbMainWindowDesign, IOfbMainWindow):
    def __init__(self, ctx: IOfbQtApplication):
        super().__init__()

        self.ctx = ctx
        self.ofb = ctx.ofb
        self._exit_started: bool = False

        self.setupUi(self)

        # Win32 staff
        self.setWindowIcon(QIcon(str(ASSETS_PATH / "icon.png")))
        if sys.platform == "win32":
            self.body_content.setStyleSheet(WIN32_BODY_STYLE)

        # Extras button
        self.extra_options_button.setIcon(
            get_qt_icon_colored("settings", self.palette().text().color().getRgb())
        )

        self.extra_menu = QMenu()
        self.extra_options_button.setMenu(self.extra_menu)
        self._fill_extras_menu()

        self.tabs = OfbQtSettingsTabHelper(self.tabs_list_content, self.body_content)

        self._ui_update_task: Optional[asyncio.Task] = None
        self._ui_modules: list[OfbQtCommonModule] = []

        # Header section
        if self.ctx.ofb.role == "standalone":
            self._attach_module(self.tr("Select device"), OfbQtChooseDeviceModule(self.tabs.root, self.ctx))

        # Device-related modules
        self.device_section = self.tabs.add_section("")
        self._attach_module(self.tr("Device info"), OfbQtDeviceInfoModule(self.tabs.root, self.ctx))
        self._attach_module(self.tr("Dual-connect"), OfbQtDualConnectModule(self.tabs.root, self.ctx))
        self._attach_module(self.tr("Gestures"), OfbQtGesturesModule(self.tabs.root, self.ctx))
        self._attach_module(self.tr("Sound quality"), OfbQtSoundQualityModule(self.tabs.root, self.ctx))
        self._attach_module(self.tr("Other settings"), OfbQtDeviceOtherSettingsModule(self.tabs.root, self.ctx))

        # App-related modules
        self.tabs.add_section(self.tr("Application"))
        self._attach_module(self.tr("User interface"), OfbEmptyModule(self.tabs.root, self.ctx))
        if OfbQtHotkeysModule.available():
            self._attach_module(self.tr("Keyboard shortcuts"), OfbQtHotkeysModule(self.tabs.root, self.ctx))
        if sys.platform == "linux":
            self._attach_module(self.tr("Linux-related"), OfbQtLinuxExtrasModule(self.tabs.root, self.ctx))
        self._attach_module(self.tr("About..."), OfbQtAboutModule(self.tabs.root, self.ctx))

        # Finish
        self.default_tab = 2, 0
        self.tabs.finalize_list()
        self.tabs.set_active_tab(*self.default_tab)

    def _fill_extras_menu(self):
        bugreport_action = self.extra_menu.addAction(self.tr("Bugreport..."))
        bugreport_action.setShortcut("F2")
        # noinspection PyUnresolvedReferences
        bugreport_action.triggered.connect(self.on_bugreport)

        temp_device_action = self.extra_menu.addAction(self.tr("Temporary replace device"))
        temp_device_action.setShortcut("Ctrl+D")
        # noinspection PyUnresolvedReferences
        temp_device_action.triggered.connect(self.temporary_change_device)

        self.extra_menu.addSeparator()
        hide_action = self.extra_menu.addAction(self.tr("Close this window"))
        hide_action.setShortcut(QKeySequence('Ctrl+W'))
        # noinspection PyUnresolvedReferences
        hide_action.triggered.connect(self.hide)

        exit_action = self.extra_menu.addAction(self.tr("Exit OpenFreebuds"))
        exit_action.setShortcut(QKeySequence('Ctrl+Q'))
        # noinspection PyUnresolvedReferences
        exit_action.triggered.connect(self.on_exit)

    @asyncSlot()
    async def temporary_change_device(self):
        async with qt_error_handler("OfbQtMain_TempConnect", self.ctx):
            result, name, address = await OfbQtManualConnectDialog(self).get_user_response()
            if not result:
                return
            await self.ctx.ofb.start(name, address)

    @asyncSlot()
    async def on_bugreport(self):
        await OfbQtReportTool(self.ctx).create_and_show()

    @asyncSlot()
    async def on_exit(self):
        async with qt_error_handler("OfbQtMain_OnExit", self.ctx):
            await self.ctx.exit()

    def _attach_module(self, label: str, module: OfbQtCommonModule):
        entry = self.tabs.add_tab(label, module)
        self._ui_modules.append(module)
        module.list_item = entry.list_item

    async def boot(self):
        async with qt_error_handler("OfbQtMain_Boot", self.ctx):
            await self._update_ui(OfbCoreEvent(None))

    async def _update_ui(self, event: OfbCoreEvent):
        if event.kind_match(OfbEventKind.STATE_CHANGED):
            visible = await self.ofb.get_state() == IOpenFreebuds.STATE_CONNECTED
            self._device_section_set_visible(visible)

        for mod in self._ui_modules:
            try:
                await mod.update_ui(event)
            except Exception:
                log.exception(f"Failed to update UI {mod}")

    async def _update_loop(self):
        """
        Background task that will subscribe to core event bus and watch
        for changes to perform settings UI update
        """

        async with qt_error_handler("OfbQtSettings_UpdateLoop", self.ctx):
            member_id = await self.ctx.ofb.subscribe()
            log.info(f"Settings UI update loop started, member_id={member_id}")

            # First-time force update everything
            await self._update_ui(OfbCoreEvent(None))

            try:
                while True:
                    kind, *args = await self.ofb.wait_for_event(member_id)
                    await self._update_ui(OfbCoreEvent(kind, *args))
            except asyncio.CancelledError:
                await self.ofb.unsubscribe(member_id)
                log.info("Settings UI update loop finished")

    def _device_section_set_visible(self, visible):
        self.device_section.set_visible(visible)
        if not visible and self.tabs.active_tab.section == self.device_section:
            self.tabs.set_active_tab(*self.default_tab)

    def closeEvent(self, e):
        if self.isVisible():
            e.ignore()
            self.hide()
            return

    def showEvent(self, e):
        e.accept()
        self._ui_update_task = asyncio.create_task(self._update_loop())

    def hideEvent(self, e):
        e.accept()
        if self._ui_update_task is not None:
            self._ui_update_task.cancel()
