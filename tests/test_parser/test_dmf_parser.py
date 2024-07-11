import unittest

from py3comtrade.parser.dmf_parser import DmfParser


class TestDMFParser(unittest.TestCase):
    def setUp(self):
        file_name = '../data/xtz.dmf'
        self.parser = DmfParser(file_name)

    def test_get_line(self):
        test_data = 0
        parsed_data = self.parser.get_line(test_data)
        expected_output = {
            "cfg_an": 4,
            "name": "xyx",
            "bus_idx": 1,
            "bus_name": "220kV I母线",
            "_type": 'A',
            "isUse": True,
            "acvchn": [1, 2, 3, 4],
            "accchn": [13, 14, 15, 16],
            "stachn": [33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44],
            "rx": {'r0': '0.2717', 'r1': '0.0893', 'x0': '0.6384', 'x1': '0.3074'}
        }
        self.assertEqual(parsed_data, expected_output,
                         msg="get_buses_name函数的输出与预期不符")

    def test_lines_name(self):
        parsed_data = self.parser.get_lines_name()[1]
        expected_output = "fx2x"
        self.assertEqual(parsed_data, expected_output,
                         msg="get_lines_name函数的输出与预期不符")

    def test_get_line_index(self):
        test_data = "fx1x"
        parsed_data = self.parser.get_line_index(test_data)
        expected_output = 2
        self.assertEqual(parsed_data, expected_output,
                         msg="get_lines_index函数的输出与预期不符")

    def test_get_buses_name(self):
        parsed_data = self.parser.get_buses_name()[1]
        expected_output = "220kV II母线"
        self.assertEqual(parsed_data, expected_output,
                         msg="get_buses_name函数的输出与预期不符")

    def test_get_bus_index_of_dmf_id(self):
        test_data = 2
        parsed_data = self.parser.get_bus_index_of_dmf_id(test_data)
        expected_output = 1
        self.assertEqual(parsed_data, expected_output,
                         msg="get_bus_index_of_dmf_id函数的输出与预期不符")

    def test_get_bus_index_of_name(self):
        test_data = "220kV II母线"
        parsed_data = self.parser.get_bus_index_of_name(test_data)
        expected_output = 1
        self.assertEqual(parsed_data, expected_output,
                         msg="get_bus_index_of_name函数的输出与预期不符")

    def test_bus_name(self):
        test_data = 1
        parsed_data = self.parser.get_bus_name(test_data)
        expected_output = "220kV II母线"
        self.assertEqual(parsed_data, expected_output,
                         msg="get_bus_name函数的输出与预期不符")

    def test_get_bus_voltage_channels(self):
        test_data = 0
        parsed_data = self.parser.get_bus_voltage_channels(test_data)
        expected_output = [1, 2, 3, 4]
        self.assertEqual(parsed_data, expected_output,
                         msg="get_bus_voltage_channels函数的输出与预期不符")

    def test_get_bus(self):
        test_data = 0
        parsed_data = self.parser.get_bus(test_data)
        expected_output = {
            "cfg_an": 1,
            "name": "220kV I母线",
            "_type": 'V',
            "isUse": True,
            "acvchn": [1, 2, 3, 4],
            "stachn": [1, 3]
        }
        self.assertEqual(parsed_data, expected_output,
                         msg="get_bus_voltage_channels函数的输出与预期不符")


if __name__ == '__main__':
    unittest.main()
    # suite = unittest.TestSuite()
    # suite.addTest(TestDMFParser("test_get_buses_name"))
    # unittest.TextTestRunner().run(suite)
