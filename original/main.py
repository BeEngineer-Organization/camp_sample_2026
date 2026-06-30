# main.py
import engine
import cpu_ai
import my_ai

print("自分のAI VS ランダムCPU")
# 1000回対戦させて勝率をチェック
engine.run_games(my_ai=my_ai, cpu_ai=cpu_ai, num_games=1000)
