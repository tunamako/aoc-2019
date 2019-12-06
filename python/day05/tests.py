import os
import sys
import unittest

from day05 import AdventMachine


class TestAdventMachine(unittest.TestCase):

	def setUp(self):
		self.test_machine = AdventMachine(return_output=True)

	def _test_data_helper(self, tape, data):

		for _input, expected in data:
			self.test_machine.reinit(tape, _input)
			self.assertEqual(self.test_machine.execute(), expected)

	def test_PosEq(self):
		tape = [3,9,8,9,10,9,4,9,99,-1,8]
		data = [(8, [1]), (9, [0]), (7, [0])]
		self._test_data_helper(tape, data)

	def test_PosLess(self):
		tape = [3,9,7,9,10,9,4,9,99,-1,8]
		data = [(2, [1]), (10, [0]), (8, [0])]
		self._test_data_helper(tape, data)

	def test_ImEq(self):
		tape = [3,3,1108,-1,8,3,4,3,99] 
		data = [(8, [1]), (9, [0]), (7, [0])]
		self._test_data_helper(tape, data)

	def test_ImLess(self):
		tape = [3,3,1107,-1,8,3,4,3,99] 
		data = [(7, [1]), (8, [0]), (9, [0])]
		self._test_data_helper(tape, data)

	def test_JMP(self):
		tape = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
		data = [(0, [0]), (1, [1]), (2, [1])]
		self._test_data_helper(tape, data)

		tape = [3,3,1105,-1,9,1101,0,0,12,4,12,99,1]
		data = [(0, [0]), (1, [1]), (2, [1])]
		self._test_data_helper(tape, data)

	def test_All(self):
		tape = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
		data = [(7, [999]), (8, [1000]), (9, [1001])]
		self._test_data_helper(tape, data)


if __name__ == "__main__":
	unittest.main(buffer=True)