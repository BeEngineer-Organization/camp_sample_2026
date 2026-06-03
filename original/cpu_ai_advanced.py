import random

def think_action(cpu_info):
   
    # 手札を小さい順に並べ替えておく
    sorted_hand = sorted(cpu_info["own_hand"])
    
    if cpu_info["current_score"] > 0:
        return sorted_hand[-1] # リストの一番最後（最大）
    
    elif cpu_info["current_score"] < 0:
        return sorted_hand[0] # リストの一番最初（最小）