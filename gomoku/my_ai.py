# my_ai.py
import engine
import random

def count_lines(board, x, y, player):
    """
    【ヘルパー関数】
    指定した座標(x, y)に石を置いたと仮定して、
    「タテ・ヨコ・ナナメに何個石が繋がるか」を計算し、その点数を返す。
    """
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    score = 0
    
    for dx, dy in directions:
        count = 1 # 置いた石自身でまず1個
        
        # プラス方向（右、下など）にいくつ繋がっているか
        nx, ny = x + dx, y + dy
        while 0 <= nx < engine.BOARD_SIZE and 0 <= ny < engine.BOARD_SIZE and board[ny][nx] == player:
            count += 1
            nx += dx
            ny += dy
            
        # マイナス方向（左、上など）にいくつ繋がっているか
        nx, ny = x - dx, y - dy
        while 0 <= nx < engine.BOARD_SIZE and 0 <= ny < engine.BOARD_SIZE and board[ny][nx] == player:
            count += 1
            nx -= dx
            ny -= dy
            
        # 繋がった数に応じて激しく点数をつける！
        if count >= 5: score += 100000  # 5個並ぶなら絶対勝てる！
        elif count == 4: score += 10000 # 4個並ぶ（リーチ）
        elif count == 3: score += 100   # 3個並ぶ
        elif count == 2: score += 10    # 2個並ぶ
        
    return score

def think_action(board, valid_moves, my_player):

    """候補（石の周り）の中からランダムに打つだけの弱いAI"""
    return random.choice(valid_moves)

    # """
    # 五目並べのAIのメインロジック。
    # 「攻撃のチャンス」と「防御のピンチ」を両方採点する！
    # """
    # best_score = -1
    # best_moves = []
    # enemy_player = 3 - my_player # 自分が1なら相手は2、自分が2なら相手は1になる計算
    
    # for move in valid_moves:
    #     x, y = move
        
    #     # 1. 攻撃の点数：ここに「自分」の石を置いたら、何個繋がるか？
    #     attack_score = count_lines(board, x, y, my_player)
        
    #     # 2. 防御の点数：ここに「相手」が石を置いたら、相手は何個繋がってしまうか？
    #     # （相手が5個繋がる場所を自分が先に奪えば、それは自分の勝利と同じ価値がある！）
    #     defense_score = count_lines(board, x, y, enemy_player)
        
    #     # 🌟 生徒が考えるポイント：攻撃と防御、どっちを優先する？ 🌟
    #     # とりあえず合計して、その場所の「総合的な価値」とする
    #     total_score = attack_score + defense_score
        
    #     # 最高得点を更新した場合
    #     if total_score > best_score:
    #         best_score = total_score
    #         best_moves = [move]
    #     # 同点だった場合
    #     elif total_score == best_score:
    #         best_moves.append(move)
            
    # # 最高得点の手の中からランダムに選ぶ
    # return random.choice(best_moves)