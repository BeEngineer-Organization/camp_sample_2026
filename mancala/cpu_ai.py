# cpu_ai.py
import random

def think_action(board, valid_moves, my_player):
    """何も考えず、選べる穴の中からランダムに1つ選ぶ弱いAI"""
    return random.choice(valid_moves)