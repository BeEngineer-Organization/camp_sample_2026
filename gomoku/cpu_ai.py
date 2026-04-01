# cpu_ai.py
import random

def think_action(board, valid_moves, my_player):
    """候補（石の周り）の中からランダムに打つだけの弱いAI"""
    return random.choice(valid_moves)