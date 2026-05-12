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
        "my_hand": list(range(1, 14)), # プレイヤー0の手札(1〜13)
        "cpu_hand": list(range(1, 14)), # プレイヤー1の手札(1〜13)
        "my_score": 0,
        "cpu_score": 0,
        "my_used": [], # 相手の思考を読むために、使ったカードを記録
        "cpu_used": []
    }

def run_games(my_ai, cpu_ai, num_games=1000):
    my_wins = 0
    cpu_wins = 0
    draws = 0
    
    print(f"オリジナルゲーム 自動対戦を {num_games} 試合開始します。")
    
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
            my_info = {
                "turn": turn,
                "current_score": turn_score,
                "own_hand": copy.deepcopy(state["my_hand"]),
                "own_total": state["my_score"],
                "enemy_total": state["cpu_score"],
                "enemy_used": copy.deepcopy(state["cpu_used"])
            }
            cpu_info = {
                "turn": turn,
                "current_score": turn_score,
                "own_hand": copy.deepcopy(state["cpu_hand"]),
                "own_total": state["cpu_score"],
                "enemy_total": state["my_score"],
                "enemy_used": copy.deepcopy(state["my_used"])
            }
            
            # 両プレイヤーが同時にカードを選ぶ
            my_play = my_ai.think_action(my_info)
            if my_play in state["my_hand"]:
                pass
            else:
                my_play = random.choice(state["my_hand"])
                
            cpu_play = cpu_ai.think_action(cpu_info)
            if cpu_play in state["cpu_hand"]:
                pass
            else:
                cpu_play = random.choice(state["cpu_hand"])
                
            # 出したカードを手札から消し、使用済みリストに追加
            state["my_hand"].remove(my_play)
            state["cpu_hand"].remove(cpu_play)
            state["my_used"].append(my_play)
            state["cpu_used"].append(cpu_play)
            
            # 勝敗判定（数字が大きい方が得点を獲得）
            if my_play > cpu_play:
                state["my_score"] += turn_score
            elif cpu_play > my_play:
                state["cpu_score"] += turn_score
            # 引き分けの場合はどちらにも得点は入らない（流れる）

        # 7ターン終了時の合計スコアで勝敗決定
        if state["my_score"] > state["cpu_score"]:
            my_wins += 1
        elif state["cpu_score"] > state["my_score"]:
            cpu_wins += 1
        else:
            draws += 1
            
    print("【最終結果】")
    print(f"あなたの勝利: {my_wins} 回")
    print(f"CPUの勝利: {cpu_wins} 回")
    print(f"引き分け: {draws} 回")