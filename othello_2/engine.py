# engine.py
import copy

DIRECTIONS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]

def get_initial_board():
    board = [[0] * 8 for _ in range(8)]
    board[3][3], board[4][4] = -1, -1  # 白(後手)
    board[3][4], board[4][3] = 1, 1    # 黒(先手)
    return board

def is_on_board(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def get_flipped_disks(board, x, y, color):
    if board[y][x] != 0:
        return []
    flipped_disks = []
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        temp_flipped = []
        while is_on_board(nx, ny) and board[ny][nx] == -color:
            temp_flipped.append((nx, ny))
            nx += dx
            ny += dy
        if is_on_board(nx, ny) and board[ny][nx] == color:
            flipped_disks.extend(temp_flipped)
    return flipped_disks

def get_valid_moves(board, color):
    valid_moves = []
    for y in range(8):
        for x in range(8):
            if get_flipped_disks(board, x, y, color):
                valid_moves.append((x, y))
    return valid_moves

def get_next_board(board, move, color):
    x, y = move
    new_board = copy.deepcopy(board)
    flipped = get_flipped_disks(new_board, x, y, color)
    new_board[y][x] = color
    for fx, fy in flipped:
        new_board[fy][fx] = color
    return new_board

def run_games(player_black, player_white, num_games=100):
    print(f"🎮 オセロAI(ロジック型) 自動対戦を {num_games} 試合開始します...\n")
    black_wins, white_wins, draws = 0, 0, 0

    for _ in range(num_games):
        board = get_initial_board()
        current_color = 1
        pass_count = 0
        
        while pass_count < 2:
            valid_moves = get_valid_moves(board, current_color)
            if not valid_moves:
                pass_count += 1
                current_color *= -1
                continue
            pass_count = 0
            
            current_player = player_black if current_color == 1 else player_white
            try:
                move = current_player.think_action(copy.deepcopy(board), valid_moves, current_color)
                if move not in valid_moves: move = valid_moves[0]
            except:
                move = valid_moves[0]
                
            board = get_next_board(board, move, current_color)
            current_color *= -1

        black_score = sum(row.count(1) for row in board)
        white_score = sum(row.count(-1) for row in board)
        
        if black_score > white_score: black_wins += 1
        elif white_score > black_score: white_wins += 1
        else: draws += 1

    print("=== 最終結果 ===")
    print(f"黒 (先手) の勝利: {black_wins} 回")
    print(f"白 (後手) の勝利: {white_wins} 回")
    print(f"引き分け: {draws} 回")