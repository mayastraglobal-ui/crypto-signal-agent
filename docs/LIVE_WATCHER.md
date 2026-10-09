# Live watcher: instant Telegram alerts (setup guide)

The hourly GitHub scan checks the market once an hour, and GitHub often starts it late. That is too slow for
scalping. The **live watcher** runs all the time on a free Oracle Cloud server. Every 5 minutes, about 10–30
seconds after a candle closes, it checks your strategies on the newest **OKX USDT-perpetual** candles and sends you
a Telegram message right away.

It runs the same engine as the hourly scan, in your order:

1. **1W / 1D**: the trend. A strong weekly trend against the trade blocks it.
2. **4H / 1H**: bull or bear. A trade needs most of these timeframes to agree.
3. **1H / 30m / 15m**: the strategy rules, on the timeframe whose candle just closed.
4. **5m**: the entry check, for strategies that use it.
5. **Alert**: entry zone, stop-loss, TP1/TP2/TP3, position size for your account, maximum hold time and why.

**Which strategies alert?** Only strategies that passed the daily research:

| Research status | Telegram alert |
|---|---|
| APPROVED | 🟢/🔴 **LIVE** (a real signal) |
| PAPER_TRADING | 📝 **PAPER** (practice only: the strategy is still being proven) |
| anything else | nothing |

Right now no strategy is APPROVED or PAPER_TRADING, so the watcher stays quiet until the daily research promotes
one. Silence means "no strategy that passed the tests has a setup", not that the watcher is broken. It also sends
one "still running" message a day, and a warning if it stops working.

The watcher never places orders and never needs your OKX keys. You place the trade yourself.

---

## Step 1: create the free Oracle Cloud server (about 15 minutes, once)

1. Go to https://www.oracle.com/cloud/free/ and click **Start for free**. Use your email and choose your
   **home region** (the nearest one; it can't be changed later). Oracle asks for a card to check you are a real
   person. Always Free resources are not charged.
2. When you're in the console: menu ☰ → **Compute** → **Instances** → **Create instance**.
3. Name: `crypto-watcher`.
4. **Image and shape** → **Edit**:
   - Image: **Canonical Ubuntu 24.04**
   - Shape: **Ampere** → **VM.Standard.A1.Flex**, **1 OCPU**, **6 GB memory** (shows "Always Free-eligible").
   - If Oracle says it has no Ampere capacity, try again later or pick another availability domain.
5. **Add SSH keys** → **Generate a key pair for me** → click **Save private key** and keep the file safe.
6. Click **Create**. After 1–2 minutes the instance is **RUNNING**. Copy its **Public IP address**.

## Step 2: install the watcher (about 5 minutes)

Connect to the server. The easiest way is from the Oracle console: click the **Cloud Shell** icon (`>_`, top
right), upload your private key file (Cloud Shell menu ⚙ → **Upload**), then type
(replace the file name and the IP):

```bash
chmod 600 ssh-key-*.key
ssh -i ssh-key-*.key ubuntu@YOUR.PUBLIC.IP
```

On Windows you can also use PowerShell with the same `ssh -i ... ubuntu@IP` command.

On the server, paste this one line:

```bash
curl -fsSL https://raw.githubusercontent.com/mayastraglobal-ui/crypto-signal-agent/main/deploy/install_oracle.sh | bash
```

It installs Python, downloads your agent, and sets it up as a background service that restarts by itself after a
crash or a reboot.

## Step 3: connect Telegram (about 5 minutes)

1. In Telegram, open **@BotFather** → send `/newbot` → choose a name and a username ending in `bot`.
   BotFather replies with a **token** like `123456789:AAH...`. Keep it secret.
2. Open your new bot (the link BotFather gives) and press **Start**, or send it `hi`.
3. On the server:
   ```bash
   nano ~/.crypto-agent.env
   ```
   Put the token after `TELEGRAM_BOT_TOKEN=`. Save with Ctrl+O, Enter, then Ctrl+X.
4. Find your chat id:
   ```bash
   cd ~/crypto-signal-agent && set -a && . ~/.crypto-agent.env && set +a && .venv/bin/python live_watcher.py --find-chat-id
   ```
   Put the number it prints after `TELEGRAM_CHAT_ID=` in the same file (`nano ~/.crypto-agent.env` again).
5. Test and start:
   ```bash
   set -a && . ~/.crypto-agent.env && set +a && .venv/bin/python live_watcher.py --test-telegram
   sudo systemctl restart crypto-watcher
   ```
   You should get "Telegram works", then "Live watcher started".

## Commands and buttons in Telegram

The bot answers `/status`, `/trades`, `/weather` (the market weather), `/tests on|off` (🔵 TEST alerts, `docs/WINDOWS_WATCHER.md`), `/pause` (`/pause 2h`), `/resume` and `/help`,
only in your own chat. Under
each alert, **✅ Took it** makes the watcher follow the trade (TP1 → stop to entry, TP2 → stop to TP1, last TP, stop,
time stop: the backtests' rules) and message you at each step; **❌ Skipped** is only recorded. Everything is saved
in `journal/my_trades.csv` on the server. Details: `docs/WINDOWS_WATCHER.md`, "Using the bot from your phone".
Optional **journal sync** (the agent learns from your own trades): `python live_watcher.py --setup-github` (a
fine-grained token, Contents: read and write on this repository) - see `docs/WINDOWS_WATCHER.md`, "Journal sync".

## Every day: nothing to do

- The watcher pulls your repository every hour, so new strategy statuses, coins and settings arrive by themselves.
- To update the code after a change is merged, run the install line from step 2 again.
- Useful commands on the server:

| What | Command |
|---|---|
| Is it running? | `sudo systemctl status crypto-watcher` |
| What is it doing? | `journalctl -u crypto-watcher -f` (Ctrl+C to stop watching) |
| Restart | `sudo systemctl restart crypto-watcher` |
| Stop | `sudo systemctl stop crypto-watcher` |
| Which strategies may alert | `cd ~/crypto-signal-agent && .venv/bin/python live_watcher.py --status` |

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
5m check: CONFIRMED on the 16:20 UTC 5m bar close
Trend: 1W WEAK_BULL · 1D STRONG_BULL · 4H WEAK_BULL · 1H STRONG_BULL
Valid for 2 15m candles. Skip it if price reaches the stop or TP1 first.
```

- **Entry zone**: enter only inside it. If price has already moved past it, skip the trade.
- **Stop-loss / TP**: set them on OKX as soon as you enter. "Close 50%" = take half the position at that target.
- **Size**: at your risk per trade (`config.yaml` → `account`), the position that loses exactly that amount at
  the stop. It's never more than 3x leverage: a tighter stop gives a smaller position instead.
- **⚠️ lines**: for example a high-impact event (CPI, FOMC) within 60 minutes. The risk rules say no live entry then.

## Good to know

- Prices come from **OKX perpetuals** (what you trade). The research backtests use Binance spot candles; the two
  normally differ by less than 0.05%.
- The hourly scan stays the official record: it logs the same signals, emails them and tracks the results.
- If you change `config.yaml` → `live_watcher` (for example the cooldown), the watcher picks it up within an hour.
