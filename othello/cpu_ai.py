# cpu_ai.py
import engine
import random

def think_action(board, valid_moves, my_color):
    """
    CPUの思考ロジック：
    打てる場所の中で、一番たくさん石をひっくり返せる場所を選ぶ（貪欲法）
    同点の場合はランダムに選択する
    """
    max_flipped = -1
    best_moves = []
    
    for move in valid_moves:
        x, y = move
        # その場所に打ったら何枚ひっくり返るか取得
        flipped_disks = engine.get_flipped_disks(board, x, y, my_color)
        num_flipped = len(flipped_disks)
        
        # もし今までの最高記録を「更新」したら、リストをリセットして入れ直す
        if num_flipped > max_flipped:
            max_flipped = num_flipped
            best_moves = [move]
            
        # もし今までの最高記録と「同点」なら、リストに追加（仲間にいれる）
        elif num_flipped == max_flipped:
            best_moves.append(move)
            
    # 同点1位の候補の中から、ランダムに1つ選んで返す
    return random.choice(best_moves)
