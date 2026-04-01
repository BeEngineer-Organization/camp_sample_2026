# engine.py
import copy
import random

def get_initial_board():
    """初期盤面。各穴に4個ずつ石が入っており、ゴール(6と13)は0個"""
    return [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]

def get_valid_moves(board, player):
    """現在のプレイヤーが石を取れる穴のインデックスリストを返す"""
    moves = []
    start = 0 if player == 0 else 7
    end = 5 if player == 0 else 12
    for i in range(start, end + 1):
        if board[i] > 0:
            moves.append(i)
    return moves

def get_next_state(board, move, player):
    """
    【重要】指定した穴(move)から石を取って配った後の、
    「未来の盤面」と「次のプレイヤー」を返す関数。
    """
    new_board = copy.deepcopy(board)
    stones = new_board[move]
    new_board[move] = 0
    
    current_idx = move
    my_store = 6 if player == 0 else 13
    enemy_store = 13 if player == 0 else 6
    
    # 石を1個ずつ配る（種まき）
    while stones > 0:
        current_idx = (current_idx + 1) % 14 # 配列の末尾を超えたら0に戻る
        # 相手のゴールには入れない
        if current_idx == enemy_store:
            continue
        new_board[current_idx] += 1
        stones -= 1
        
    next_player = 1 - player # 基本は相手のターンになる
    
    # 【特殊ルール1：ぴったりゴール】
    # 最後の石が自分のゴールに入ったら、もう一度自分のターン！
    if current_idx == my_store:
        next_player = player
        
    # 【特殊ルール2：横取り】
    # 最後の石が「自分の陣地の空だった穴」に入ったら、対面の相手の石ごと奪う！
    else:
        if new_board[current_idx] == 1:
            if (player == 0 and 0 <= current_idx <= 5) or (player == 1 and 7 <= current_idx <= 12):
                opposite_idx = 12 - current_idx # 対面のインデックス計算
                if new_board[opposite_idx] > 0:
                    # 横取り発動！
                    new_board[my_store] += new_board[current_idx] + new_board[opposite_idx]
                    new_board[current_idx] = 0
                    new_board[opposite_idx] = 0
                    
    # 【終了判定】どちらかの陣地がすべて空になったらゲーム終了
    p0_stones = sum(new_board[0:6])
    p1_stones = sum(new_board[7:13])
    
    if p0_stones == 0 or p1_stones == 0:
        # 残った石をすべて自分のゴールに入れる
        new_board[6] += p0_stones
        new_board[13] += p1_stones
        for i in range(6): new_board[i] = 0
        for i in range(7, 13): new_board[i] = 0
        
    return new_board, next_player

def is_game_over(board):
    return sum(board[0:6]) == 0 or sum(board[7:13]) == 0

def run_games(player0_ai, player1_ai, num_games=100):
    p0_wins = 0
    p1_wins = 0
    draws = 0
    players = [player0_ai, player1_ai]
    
    print(f"🎮 マンカラAI 自動対戦を {num_games} 試合開始します...\n")
    
    for _ in range(num_games):
        board = get_initial_board()
        current_player = 0
        turn_count = 0
        
        while not is_game_over(board) and turn_count < 1000:
            valid_moves = get_valid_moves(board, current_player)
            if not valid_moves:
                current_player = 1 - current_player
                continue
                
            ai = players[current_player]
            try:
                move = ai.think_action(copy.deepcopy(board), valid_moves, current_player)
                if move not in valid_moves:
                    move = random.choice(valid_moves)
            except Exception as e:
                print(f"AIエラー (Player {current_player}): {e}")
                move = random.choice(valid_moves)
                
            board, current_player = get_next_state(board, move, current_player)
            turn_count += 1
            
        score0 = board[6]
        score1 = board[13]
        if score0 > score1: p0_wins += 1
        elif score1 > score0: p1_wins += 1
        else: draws += 1
            
    print("=== 最終結果 ===")
    print(f"先手 (Player 0) の勝利: {p0_wins} 回")
    print(f"後手 (Player 1) の勝利: {p1_wins} 回")
    print(f"引き分け: {draws} 回")