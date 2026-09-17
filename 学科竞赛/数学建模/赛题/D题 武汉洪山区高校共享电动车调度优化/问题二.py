#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

REGION = ["武汉大学(Z01)", "华中科技大学(Z04)", "武汉理工大学(Z02)",
          "华中师范大学(Z03)", "总站"]
INITIAL = [40, 30, 30, 20, 120]
DIST = [[0, 12.5, 7.5, 3.5, 7.0], [12.5, 0, 10.0, 9.0, 6.5],
        [7.5, 10.0, 0, 4.0, 3.5], [3.5, 9.0, 4.0, 0, 3.0],
        [7.0, 6.5, 3.5, 3.0, 0]]
COST_PER_KM = 1.5
ROUND_COST = [[(DIST[i][j] + DIST[j][i]) * COST_PER_KM for j in range(5)] for i in range(5)]

DEMAND = [
    [[55, 53, 51], [55, 56, 58], [47, 47, 48], [47, 50, 48]],
    [[55, 53, 51], [55, 56, 58], [47, 47, 48], [47, 50, 48]],
    [[70, 69, 71], [68, 64, 70], [52, 51, 54], [64, 63, 65]],
    [[71, 69, 69], [44, 48, 52], [68, 70, 67], [63, 63, 66]],
    [[71, 69, 69], [44, 48, 52], [68, 70, 67], [63, 63, 66]],
    [[70, 69, 71], [68, 64, 70], [52, 51, 54], [64, 63, 65]],
    [[55, 53, 51], [55, 56, 58], [47, 47, 48], [47, 50, 48]],
]

DAYS = [(datetime(2025, 5, 21) + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
SLOTS = ["早(07-09)", "中(12-14)", "晚(17-19)"]

remaining = INITIAL.copy()
schedules, total_cost = [], 0.0

for day in range(7):
    for slot in range(3):
        needed = [DEMAND[day][r][slot] for r in range(4)]
        surplus = [(r, remaining[r]) for r in range(4) if remaining[r] > 0]
        deficit = [(r, max(0, needed[r] - remaining[r])) for r in range(4)]

        # ① 高校间整批互调（≥10 才发车）
        for to_r, need in deficit:
            for from_r, extra in surplus:
                if from_r == to_r or need <= 0 or extra <= 0:
                    continue
                send = min(extra, need)
                if send < 10:          # ← 阈值过滤
                    continue
                cost = ROUND_COST[from_r][to_r]
                schedules.append((DAYS[day], SLOTS[slot], REGION[from_r], REGION[to_r], send, round(cost, 2)))
                total_cost += cost
                remaining[from_r] -= send
                remaining[to_r]   += send
                need              -= send

        # ② 总站兜底（≥10 才发车）
        for to_r, need in [(r, max(0, needed[r] - remaining[r])) for r in range(4)]:
            if need <= 0:
                continue
            send = min(need, remaining[4])
            if send < 10:              # ← 阈值过滤
                continue
            cost = ROUND_COST[4][to_r]
            schedules.append((DAYS[day], SLOTS[slot], REGION[4], REGION[to_r], send, round(cost, 2)))
            total_cost += cost
            remaining[4]   -= send
            remaining[to_r] += send

print("武汉洪山区共享电动车一周≥10辆调度方案\n")
print("-" * 95)
print(f"{'日期':<12}{'时段':<12}{'调出区域':<18}{'调入区域':<18}{'数量':>6}{'成本(元)':>12}")
print("-" * 95)
for d, s, fr, to, q, c in schedules:
    print(f"{d:<12}{s:<12}{fr:<18}{to:<18}{q:>6}{c:>12}")
print("-" * 95)
print(f"一周总调度成本（≥10辆）：{total_cost:.2f} 元")