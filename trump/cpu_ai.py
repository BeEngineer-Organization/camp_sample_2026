# cpu_ai.py
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