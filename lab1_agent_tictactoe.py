"""
پروژه آزمایشگاه هوش مصنوعی - جلسه اول و دوم
بهبود و انطباق معماری سه عاملی کلاس روی محیط بازی دوز (Tic-Tac-Toe)
مقایسه عامل تصادفی (Random) در برابر عامل واکنشی (Rule-based Reflex)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# تعریف وضعیت برد در دوز ۳x۳
WIN_COMBINATIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # سطرها
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # ستون‌ها
    [0, 4, 8], [2, 4, 6]              # قطرها
]

def check_winner(board):
    for combo in WIN_COMBINATIONS:
        if board[combo[0]] != 0 and board[combo[0]] == board[combo[1]] == board[combo[2]]:
            return board[combo[0]]  # 1 برای X، -1 برای O
    if 0 not in board:
        return 0  # تساوی
    return None  # بازی ادامه دارد

def get_available_moves(board):
    return [i for i, v in enumerate(board) if v == 0]

def reflex_agent_move(board, player, rng):
    """عامل واکنشی: اگر برد آنی یا دفع باخت در یک حرکت ممکن باشد، آن را انجام می‌دهد؛ وگرنه تصادفی بازی می‌کند"""
    available = get_available_moves(board)
    opponent = -player

    # ۱. بررسی حرکت برد آنی
    for move in available:
        temp_board = board.copy()
        temp_board[move] = player
        if check_winner(temp_board) == player:
            return move

    # ۲. بررسی سد کردن حرکت برد حریف
    for move in available:
        temp_board = board.copy()
        temp_board[move] = opponent
        if check_winner(temp_board) == opponent:
            return move

    # ۳. انتخاب تصادفی در صورت نبود خطر/فرصت آنی
    return rng.choice(available)

def play_one_game(agent_x_type, agent_o_type, seed):
    rng = np.random.default_rng(seed)
    board = np.zeros(9, dtype=int)
    current_player = 1  # 1: X (عامل تحت آزمایش), -1: O (حریف)

    while True:
        available = get_available_moves(board)
        if not available:
            return "Draw"

        # انتخاب حرکت بر اساس نوع عامل
        agent_type = agent_x_type if current_player == 1 else agent_o_type
        if agent_type == "random":
            action = rng.choice(available)
        elif agent_type == "reflex":
            action = reflex_agent_move(board, current_player, rng)

        board[action] = current_player
        result = check_winner(board)
        if result is not None:
            if result == 1:
                return "Agent X Win"
            elif result == -1:
                return "Agent O Win"
            else:
                return "Draw"

        current_player = -current_player

# ارزیابی آماری در ۱۰۰ تکرار (مشابه ساختار کد کلاسی جاروبرقی)
RUNS = 100
experiments = [
    ("Random vs Random", "random", "random"),
    ("Reflex vs Random", "reflex", "random")
]

results = []
for name, p_x, p_o in experiments:
    for s in range(RUNS):
        outcome = play_one_game(p_x, p_o, seed=s)
        results.append({"Experiment": name, "Outcome": outcome})

df = pd.DataFrame(results)
summary = pd.crosstab(df["Experiment"], df["Outcome"], normalize="index") * 100
print("=== نتایج آزمایش شبیه‌سازی ۱۰۰ بازی دوز ===")
print(summary.round(1))

# رسم نمودار مقایسه‌ای نتایج
summary.plot(kind="bar", stacked=True, figsize=(8, 4), color=["#f59e0b", "#10b981", "#ef4444"])
plt.title("Tic-Tac-Toe Agents Benchmark (100 Games)")
plt.ylabel("Percentage (%)")
plt.xlabel("Experiment Setup")
plt.xticks(rotation=0)
plt.legend(title="Outcome", bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.savefig("benchmark_result.png")
print("\nنمودار مقایسه‌ای با نام benchmark_result.png ذخیره شد.")