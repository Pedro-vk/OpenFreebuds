CMD_BATTERY_READ = b"\x01\x08"
CMD_BATTERY_NOTIFY = b"\x01\x27"
CMD_AUTO_PAUSE_READ = b"\x2b\x11"
CMD_AUTO_PAUSE_WRITE = b"\x2b\x10"
CMD_DUAL_TAP_READ = b"\x01\x20"
CMD_DUAL_TAP_WRITE = b"\x01\x1f"
CMD_TRIPLE_TAP_READ = b"\x01\x26"
CMD_TRIPLE_TAP_WRITE = b"\x01\x25"
CMD_LONG_TAP_SPLIT_READ_BASE = b"\x2b\x17"
CMD_LONG_TAP_SPLIT_READ_ANC = b"\x2b\x19"
CMD_LONG_TAP_SPLIT_WRITE_BASE = b"\x2b\x16"
CMD_LONG_TAP_SPLIT_WRITE_ANC = b"\x2b\x18"
CMD_SWIPE_READ = b"\x2b\x1f"
CMD_SWIPE_WRITE = b"\x2b\x1e"
CMD_LOW_LATENCY = b"\x2b\x6c"
CMD_DUAL_CONNECT_ENABLED_READ = b"\x2b\x2f"
CMD_DUAL_CONNECT_ENABLED_WRITE = b"\x2b\x2e"
CMD_DUAL_CONNECT_ENUMERATE = b"\x2b\x31"
CMD_DUAL_CONNECT_PREFERRED_WRITE = b"\x2b\x32"
CMD_DUAL_CONNECT_EXECUTE = b"\x2b\x33"
CMD_DUAL_CONNECT_CHANGE_EVENT = b"\x2b\x36"