#!/usr/bin/python

import sys
import json
import socket

valid_moves = []

def get_move(player, board):
  # make sure moves is empty each turn
  valid_moves.clear

  # TODO determine valid moves

  # need to check horizontal

  # need to check vertical
  vertical_check(player, board, 'l_to_r')
  vertical_check(player, board, 'r_to_l')

  print(valid_moves)



  # need to check diagonal

  # TODO determine best move
  return [2, 3]


def vertical_check(player, board, direction):
  if direction == 'l_to_r':
    start, end, step = 0, len(board[0]) - 2, 1
  elif direction == 'r_to_l':
    start, end, step = len(board[0]) - 1, 1, -1

  for i in range(len(board)):
    for j in range(start, end, step):
      if board[i][j] == player and board[i][j+step] != player and board[i][j+step] != 0:
        while (j+2*step != end) and (board[i][j+2*step] != player):
          if board[i][j+2*step] == 0:
            valid_moves.append([i, j+2*step])
          j += step
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
