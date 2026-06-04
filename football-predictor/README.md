# ⚽ Football Predictor — 10-Agent 足球预测分析团队

一套在 **Claude Code** 中运行的多 agent 足球比赛分析系统。10 个角色各司其职，最终向比分预测收敛，输出供你做决策参考。

---

## 🧩 团队成员（10 个 subagent）

| # | 代号 | agent name | 职责 | 模型 |
|---|------|-----------|------|------|
| 1 | 阿数 | `data-collector` | 抓基础数据：战绩、进失球、主客场、历史交锋 | haiku |
| 2 | 小盘 | `odds-analyst` | 盘口赔率分析，识别庄家倾向（**核心信号源**） | sonnet |
| 3 | 老情 | `intel-scout` | 临场情报：伤停、停赛、轮换、发布会信号 | sonnet |
| 4 | 战哥 | `tactics-analyst` | 战术对位、阵型克制、比赛节奏预判 | sonnet |
| 5 | 比分 | `score-modeler` | xG/泊松模型跑比分概率（**核心产出**） | sonnet |
| 6 | 状态 | `form-evaluator` | 球队/球员状态、心理惯性、体能 | haiku |
| 7 | 主场 | `context-checker` | 天气、场地、裁判、主场氛围 | haiku |
| 8 | 大势 | `motivation-analyst` | 联赛处境、比赛动机强弱 | haiku |
| 9 | 审表 | `backtest-auditor` | 复盘命中率、淘汰差判断（带持久记忆） | sonnet |
| 10 | 总管 | `coordinator` | 调度全员、汇总、最终研判 | opus |

> 模型分配逻辑：纯采集/边缘因素用便宜快的 haiku，需要推理的分析用 sonnet，统筹决策用 opus。可按需在各 agent 文件里调整。

---

## 📁 项目结构

```
football-predictor/
├── .claude/
│   └── agents/              # 10 个 subagent 定义（已 check 进版本控制供团队共享）
│       ├── 01-data-collector.md
│       ├── ...
│       └── 10-coordinator.md
├── src/
│   ├── fetch_data.py        # 基础数据抓取（骨架，需接入 API）
│   ├── fetch_odds.py        # 盘口抓取（需自行补充）
│   └── score_model.py       # 泊松比分模型（可直接跑）
├── data/                    # 抓取的数据 & 预测记录
└── README.md
```

---

## 🚀 使用方法

### 1. 准备工作
```bash
# 安装依赖
pip install requests

# 设置数据源 API key（推荐 football-data.org 或 API-Football）
export FOOTBALL_API_KEY="你的key"
```

### 2. 在 Claude Code 里启动
```bash
cd football-predictor
claude
```

### 3. 让总管跑一场完整分析
直接用自然语言指挥「总管」，它会自动按顺序调度其他 9 位：
```
用 coordinator 分析周六 阿森纳 vs 切尔西 这场，给我完整研判
```

### 4. 也可以单独点名某位专家
```
@odds-analyst 看一下这场的亚盘水位变化说明什么
用 score-modeler 跑一下这场的比分概率
```

### 5. 赛后复盘（让团队越用越准）
```
用 backtest-auditor 复盘本周所有预测的命中率
```

---

## 🔌 接入真实数据源

`src/fetch_data.py` 和 `fetch_odds.py` 目前是骨架，把 `TODO` 处替换成真实 API 即可：

- **football-data.org** — 免费档覆盖五大联赛，每分钟 10 次
- **API-Football (api-sports.io)** — 免费档每天 100 次，数据全面
- **盘口数据** — 多数赔率 API 需付费，可考虑 The Odds API 等

> 比分模型 `score_model.py` 无需 API，输入攻防参数即可直接运行。

---

## ⚠️ 重要提醒（请务必阅读）

这套系统能帮你把分析做得更系统、更量化，但有几条底线必须清楚：

1. **博彩本质是负期望活动**。庄家通过抽水（vig）长期占据数学优势，再完善的分析团队也只能**缩小劣势，无法保证盈利**。
2. **单场预测不确定性极高**。足球是低分、高随机性运动——即使模型给出的最高概率比分，发生率通常也只有 10-15%。没有任何「必中」。
3. **短期命中 ≠ 方法有效**。几次猜对可能只是方差。务必用足够大的样本（审表的工作）来评估，不要因连胜就加大投入。
4. **请理性对待**：设定预算上限、把竞猜当娱乐、用闲钱、绝不追损或借钱投注。
5. 如果你发现自己出现追损、隐瞒、影响生活或情绪的情况，这可能是赌博成瘾的信号，建议寻求专业帮助（如各地的戒赌热线）。

系统里的每个 agent，尤其是「总管」和「审表」，都被设计为在给出预测的同时守护你的理性判断——这是有意为之，不是多余的唠叨。
