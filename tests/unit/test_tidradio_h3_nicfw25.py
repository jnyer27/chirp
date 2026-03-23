# Copyright 2026 RadioDroid — unit tests for TD-H3 nicFW 2.5 mode/bandwidth mapping
import unittest

from chirp import chirp_common, memmap
from chirp.drivers import tidradio_h3_nicfw25 as h3


class TestH3FwChirpModeMap(unittest.TestCase):
    def test_fw_to_chirp_fm_am_auto_usb(self):
        self.assertEqual(h3._fw_channel_mode_to_chirp(1, False), "FM")
        self.assertEqual(h3._fw_channel_mode_to_chirp(1, True), h3.NFM)
        self.assertEqual(h3._fw_channel_mode_to_chirp(2, False), "AM")
        self.assertEqual(h3._fw_channel_mode_to_chirp(2, True), h3.NAM)
        self.assertEqual(h3._fw_channel_mode_to_chirp(0, False), "Auto")
        self.assertEqual(h3._fw_channel_mode_to_chirp(0, True), "Auto")
        self.assertEqual(h3._fw_channel_mode_to_chirp(3, False), "USB")
        self.assertEqual(h3._fw_channel_mode_to_chirp(3, True), "USB")

    def test_chirp_to_fw_nfm_nam(self):
        m = chirp_common.Memory()
        m.mode = h3.NFM
        self.assertEqual(h3._chirp_mode_to_fw_channel(m), (1, True))
        m.mode = h3.NAM
        self.assertEqual(h3._chirp_mode_to_fw_channel(m), (2, True))
        m.mode = "FM"
        self.assertEqual(h3._chirp_mode_to_fw_channel(m), (1, False))

    def test_valid_modes_includes_narrow(self):
        r = h3.TH3NicFw25(None)
        rf = r.get_features()
        self.assertIn(h3.NFM, rf.valid_modes)
        self.assertIn(h3.NAM, rf.valid_modes)


class TestH3EepromRoundTrip(unittest.TestCase):
    def _fresh_mmap(self):
        data = bytearray(8192)
        data[0x1900] = 0xD8
        data[0x1901] = 0x2F
        # Slot 1 @ 0x40: non-zero RX/TX so get_memory builds mem.extra (not early-empty).
        f10 = 14652000  # 146.520 MHz in 10 Hz units
        data[0x40:0x44] = f10.to_bytes(4, "big")
        data[0x44:0x48] = f10.to_bytes(4, "big")
        return memmap.MemoryMapBytes(bytes(data))

    def test_set_get_nfm(self):
        r = h3.TH3NicFw25(self._fresh_mmap())
        r.process_mmap()
        mem = chirp_common.Memory()
        mem.number = 1
        mem.empty = False
        mem.freq = 146520000
        mem.duplex = ""
        mem.offset = 0
        mem.mode = h3.NFM
        mem.power = "1"
        mem.name = "T"
        mem.tmode = ""
        r.set_memory(mem)
        out = r.get_memory(1)
        self.assertFalse(out.empty)
        self.assertEqual(out.mode, h3.NFM)

    def test_set_get_fm_narrow_via_extra(self):
        r = h3.TH3NicFw25(self._fresh_mmap())
        r.process_mmap()
        mem = r.get_memory(1)
        self.assertFalse(mem.empty)
        mem.mode = "FM"
        mem.power = "1"
        mem.name = "X"
        mem.tmode = ""
        for item in mem.extra:
            if item.get_name() == "bandwidth" and hasattr(item.value, "set_value"):
                item.value.set_value("Narrow")
        r.set_memory(mem)
        out = r.get_memory(1)
        self.assertEqual(out.mode, h3.NFM)


if __name__ == "__main__":
    unittest.main()
