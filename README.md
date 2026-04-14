# 📈 Market Royale Trading Bot – FinalStrategy

> **An event-driven algorithmic trading bot developed for the Market Royale Hackathon at APOGEE '26 (BITS Pilani).**

This repository contains `FinalStrategy`, an automated trading algorithm designed to react to real-time market data and news signals. Operating within a simulated exchange environment, the bot trades commodities (e.g., Oil, Steel, Grain) by capitalizing on market inefficiencies while strictly adhering to built-in risk management protocols.

---

## 🚀 Overview

The core objective of this bot is to maximize portfolio value through **news-driven trading**. By analyzing incoming news feeds alongside real-time market depth, the bot makes split-second decisions to enter or exit positions, prioritizing capital preservation during periods of high volatility.

**Hackathon Details:**
* **Event:** Market Royale (APOGEE '26, BITS Pilani)
* **Duration:** 48 Hours
* **Objective:** Maximize portfolio PnL in a simulated volatile market
* **Architecture:** Event-driven Algorithmic Trading

---

## 🧠 Strategy & Logic

The trading logic is built on the premise that news dictates short-term price momentum. However, to prevent exposure to market whipsaws, the strategy is heavily insulated with automated risk-management constraints.

### The Core Engine:
- 📊 **Positive News Surge → Execute `BUY` Order**
- 📉 **Negative News Drop → Execute `SELL` Order**
- 🧯 **Dynamic Exits → Stop-Loss & Time-Decay Mechanisms**

---

## ⚙️ Key Features

### 1. Precision Entry Protocol
- **Signal Filtering:** Enters a trade *only* when a statistically significant news signal is detected.
- **Overtrade Prevention:** Strictly monitors current open positions to avoid redundant entries and capital overexposure.

### 2. State & Position Tracking
Maintains a continuous internal state of the order book, tracking:
- Current directional exposure (Long/Short)
- Exact entry pricing
- Time-in-trade (Holding duration)

### 3. Strict Risk Management (Capital Preservation)
- **Hard Stop-Loss:** Automatically liquidates the position if drawdowns exceed **1.5%**.
- **Signal Reversal Exit:** Instantly closes trades if conflicting/opposite news hits the feed.
- **Time-Based Exit (Decay):** Forces a position close after a maximum holding period of 300 ticks to prevent exposure to stagnant capital.

### 4. Position Constraints
- **Absolute Limits:** Respects exchange-mandated max position limits (±500 units).
- **Standardized Lot Sizing:** Uses fixed initial trade sizing to maintain predictable risk/reward ratios.

---

## 🔄 Execution Flow

The bot operates on a high-frequency event loop. On every market tick, the execution pipeline is as follows:

1. **Ingest:** Receive market observations (Bid, Ask, Midprice, Book Depth, News).
2. **State Update:** Update internal price history and portfolio cash balance.
3. **Position Check:** - *If in a trade:* Evaluate against Stop-Loss, Signal Reversal, and Time-Decay conditions. Liquidate if triggered.
4. **Signal Evaluation:** - *If flat (no trade):* Parse news severity and enter a `LONG` or `SHORT` position accordingly.
5. **Execution:** Dispatch order array back to the exchange matching engine.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Architecture:** Event-Driven Programming
* **Integration:** Custom Trading Simulation API

---

## 📦 Project Structure

```text
FinalStrategy/
│── final_strategy.py   # Core algorithmic logic and event loop
│── README.md           # Project documentation
