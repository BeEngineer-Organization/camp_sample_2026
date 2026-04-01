# engine.py
import copy
from collections import deque

# 盤面は9x9マス。
# Player 0 は y=8(一番下)を目指し、Player 1 は y=0(一番上)を目指す。

def get_initial_state():
    return {
        "p_pos": [(4, 1), (4, 7)], # 各プレイヤーの(x, y)座標（Player 0は下から、Player 1は上から）
        "walls": set(),            # ("h", x, y) 横壁 または ("v", x, y) 縦壁
        "wall_counts": [10, 10]    # 残りの壁の枚数
    }

def is_wall_blocking(walls, x, y, nx, ny):
    """マス(x, y)から(nx, ny)へ移動する間に壁があるか判定する"""
    if x == nx:
        if y < ny: # 下へ移動
            return ("h", x, y) in walls or ("h", x-1, y) in walls
        else:      # 上へ移動
            return ("h", x, y-1) in walls or ("h", x-1, y-1) in walls
    elif y == ny:
        if x < nx: # 右へ移動
            return ("v", x, y) in walls or ("v", x, y-1) in walls
        else:      # 左へ移動
            return ("v", x-1, y) in walls or ("v", x-1, y-1) in walls
    return True

def is_valid_wall(walls, d, x, y):
    """その場所に壁を置けるか（他の壁と衝突しないか）判定する"""
    if (d, x, y) in walls: return False
    if d == "h":
        if ("h", x-1, y) in walls or ("h", x+1, y) in walls or ("v", x, y) in walls:
            return False
    else: # "v"
        if ("v", x, y-1) in walls or ("v", x, y+1) in walls or ("h", x, y) in walls:
            return False
    return True

def get_shortest_path_distance(pos, player_id, walls):
    """
    【重要】AIが使うヘルパー関数。
    現在地(pos)からゴールまでの「最短距離（何歩で着くか）」を計算して返す。
    道が完全に塞がれている場合は 999 を返す。
    """
    queue = deque([(pos[0], pos[1], 0)])
    visited = set([pos])
    target_y = 8 if player_id == 0 else 0
    
    while queue:
        x, y, dist = queue.popleft()
        if y == target_y:
            return dist
            
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 9 and 0 <= ny < 9:
                if not is_wall_blocking(walls, x, y, nx, ny):
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny, dist + 1))
    return 999 # ゴール不可（ルール違反の壁置きを検知するため）

def get_valid_moves(state, player):
    """現在選べる「移動」と「壁置き」のすべてのアクションをリストで返す"""
    moves = []
    px, py = state["p_pos"][player]
    enemy_pos = state["p_pos"][1 - player]
    walls = state["walls"]
    
    # 1. 移動手 ("move", nx, ny) の列挙
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = px + dx, py + dy
        if 0 <= nx < 9 and 0 <= ny < 9:
            if not is_wall_blocking(walls, px, py, nx, ny):
                if (nx, ny) == enemy_pos:
                    # 相手がいる場合、真っ直ぐ飛び越せるかチェック
                    nnx, nny = nx + dx, ny + dy
                    if 0 <= nnx < 9 and 0 <= nny < 9:
                        if not is_wall_blocking(walls, nx, ny, nnx, nny):
                            moves.append(("move", nnx, nny))
                else:
                    moves.append(("move", nx, ny))
                    
    # 2. 壁置き手 ("wall", d, x, y) の列挙
    if state["wall_counts"][player] > 0:
        for d in ["h", "v"]:
            for x in range(8):
                for y in range(8):
                    if is_valid_wall(walls, d, x, y):
                        # 壁を置いた後、両者がゴールにたどり着けるか（閉じ込めていないか）チェック
                        new_walls = walls.copy()
                        new_walls.add((d, x, y))
                        if get_shortest_path_distance(state["p_pos"][0], 0, new_walls) != 999 and \
                           get_shortest_path_distance(state["p_pos"][1], 1, new_walls) != 999:
                            moves.append(("wall", d, x, y))
    
    return moves

def get_next_state(state, move, player):
    """行動を適用した未来の盤面を返す"""
    new_state = {
        "p_pos": list(state["p_pos"]),
        "walls": set(state["walls"]),
        "wall_counts": list(state["wall_counts"])
    }
    
    if move[0] == "move":
        new_state["p_pos"][player] = (move[1], move[2])
    elif move[0] == "wall":
        new_state["walls"].add((move[1], move[2], move[3]))
        new_state["wall_counts"][player] -= 1
        
    return new_state

def run_games(player0_ai, player1_ai, num_games=10):
    p0_wins = 0
    p1_wins = 0
    print(f"🎮 コリドールAI 自動対戦を {num_games} 試合開始します...\n")
    
    for game in range(num_games):
        state = get_initial_state()
        current_player = 0
        turn = 0
        
        while turn < 200: # 無限ループ防止
            valid_moves = get_valid_moves(state, current_player)
            ai = player0_ai if current_player == 0 else player1_ai
            
            try:
                move = ai.think_action(copy.deepcopy(state), valid_moves, current_player)
                if move not in valid_moves:
                    move = valid_moves[0]
            except Exception as e:
                print(f"AIエラー (Player {current_player}): {e}")
                move = valid_moves[0]
                
            state = get_next_state(state, move, current_player)
            
            # 勝敗判定
            if state["p_pos"][0][1] == 8:
                p0_wins += 1; break
            elif state["p_pos"][1][1] == 0:
                p1_wins += 1; break
                
            current_player = 1 - current_player
            turn += 1
            
    print("=== 最終結果 ===")
    print(f"先手 (Player 0) の勝利: {p0_wins} 回")
    print(f"後手 (Player 1) の勝利: {p1_wins} 回")