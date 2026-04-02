# cpu_ai.py
import random

def think_action(turn, current_score, my_hand, my_total, enemy_total, enemy_used):
    """何も考えず、手札からランダムに1枚出すだけのCPU"""
    return random.choice(my_hand)



# def think_action(turn, current_score, my_hand, my_total, enemy_total, enemy_used):
#     """
#     AIの思考ロジック。
#     引数で「今のターンの得点」や「自分の手札」などの情報が渡されてきます。
#     """
    
#     # 手札を小さい順に並べ替えておく（戦略を立てやすくするため）
#     sorted_hand = sorted(my_hand)
    
#     # =========================================================
#     # 戦略1：得点が「プラス」の時は、勝ちに行きたい！
#     # =========================================================
#     if current_score > 0:
#         # 100点以上の超高得点なら、手札の一番強いカード（最大値）を惜しみなく出す
#         if current_score >= 100:
#             return sorted_hand[-1] # リストの一番最後（最大）
            
#         # まあまあの得点なら、真ん中くらいのカードを出して節約する
#         elif current_score >= 30:
#             mid_index = len(sorted_hand) // 2
#             return sorted_hand[mid_index]
            
#         # 点数が低いなら、弱いカードを適当に出しておく
#         else:
#             return sorted_hand[1] # 弱めのカード（0番目はマイナス用に温存）

#     # =========================================================
#     # 戦略2：得点が「マイナス」の時は、相手に押し付けたい（わざと負けたい）！
#     # =========================================================
#     elif current_score < 0:
#         # 絶対に引き取りたくない大ダメージの時は、手札で一番弱いカードを出して負ける
#         if current_score <= -50:
#             return sorted_hand[0] # リストの一番最初（最小）
            
#         # 軽いマイナスなら、少し弱めのカードでやり過ごす
#         else:
#             return sorted_hand[0]

#     # 得点が0の時は適当に一番弱いものを出す
#     return sorted_hand[0]