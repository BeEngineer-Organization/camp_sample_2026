# engine.py
import random
import copy
import itertools
from collections import defaultdict

def create_deck():
    """デッキを作成する"""
    suits = ["spade", "heart", "diamond", "club"]
    deck = []
    for suit in suits:
        for num in range(1, 14):
            # カードの強さ（3が最弱、2が最強、Aは14、2は15）
            if num == 1: power = 14
            elif num == 2: power = 15
            else: power = num
            deck.append({"suit": suit, "num": num, "power": power})
    deck.append({"suit": "joker", "num": 0, "power": 16}) # Jokerは最強
    return deck

def is_stronger(play_power, field_power, is_revolution):
    """カードの強さを比較する（革命対応）"""
    if play_power == 16: return True  # Jokerは革命時も常に強い設定
    if field_power == 16: return False
    if is_revolution:
        return play_power < field_power
    return play_power > field_power

def get_legal_moves(hand, field_state):
    """手札から、ルール上出せるカードの組み合わせリストを返す"""
    moves = [[]] # 空リストは「パス」を意味し、常に合法
    
    # 手札を数字ごとにグループ化
    num_groups = defaultdict(list)
    jokers = []
    for c in hand:
        if c["suit"] == "joker":
            jokers.append(c)
        else:
            num_groups[c["num"]].append(c)

    field_cards = field_state["cards"]
    is_rev = field_state["is_revolution"]
    bound_suits = field_state["bound_suit"]

    if len(field_cards) == 0:
        # 場が空の場合：任意のペア数が出せる
        for num, cards in num_groups.items():
            for i in range(1, len(cards) + 1):
                for combo in itertools.combinations(cards, i):
                    moves.append(list(combo))
        if jokers:
            moves.append([jokers[0]])
    else:
        # 場にカードがある場合
        field_len = len(field_cards)
        
        # スペ3返し判定（場がJoker1枚の時）
        if field_len == 1 and field_cards[0]["suit"] == "joker":
            spade3 = [c for c in hand if c["suit"] == "spade" and c["num"] == 3]
            if spade3:
                moves.append([spade3[0]])
                
        field_power = field_cards[0]["power"]

        # ペア出しの判定
        for num, cards in num_groups.items():
            if len(cards) >= field_len:
                for combo in itertools.combinations(cards, field_len):
                    combo_list = list(combo)
                    if is_stronger(combo_list[0]["power"], field_power, is_rev):
                        # スート縛りの判定
                        if bound_suits:
                            combo_suits = set(c["suit"] for c in combo_list)
                            if set(bound_suits) == combo_suits:
                                moves.append(combo_list)
                        else:
                            moves.append(combo_list)
        # Jokerの単体出し
        if jokers and field_len == 1:
            moves.append([jokers[0]])

    return moves

def run_games(players, num_games=100):
    """ゲームを進行するメインループ"""
    win_counts = {i: 0 for i in range(len(players))}
    
    print(f"🎮 {num_games}回の自動対戦テストを開始します...\n")

    for game_id in range(num_games):
        deck = create_deck()
        random.shuffle(deck)
        hands = [deck[i::len(players)] for i in range(len(players))]
        
        field_state = {
            "cards": [],
            "is_revolution": False,
            "bound_suit": None,
            "pass_count": 0
        }
        
        active_players = list(range(len(players)))
        turn_idx = 0
        ranks = []
        
        while len(active_players) > 1:
            # 全員パスで場が流れる
            if field_state["pass_count"] >= len(active_players) - 1 and len(field_state["cards"]) > 0:
                field_state["cards"] = []
                field_state["bound_suit"] = None
                field_state["pass_count"] = 0
                
            p_idx = active_players[turn_idx % len(active_players)]
            player_module = players[p_idx]
            current_hand = hands[p_idx]
            
            legal_moves = get_legal_moves(current_hand, field_state)
            
            # AIの行動を取得（エラー時は強制パス）
            try:
                played_cards = player_module.think_action(
                    copy.deepcopy(current_hand),
                    copy.deepcopy(field_state),
                    copy.deepcopy(legal_moves)
                )
            except Exception as e:
                played_cards = []

            # AIが返してきた手（played_cards）が、本当にlegal_movesの中に存在するかチェック
            is_valid = False
            play_sigs = set((c["suit"], c["num"]) for c in played_cards)
            for move in legal_moves:
                move_sigs = set((c["suit"], c["num"]) for c in move)
                if move_sigs == play_sigs:
                    is_valid = True
                    break
                    
            if not is_valid:
                played_cards = [] # 不正な手はパス扱い
                
            if len(played_cards) == 0:
                field_state["pass_count"] += 1
            else:
                field_state["pass_count"] = 0
                
                # スート縛りの発生判定
                if len(field_state["cards"]) > 0 and field_state["bound_suit"] is None:
                    prev_suits = set(c["suit"] for c in field_state["cards"])
                    curr_suits = set(c["suit"] for c in played_cards)
                    if prev_suits == curr_suits:
                        field_state["bound_suit"] = list(curr_suits)
                
                field_state["cards"] = played_cards
                
                # 手札から出したカードを削除
                for pc in played_cards:
                    hands[p_idx] = [c for c in hands[p_idx] if not (c["suit"] == pc["suit"] and c["num"] == pc["num"])]
                
                force_clear = False
                
                # 【8切り】判定
                if any(c["num"] == 8 for c in played_cards):
                    force_clear = True
                    
                # 【スペ3返し】判定
                if len(played_cards) == 1 and played_cards[0]["suit"] == "spade" and played_cards[0]["num"] == 3:
                    if len(field_state["cards"]) == 1 and field_state["cards"][0]["suit"] == "joker":
                        force_clear = True
                        
                # 【革命】判定
                if len(played_cards) >= 4:
                    field_state["is_revolution"] = not field_state["is_revolution"]
                    
                # 【7渡し】判定
                sevens_count = sum(1 for c in played_cards if c["num"] == 7)
                for _ in range(sevens_count):
                    if len(hands[p_idx]) > 0:
                        try:
                            # AIに渡すカードを選ばせる
                            give_c = player_module.think_give_card(copy.deepcopy(hands[p_idx]))
                            # 自分の手札から削除
                            hands[p_idx] = [c for c in hands[p_idx] if not (c["suit"] == give_c["suit"] and c["num"] == give_c["num"])]
                            # 次の生き残っているプレイヤーを探して渡す
                            next_idx_pos = (active_players.index(p_idx) + 1) % len(active_players)
                            hands[active_players[next_idx_pos]].append(give_c)
                        except:
                            pass # エラー時は渡さない処理にする

                if force_clear:
                    field_state["cards"] = []
                    field_state["bound_suit"] = None
                    field_state["pass_count"] = 0
                    if len(hands[p_idx]) > 0:
                        continue # 8を出した本人のターンから再開（turn_idxを進めない）

            # 上がり判定
            if len(hands[p_idx]) == 0:
                ranks.append(p_idx)
                active_players.remove(p_idx)
            else:
                turn_idx += 1
                
        # 最後に残った1人を記録
        ranks.append(active_players[0])
        win_counts[ranks[0]] += 1 # 1位の回数を加算

    print("=== 最終勝率レポート ===")
    for p_idx, wins in win_counts.items():
        win_rate = (wins / num_games) * 100
        name = "あなた(my_ai)" if p_idx == 0 else f"CPU_{p_idx}"
        print(f"{name} の1位獲得回数: {wins}回 (勝率 {win_rate:.1f}%)")