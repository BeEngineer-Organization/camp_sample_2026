# cpu_ai.py
import engine
import random

def think_action(board, valid_moves, my_color):
    """一番多く石をひっくり返せる場所を選ぶだけのAI"""
    best_moves = []
    max_flipped = -1
    
    for move in valid_moves:
        x, y = move
        flipped = len(engine.get_flipped_disks(board, x, y, my_color))
        if flipped > max_flipped:
            max_flipped = flipped
            best_moves = [move]
        elif flipped == max_flipped:
            best_moves.append(move)
            
    return random.choice(best_moves)