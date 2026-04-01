# main.py
import engine
import cpu_ai
import my_ai

print("【第1部】 あなた(黒:先手) VS 相手CPU(白:後手)")
engine.run_games(player1_ai=my_ai, player2_ai=cpu_ai, num_games=20)

print("\n-----------------------------------\n")

print("【第2部】 相手CPU(黒:先手) VS あなた(白:後手)")
engine.run_games(player1_ai=cpu_ai, player2_ai=my_ai, num_games=20)