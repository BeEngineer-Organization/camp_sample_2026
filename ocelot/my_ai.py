# my_ai.py
import engine, random

# 生徒が自分で考えて点数を調整する「重みづけマトリクス（評価ボード）」
# 角(0,0など)は絶対取られないので超高得点。角の斜め内側(1,1など)は危険なのでマイナス！
WEIGHT_BOARD = [
    [ 30, -12,   0,  -1,  -1,   0, -12,  30],
    [-12, -15,  -3,  -3,  -3,  -3, -15, -12],
    [  0,  -3,   0,  -1,  -1,   0,  -3,   0],
    [ -1,  -3,  -1,  -1,  -1,  -1,  -3,  -1],
    [ -1,  -3,  -1,  -1,  -1,  -1,  -3,  -1],
    [  0,  -3,   0,  -1,  -1,   0,  -3,   0],
    [-12, -15,  -3,  -3,  -3,  -3, -15, -12],
    [ 30, -12,   0,  -1,  -1,   0, -12,  30]
]

def evaluate_board(board, my_color):
    """盤面全体の「有利さ」を点数化する関数"""
    score = 0
    for y in range(8):
        for x in range(8):
            if board[y][x] == my_color:
                # 自分の石ならプラス点
                score += WEIGHT_BOARD[y][x]
            elif board[y][x] == -my_color:
                # 相手の石ならマイナス点
                score -= WEIGHT_BOARD[y][x]
    return score

def think_action(board, valid_moves, my_color):

    max_flipped = -1
    best_moves = [] # ★ 最高記録の手を保存する「リスト」に変更
    
    for move in valid_moves:
        x, y = move
        flipped_disks = engine.get_flipped_disks(board, x, y, my_color)
        num_flipped = len(flipped_disks)
        
        # もし今までの最高記録を「更新」したら、リストをリセットして入れ直す
        if num_flipped > max_flipped:
            max_flipped = num_flipped
            best_moves = [move]
            
        # もし今までの最高記録と「同点」なら、リストに追加（仲間にいれる）
        elif num_flipped == max_flipped:
            best_moves.append(move)
            
    # ★ 同点1位の候補の中から、ランダムに1つ選んで返す！
    return random.choice(best_moves)


    # """
    # 自分のターンの行動を決める関数。
    # """
    # best_move = valid_moves[0]
    # best_score = -99999  # あり得ないくらい低い点数で初期化
    
    # # 打てる場所をすべて試して、未来の盤面を採点する
    # for move in valid_moves:
        
    #     # 1. engineを使って「自分がその場所に打ったあとの未来の盤面」を作る
    #     future_board = engine.get_next_board(board, move, my_color)
        
    #     # 2. 未来の盤面を、自分が作った点数表で採点する
    #     score = evaluate_board(future_board, my_color)
        
    #     # 3. 今までの最高得点を更新したら、その手を記録する
    #     if score > best_score:
    #         best_score = score
    #         best_move = move
            
    # # ★上位生（2年生以上）へのヒント★
    # # ここでは「自分が打った直後」の点数しか見ていない。
    # # この future_board に対して、相手(enemy_color = -my_color) が
    # # どんな反撃をしてくるか？を `engine.get_valid_moves` で取得して
    # # ループ（先読み）させれば、さらに賢いAI（ミニマックス法）になるぞ！

    # return best_move