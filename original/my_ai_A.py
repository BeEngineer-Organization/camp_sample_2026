# A. 相手の手札を記録しておく
import random

def think_action(my_info):

    current_score = my_info["card1"] * my_info["card2"]
    
    # 手札を小さい順に並べ替えておく
    sorted_hand = sorted(my_info["own_hand"])

    # 相手の残り手札を推測して、小さい順に並べ替えておく
    all_cards = list(range(1, 14))
    enemy_remaining = sorted(list(set(all_cards) - set(my_info["enemy_used"])))
    
    # 相手の手札の最大値と最小値を把握
    enemy_max = enemy_remaining[-1]
    enemy_min = enemy_remaining[0]

    if current_score > 0:
        # 相手の最大値より大きいカードで確実に勝つ（自分の手札を小さい方から確認）
        for card in sorted_hand:
            if card > enemy_max:
                return card
        # 全てのカードが相手の最大値以下なら、最大値を出す
        return sorted_hand[-1]

    elif current_score < 0:
        # 相手の最小値より小さいカードで確実に負ける（自分の手札を大きい方から確認）
        for card in reversed(sorted_hand):
            if card < enemy_min:
                return card
        # 全てのカードが相手の最小値以上なら、最小値を出す
        return sorted_hand[0]    

    return random.choice(my_info["own_hand"])