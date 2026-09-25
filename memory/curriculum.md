# Curriculum - the agent's rotating reading plan

The daily review studies ONE item per day (the fact sheet names today's item: the first one not studied yet, then the
one studied longest ago). For that item it:
1. finds and opens the real source (papers: the journal or an open preprint such as SSRN / arXiv; books: public
   summaries, reviews or the author's own papers - never copied text; post-mortems: official reports or reputable
   reporting);
2. writes ONE record in `memory/research_sources.md` with a title starting `[Cxx]`, the URL it opened, the claim, the
   evidence class and what it means for this system;
3. writes AT MOST ONE testable hypothesis into `memory/experiments.md` (evidence `HYPOTHESIS`), if the item suggests one.

**References below are written from the build session's memory and have NOT been opened.** Check the title, authors,
year and venue on the real source before recording anything. If the source cannot be found or opened, record that
("not opened") and do not cite it. Operator: add, remove or reorder items freely (keep the `## Cxx · kind · title` lines).
Kinds: paper · book · exchange_research · post_mortem · interview.

## C01 · paper · Time series momentum
- read: Moskowitz, Ooi, Pedersen - "Time Series Momentum", Journal of Financial Economics (2012).
- look for: does a market's own past 12-month return predict its next month, across asset classes? How big, how costly?
- for us: the trend-following family (donchian_breakout, supertrend_flip) - which lookbacks and holding periods?

## C02 · paper · Risks and returns of cryptocurrency
- read: Liu, Tsyvinski - "Risks and Returns of Cryptocurrency", Review of Financial Studies (2021).
- look for: time-series momentum and investor attention as predictors of crypto returns; which horizons.
- for us: which of our timeframes match the horizons where they found predictability?

## C03 · paper · Common risk factors in cryptocurrency
- read: Liu, Tsyvinski, Wu - "Common Risk Factors in Cryptocurrency", Journal of Finance (2022).
- look for: market, size and momentum factors in the cross-section of coins.
- for us: cross-coin ideas (idea factory f) - do stronger coins keep outperforming?

## C04 · paper · The deflated Sharpe ratio
- read: Bailey, Lopez de Prado - "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and
  Non-Normality", Journal of Portfolio Management (2014).
- look for: how the number of trials should raise the bar for a backtest.
- for us: compare with our Bonferroni trials bar (memory/trials.csv) - too strict, too loose?

## C05 · paper · Multiple testing in factor research
- read: Harvey, Liu, Zhu - "... and the Cross-Section of Expected Returns", Review of Financial Studies (2016).
- look for: why a t-statistic of 2 is not enough after hundreds of tested factors.
- for us: the same problem for strategy ideas and the lab.

## C06 · paper · Arbitrage and price differences between crypto exchanges
- read: Makarov, Schoar - "Trading and Arbitrage in Cryptocurrency Markets", Journal of Financial Economics (2020).
- look for: how prices differ across exchanges and countries, and why they persist.
- for us: our data comes from one exchange at a time (Binance, OKX fallback) - what can differ?

## C07 · paper · Market liquidity and funding liquidity
- read: Brunnermeier, Pedersen - "Market Liquidity and Funding Liquidity", Review of Financial Studies (2009).
- look for: how margin calls and funding stress create spirals of selling.
- for us: liquidation cascades and funding (memory/market_mechanics.md); the funding / open-interest building blocks.

## C08 · paper · A century of trend following
- read: Hurst, Ooi, Pedersen - "A Century of Evidence on Trend-Following Investing", Journal of Portfolio Management (2017).
- look for: in which market conditions trend following made and lost money.
- for us: the playbook - do our trend families fail in the same regimes?

## C09 · paper · Foundations of technical analysis
- read: Lo, Mamaysky, Wang - "Foundations of Technical Analysis", Journal of Finance (2000).
- look for: a statistical test of chart patterns; which patterns carried information.
- for us: candle / SMC pattern evidence vs random entries (reports/feature_evidence.json).

## C10 · paper · Simple technical trading rules
- read: Brock, Lakonishok, LeBaron - "Simple Technical Trading Rules and the Stochastic Properties of Stock Returns",
  Journal of Finance (1992).
- look for: moving-average and range-breakout rules; later studies on whether the effect survived costs.
- for us: ema_9_21_cross and donchian_breakout - did the edge disappear after publication and costs?

## C11 · book · Market Wizards (principles)
- read: Schwager - "Market Wizards" (1989): public summaries and reviews only, never copied text.
- look for: principles most of the interviewed traders share (risk control, cutting losses, position size).
- for us: which principle does this system already enforce, and which one is missing?

## C12 · book · Trading and Exchanges (who is on the other side)
- read: Harris - "Trading and Exchanges: Market Microstructure for Practitioners" (2003): summaries, lecture notes.
- look for: the types of traders (informed, liquidity, noise) and who profits from whom.
- for us: the edge blocks' "who_pays" lines - are they realistic?

## C13 · book · Evidence-Based Technical Analysis
- read: Aronson - "Evidence-Based Technical Analysis" (2006): summaries, reviews, the author's articles.
- look for: data-mining bias and how to test many rules honestly.
- for us: the variant search (idea factory e) and the trials counter.

## C14 · book · Fooled by Randomness
- read: Taleb - "Fooled by Randomness" (2001): summaries and reviews.
- look for: luck mistaken for skill; survivorship; rare large losses.
- for us: rsi2_dip_buy's "many small wins, rare large losses" - is the drawdown test enough?

## C15 · exchange_research · Options expiries and max pain
- read: exchange or data-provider research on BTC / ETH options expiries (e.g. Deribit's own articles).
- look for: does price behave differently around large expiries? What evidence, how measured?
- for us: the Deribit expiry data in reports/feeds.json - worth a testable filter?

## C16 · exchange_research · Funding rates and crowded positioning
- read: exchange research (e.g. Binance Research) or data providers on perpetual funding and open interest.
- look for: what extreme funding or rising open interest has been followed by.
- for us: the funding_z / oi_chg building blocks (Part C) - a hypothesis to test.

## C17 · exchange_research · Liquidity and order books
- read: a crypto market-data provider's research on order-book depth and slippage (e.g. Kaiko).
- look for: how depth changes by hour, weekday and around news.
- for us: our slippage assumption (config.yaml costs) - realistic for the signal coins?

## C18 · post_mortem · LTCM (1998)
- read: public accounts of Long-Term Capital Management's collapse (reports, reputable reporting, book summaries).
- look for: leverage, correlated positions, liquidity drying up.
- for us: correlated positions (the risk engine's correlation groups) - is the limit tight enough?

## C19 · post_mortem · 12 March 2020 crypto crash
- read: reputable reporting / exchange post-mortems on the March 2020 crash and the liquidation cascade.
- look for: how liquidations, exchange outages and funding interacted.
- for us: data-quality halts and the volatility_spike loss tag - would they have protected us?

## C20 · post_mortem · Terra / LUNA (May 2022)
- read: reputable reporting and published analyses of the UST de-peg.
- look for: how a "stable" asset lost its peg and what warning signs existed.
- for us: stablecoin risk to the USDT pairs we trade - anything to monitor?

## C21 · post_mortem · FTX (November 2022)
- read: official filings / reputable reporting on the FTX collapse.
- look for: exchange counterparty risk; how quickly withdrawals stopped.
- for us: exchange incidents in events.yaml and the data-source fallback.

## C22 · post_mortem · Three Arrows Capital (2022)
- read: reputable reporting / court documents on 3AC's failure.
- look for: leverage, illiquid positions, correlated bets.
- for us: never scale risk after wins - check the risk engine's limits.

## C23 · interview · A systematic trader on process
- read / listen: one long interview with a professional systematic or crypto trader (a well-known podcast or
  published interview). Note who, where, when.
- look for: how they decide an edge is dead; how they size positions.
- for us: compare with our kill rules and the paper retirement limits.

## C24 · interview · A discretionary trader on risk
- read / listen: one interview with a professional discretionary trader. Note who, where, when.
- look for: how they handle losing streaks and news events.
- for us: the risk engine's daily / weekly loss limits - explain them in plain words to the operator.
