# my_ai.py
import engine
import random

def think_action(board, valid_moves, my_player):

    """何も考えず、選べる穴の中からランダムに1つ選ぶ弱いAI"""
    return random.choice(valid_moves)


    # """
    # マンカラの強いAIを目指すロジック。
    # """
    # my_store = 6 if my_player == 0 else 13
    
    # # =========================================================
    # # 戦略1：【ぴったりゴール】でもう1回自分のターンにする！
    # # =========================================================
    # perfect_moves = []
    # for move in valid_moves:
    #     stones = board[move] # その穴に入っている石の数
        
    #     # 「穴の場所（インデックス）」＋「石の数」が、ゴールの場所と一致するか？
    #     if move + stones == my_store:
    #         perfect_moves.append(move)
            
    # if perfect_moves:
    #     # ぴったりゴールできる手が複数ある場合は、その中からランダムに選んで確実に実行する
    #     return random.choice(perfect_moves)

    # # =========================================================
    # # 戦略2：【1手先読み】で一番点数（ゴールの石）が増える手を探す
    # # =========================================================
    # best_score = -1
    # best_moves = []
    
    # for move in valid_moves:
    #     # engineを使って、この手を選んだ時の「未来の盤面」を作る
    #     future_board, next_player = engine.get_next_state(board, move, my_player)
        
    #     # 未来の自分のゴールの石の数を調べる
    #     future_score = future_board[my_store]
        
    #     if future_score > best_score:
    #         best_score = future_score
    #         best_moves = [move] # 最高得点の手をリストに入れる
    #     elif future_score == best_score:
    #         best_moves.append(move) # 同点なら仲間に加える
            
    # # 一番ゴールの石が増える手（複数あればランダム）を選ぶ
    # return random.choice(best_moves)