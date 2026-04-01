# Lv.0
import random

def think_action(hand, field_state, legal_moves):
    """出せる手(legal_moves)の中から、一番弱いカードを選ぶCPU"""
    if len(legal_moves) <= 1: # [[]]（パスしかできない場合）
        return []
        
    # パス（空リスト）を除外
    actual_moves = [move for move in legal_moves if len(move) > 0]
    
    # 革命中かどうかで「弱い」の基準が変わる
    is_rev = field_state["is_revolution"]
    
    # リストの最初のカードの power で並び替える
    if is_rev:
        # 革命中は power が大きい（=数字が小さい）方が弱いので、降順
        sorted_moves = sorted(actual_moves, key=lambda x: x[0]["power"], reverse=True)
    else:
        # 通常時は power が小さい方が弱いので、昇順
        sorted_moves = sorted(actual_moves, key=lambda x: x[0]["power"])

    # 一番弱い組み合わせを出す
    return sorted_moves[0]

def think_give_card(hand):
    """7を出した時、適当に1枚渡すCPU"""
    return random.choice(hand)

# Lv.1

# def think_action(hand, field_state, legal_moves):
#     """
#     自分のターンの行動を決める関数。
#     legal_moves には「ルール上出せるカードの組み合わせ（リスト）」が入っています。
#     例: [ [], [{'suit': 'spade', 'num': 3, 'power': 3}] ] （最初の空リストはパス）
#     """
#     if len(legal_moves) <= 1:
#         return [] # 出せるカードがないのでパス

#     actual_moves = [move for move in legal_moves if len(move) > 0]

#     # --------------------------------------------------------
#     # 生徒の戦略例：8とJoker(power:16)は温存して、それ以外の弱いカードを出す！
#     # --------------------------------------------------------
#     candidate_moves = []
#     for move in actual_moves:
#         # move は出すカードのリスト（ペアなら複数枚入っている）
#         first_card = move[0]
#         if first_card["num"] != 8 and first_card["power"] != 16:
#             candidate_moves.append(move)

#     if len(candidate_moves) > 0:
#         # 温存カード以外に出せるものがある場合
#         if field_state["is_revolution"]:
#             # 革命中はpowerが大きいものから
#             sorted_moves = sorted(candidate_moves, key=lambda x: x[0]["power"], reverse=True)
#         else:
#             sorted_moves = sorted(candidate_moves, key=lambda x: x[0]["power"])
#         return sorted_moves[0]
#     else:
#         # 8やJokerしか出せないピンチの場合は、仕方なく一番弱いものを出す
#         sorted_moves = sorted(actual_moves, key=lambda x: x[0]["power"])
#         return sorted_moves[0]


# def think_give_card(hand):
#     """
#     【7渡し】専用ロジック。
#     自分が7を出した直後に呼ばれます。hand（手札）の中から押し付ける1枚を返します。
#     """
#     # 革命中かどうかで渡すカードを変える高度な戦略も可能ですが、
#     # とりあえず一番 power が小さい（弱い）カードを押し付ける例
#     sorted_hand = sorted(hand, key=lambda x: x["power"])
#     return sorted_hand[0]


# # Lv.2

# def think_action(hand, field_state, legal_moves):
#     if len(legal_moves) <= 1:
#         return []

#     actual_moves = [move for move in legal_moves if len(move) > 0]
#     field_cards = field_state["cards"]
#     is_rev = field_state["is_revolution"]

#     # =========================================================
#     # 🌟 必勝ヘルパー関数：カードの「もったいなさ」を計算して並び替える
#     # =========================================================
#     def sort_moves_by_power(moves):
#         def get_eval_power(move):
#             p = move[0]["power"]
#             if p == 16: return 100  # Jokerは常に最後に回す（絶対温存）
#             if is_rev: return -p    # 革命中は 2(15) が最弱になるためマイナス反転
#             return p
#         # 評価値が小さい（＝一番もったいない度が低い）順に並べる
#         return sorted(moves, key=get_eval_power)

#     # ---------------------------------------------------------
#     # 戦略0：【上がり確実】な手があれば絶対に出す！
#     # ---------------------------------------------------------
#     for move in actual_moves:
#         if len(move) == len(hand):
#             return move

#     # ---------------------------------------------------------
#     # 戦略1：【場が空の時（自分が初手）】の最強ムーブ
#     # ---------------------------------------------------------
#     if len(field_cards) == 0:
#         # なるべく「複数枚出し（ペア）」から処理して手札を減らす！
#         moves_by_len = sorted(actual_moves, key=lambda x: len(x), reverse=True)
        
#         safe_moves = []
#         for m in moves_by_len:
#             p = m[0]["power"]
#             # 8, 2, Jokerは初手から無駄撃ちしない
#             if m[0]["num"] != 8 and p != 15 and p != 16:
#                 safe_moves.append(m)
        
#         if safe_moves:
#             # 枚数が一番多い手の中で、一番弱いものを出す
#             max_len = len(safe_moves[0])
#             best_len_moves = [m for m in safe_moves if len(m) == max_len]
#             return sort_moves_by_power(best_len_moves)[0]
#         else:
#             return sort_moves_by_power(actual_moves)[0]

#     # ---------------------------------------------------------
#     # 戦略2：【特殊ルール】の最適化
#     # ---------------------------------------------------------
#     # ① スペ3返し確殺
#     if len(field_cards) == 1 and field_cards[0]["power"] == 16:
#         for m in actual_moves:
#             if m[0]["suit"] == "spade" and m[0]["num"] == 3:
#                 return m

#     # ② 賢い8切り（場に強いカードが出ている、または自分の手札が3枚以下の時だけ発動）
#     field_power = field_cards[0]["power"]
#     if field_power >= 10 or len(hand) <= 3:
#         for m in actual_moves:
#             if m[0]["num"] == 8:
#                 return m

#     # ③ 無理のないスート縛り
#     if field_state["bound_suit"] is None:
#         target_suits = set(c["suit"] for c in field_cards)
#         bind_moves = []
#         for m in actual_moves:
#             if set(c["suit"] for c in m) == target_suits:
#                 p = m[0]["power"]
#                 # 強いカードを使ってまで無理に縛らない
#                 if p != 15 and p != 16 and m[0]["num"] != 8:
#                     bind_moves.append(m)
#         if bind_moves:
#             return sort_moves_by_power(bind_moves)[0]

#     # ---------------------------------------------------------
#     # 戦略3：【ペア崩し防止】を考慮した通常出し
#     # ---------------------------------------------------------
#     candidate_moves = []
#     for m in actual_moves:
#         p = m[0]["power"]
#         if m[0]["num"] != 8 and p != 15 and p != 16:
#             candidate_moves.append(m)
            
#     if candidate_moves:
#         if len(field_cards) == 1:
#             # 手札の各数字の枚数をカウントする
#             num_counts = {}
#             for c in hand:
#                 num_counts[c["num"]] = num_counts.get(c["num"], 0) + 1
                
#             no_break_moves = []
#             for m in candidate_moves:
#                 # 1枚しかない（ペアになっていない）カードだけを候補にする
#                 if num_counts[m[0]["num"]] == 1: 
#                     no_break_moves.append(m)
                    
#             if no_break_moves:
#                 return sort_moves_by_power(no_break_moves)[0]
                
#         # ペアを崩さない手がない場合は仕方なく出す
#         return sort_moves_by_power(candidate_moves)[0]
        
#     # 温存カードしか出せない大ピンチの時
#     return sort_moves_by_power(actual_moves)[0]


# def think_give_card(hand):
#     # 【7渡し】一番弱いカードを押し付ける（革命も考慮）
#     # ※is_revの情報が渡ってこないため、常に通常時の最弱を渡す
#     sorted_hand = sorted(hand, key=lambda x: x["power"])
#     if sorted_hand[0]["power"] == 16 and len(sorted_hand) > 1:
#         return sorted_hand[1] # ジョーカーしか手札にない時以外の事故防止
#     return sorted_hand[0]