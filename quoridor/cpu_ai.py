# cpu_ai.py
import engine

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