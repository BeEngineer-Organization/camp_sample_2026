# my_ai.py

def think_action(turn, current_score, my_hand, my_total, enemy_total, enemy_used):
    """
    最強を目指したAIの思考ロジック。
    
    戦略の柱：
    1. 相手の残り手札を推測して、ギリギリ勝てる/負けるカードを選ぶ
    2. スコア差を考慮して、リスク管理を行う
    3. ターン進行に応じて、手札の温存と使用のバランスを取る
    """
    
    # 手札を小さい順に並べ替え
    sorted_hand = sorted(my_hand)
    
    # 相手の残り手札を推測（1～13から使用済みを除く）
    all_cards = set(range(1, 14))
    enemy_remaining = sorted(list(all_cards - set(enemy_used)))
    
    # 相手の最大値と最小値を把握
    enemy_max = enemy_remaining[-1] if enemy_remaining else 0
    enemy_min = enemy_remaining[0] if enemy_remaining else 14
    
    # スコア差を計算
    score_diff = my_total - enemy_total
    
    # 残りターン数
    remaining_turns = 8 - turn
    
    # =========================================================
    # 戦略1：プラス得点の場合 - 勝ちたい
    # =========================================================
    if current_score > 0:
        # 超高得点（100点以上）の場合
        if current_score >= 100:
            # 相手の最大値より大きいカードで確実に勝つ
            for card in sorted_hand:
                if card > enemy_max:
                    return card
            # 全てのカードが相手の最大値以下なら、最大値を出す
            return sorted_hand[-1]
        
        # 高得点（50～99点）の場合
        elif current_score >= 50:
            # 相手の最大値+1のカードがあれば、それを出す（最小コストで勝つ）
            for card in sorted_hand:
                if card > enemy_max:
                    return card
            # なければ、手札の上位30%のカードを出す
            target_index = max(len(sorted_hand) - 1 - len(sorted_hand) // 3, 0)
            return sorted_hand[target_index]
        
        # 中得点（20～49点）の場合
        elif current_score >= 20:
            # 大きくリードしている場合（50点以上差）は節約
            if score_diff >= 50:
                # 相手の平均値より少し上のカードを出す
                enemy_avg = sum(enemy_remaining) / len(enemy_remaining) if enemy_remaining else 7
                for card in sorted_hand:
                    if card > enemy_avg:
                        return card
                return sorted_hand[len(sorted_hand) // 2]
            
            # 接戦または負けている場合は、中間カードで勝負
            mid_index = len(sorted_hand) // 2
            return sorted_hand[mid_index]
        
        # 低得点（1～19点）の場合
        else:
            # 終盤（残り2ターン以下）なら、弱いカードを出して温存
            if remaining_turns <= 2:
                return sorted_hand[0]
            
            # 序盤～中盤は、相手の中央値より少し下のカードで様子見
            if len(sorted_hand) >= 3:
                return sorted_hand[1]
            else:
                return sorted_hand[0]
    
    # =========================================================
    # 戦略2：マイナス得点の場合 - 負けたい（相手に押し付ける）
    # =========================================================
    elif current_score < 0:
        # 超大ダメージ（-100点以下）の場合
        if current_score <= -100:
            # 相手の最小値より小さいカードで確実に負ける
            for card in reversed(sorted_hand):
                if card < enemy_min:
                    return card
            # 全てのカードが相手の最小値以上なら、最小値を出す
            return sorted_hand[0]
        
        # 大ダメージ（-50～-99点）の場合
        elif current_score <= -50:
            # 相手の最小値-1のカードがあれば、それを出す（確実に負ける）
            for card in reversed(sorted_hand):
                if card < enemy_min:
                    return card
            # なければ、最弱カードを出す
            return sorted_hand[0]
        
        # 中ダメージ（-20～-49点）の場合
        elif current_score <= -20:
            # 大きく負けている場合（-50点以上差）は、あえてマイナスを引き取る
            if score_diff <= -50:
                # 相手の中央値より上のカードで勝ちに行く
                if enemy_remaining:
                    enemy_median = enemy_remaining[len(enemy_remaining) // 2]
                    for card in sorted_hand:
                        if card > enemy_median:
                            return card
                return sorted_hand[-1]
            
            # リードしている、または接戦の場合は負けを狙う
            return sorted_hand[0]
        
        # 軽いダメージ（-1～-19点）の場合
        else:
            # 終盤なら最弱カードで負ける
            if remaining_turns <= 2:
                return sorted_hand[0]
            
            # 序盤～中盤は、相手の下位カードより少し下を出す
            if len(sorted_hand) >= 2:
                return sorted_hand[0]
            else:
                return sorted_hand[0]
    
    # =========================================================
    # 戦略3：得点が0の場合 - 引き分け狙い or 最弱カード
    # =========================================================
    else:
        # 相手の使用済みカードから、相手が出しそうなカードを予測
        # 相手も0点なので適当に出す可能性が高い → 最弱カードを出す
        return sorted_hand[0]
