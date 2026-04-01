# main.py
import engine
import cpu_ai
import my_ai

print("【第1部】 あなた(黒:先手) VS 相手CPU(白:後手)")
# 50回対戦させる
engine.run_games(player_black=my_ai, player_white=cpu_ai, num_games=50)

print("\n-----------------------------------\n")

print("【第2部】 相手CPU(黒:先手) VS あなた(白:後手)")
# 攻守を入れ替えて50回対戦させる
engine.run_games(player_black=cpu_ai, player_white=my_ai, num_games=50)