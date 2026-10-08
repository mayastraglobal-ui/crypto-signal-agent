# Live watcher on your Windows PC (step-by-step)

Your Windows PC runs the live watcher day and night. Every 5 minutes, about 10–30 seconds after a candle closes, it
checks the market on **OKX perpetuals** and sends a **Telegram** alert when a strategy that passed GitHub's tests
has a setup: entry zone, stop-loss, TP1/TP2/TP3, position size for your account, max hold time and the trend.

- **GitHub stays the brain.** Research, backtests, coin selection, strategy statuses, emails and the official
  record don't change. The PC only reads GitHub's decisions (every hour, automatically) and watches the market fast.
- It never places trades and never needs your OKX password or API keys.
- Until a strategy reaches PAPER_TRADING or APPROVED, the watcher stays quiet. You'll still get a
  "still running" message every day.

You need about **20 minutes** once, and a Telegram account on your phone.

---

## Step 1: download the agent (2 minutes)

1. Open https://github.com/mayastraglobal-ui/crypto-signal-agent
2. Click the green **Code** button → **Download ZIP**.
3. Open your Downloads folder, right-click the ZIP → **Extract All…**, and extract it to an easy place, for
   example `C:\CryptoAgent`.
   You now have a folder like `C:\CryptoAgent\crypto-signal-agent-main` with a `windows` folder inside.

> Keep the folder somewhere simple, without brackets in the path (not inside "Program Files (x86)").

## Step 2: run the setup (10–15 minutes, mostly waiting)

1. Open the `windows` folder and **double-click `1_setup.bat`**.
   If Windows shows "Windows protected your PC", click **More info** → **Run anyway**. It's your own file from
   your GitHub.
2. The setup does 5 things and tells you what it's doing:

| Step | What happens | What you do |
|---|---|---|
| 1. Python | Looks for Python. If it's missing, it installs it with Windows' own installer (winget) | Say **Yes** if Windows asks. If it says "close this window", close it and double-click `1_setup.bat` again |
| 2. Packages | Installs what the agent needs (2–5 minutes) | Wait |
| 3. Telegram | Sets up your bot, see below | Follow the text in the window |
| 4. Sleep | Asks to keep the PC awake when plugged in | Press **Y** (needed for alerts at night) |
| 5. Auto-start | Asks to start the watcher every time you sign in to Windows | Press **Y** |

**Telegram part (step 3 of the setup):**
1. On your phone, open Telegram and search **@BotFather** (blue tick) → press Start → send `/newbot`.
2. Choose a name (for example `My Crypto Alerts`), then a username that ends in `bot` (for example
   `mycryptoalerts123_bot`).
3. BotFather sends a **token** like `123456789:AAH...`. Copy it.
   (Easiest: open Telegram on the PC at https://web.telegram.org, or send the token to yourself.)
4. Paste the token into the setup window and press Enter. *(Right-click pastes in the black window.)*
5. The window shows a link to your bot: open it in Telegram and press **START**.
6. Within a few seconds the setup finds your chat and sends **"✅ Telegram works"** to your phone.

At the end, press **Y** to start the watcher now. A minimized window **"Crypto Watcher"** appears on the taskbar,
and Telegram says **"▶️ Live watcher started"**.

## Step 3: done. What it looks like day to day

- **Keep the "Crypto Watcher" window open** (minimized is fine). Closing it stops the alerts.
- It starts by itself when you sign in to Windows (if you chose Y in step 5).
- It restarts by itself if it ever crashes, and warns you on Telegram if checks keep failing.
- Every hour it downloads GitHub's newest decisions (strategy statuses, coins, settings). Nothing to do.
- Once a day you get **"✅ Live watcher running"**. If that message stops coming, check the PC.

## Using the bot from your phone

Send these to your bot in Telegram (or type `/` and pick one). The bot only answers **your** chat.

| Command | What you get |
|---|---|
| `/status` | Is it running, the last market check, which strategies it watches, paused or not, a newer version waiting |
| `/trades` | The trades you took that it is following, and your results of the last 30 days |
| `/result 1.2` | Your real result of the last finished trade, in R after fees (-1 = the full stop lost, 2 = twice what you risked). `/result <id> 1.2` for an older one (ids in `/trades`) |
| `/weather` | What kind of market day it is: **trend up / trend down / range / choppy / news risk**, BTC's usual 24h move (measured from the past, not a forecast), crowding (funding, open interest), the next events, what fits today and what to avoid. Made by GitHub's hourly scan; it never creates a signal or changes a rule |
| `/pause` | No new trade alerts until `/resume`. `/pause 2h` or `/pause 30m` = for a while, then on again by itself |
| `/resume` | New trade alerts on again |
| `/help` | The list |

**Buttons under each alert:**
- **✅ Took it** → the watcher follows that trade on 5-minute candles, with the same rules as the backtests, and
  messages you:
  - 🎯 **TP1 hit** → close the share it says, and move the stop-loss to your entry (break-even).
  - 🎯 **TP2 hit** → close the share it says, and move the stop-loss to TP1.
  - 🏁 **last TP hit**, 🛑 **stop hit**, or ⏱ **time stop** (the strategy's max hold is over → close the rest).
  - Each of these also gives the result in R (1R = what you risked).
- **❌ Skipped** → only recorded. You can change your mind with the other button.
- **🏁 I closed it** (appears after ✅) → you closed it yourself; it stops following.

`/pause` never stops the messages about trades you already took. Everything you press is saved on the PC in
`journal\my_trades.csv` (opens in Excel), so your real results are kept. Updates never touch that file.

The follow-up messages come about 10–30 seconds after each 5-minute candle closes. They remind you what to do; they
don't replace the stop-loss and TP orders on OKX, so always put those on OKX as soon as you enter.

## Journal sync (optional, 5 minutes): let the agent learn from your own trades

Your button presses stay on the PC unless you switch this on. With it, the watcher uploads
`journal\my_trades.csv` to GitHub (its own branch, `journal`) after every 5-minute check when something changed,
and the hourly scan turns it into **"Your own trades"** in the Sunday weekly email and in Claude's daily and weekly
fact sheets (`reports/journal_review.md`):

- **Every alert gets a plan result**, also the ones you skip or don't answer: the watcher follows each alert
  silently with the backtest's rules. So the agent can tell whether your skips help or hurt.
- **Your real result** (`/result 1.2` after a trade; the bot asks for it) vs the plan for the same trade: the gap
  is your fees, slippage, late entries and early exits - the part of the backtest you don't get.
- **Closing early**: what it cost or saved you, per trade.

It only reports. It never changes a strategy, a gate, a cost or an approval - a finding like "your real costs look
higher than the backtest's" is for you to decide on.

**Set it up (once):**
1. On GitHub (signed in), open https://github.com/settings/personal-access-tokens/new
2. **Token name**: `crypto journal` · **Expiration**: 1 year · **Repository access**: *Only select repositories* →
   `mayastraglobal-ui/crypto-signal-agent`
3. **Permissions** → Repository permissions → **Contents: Read and write**. Nothing else.
4. **Generate token** and copy it (it starts with `github_pat_`).
5. On the PC, double-click **`windows\6_journal_sync.bat`**, paste the token, press Enter. It uploads your journal
   once to check the token, saves it in `telegram.env` (private, never uploaded) and restarts the watcher.
6. `/status` in Telegram now shows **Journal sync to GitHub: uploaded …**.

Good to know: the repository is public, so the `journal` branch is too - it holds your alerts, choices and results
in R (no account, balance or keys). The token can only write files of this one repository; keep `telegram.env`
private. When the token expires, `/status` shows "failing": make a new one and run `6_journal_sync.bat` again.

## The buttons (all in the `windows` folder)

| File | What it does |
|---|---|
| `1_setup.bat` | First setup; run it again to change the Telegram bot or repair the install |
| `2_start_watcher.bat` | Start the watcher (if you closed it) |
| `3_stop_watcher.bat` | Stop the watcher |
| `4_update.bat` | Download the newest version from GitHub (keeps your Telegram settings). Telegram tells you when an update is available |
| `5_remove_autostart.bat` | Stop it from starting with Windows |
| `6_journal_sync.bat` | Optional: send your journal to GitHub so the agent learns from your trades (see Journal sync) |
| `run_watcher.bat` | The watcher itself (the start button and auto-start use it) |

## Reading an alert

```
🟢 LIVE LONG SOL · SOL-USDT-SWAP
15m · donchian_breakout v1.0
Entry zone: 120.36 – 120.84 (planned 120.60)
Stop-loss: 119.40 (1.00% away = 1R)
TP1: 123.00 (2.0R, close 50%)
TP2: 124.20 (3.0R, close 50%)
Size at 0.5% risk ($5.00): 4.17 SOL ≈ $503, 0.50x
Max hold: 30 candles (~7h30m)
Trend: 1W WEAK_BULL · 1D STRONG_BULL · 4H WEAK_BULL · 1H STRONG_BULL
Valid for 2 15m candles. Skip it if price reaches the stop or TP1 first.
```

- Under each alert: **✅ Took it** / **❌ Skipped** (see "Using the bot from your phone" above).
- 🟢/🔴 **LIVE** = an approved strategy. 📝 **PAPER** = practice only (the strategy is still being proven).
- Enter only inside the **entry zone**; if price already ran past it, skip.
- Put the **stop-loss and TPs** on OKX as soon as you enter. "Close 50%" = take half of the position there.
- **⚠️** lines (for example a CPI or FOMC event within 60 minutes) mean the risk rules say: no live entry now.

## Good to know

- **Windows Update restarts:** after a restart the PC waits at the sign-in screen. The watcher starts when you
  sign in. If the PC must recover with nobody there, you can turn on automatic sign-in (search "netplwiz"), but
  only on a PC nobody else can use.
- **Internet drops:** the watcher retries by itself. After 3 failed checks in a row you get a ⚠️ on Telegram, and
  a "recovered" message when it works again.
- **Power:** keep a laptop plugged in. The screen may turn off, which is fine. Since 2026-10-06 the watcher also
  tells Windows not to sleep while it runs. A shared or work PC can still be forced to sleep, restart or sign out
  by its administrator's rules; signing out stops the watcher (locking the screen does not).
- **Checking from far away:** with a remote-desktop app (for example Chrome Remote Desktop) on the PC and your
  phone, you can look at the watcher window and restart it without going there.
- **Log file:** `logs\live_watcher.log` in the agent folder shows everything it did.
- **Only one copy runs.** Starting it twice is harmless: the second copy closes itself.
- **Your Telegram token** is stored only in `telegram.env` in the agent folder. Don't share that file.

## Problems

| Problem | Fix |
|---|---|
| "Python is not installed" again after installing | Close the window and double-click `1_setup.bat` again (Windows needs a new window to see Python) |
| winget not found / install failed | Install Python from https://www.python.org/downloads/ and tick **"Add python.exe to PATH"** on the first screen, then run `1_setup.bat` again |
| "That token does not work" | Copy the token again from BotFather (the whole line with the colon), run `1_setup.bat` again |
| "No message arrived" | Open your bot in Telegram, press **START**, then run `1_setup.bat` again |
| The bot doesn't answer `/status` | Check, in this order: 1) is the **Crypto Watcher** window on the taskbar? If not, double-click `2_start_watcher.bat`. 2) Is its title starting with **"Select"**? A mouse click froze it (QuickEdit): press **Esc** (the watcher turns QuickEdit off itself since 2026-10-06). 3) Did the PC sleep, restart or sign out? Sign in; the watcher starts with Windows. 4) Look at the end of `logs\live_watcher.log`: "Telegram commands: ..." = the network blocks Telegram. |
| No answer for a few minutes right after a start or an update | Normal: the first market check downloads ~250 batches of candles; through a slow VPN this takes minutes and the bot answers afterwards. Wait ~10 minutes before `/status` |
| `/status` or the window shows "problems: config.yaml: ChunkedEncodingError" / "ConnectionError" | The connection to GitHub broke during the hourly download (often a slow VPN server). Each file is tried 3 times; a file is only replaced by a complete download, so the watcher keeps working with the last good copy and tries again next hour. If it shows every hour: pick a faster VPN server (around 100 ms) |
| No "✅ Live watcher running" message in the morning | It sends one every day at 00:05 UTC. None = it was not running at that time: check the PC |
| After `4_update.bat` the bot is silent | Older versions asked "Start the watcher again now?" and waited; answer **Y** (since 2026-10-06 it starts by itself after 20 seconds) |
| No "started" message | Run `2_start_watcher.bat`; look at `logs\live_watcher.log` |
| Telegram says a newer version is on GitHub | Double-click `4_update.bat` |

Running it on the Mac or a Linux server instead is described in `docs/LIVE_WATCHER.md`.
