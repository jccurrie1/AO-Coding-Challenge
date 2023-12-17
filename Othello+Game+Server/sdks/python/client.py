#!/usr/bin/python

import sys
import json
import socket

valid_moves = []
static_weight = [
  [100, -30, 6, 2, 2, 6, -30, 100],
  [-30, -50, 0, 0, 0, 0, -50, -30],
  [6, 0, 0, 0, 0, 0, 0, 6],
  [2, 0, 0, 3, 3, 0, 0, 2],
  [2, 0, 0, 3, 3, 0, 0, 2],
  [6, 0, 0, 0, 0, 0, 0, 6],
  [-30, -50, 0, 0, 0, 0, -50, -30],
  [100, -30, 6, 2, 2, 6, -30, 100]
]

def get_move(player, board):
  valid_moves.clear()

  # horizontal
  check_for_valid_move(player, board, start_x=0, end_x=8, step_x=1, second_coordinate_change_x=0, third_coordinate_change_x=0, start_y=0, end_y=6, step_y=1, second_coordinate_change_y=1, third_coordinate_change_y=2) # left to right
  check_for_valid_move(player, board, start_x=0, end_x=8, step_x=1, second_coordinate_change_x=0, third_coordinate_change_x=0, start_y=7, end_y=1, step_y=-1, second_coordinate_change_y=-1, third_coordinate_change_y=-2) # right to left

  # vertical
  check_for_valid_move(player, board, start_x=0, end_x=6, step_x=1, second_coordinate_change_x=1, third_coordinate_change_x=2, start_y=0, end_y=8, step_y=1, second_coordinate_change_y=0, third_coordinate_change_y=0) # top to bottom
  check_for_valid_move(player, board, start_x=7, end_x=1, step_x=-1, second_coordinate_change_x=-1, third_coordinate_change_x=-2, start_y=0, end_y=8, step_y=1, second_coordinate_change_y=0, third_coordinate_change_y=0) # bottom to top

  # diagonal
  check_for_valid_move(player, board, start_x=0, end_x=6, step_x=1, second_coordinate_change_x=1, third_coordinate_change_x=2, start_y=0, end_y=6, step_y=1, second_coordinate_change_y=1, third_coordinate_change_y=2) # top left to bottom right
  check_for_valid_move(player, board, start_x=0, end_x=6, step_x=1, second_coordinate_change_x=1, third_coordinate_change_x=2, start_y=7, end_y=1, step_y=-1, second_coordinate_change_y=-1, third_coordinate_change_y=-2) # top right to bottom left
  check_for_valid_move(player, board, start_x=7, end_x=1, step_x=-1, second_coordinate_change_x=-1, third_coordinate_change_x=-2, start_y=7, end_y=1, step_y=-1, second_coordinate_change_y=-1, third_coordinate_change_y=-2) # bottom right to top left
  check_for_valid_move(player, board, start_x=7, end_x=1, step_x=-1, second_coordinate_change_x=-1, third_coordinate_change_x=-2, start_y=0, end_y=6, step_y=1, second_coordinate_change_y=1, third_coordinate_change_y=2) # bottom left to top right

  # Map valid moves to their respective weights
  weights = {tuple(move): static_weight[move[0]][move[1]] for move in valid_moves}
  best_move = max(weights, key=weights.get)

  return list(best_move)

def check_for_valid_move(player, board, start_x, end_x, step_x, second_coordinate_change_x, third_coordinate_change_x, start_y, end_y, step_y, second_coordinate_change_y, third_coordinate_change_y):
  for x in range(start_x, end_x, step_x):
    for y in range(start_y, end_y, step_y):
      if board[x][y] == player and board[x+second_coordinate_change_x][y+second_coordinate_change_y] != player and board[x+second_coordinate_change_x][y+second_coordinate_change_y] != 0:
        searcher_x = x + third_coordinate_change_x
        searcher_y = y + third_coordinate_change_y
        while (searcher_x != -1) and (searcher_x != 8) and (searcher_y != -1) and (searcher_y != 8) and (board[searcher_x][searcher_y] != player):
          if board[searcher_x][searcher_y] == 0:
            if [searcher_x, searcher_y] not in valid_moves:
              valid_moves.append([searcher_x, searcher_y])
              break
            else:
              break
          searcher_x += second_coordinate_change_x
          searcher_y += second_coordinate_change_y
      else:
        continue

def prepare_response(move):
  response = '{}\n'.format(move).encode()
  print('sending {!r}'.format(response))
  return response

if __name__ == "__main__":
  port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337
  host = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname()

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    sock.connect((host, port))
    while True:
      data = sock.recv(1024)
      if not data:
        print('connection to server closed')
        break
      json_data = json.loads(str(data.decode('UTF-8')))
      board = json_data['board']
      maxTurnTime = json_data['maxTurnTime']
      player = json_data['player']
      print(player, maxTurnTime, board)

      move = get_move(player, board)
      response = prepare_response(move)
      sock.sendall(response)
  finally:
    sock.close()
