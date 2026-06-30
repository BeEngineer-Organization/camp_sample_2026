# B. スコア差による場合分け
import random

def think_action(my_info):

    current_score = my_info["card1"] * my_info["card2"]
    
    # 手札を小さい順に並べ替えておく
    sorted_hand = sorted(my_info["own_hand"])

    # スコア差を計算
    score_diff = my_info["own_total"] - my_info["enemy_total"]

    # 戦略1：得点が「プラス」の時は、勝ちたい！
    if current_score > 0:
        # 超高得点（100点以上）なら、手札の一番強いカードを出す
        if current_score >= 100:
            return sorted_hand[-1] # リストの一番最後（最大）
            
        # まあまあの得点（30~99点）なら、真ん中くらいのカードを出して節約する
        elif current_score >= 30:

            # 接戦のときには勝ちにいく
            if -20 <= score_diff <= 20:
                return sorted_hand[-1]
            
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

            # 接戦のときには負けにいく
            if -20 <= score_diff <= 20:
                return sorted_hand[0]
            
            return sorted_hand[2]
            
    return random.choice(my_info["own_hand"])