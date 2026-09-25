# Task: daily review (every day at 23:30 Beijing = 15:30 UTC; AGENT_PROMPT.md sections 17, 19, 22)

Read `tasks/COMMON.md` first and follow it. Your branch is `claude/brain-daily`. Your fact sheet is
`python brain_pack.py daily`. The `## Summary` of your file goes into the next morning's [DAILY] email.
You may add strategy cards to `strategies_lab.yaml` (step 5; COMMON.md rule 4).

## Steps
1. Run the start commands from COMMON.md. Read the fact sheet, then your last daily reviews, then
   `memory/lessons.md`, the newest part of `memory/failure_journal.md` and `memory/experiments.md`
   (section 17.8: always read history before proposing a change).
2. **Wins, losses, invalidations and expiries of the last 24 hours**, with LIVE, PAPER and VALIDATION kept
   apart.
   - For each loss, use the engine's tags and MAE/MFE (MAE = how far the trade went against you, MFE = how
     far it went in your favour).
   - Answer the 8 questions of section 17.3 in short form: was it the strategy, the regime, the timing, the
     stop or target, the sample size, the costs, the timeframe? Is it systematic or random?
   - Do not overrule the engine's tags. You may add a **root cause** as a new record in
     `memory/failure_journal.md` (evidence `MODEL_OUTPUT` or `HYPOTHESIS`, since it is your reading).
3. **Missed strong moves.** For each one in the fact sheet, say:
   - whether it was identifiable **before** it started;
   - whether it was filtered out, blocked, detected too late, or caught by another strategy.

   **Never propose a rule change just because a move was large.** Add a record to `memory/missed_trades.md`
   only when you add something the engine's own entry does not say.
4. **Regime shifts** worth knowing, from the engine's matrix and lifecycle changes.
5. **At most ONE refinement per failing strategy** (sections 17.5-17.6), and only when the fact sheet's
   diagnosis supports it with enough trades (30 or more).
   - Write it as a **hypothesis** with exactly one change: "v1.1: add rel_vol > 1.5 because
     low_relative_volume is systematic in 38% of losses (n = 64)".
   - Queue it as a record in `memory/experiments.md` (evidence `HYPOTHESIS`).
   - If it is strong enough to test now, ALSO append it as a card to `strategies_lab.yaml` (`factory: failure`, or
     `missed_move` for step 3's moves; COMMON.md rule 4:
     a new version changing exactly that one thing, `added` = today). Stay within the limits the fact sheet
     shows; leave room for the weekly research (usually at most 1 card a day from the daily review).
6. **Curriculum (one item a day).** The fact sheet names today's item from `memory/curriculum.md` (a paper, the
   principles of a trading book from public summaries - never copied text, exchange research, a post-mortem of a
   blow-up, or an interview with a professional trader).
   - Find and open the real source. The reference in the plan is from memory: check title, authors, year.
   - Write ONE record in `memory/research_sources.md` titled `[<id>] <title>`, with the URL you opened, the claim,
     its evidence class and what it means for this system. Could not open it? Write that, and cite nothing.
   - At most ONE testable hypothesis from it into `memory/experiments.md` (evidence `HYPOTHESIS`).
7. **Memory reviews due.** For each record the fact sheet lists, add a NEW record to the same file:
   - title `Review: <old title>`;
   - status CONFIRMED, REJECTED or KEEP, with what today's evidence says;
   - a new review date.

   Never edit the old record.
8. **Candidate lessons.** A candidate becomes a lesson in `memory/lessons.md` only if all of these hold:
   - it is systematic in 2 or more tests;
   - the numbers are in the fact sheet;
   - no existing lesson already says it.

   The evidence field then reads `BACKTEST_EVIDENCE: <tests> tests, <trades> trades`, with the cells listed
   in the details. Otherwise, say in the review why it is not a lesson yet.
9. **Write the review** to the path the fact sheet gives. Use these headings:
   - `# Daily review <date>`
   - `## Summary`: 3-8 lines, the most important first.
   - `## Results (LIVE / PAPER / VALIDATION)`
   - `## Losses and why`
   - `## Missed moves`
   - `## Regime`
   - `## Refinements queued` (and the lab cards you added, if any)
   - `## Curriculum` (today's item: what you read, the record, the hypothesis if any)
   - `## Reviews done`
   - `## Lessons`
   - `## Tomorrow`: what to watch, and what NOT to do.
   - End with: **Research signal. Not financial advice.**
10. Run the end commands from COMMON.md.
