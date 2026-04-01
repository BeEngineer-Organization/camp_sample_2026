# main.py
import engine
import cpu_ai
import my_ai

# プレイヤーの参加セット（自分のAI 1人 vs CPU 3人）
players = [
    my_ai,          # Player 0: 生徒のAI
    cpu_ai,         # Player 1: 敵AI
    cpu_ai,         # Player 2: 敵AI
    cpu_ai          # Player 3: 敵AI
]

# 1000回対戦させる！
engine.run_games(players, num_games=1000)