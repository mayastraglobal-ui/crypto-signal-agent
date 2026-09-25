# Beginner course - one short lesson a day (for the operator)

Not the agent's reading plan (that is memory/curriculum.md). The [DAILY] email carries the next lesson (reports/curriculum_sent.json remembers which ones you had; after the last
one it starts again). Each lesson is tied to something you can see in THIS system. Written for a beginner; nothing
here is financial advice. The operator may edit, reorder or add lessons (keep the `## Lxx · title` headings).

## L01 · What "R" means
R is the amount you risk on one trade: the distance from your entry to your stop-loss.
A trade that wins +2R made twice what it risked; -1R means the stop was hit.
Measuring everything in R lets us compare coins and strategies of any price.
Try it: in reports/latest.md, section 3, the "Avg R" column is the average result per trade, in R.

## L02 · The stop-loss comes first
The stop-loss is the price where the idea is wrong and the trade closes with a small loss.
Every signal here has its stop decided BEFORE entry; it never moves further away.
Without a stop, one bad trade can wipe out many good ones.
Try it: an [ENTRY] email shows entry, stop and targets - the stop is always there.

## L03 · Targets and taking profit in parts
A target (take-profit, TP) is where part of the trade is closed in profit.
Closing in parts (e.g. 40% / 30% / 30% at 1R / 2R / 3R) locks in some profit and lets the rest run.
New lab strategies must have their first target at least 2R away.
Try it: config.yaml -> trade_plan shows the default split.

## L04 · Fees eat small edges
Every trade pays fees and slippage (the price moving while your order fills).
Cost in R = cost / stop distance: the tighter the stop, the bigger the bite.
The engine refuses strategies whose costs are over 1/4 of the stop, and tests them again with costs +50%.
Try it: the "Cost" column in report section 3.

## L05 · Backtest, paper, live - never add them up
Backtest = the rules run on past data. Paper = live signals that are only logged. Live = APPROVED signals you get emailed.
Each stage is a harder test; results are always shown apart.
A great backtest with bad paper results usually means the backtest was lucky or unrealistic.
Try it: the [WEEKLY] email section 1 keeps LIVE / PAPER / VALIDATION apart.

## L06 · Luck looks like skill when you test many ideas
Test 100 random strategies and a few will look great by chance.
That is why the trials counter raises the bar as more ideas are tested (now about 3 "standard errors").
A strategy must beat that bar, not just be positive.
Try it: report section 3b, "Trials counter".

## L07 · Market regime
A regime is the market's current "weather": strong up-trend, range, high volatility, and so on.
Most strategies only work in some regimes; the engine lets each one trade only in the regimes it lists.
Try it: memory/playbook.md shows, per regime, what made and lost money in the backtests.

## L08 · The control twin
A fancy ingredient (like an SMC pattern or a 5-minute check) must prove it adds something.
So each such strategy is compared with a "twin": the same idea WITHOUT the ingredient.
If the twin does as well, the ingredient is only decoration.
Try it: report section 3b, "SMC vs control twin".

## L09 · The edge block: why should this make money?
Every idea must say who is on the other side of the trade and why they lose, what market behaviour drives it,
when it should fail, and what result would kill it.
An idea without a clear edge is a pattern, not a strategy.
Try it: strategies.yaml -> any card's `edge:` block; approval packs show it at the top.

## L10 · Risk per trade and position size
Risk per trade = how much of the account you lose if the stop is hit (0.5% for the first 30 days, then at most 1%).
Position size = risk in dollars / stop distance. A wide stop means a smaller position, not a bigger risk.
Try it: an [ENTRY] email shows the position size and the dollars at risk.

## L11 · "No trade" is a result
Most hours there is no good setup. Forcing trades is how accounts lose money.
When no strategy has shown an edge in the current regime, standing aside IS the plan.
Try it: memory/playbook.md - regimes where "NOTHING made money".

## L12 · News and event risk
Big scheduled releases (CPI, jobs report, FOMC) can move crypto sharply in minutes.
The engine blocks live entries from 60 minutes before to 60 minutes after each one.
Try it: events.yaml lists them in UTC; the briefing names the next ones.

## L13 · How to read an approval pack - and say no
Before any strategy sends live emails, you get an approval pack: its edge, backtest, walk-forward, paper results,
twin comparison and weaknesses. Saying nothing = no.
Look for: enough paper signals, paper close to the backtest, and weaknesses you understand.
Try it: reports/approval/ (empty until a strategy qualifies - that is normal).

## L14 · Headlines are claims, not evidence
A news headline tells you what someone says happened, not what the price will do.
The briefings quote headlines with their source and never use them as a reason to trade.
Try it: the "Outside feeds" part of a briefing, and memory/market_mechanics.md for how markets really move.
