# engine.py
import random
import copy

def get_initial_state():
    """ゲームの初期状態を生成する"""
    # スコア用山札：ハート(+1〜+13)とダイヤ(-1〜-13)
    score_deck = [i for i in range(1, 14)] + [-i for i in range(1, 14)]
    random.shuffle(score_deck)
    
    return {
        "score_deck": score_deck,
        "p0_hand": list(range(1, 14)), # プレイヤー0の手札(1〜13)
        "p1_hand": list(range(1, 14)), # プレイヤー1の手札(1〜13)
        "p0_score": 0,
        "p1_score": 0,
        "p0_used": [], # 相手の思考を読むために、使ったカードを記録
        "p1_used": []
    }

def run_games(player0_ai, player1_ai, num_games=1000):
    p0_wins = 0
    p1_wins = 0
    draws = 0
    
    print(f"🎮 トランプ心理戦AI 自動対戦を {num_games} 試合開始します...\n")
    
    for game in range(num_games):
        state = get_initial_state()
        
        # 全7ターン進行する
        for turn in range(1, 8):
            # 山札から2枚めくって得点を計算する
            card1 = state["score_deck"].pop()
            card2 = state["score_deck"].pop()
            turn_score = card1 * card2
            
            # AIに渡す情報を準備
            # 不正防止のため、相手の手札や山札の残りは渡さない
            p0_info = {
                "turn": turn,
                "current_score": turn_score,
                "my_hand": copy.deepcopy(state["p0_hand"]),
                "my_total": state["p0_score"],
                "enemy_total": state["p1_score"],
                "enemy_used": copy.deepcopy(state["p1_used"])
            }
            p1_info = {
                "turn": turn,
                "current_score": turn_score,
                "my_hand": copy.deepcopy(state["p1_hand"]),
                "my_total": state["p1_score"],
                "enemy_total": state["p0_score"],
                "enemy_used": copy.deepcopy(state["p0_used"])
            }
            
            # 両プレイヤーが同時にカードを選ぶ
            try:
                p0_play = player0_ai.think_action(**p0_info)
                if p0_play not in state["p0_hand"]: p0_play = random.choice(state["p0_hand"])
            except:
                p0_play = random.choice(state["p0_hand"])
                
            try:
                p1_play = player1_ai.think_action(**p1_info)
                if p1_play not in state["p1_hand"]: p1_play = random.choice(state["p1_hand"])
            except:
                p1_play = random.choice(state["p1_hand"])
                
            # 出したカードを手札から消し、使用済みリストに追加
            state["p0_hand"].remove(p0_play)
            state["p1_hand"].remove(p1_play)
            state["p0_used"].append(p0_play)
            state["p1_used"].append(p1_play)
            
            # 勝敗判定（数字が大きい方が得点を獲得）
            if p0_play > p1_play:
                state["p0_score"] += turn_score
            elif p1_play > p0_play:
                state["p1_score"] += turn_score
            # 引き分けの場合はどちらにも得点は入らない（流れる）

        # 7ターン終了時の合計スコアで勝敗決定
        if state["p0_score"] > state["p1_score"]:
            p0_wins += 1
        elif state["p1_score"] > state["p0_score"]:
            p1_wins += 1
        else:
            draws += 1
            
    print("=== 最終結果 ===")
    print(f"Player 0 の勝利: {p0_wins} 回")
    print(f"Player 1 の勝利: {p1_wins} 回")
    print(f"引き分け: {draws} 回")