# engine.py
import copy
import random

BOARD_SIZE = 15

def get_initial_board():
    """15x15の初期盤面（0: 空き, 1: 黒/先手, 2: 白/後手）"""
    return [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

def get_candidate_moves(board):
    """
    【重要なる最適化】
    225マスすべてを探すとAIの計算が遅くなるため、
    「すでに石が置かれているマスの周囲1マス」だけを候補として返す。
    """
    moves = set()
    has_stone = False
    
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] != 0:
                has_stone = True
                # 周囲8方向の空きマスを候補に追加
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                            if board[ny][nx] == 0:
                                moves.add((nx, ny))
                                
    # 盤面に一つも石がない（初手）場合は、中央を返す
    if not has_stone:
        return [(BOARD_SIZE // 2, BOARD_SIZE // 2)]
        
    return list(moves)

def get_next_board(board, move, player):
    """石を置いた後の未来の盤面を返す"""
    x, y = move
    new_board = copy.deepcopy(board)
    new_board[y][x] = player
    return new_board

def check_win(board, player):
    """タテ・ヨコ・ナナメのどこかに、指定したプレイヤーの石が5つ並んでいるかチェック"""
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == player:
                for dx, dy in directions:
                    count = 1
                    nx, ny = x + dx, y + dy
                    while 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[ny][nx] == player:
                        count += 1
                        nx += dx
                        ny += dy
                    if count >= 5:
                        return True
    return False

def run_games(player1_ai, player2_ai, num_games=20):
    """
    五目並べは1試合が長くなりやすいため、デフォルトは20試合。
    """
    p1_wins = 0
    p2_wins = 0
    draws = 0
    
    print(f"🎮 五目並べAI 自動対戦を {num_games} 試合開始します...\n")
    
    for game in range(num_games):
        board = get_initial_board()
        current_player = 1 # 1: 黒(先手), 2: 白(後手)
        turn = 0
        
        while turn < BOARD_SIZE * BOARD_SIZE:
            valid_moves = get_candidate_moves(board)
            if not valid_moves:
                break # 打つ場所がなくなったら引き分け
                
            ai = player1_ai if current_player == 1 else player2_ai
            
            try:
                move = ai.think_action(copy.deepcopy(board), valid_moves, current_player)
                if move not in valid_moves:
                    move = random.choice(valid_moves)
            except Exception as e:
                print(f"AIエラー (Player {current_player}): {e}")
                move = random.choice(valid_moves)
                
            board = get_next_board(board, move, current_player)
            
            if check_win(board, current_player):
                if current_player == 1: p1_wins += 1
                else: p2_wins += 1
                break
                
            current_player = 3 - current_player # 1なら2に、2なら1に切り替え
            turn += 1
            
        else:
            draws += 1 # 盤面がすべて埋まった
            
    print("=== 最終結果 ===")
    print(f"先手 (Player 1) の勝利: {p1_wins} 回")
    print(f"後手 (Player 2) の勝利: {p2_wins} 回")
    print(f"引き分け: {draws} 回")