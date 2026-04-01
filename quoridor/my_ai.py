# my_ai.py
import engine
import random

def think_action(state, valid_moves, my_player):
    """
    壁は一切使わず、自分のゴールへの「最短距離が短くなる移動手」だけを選ぶ単純なAI
    """
    best_move = valid_moves[0]
    shortest_dist = 999
    
    for move in valid_moves:
        if move[0] == "move": # 移動手だけを探す
            future_state = engine.get_next_state(state, move, my_player)
            # 自分が移動した後の、ゴールまでの距離を計算
            dist = engine.get_shortest_path_distance(future_state["p_pos"][my_player], my_player, future_state["walls"])
            
            if dist < shortest_dist:
                shortest_dist = dist
                best_move = move
                
    return best_move


    # """
    # コリドールのAIのメインロジック。
    # 「自分はより早くゴールへ」「相手はより遠回りさせる」手を採点する！
    # """
    # best_score = -9999
    # best_moves = []
    # enemy_player = 1 - my_player
    
    # for move in valid_moves:
    #     # その手（移動または壁置き）を実行した未来の盤面を作る
    #     future_state = engine.get_next_state(state, move, my_player)
    #     future_walls = future_state["walls"]
        
    #     # 1. 自分のゴールまでの最短距離（小さいほど嬉しい！）
    #     my_dist = engine.get_shortest_path_distance(future_state["p_pos"][my_player], my_player, future_walls)
        
    #     # 2. 相手のゴールまでの最短距離（大きいほど嬉しい！）
    #     enemy_dist = engine.get_shortest_path_distance(future_state["p_pos"][enemy_player], enemy_player, future_walls)
        
    #     # 🌟 生徒が考えるポイント：この盤面の「有利さ(点数)」を数式で表す！ 🌟
    #     # 例：「相手の距離」から「自分の距離」を引く。この数字が大きいほど自分が有利。
    #     score = enemy_dist - my_dist
        
    #     # 最高得点を更新した場合
    #     if score > best_score:
    #         best_score = score
    #         best_moves = [move]
    #     # 同点だった場合
    #     elif score == best_score:
    #         best_moves.append(move)
            
    # # 最高得点の手の中からランダムに選ぶ
    # return random.choice(best_moves)