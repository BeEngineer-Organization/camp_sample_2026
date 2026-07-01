# E. 残っている山札のプラス・マイナスの偏りを利用する
import random

# 得点用の山札から既に出たカードを記録しておくリスト
card_list = []

def think_action(my_info):

    current_score = my_info["card1"] * my_info["card2"]

    # 手札を小さい順に並べ替えておく
    sorted_hand = sorted(my_info["own_hand"])

    if my_info["turn"] == 1:
        card_list.clear()

    card_list.append(my_info["card1"])
    card_list.append(my_info["card2"])

    # 最初の山札(26枚)
    all_cards = [i for i in range(1, 14)] + [-i for i in range(1, 14)]

    # 残っているカードだけを抽出
    remaining_cards = all_cards.copy()
    for card in card_list:
        remaining_cards.remove(card)

    # 残ったカードのうち、プラスの枚数とマイナスの枚数を数える

    plus_count = 0
    minus_count = 0

    for card in remaining_cards:
        if card > 0:
            plus_count += 1

    for card in remaining_cards:
        if card < 0:
            minus_count += 1

    count_diff = plus_count - minus_count

    # どちらかに極端に偏っているなら次のターンはマイナスの得点になりやすい
    if count_diff >= 5 or count_diff <= -5:
        # 今のターンの得点がプラスなら勝っておきたい
        if current_score > 0:
            return sorted_hand[-1] # 一番強いカードを出す

    # 戦略1：得点が「プラス」の時は、勝ちたい！
    if current_score > 0:
        # 超高得点（100点以上）なら、手札の一番強いカードを出す
        if current_score >= 100:
            return sorted_hand[-1] # リストの一番最後（最大）
            
        # まあまあの得点（30~99点）なら、真ん中くらいのカードを出して節約する
        elif current_score >= 30:
            mid_index = len(sorted_hand) // 2
            return sorted_hand[mid_index]
            
        # 得点が低いなら、弱いカードを適当に出しておく
        else:
            return sorted_hand[1] # 弱めのカード（0番目はマイナス用に温存）


    # 戦略2：得点が「マイナス」の時は、負けたい！
    elif current_score < 0:
        # 大ダメージ（50点以上のマイナス）の時は、手札で一番弱いカードを出して負ける
        if current_score <= -50:
            return sorted_hand[0] # リストの一番最初（最小）
            
        # 軽いマイナスなら、少し弱めのカードでやり過ごす
        else:
            return sorted_hand[2]
            
    return random.choice(my_info["own_hand"])

