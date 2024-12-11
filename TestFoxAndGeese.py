# Fox and Geese testing script
# JC4004 Computational Intelligence 2024-25

import copy
from importlib import import_module  

class FoxAndGoose:

  # =================================================
  # Initialise the board for a new game
  def __init__(self):
    
    # Initialise a new game
    self.board = [
        [' ',' ','.','.','.',' ',' '],
        [' ',' ','.','.','.',' ',' '],
        ['.','.','.','.','.','.','.'],
        ['G','.','.','F','.','.','G'],
        ['G','G','G','G','G','G','G'],
        [' ',' ','G','G','G',' ',' '],
        [' ',' ','G','G','G',' ',' ']
    ]
    self.fox_illegal = 0
    self.goose_illegal = 0
    self.rounds_played = 0
    self.winner = ''


  # =================================================
  # Increase counter for illegal moves
  def increase_illegal_moves(self,is_fox):
    if is_fox:
      self.fox_illegal += 1
    else:
      self.goose_illegal += 1

  # =================================================
  # Check if the move is valid and update the board
  def is_valid_move(self, is_fox, moves):

    # Round is counted even if the move is illegal
    self.rounds_played += 1

    # Test for valid number of moves and value of staring position
    # 目标格式测试
    if len(moves) < 2:
      self.increase_illegal_moves(is_fox)
      return False
    # 棋盘上范围测试
    elif moves[0][0] < 0 or moves[0][0] >= len(self.board) or moves[0][1] < 0 or moves[0][1] >= len(self.board):
      self.increase_illegal_moves(is_fox)
      return False
    # 绵羊的坐标只有两个
    elif len(moves) > 2 and not is_fox:
      self.increase_illegal_moves(is_fox)
      return False
    # 原始位置不是一只羊，但是却是认为是移动了羊
    elif self.board[moves[0][0]][moves[0][1]] != 'G' and is_fox == False:
      self.increase_illegal_moves(is_fox)
      return False
    elif self.board[moves[0][0]][moves[0][1]] != 'F' and is_fox == True:
      self.increase_illegal_moves(is_fox)
      return False

    # Initialise
    new_board = copy.deepcopy(self.board)
    captured = False

    # Loop through moves to test their validity
    for i in range(len(moves)-1):
      from_pos = moves[i]
      to_pos = moves[i + 1]
      # 横纵坐标都没有变化，原地没动 为错误
      if from_pos[0] == to_pos[0] and from_pos[1] == to_pos[1]:
        self.increase_illegal_moves(is_fox)
        return False
      # 横纵坐标都发生了变化，说明斜着运动， 都是奇或者偶数 返回错误 --- 因为只有奇奇和偶偶的能走斜线，根据题目棋盘
      if (from_pos[0] != to_pos[0] and from_pos[1] != to_pos[1]) and ((from_pos[0] % 2) != (from_pos[1] % 2)):
        self.increase_illegal_moves(is_fox)
        return False
      # 飞出棋盘
      elif to_pos[0] < 0 or to_pos[1] < 0 or to_pos[0] >= len(new_board) or to_pos[1] >= len(new_board):
        self.increase_illegal_moves(is_fox)
        return False
      # 不能走的地方
      elif new_board[to_pos[0]][to_pos[1]] != '.':
        self.increase_illegal_moves(is_fox)
        return False
      # 跨越的距离大过两步的就错误
      elif abs(from_pos[0] - to_pos[0]) > 2 or abs(from_pos[1] - to_pos[1]) > 2:
        self.increase_illegal_moves(is_fox)
        return False
      # 等于两步的情况
      elif abs(from_pos[0] - to_pos[0]) > 1 or abs(from_pos[1] - to_pos[1]) > 1:
        
        # You can only move more than one step if you are a fox capturing a goose，
        #羊不走两步所以错，抓到羊的狐狸一定走的是两步或者以上，
        if (not is_fox) or (not captured and i > 0):
          self.increase_illegal_moves(is_fox)
          return False
        #走两步的情况下，不可能出现了奇数和
        elif (abs(from_pos[0] - to_pos[0]) + abs(from_pos[1] - to_pos[1])) % 2 != 0:
          self.increase_illegal_moves(is_fox)
          return False       
        # 中间不能是羊之外的东西
        mid_pos = [(from_pos[0] + to_pos[0]) // 2, (from_pos[1] + to_pos[1]) // 2]
        if new_board[mid_pos[0]][mid_pos[1]] != 'G':
          self.increase_illegal_moves(is_fox)
          return False
        new_board[to_pos[0]][to_pos[1]] = new_board[from_pos[0]][from_pos[1]]
        new_board[mid_pos[0]][mid_pos[1]] = '.'
        new_board[from_pos[0]][from_pos[1]] = '.'
        captured = True
      else:
        # 一步行为
        # You can only chain moves if you are capturing consecutively
        # 如果target 有多个，直接否决
        if i > 0:
          self.increase_illegal_moves(is_fox)
          return False

        # This move is legal
        new_board[to_pos[0]][to_pos[1]] = new_board[from_pos[0]][from_pos[1]]
        new_board[from_pos[0]][from_pos[1]] = '.' # 更新移动后的棋盘
        captured = False # 没有吃到栋

    # Legal move(s): update the board
    self.board = new_board
    return True

  # =================================================
  # Check if the game is won by one player
  def check_win(self):
    
    # Checks if the game is won by the fox
    goose_count = 0
    for i in range(len(self.board)):
      for j in range(len(self.board[i])):
        if self.board[i][j] == 'G':
          goose_count += 1
    
    # If less than 4 geese left, the fox wins
    if goose_count < 4:
      self.winner = 'F'
      return True

    # Checks if the game is won by the geese
    fox_pos = [0,0]
    for i in range(len(self.board)):
      for j in range(len(self.board[i])):
        if self.board[i][j] == 'F':
          fox_pos = [i,j]
          break

    # Can the fox move? # 检测一圈的方格
    for i in range(max(fox_pos[0]-1,0),min(fox_pos[0]+2,len(self.board))):
      for j in range(max(fox_pos[1]-1,0),min(fox_pos[1]+2,len(self.board))):
        if (i == fox_pos[0] or j == fox_pos[1]) or ((fox_pos[0] % 2) == (fox_pos[1] % 2)):
          if self.board[i][j] == '.':
            return False  # Fox can move one step
          if self.board[i][j] == 'G':
            capture_pos = [i+i-fox_pos[0],j+j-fox_pos[1]]
            if capture_pos[0] >= 0 and capture_pos[0] < len(self.board) and capture_pos[1] >= 0 and capture_pos[1] < len(self.board):
              if self.board[capture_pos[0]][capture_pos[1]] == '.':
                return False  # Fox can capture a goose

    # The fox cannot move, the geese win
    self.winner = 'G'
    return True

  # =================================================
  # Play one round of the game between players 1 (goose) and 2 (fox)
  def play(self, player_1, player_2):
    
    # Play a round of the game
    game_over = False
    rounds_played = 0
    while not game_over:

      # The goose plays first
      temp_board = copy.deepcopy(self.board)
      try:             
        move = player_1.play_goose(temp_board)
        if not self.is_valid_move(False,move):
          print("Illegal move by goose!")
      except Exception as e: 
          print("Exception caught for goose!") # 走错一步直接结束游戏，并且判罚
          print(e)
          self.winner = 'F'
          game_over = True
          break
      
      if self.check_win():  
        game_over = True
      else:

        # The fox plays second
        temp_board = copy.deepcopy(self.board)
        try:
          move = player_2.play_fox(temp_board)
          if not self.is_valid_move(True,move):
            print("Illegal move by fox!")
        except Exception as e:  
          print("Exception caught for fox!")
          print(e)
          self.winner = 'G'
          game_over = True        

        if self.check_win():
          game_over = True  

      # Make sure that the game doesn't last forever (deadlock)
      rounds_played += 1
      if rounds_played > 999:
        game_over = True  
    
    # Game is over
    if self.winner == 'G':
      print("Goose won!")      
    elif self.winner == 'F':
      print("Fox won!")
    else:
      print("Game over, no winner!")
    print("Rounds played: " + str(rounds_played))
    print("Goose made " + str(self.goose_illegal) + " illegal move(s)")
    print("Fox made " + str(self.fox_illegal) + " illegal move(s)")


# ===================================================
# The main function demonstrates how to run a game
if __name__ == "__main__":
  
  # Init the game
  game = FoxAndGoose()
  
  # Import the players
  module = __import__("Team00") 
  player1 = getattr(module, "Player")() 
  module = __import__("Team00") 
  player2 = getattr(module, "Player")() 
  
  # Play the game
  game.play(player1, player2)
  
# ==== End of file