# main.py
import engine
import cpu_ai
import my_ai

print("【第1部】 あなた(先手:下から上へ) VS 相手CPU(後手:上から下へ)")
engine.run_games(player0_ai=my_ai, player1_ai=cpu_ai, num_games=10)

print("\n-----------------------------------\n")

print("【第2部】 相手CPU(先手) VS あなた(後手)")
engine.run_games(player0_ai=cpu_ai, player1_ai=my_ai, num_games=10)