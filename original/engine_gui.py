import pygame
import random
import copy
import sys
import os
import argparse
import importlib

# ゲームの初期化
pygame.init()

# フォント設定
import os

font_path = "/System/Library/Fonts/Hiragino Sans GB.ttc"

if os.path.exists(font_path):
    font = pygame.font.Font(font_path, 24)
    large_font = pygame.font.Font(font_path, 36)
else:
    # 別の候補パス
    font_path_alt = "/System/Library/Fonts/STHeiti Light.ttc"
    if os.path.exists(font_path_alt):
        font = pygame.font.Font(font_path_alt, 24)
        large_font = pygame.font.Font(font_path_alt, 36)
    else:
        font = pygame.font.SysFont(None, 24)
        large_font = pygame.font.SysFont(None, 36)

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AI Card Game Engine")
clock = pygame.time.Clock()

# カラー定義
BG_COLOR = (30, 40, 50)
CARD_SCORE_POS = (180, 50, 50)
CARD_SCORE_NEG = (50, 100, 150)
P1_COLOR = (50, 180, 100)  # プレイヤー1の色 (旧MY)
P2_COLOR = (200, 80, 80)  # プレイヤー2の色 (旧CPU)
TEXT_COLOR = (240, 240, 240)

def get_initial_state():
    score_deck = [i for i in range(1, 14)] + [-i for i in range(1, 14)]
    random.shuffle(score_deck)
    return {
        "score_deck": score_deck,
        "p1_hand": list(range(1, 14)),
        "p2_hand": list(range(1, 14)),
        "p1_score": 0,
        "p2_score": 0,
        "p1_used": [],
        "p2_used": []
    }

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_card(text, x, y, width, height, bg_color):
    pygame.draw.rect(screen, bg_color, (x, y, width, height), border_radius=5)
    pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height), 2, border_radius=5)
    txt_img = font.render(text, True, TEXT_COLOR)
    txt_rect = txt_img.get_rect(center=(x + width/2, y + height/2))
    screen.blit(txt_img, txt_rect)

def main():
    # --- コマンドライン引数の解析 ---
    parser = argparse.ArgumentParser(description="AI Card Game Tournament")
    parser.add_argument("ai1", help="プレイヤー1のAIファイル名 (拡張子なし)")
    parser.add_argument("ai2", help="プレイヤー2のAIファイル名 (拡張子なし)")
    parser.add_argument("--name1", default="Player1", help="プレイヤー1の表示名")
    parser.add_argument("--name2", default="Player2", help="プレイヤー2の表示名")
    args = parser.parse_args()

    # 指定されたAIファイルを動的にインポート
    try:
        ai1_module = importlib.import_module(args.ai1)
        ai2_module = importlib.import_module(args.ai2)
    except ModuleNotFoundError as e:
        print(f"エラー: AIファイルが見つかりません。 {e}")
        sys.exit(1)

    name1 = args.name1
    name2 = args.name2

    # --- ゲーム状態の初期化 ---
    state = get_initial_state()
    turn = 1
    game_count = 1
    MAX_GAMES = 3
    
    p1_wins = 0
    p2_wins = 0
    draws = 0
    
    card1 = state["score_deck"].pop()
    card2 = state["score_deck"].pop()
    
    p1_play, p2_play = None, None
    turn_resolved = False
    game_over = False
    all_games_over = False

    while True:
        screen.fill(BG_COLOR)
        
        # --- イベント処理 ---
        advance_step = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                advance_step = True

        # --- ロジック処理 ---
        if advance_step and not all_games_over:
            if not game_over:
                if not turn_resolved:
                    p1_info = {
                        "turn": turn, "card1": card1, "card2": card2,
                        "own_hand": copy.deepcopy(state["p1_hand"]), "own_total": state["p1_score"],
                        "enemy_total": state["p2_score"], "enemy_used": copy.deepcopy(state["p2_used"])
                    }
                    p2_info = {
                        "turn": turn, "card1": card1, "card2": card2,
                        "own_hand": copy.deepcopy(state["p2_hand"]), "own_total": state["p2_score"],
                        "enemy_total": state["p1_score"], "enemy_used": copy.deepcopy(state["p1_used"])
                    }
                    
                    chosen_p1 = ai1_module.think_action(p1_info)
                    p1_play = chosen_p1 if chosen_p1 in state["p1_hand"] else random.choice(state["p1_hand"])
                    
                    chosen_p2 = ai2_module.think_action(p2_info)
                    p2_play = chosen_p2 if chosen_p2 in state["p2_hand"] else random.choice(state["p2_hand"])
                    
                    current_score = card1 * card2
                    if p1_play > p2_play:
                        state["p1_score"] += current_score
                    elif p2_play > p1_play:
                        state["p2_score"] += current_score
                    
                    state["p1_hand"].remove(p1_play)
                    state["p2_hand"].remove(p2_play)
                    state["p1_used"].append(p1_play)
                    state["p2_used"].append(p2_play)
                    
                    turn_resolved = True
                else:
                    if turn < 7:
                        turn += 1
                        card1 = state["score_deck"].pop()
                        card2 = state["score_deck"].pop()
                        p1_play, p2_play = None, None
                        turn_resolved = False
                    else:
                        if state["p1_score"] > state["p2_score"]:
                            p1_wins += 1
                        elif state["p2_score"] > state["p1_score"]:
                            p2_wins += 1
                        else:
                            draws += 1
                        game_over = True
                        
                        if game_count >= MAX_GAMES:
                            all_games_over = True
            else:
                game_count += 1
                state = get_initial_state()
                turn = 1
                card1 = state["score_deck"].pop()
                card2 = state["score_deck"].pop()
                p1_play, p2_play = None, None
                turn_resolved = False
                game_over = False

        # --- 画面描画（横幅900ベースに調整） ---
        # 1. 統計情報（行を分けてすっきり配置）
        
        # 【1行目：ゲームの進行状況】（左右にバランスよく配置）
        draw_text(f"試合数: {game_count} / {MAX_GAMES}", font, TEXT_COLOR, 200, 15)
        draw_text(f"ターン: {turn} / 7", large_font, TEXT_COLOR, 600, 10)
        
        # 【2行目：プレイヤー同士の勝敗数・戦績】（中央付近にゆったり配置）
        p1_stats_text = f"{name1}: {p1_wins}勝"
        p2_stats_text = f"{name2}: {p2_wins}勝"
        draws_text = f"（引き分け: {draws}）"
        
        draw_text(p1_stats_text, font, P1_COLOR, 200, 50)
        draw_text(p2_stats_text, font, P2_COLOR, 400, 50)
        draw_text(draws_text, font, TEXT_COLOR, 580, 50)
        
        # 2. めくられたスコアカード
        score_color = CARD_SCORE_POS if (card1 * card2) >= 0 else CARD_SCORE_NEG
        draw_card(f"{card1}", 380, 90, 65, 90, score_color)
        draw_card(f"{card2}", 465, 90, 65, 90, score_color)
        draw_text(f"このターンの得点: {card1 * card2}", font, TEXT_COLOR, 360, 195)

        # 3. プレイヤー1手札（左端）
        draw_text(f"{name1}手札", font, P1_COLOR, 15, 70)
        for num in range(1, 14):
            y_pos = 105 + (num-1) * 36
            if num in state["p1_hand"]:
                draw_card(f"{num}", 20, y_pos, 45, 30, P1_COLOR)
            else:
                pygame.draw.rect(screen, (40, 50, 60), (20, y_pos, 45, 30), 1, border_radius=5)

        # 4. プレイヤー2手札（右端の文字切れを完全に防止する右寄せ処理）
        p2_title_text = f"{name2}手札"
        p2_title_surface = font.render(p2_title_text, True, P2_COLOR)
        # 右端の基準（X=870）に合わせて、文字の幅（width）の分だけ左に引いた位置を描画開始点にする
        p2_title_x = 870 - p2_title_surface.get_width()
        screen.blit(p2_title_surface, (p2_title_x, 70))

        for num in range(1, 14):
            y_pos = 105 + (num-1) * 36
            if num in state["p2_hand"]:
                draw_card(f"{num}", 825, y_pos, 45, 30, P2_COLOR)
            else:
                pygame.draw.rect(screen, (40, 50, 60), (825, y_pos, 45, 30), 1, border_radius=5)

        # 5. 出したカードと勝敗の開示
        # プレイヤー1のスコア（左側：位置固定）
        draw_text(f"{name1} スコア: {state['p1_score']}", font, P1_COLOR, 200, 260)
        
        # プレイヤー2のスコア（右側：文字切れ・被り防止の右寄せ処理）
        p2_score_text = f"{name2} スコア: {state['p2_score']}"
        p2_score_surface = font.render(p2_score_text, True, P2_COLOR)
        # 中央の対戦エリア（X=700付近）の右端に合わせて右寄せにする
        p2_score_x = 700 - p2_score_surface.get_width()
        screen.blit(p2_score_surface, (p2_score_x, 260))

        if turn_resolved:
            draw_card(f"{p1_play}", 375, 320, 70, 95, P1_COLOR)
            draw_card(f"{p2_play}", 465, 320, 70, 95, P2_COLOR)
            
            if p1_play > p2_play:
                txt_str, txt_col = f"{name1} の勝ち！", P1_COLOR
            elif p2_play > p1_play:
                txt_str, txt_col = f"{name2} の勝ち！", P2_COLOR
            else:
                txt_str, txt_col = "引き分け", TEXT_COLOR
                
            txt_surface = font.render(txt_str, True, txt_col)
            txt_rect = txt_surface.get_rect(center=(450, 450))
            screen.blit(txt_surface, txt_rect)
        
        # 6. 【最終結果表示】
        if all_games_over:
            pygame.draw.rect(screen, (10, 15, 20), (200, 150, 500, 300), border_radius=10)
            pygame.draw.rect(screen, TEXT_COLOR, (200, 150, 500, 300), 2, border_radius=10)
            
            if p1_wins > p2_wins:
                res_title = f"総合勝者：{name1} の勝利！"
                res_color = P1_COLOR
            elif p2_wins > p1_wins:
                res_title = f"総合勝者：{name2} の勝利！"
                res_color = P2_COLOR
            else:
                res_title = "総合結果：引き分け！"
                res_color = TEXT_COLOR

            lines = [
                ("【最終結果発表】", large_font, TEXT_COLOR, 180),
                (f"最終戦績: {name1} {p1_wins}勝  vs  {name2} {p2_wins}勝", font, TEXT_COLOR, 250),
                (res_title, font, res_color, 320),
                ("×ボタンで終了してください", font, (150, 150, 150), 390)
            ]

            for text_str, font_obj, color, y_pos in lines:
                txt_surface = font_obj.render(text_str, True, color)
                txt_rect = txt_surface.get_rect(center=(450, y_pos + txt_surface.get_height()/2))
                screen.blit(txt_surface, txt_rect)
            
        # 7. 1試合ごとの終了メッセージ（文字溢れ防止のために枠を大きくしました）
        elif game_over:
            # 黒い四角の横幅を 500 -> 650 に拡大、開始位置を 200 -> 125 に変更（画面中央 X=450 基準）
            pygame.draw.rect(screen, (0, 0, 0, 200), (125, 200, 650, 200), border_radius=10)
            pygame.draw.rect(screen, TEXT_COLOR, (125, 200, 650, 200), 2, border_radius=10) # おしゃれな白い枠線も追加
            
            if state["p1_score"] > state["p2_score"]:
                res_txt = f"【第{game_count}試合終了】 {name1} の勝利！"
                res_col = P1_COLOR
            elif state["p2_score"] > state["p1_score"]:
                res_txt = f"【第{game_count}試合終了】 {name2} の勝利！"
                res_col = P2_COLOR
            else:
                res_txt = f"【第{game_count}試合終了】 引き分け！"
                res_col = TEXT_COLOR
            
            match_lines = [
                (res_txt, large_font, res_col, 240),
                ("クリックかスペースキーで次の試合へ", font, TEXT_COLOR, 310)
            ]
            
            # 横幅が広がっても、常に自動でポップアップ内の「完全中央（X=450）」に文字を配置
            for text_str, font_obj, color, y_pos in match_lines:
                txt_surface = font_obj.render(text_str, True, color)
                txt_rect = txt_surface.get_rect(center=(450, y_pos + txt_surface.get_height()/2))
                screen.blit(txt_surface, txt_rect)
                
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()