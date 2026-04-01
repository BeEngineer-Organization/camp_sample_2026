# engine.py
import copy

# 8方向（上、右上、右、右下、下、左下、左、左上）の座標変化
DIRECTIONS = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]

def get_initial_board():
    """8x8の初期盤面を生成する（0: 空き, 1: 黒, -1: 白）"""
    board = [[0] * 8 for _ in range(8)]
    board[3][3], board[4][4] = -1, -1  # 白
    board[3][4], board[4][3] = 1, 1    # 黒
    return board

def is_on_board(x, y):
    """座標が盤面に収まっているか判定する"""
    return 0 <= x < 8 and 0 <= y < 8

def get_flipped_disks(board, x, y, color):
    """
    指定した座標(x, y)に石(color)を置いた時、ひっくり返る石の座標リストを返す。
    1枚もひっくり返らない場合は空のリストを返す（＝そこには打てない）。
    """
    if board[y][x] != 0:
        return []

    flipped_disks = []
    for dx, dy in DIRECTIONS:
        nx, ny = x + dx, y + dy
        temp_flipped = []
        
        # 相手の石が続く限り進む
        while is_on_board(nx, ny) and board[ny][nx] == -color:
            temp_flipped.append((nx, ny))
            nx += dx
            ny += dy
            
        # 相手の石を挟んだ先に、自分の石があればひっくり返せる
        if is_on_board(nx, ny) and board[ny][nx] == color:
            flipped_disks.extend(temp_flipped)

    return flipped_disks

def get_valid_moves(board, color):
    """現在打てる座標(x, y)のリストを返す"""
    valid_moves = []
    for y in range(8):
        for x in range(8):
            if get_flipped_disks(board, x, y, color):
                valid_moves.append((x, y))
    return valid_moves

def get_next_board(board, move, color):
    """
    【重要】生徒が使う関数。
    指定した手(move)を打ったあとの「未来の盤面」を生成して返す。
    """
    x, y = move
    new_board = copy.deepcopy(board)
    flipped = get_flipped_disks(new_board, x, y, color)
    
    new_board[y][x] = color
    for fx, fy in flipped:
        new_board[fy][fx] = color
        
    return new_board

def run_games(player_black, player_white, num_games=100):
    """黒(1)と白(-1)のAIを戦わせるループ"""
    print(f"🎮 オセロAI 自動対戦を {num_games} 試合開始します...\n")
    
    black_wins = 0
    white_wins = 0
    draws = 0

    for game in range(num_games):
        board = get_initial_board()
        current_color = 1  # 黒からスタート
        pass_count = 0     # 連続パスの回数
        
        while pass_count < 2:
            valid_moves = get_valid_moves(board, current_color)
            
            if not valid_moves:
                # 打てる場所がないのでパス
                pass_count += 1
                current_color *= -1 # 相手のターンへ
                continue
                
            pass_count = 0
            
            # AIに行動を決めさせる
            current_player = player_black if current_color == 1 else player_white
            try:
                # 不正防止のためコピーを渡す
                move = current_player.think_action(copy.deepcopy(board), valid_moves, current_color)
            except Exception as e:
                player_name = "黒" if current_color == 1 else "白"
                print(f"AIエラー ({player_name}): {e}")
                move = valid_moves[0] # エラー時は適当な手を打つ
                
            # AIが選んだ手が本当に合法かチェック
            if move not in valid_moves:
                move = valid_moves[0]
                
            # 盤面を更新
            board = get_next_board(board, move, current_color)
            current_color *= -1

        # 勝敗判定
        black_score = sum(row.count(1) for row in board)
        white_score = sum(row.count(-1) for row in board)
        
        if black_score > white_score:
            black_wins += 1
        elif white_score > black_score:
            white_wins += 1
        else:
            draws += 1

    print("=== 最終結果 ===")
    print(f"黒 (先手) の勝利: {black_wins} 回")
    print(f"白 (後手) の勝利: {white_wins} 回")
    print(f"引き分け: {draws} 回")