#!/usr/bin/env python3
"""
score_model.py — 比分预测模型（供「比分」agent 调用）

基于泊松分布的经典足球比分模型。这是博彩业和学术界广泛使用的基线方法。

用法:
    python src/score_model.py --home-attack 1.6 --away-attack 1.1 \
        --home-defense 1.0 --away-defense 1.2 --home-advantage 1.3

核心思路:
    1. 估算两队的「预期进球数」(expected goals, λ)
    2. 假设各队进球服从泊松分布
    3. 计算所有可能比分(0:0 到 6:6)的联合概率
    4. 汇总出胜平负、大小球、最可能比分

注意: 模型输出是概率，不是预言。即使最高概率比分，发生率通常也只有 10-15%。
"""
import argparse
import json
from math import exp, factorial


def poisson_pmf(k: int, lam: float) -> float:
    """泊松分布概率质量函数: P(X=k)"""
    return (lam ** k) * exp(-lam) / factorial(k)


def build_score_matrix(home_lambda: float, away_lambda: float, max_goals: int = 6):
    """计算 0:0 到 max:max 所有比分的联合概率。"""
    matrix = {}
    for h in range(max_goals + 1):
        for a in range(max_goals + 1):
            p = poisson_pmf(h, home_lambda) * poisson_pmf(a, away_lambda)
            matrix[(h, a)] = p
    return matrix


def analyze(matrix: dict):
    """从比分矩阵汇总出各类预测。"""
    home_win = sum(p for (h, a), p in matrix.items() if h > a)
    draw = sum(p for (h, a), p in matrix.items() if h == a)
    away_win = sum(p for (h, a), p in matrix.items() if h < a)

    over_25 = sum(p for (h, a), p in matrix.items() if h + a > 2.5)
    under_25 = 1 - over_25

    btts = sum(p for (h, a), p in matrix.items() if h > 0 and a > 0)  # 双方进球

    top_scores = sorted(matrix.items(), key=lambda x: x[1], reverse=True)[:5]

    return {
        "outcome": {
            "home_win": round(home_win, 3),
            "draw": round(draw, 3),
            "away_win": round(away_win, 3),
        },
        "goals": {
            "over_2.5": round(over_25, 3),
            "under_2.5": round(under_25, 3),
            "both_teams_score": round(btts, 3),
        },
        "top_scorelines": [
            {"score": f"{h}:{a}", "prob": round(p, 3)} for (h, a), p in top_scores
        ],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--home-attack", type=float, required=True,
                   help="主队场均进球（攻击力）")
    p.add_argument("--away-attack", type=float, required=True,
                   help="客队场均进球（攻击力）")
    p.add_argument("--home-defense", type=float, default=1.0,
                   help="主队失球系数，>1 表示防守偏弱")
    p.add_argument("--away-defense", type=float, default=1.0,
                   help="客队失球系数，>1 表示防守偏弱")
    p.add_argument("--home-advantage", type=float, default=1.3,
                   help="主场优势系数，通常 1.2-1.4")
    args = p.parse_args()

    # 预期进球 = 自身攻击力 × 对手防守弱点 ×（主队额外乘主场优势）
    home_lambda = args.home_attack * args.away_defense * args.home_advantage
    away_lambda = args.away_attack * args.home_defense

    matrix = build_score_matrix(home_lambda, away_lambda)
    result = analyze(matrix)
    result["expected_goals"] = {
        "home": round(home_lambda, 2),
        "away": round(away_lambda, 2),
    }
    result["disclaimer"] = (
        "概率预测，非预言。足球随机性极高，单场偶然性大。"
        "博彩长期为负期望，请理性对待、设定预算上限。"
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
