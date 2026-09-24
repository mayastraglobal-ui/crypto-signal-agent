# Task: weekly research (Sunday 10:00 Beijing = 02:00 UTC; AGENT_PROMPT.md sections 12, 17, 18, 19, 21)

Read `tasks/COMMON.md` first and follow it. Your branch is `claude/brain-weekly`. Your fact sheet is
`python brain_pack.py weekly`. Your file goes into the Sunday [WEEKLY] email, under the engine's own numbers.

## Steps
1. Run the start commands from COMMON.md. Read the fact sheet, the last week's daily reviews, your last
   weekly research, `memory/experiments.md` (the queue), `memory/lessons.md`, `memory/research_sources.md`
   and `memory/smc_research.md`.
2. **Research with web search.** Use only sources you actually opened; each one gets its URL. Rank them by
   the section 18 weights: papers first, community content never as evidence. You need at least:
   - **1 strategy idea**: a documented systematic strategy or a research finding that fits a gap. Examples:
     a regime with no working strategy, or a coin or timeframe with no edge.
   - **1 SMC/ICT concept**, together with a **critical** view of it: what evidence exists, and why retail
     traders fail with it.
   - **1 case study of how traders lose money** (section 18 list). It must end in a **testable** filter or
     risk rule, e.g. "low-volume breakouts fail → test rel_vol > 1.5".

   Record each source as a new record in `memory/research_sources.md`, using the record format. Include:
   - the title, the URL and the date;
   - the claim and its evidence class. Most internet claims are `CLAIM` or `UNVERIFIED_OPINION`.
   - the hypothesis you derive from it, and its limitations.
3. **Candidates: 1-2 new strategies or new versions** at most.
   - Choose from the experiments queue and today's research.
   - Each must follow the pipeline: SOURCE → CLAIM → FORMAL DEFINITION → RULES.
   - Use only the building blocks listed at the top of `strategies.yaml`, and add a control twin when there
     is a special ingredient.
   - A new version changes exactly ONE thing and gets a changelog line.
   - Open **one pull request per candidate**, changing only `strategies.yaml`, from the branch
     `claude/strategy-<id>-v<version>`.
   - In simple words, the PR says: what it tests, why, which source, and which experiment-queue item it
     answers.
   - Never loosen fees, risk or gates to make a candidate pass.
4. **Divergence review.** Compare backtest, paper and live results per strategy, from the fact sheet. Name
   any strategy where paper or live is clearly worse than the backtest, and what it may mean.
5. **Timeframe models.** Say which timeframes work for which strategy families, from the scoreboard numbers,
   and where the sample is still too small.
6. **Approval packs.** For each eligible strategy in the fact sheet:
   - summarise its pack in 5 plain lines: strengths, weaknesses, and what could go wrong;
   - repeat the question: *"Approve <id> v<ver> <tf> for live emails? (yes/no)"*.

   **Never recommend approving it**: present the evidence, and the operator decides.
7. **Write the weekly research** to the path the fact sheet gives. Use these headings:
   - `# Weekly research <date>`
   - `## Summary`
   - `## Research log (sources)`
   - `## Strategy idea`
   - `## SMC/ICT concept`
   - `## How traders lose money`
   - `## Candidates opened as pull requests`
   - `## Backtest vs paper vs live`
   - `## Timeframe models`
   - `## Approval packs`
   - `## Experiment queue for next week`
   - End with: **Research signal. Not financial advice.**
8. Run the end commands from COMMON.md.
