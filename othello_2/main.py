# main.py
import engine
import cpu_ai
import my_ai

print("【第1部】 あなたのロジックAI(黒:先手) VS 単純CPU(白:後手)")
engine.run_games(player_black=my_ai, player_white=cpu_ai, num_games=50)

print("\n-----------------------------------\n")

print("【第2部】 単純CPU(黒:先手) VS あなたのロジックAI(白:後手)")
engine.run_games(player_black=cpu_ai, player_white=my_ai, num_games=50)