# my_ai.py
import random
import engine

# オセロの盤面における特定の「場所」をリストとして定義しておく
CORNERS = [(0, 0), (7, 0), (0, 7), (7, 7)]

# 角の斜め内側（X打ち）や、角の隣（C打ち）は、相手に角を取られやすくなる危険地帯
DANGER_ZONES = [
    (1, 1), (6, 1), (1, 6), (6, 6), # X打ち（角の斜め内側）
    (1, 0), (6, 0), (0, 1), (7, 1), # C打ち（角の隣）
    (0, 6), (7, 6), (1, 7), (6, 7)  # C打ち（角の隣）
]

# 盤面の端っこ（辺）は比較的安全な場所
EDGES = []
for i in range(2, 6):
    EDGES.extend([(i, 0), (i, 7), (0, i), (7, i)])

def think_action(board, valid_moves, my_color):
    """
    点数表を使わず、「人間の戦略」をif文の優先順位で表現したロジック
    上にあるif文ほど優先して実行されます。
    """

    # =========================================================
    # 戦略1：【角取り】打てる場所の中に「角」があれば、絶対にそこを打つ！
    # =========================================================
    for move in valid_moves:
        if move in CORNERS:
            return move

    # =========================================================
    # 戦略2：【危険回避】打てる場所から、相手に角をあげてしまう「危険地帯」を除外する
    # =========================================================
    safe_moves = []
    for move in valid_moves:
        if move not in DANGER_ZONES:
            safe_moves.append(move)

    # =========================================================
    # 戦略3：【端の確保】安全な場所の中に「端っこ(辺)」があれば優先して取る
    # =========================================================
    if len(safe_moves) > 0:
        edge_moves = []
        for move in safe_moves:
            if move in EDGES:
                edge_moves.append(move)
                
        if len(edge_moves) > 0:
            return random.choice(edge_moves)

        # =========================================================
        # 戦略4：【少なく取る】安全な場所しか残っていない場合、
        # 序盤〜中盤は「あえて一番少なくひっくり返す」のがオセロの定石！
        # （自分の石を増やしすぎると、後で打つ場所がなくなってしまうため）
        # =========================================================
        min_flipped = 999
        best_safe_moves = []
        for move in safe_moves:
            x, y = move
            flipped_count = len(engine.get_flipped_disks(board, x, y, my_color))
            if flipped_count < min_flipped:
                min_flipped = flipped_count
                best_safe_moves = [move]
            elif flipped_count == min_flipped:
                best_safe_moves.append(move)
                
        return random.choice(best_safe_moves)

    # =========================================================
    # 最終手段：安全な場所が1つもない（すべて危険地帯）の大ピンチ！
    # 仕方ないので、危険地帯の中で一番ひっくり返す枚数が少ない場所を選ぶ
    # =========================================================
    min_flipped = 999
    fallback_moves = []
    for move in valid_moves:
        x, y = move
        flipped_count = len(engine.get_flipped_disks(board, x, y, my_color))
        if flipped_count < min_flipped:
            min_flipped = flipped_count
            fallback_moves = [move]
        elif flipped_count == min_flipped:
            fallback_moves.append(move)
            
    return random.choice(fallback_moves)


# 将来的な生徒の実装想定案

# # 1. 相手の選択肢を奪う「モビリティ（着手可能数）の最小化」
# # （★強さの上がり幅：特大）
# # 実はオセロにおける最強の定石は、「自分の石を少なくする」ことではなく、**「相手が次に打てる場所（選択肢）を極限まで減らすこと」**です。相手の打てる場所がなくなれば、相手は嫌でも「危険地帯（X打ちやC打ち）」に打たざるを得なくなります。これを「手どまり」や「モビリティ戦略」と呼びます。

# # ロジックへの落とし込み方:
# # 自分が打った後の「未来の盤面」に対して、engine.get_valid_moves を使って**「相手が打てる場所の数」**を数えます。その数が一番「少なくなる」手を選ぶというロジックです。

# # 実装のイメージ:
# # 先ほどの「戦略4（少なく取る）」の代わりに、このロジックを入れます。


# min_enemy_moves = 999
# best_mobility_moves = []
# enemy_color = -my_color

# for move in safe_moves:
#     # 自分が打った後の未来の盤面を作る
#     future_board = engine.get_next_board(board, move, my_color)
#     # その盤面で、相手が打てる場所の「数」を調べる
#     enemy_moves_count = len(engine.get_valid_moves(future_board, enemy_color))

#     if enemy_moves_count < min_enemy_moves:
#         min_enemy_moves = enemy_moves_count
#         best_mobility_moves = [move]
#     elif enemy_moves_count == min_enemy_moves:
#         best_mobility_moves.append(move)

# return random.choice(best_mobility_moves)


# 2. 状況に応じた「危険地帯の解除」
# （★強さの上がり幅：大）
# 現在のコードでは、角の隣（DANGER_ZONES）を無条件で避けていますが、これは大きな機会損失を生むことがあります。
# **「すでに自分がその角を取っているなら、その隣はもはや危険地帯ではなく『絶対に返されない最強の陣地（確定石）』になる」**というオセロのセオリーがあります。

# ロジックへの落とし込み方:
# DANGER_ZONES から除外する前に、if文で「角の所有者」を確認します。
# 「もし board[0][0]（左上の角）が my_color なら、(0, 1), (1, 0), (1, 1) は安全リストに昇格させる」という条件分岐を追加します。

# 3. 辺の悪手「ウイング」の回避
# （★強さの上がり幅：中）
# 現在のコードは「端っこ（EDGES）なら優先して取る」としていますが、これも諸刃の剣です。
# 端っこに自分の石が並んでいても、**角に隣接するマス（C打ちの場所）に石があり、かつ角が空いている形（これをウイングと呼びます）**は、相手に角を奪われる絶好の隙を与えてしまいます。

# ロジックへの落とし込み方:
# 端っこを取る時、その手が「ウイング」を作ってしまう手かどうかを判定し、ウイングになるならその端っこは避ける、というif文を書きます。これは少し複雑な条件分岐になるため、プログラミングの論理的思考力を試す絶好の課題になります。

# # 4. 終盤の「勝ち確」スイッチ（ゲームフェーズの認識）
# # （★強さの上がり幅：大）
# # 序盤〜中盤は「少なく取る」「相手の手を減らす」が最強ですが、ゲームの終盤（盤面の空きマスが残り10マス〜12マス程度）になると、このロジックは裏目に出ます。終盤は「とにかく1枚でも多く自分の色にする（あるいは最終的に勝つ形を完全に読み切る）」必要があります。

# # ロジックへの落とし込み方:
# # 関数の冒頭で、盤面全体の「石の数（または空きマスの数）」を for 文でカウントします。


# empty_count = sum(row.count(0) for row in board)

# if empty_count <= 10:
#     # 【終盤モード】危険地帯も関係ない！とにかく一番多くひっくり返せる手を選ぶ！
#     # （ここにCPUと同じ貪欲法のロジックを書く）
# else:
#     # 【序盤・中盤モード】角を取ったり、相手の手を減らしたりする（いつものロジック）