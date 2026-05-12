# main.py
import engine
import cpu_ai
import my_ai
import my_ai_advanced

print("あなたのAI VS ランダムCPU")
# 1000回対戦させて勝率をチェック
engine.run_games(player0_ai=my_ai, player1_ai=cpu_ai, num_games=1000)