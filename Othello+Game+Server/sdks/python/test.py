import unittest
import client

class TestGetMove(unittest.TestCase):
  # def test_get_move_returns_a_valid_move(self):
  #   board = [[1, 1, 1, 1, 1, 1, 1, 0], [2, 1, 2, 1, 2, 2, 2, 2], [2, 2, 1, 2, 2, 2, 2, 2], [2, 2, 1, 2, 2, 2, 1, 2], [2, 2, 2, 1, 2, 1, 1, 2], [2, 2, 2, 2, 1, 2, 1, 2], [2, 2, 2, 2, 2, 1, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2]]
  #   self.assertEqual(client.get_move(1, board), [0, 7])

  def test_get_move_returns_a_valid_move2(self):
    board = [[2, 0, 2, 2, 2, 2, 2, 2], [1, 2, 1, 1, 1, 1, 2, 2], [1, 1, 2, 2, 1, 2, 2, 2], [1, 1, 1, 2, 1, 2, 2, 2], [1, 1, 1, 1, 2, 2, 2, 2], [1, 2, 1, 2, 2, 1, 1, 1], [1, 1, 1, 1, 2, 2, 1, 1], [0, 2, 1, 1, 1, 1, 1, 1]]
    self.assertEqual(client.get_move(1, board), [7, 0])

# class TestPrepareResponse(unittest.TestCase):
#   def test_prepare_response_returns_a_valid_response(self):
#     self.assertEqual(client.prepare_response([2, 3]), b'[2, 3]\n')

if __name__ == '__main__':
  unittest.main()
