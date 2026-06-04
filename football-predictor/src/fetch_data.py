#!/usr/bin/env python3
"""
fetch_data.py — 基础比赛数据抓取（供「阿数」agent 调用）

用法:
    python src/fetch_data.py --home "Arsenal" --away "Chelsea" --match-id "20260604_ARS_CHE"

说明:
    这是一个骨架。把 TODO 处替换成你选定的数据源 API 调用即可。
    推荐免费/低成本数据源:
      - football-data.org (免费档每分钟 10 次，覆盖主流联赛)
      - API-Football (api-sports.io，免费档每天 100 次)
      - TheSportsDB (免费，数据较基础)
"""
import argparse
import json
import os
from pathlib import Path

# 从环境变量读取 API key，不要硬编码在代码里
API_KEY = os.environ.get("FOOTBALL_API_KEY", "")
DATA_DIR = Path(__file__).parent.parent / "data"


def fetch_team_recent(team_name: str, n: int = 8) -> dict:
    """抓取某队近 n 场战绩。TODO: 替换为真实 API。"""
    # ── 示例：football-data.org 的调用方式 ──
    # import requests
    # headers = {"X-Auth-Token": API_KEY}
    # r = requests.get(f"https://api.football-data.org/v4/teams/{team_id}/matches",
    #                  headers=headers, params={"limit": n, "status": "FINISHED"})
    # return r.json()
    return {
        "team": team_name,
        "matches": [],          # 每场: {date, opponent, home_away, gf, ga, result}
        "note": "TODO: 接入真实 API",
    }


def fetch_h2h(home: str, away: str, n: int = 5) -> dict:
    """抓取两队历史交锋。TODO: 替换为真实 API。"""
    return {"home": home, "away": away, "h2h": [], "note": "TODO: 接入真实 API"}


def summarize(home_data: dict, away_data: dict, h2h: dict) -> dict:
    """整理成结构化摘要。缺失数据明确标注，绝不编造。"""
    def agg(matches):
        if not matches:
            return {"played": 0, "note": "数据缺失"}
        gf = sum(m.get("gf", 0) for m in matches)
        ga = sum(m.get("ga", 0) for m in matches)
        return {
            "played": len(matches),
            "avg_scored": round(gf / len(matches), 2),
            "avg_conceded": round(ga / len(matches), 2),
        }
    return {
        "home_summary": agg(home_data.get("matches", [])),
        "away_summary": agg(away_data.get("matches", [])),
        "h2h": h2h.get("h2h", []),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--home", required=True)
    p.add_argument("--away", required=True)
    p.add_argument("--match-id", required=True)
    args = p.parse_args()

    if not API_KEY:
        print("⚠️  未设置 FOOTBALL_API_KEY 环境变量，当前为骨架模式。")

    home_data = fetch_team_recent(args.home)
    away_data = fetch_team_recent(args.away)
    h2h = fetch_h2h(args.home, args.away)
    summary = summarize(home_data, away_data, h2h)

    DATA_DIR.mkdir(exist_ok=True)
    out = DATA_DIR / f"{args.match_id}_raw.json"
    payload = {
        "match_id": args.match_id,
        "home": args.home,
        "away": args.away,
        "raw": {"home": home_data, "away": away_data, "h2h": h2h},
        "summary": summary,
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    print(f"✅ 已写入 {out}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
