#!/usr/bin/python

import sys
import json
import socket
import random

valid_moves = []

def get_move(player, board):
  # make sure moves is empty each turn
  valid_moves.clear()

  # TODO determine valid moves

  # need to check horizontal
  horizontal_check(player, board, 'l_to_r')
  horizontal_check(player, board, 'r_to_l')

  # need to check vertical
  vertical_check(player, board, 'top_to_bottom')
  vertical_check(player, board, 'bottom_to_top')

  # need to check diagonal
  diagonal_check(player, board, 'top_left_to_bottom_right')
  diagonal_check(player, board, 'bottom_right_to_top_left')
  diagonal_check_2(player, board, 'bottom_left_to_top_right')
  diagonal_check_2(player, board, 'bottom_left_to_top_right')


  print(valid_moves, "valid moves")

  return random.choice(valid_moves)


  # TODO determine best move

def vertical_check(player, board, direction):
  if direction == 'top_to_bottom':
    start, end, step = 0, 5, 1
    change = 2
  elif direction == 'bottom_to_top':
    start, end, step = 7, 2, -1
    change = -2

  for j in range(8):
    for i in range(start, end, step):
      if board[i][j] == player and board[i+step][j] != player and board[i+step][j] != 0:
        searcher = i + change
        while (searcher != -1) and (searcher != 8) and (board[searcher][j] != player):
          if board[searcher][j] == 0:
            valid_moves.append([searcher, j])
            break
          searcher += step
      else:
        continue

def horizontal_check(player, board, direction):
  if direction == 'l_to_r':
    change = 2
    start, end, step = 0, 5, 1
  elif direction == 'r_to_l':
    start, end, step = 7, 2, -1
    change = -2

  for j in range(8):
    for i in range(start, end, step):
      if board[j][i] == player and board[j][i+step] != player and board[j][i+step] != 0:
        searcher = i + change
        while (searcher != -1) and (searcher != 8) and (board[j][searcher] != player):
          if board[j][searcher] == 0:
            valid_moves.append([j, searcher])
            break
          searcher += step
      else:
        continue

def diagonal_check(player, board, direction):
  if direction == 'top_left_to_bottom_right':
    start, end, step = 0, 6, 1
    change = 2
  elif direction == 'bottom_right_to_top_left':
    start, end, step = 7, 1, -1
    change = -2

  for j in range(start, end, step):
    for i in range(start, end, step):
      if board[j][i] == player and board[j+step][i+step] != player and board[j+step][i+step] != 0:
        searcher = i + change
        searcher2 = j + change
        while (searcher != -1) and (searcher != 8) and (searcher2 != -1) and (searcher2 != 8) and (board[searcher2][searcher] != player):
          if board[searcher2][searcher] == 0:
            if [searcher2, searcher] not in valid_moves:
              valid_moves.append([searcher2, searcher])
              break
            else:
              break
          searcher += step
          searcher2 += step
      else:
        continue

def diagonal_check_2(player, board, direction):
  if direction == 'bottom_left_to_top_right':
    starti, endi, stepi = 0, 6, 1
    startj, endj, stepj = 7, 1, -1

    changej = -2
    changei = 2
  elif direction == 'top_right_to_bottom_left':
    starti, endi, stepi = 7, 1, -1
    startj, endj, stepj = 0, 6, 1
    changei = -2
    changej = 2

  for j in range(startj, endj, stepj):
    for i in range(starti, endi, stepi):
      if board[j][i] == player and board[j+stepj][i+stepi] != player and board[j+stepj][i+stepi] != 0:
        searcher = i + changei
        searcher2 = j + changej
        while (searcher != -1) and (searcher != 8) and (searcher2 != -1) and (searcher2 != 8) and (board[searcher2][searcher] != player):
          if board[searcher2][searcher] == 0:
            if [searcher2, searcher] not in valid_moves:
              valid_moves.append([searcher2, searcher])
              break
            else:
              break
          searcher += stepi
          searcher2 += stepj
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
