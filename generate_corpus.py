import os
from pathlib import Path

CORPUS_DIR = Path(__file__).resolve().parent / "rag" / "corpus"
CORPUS_DIR.mkdir(parents=True, exist_ok=True)

documents = {
    "01_macd_divergence_guide.md": """# MACD Divergence Trading Strategy & Analysis Guide

## What is MACD Divergence?
MACD Divergence occurs when the market price of an asset (such as BTC, ETH, or EUR/USD) moves in the opposite direction of the MACD (Moving Average Convergence Divergence) histogram or MACD line. It is one of the most powerful early reversal indicators in technical analysis.

## Types of MACD Divergence
1. **Bullish Divergence**:
   - **Price Action**: Price makes a lower low.
   - **MACD Action**: MACD histogram or MACD line makes a higher low.
   - **Trading Signal**: Indicates seller momentum is waning and a bullish upward trend reversal is imminent. Traders look to open Long positions or buy spot assets near support.

2. **Bearish Divergence**:
   - **Price Action**: Price makes a higher high.
   - **MACD Action**: MACD histogram or MACD line makes a lower high.
   - **Trading Signal**: Indicates buying pressure is exhausting. Indicates a bearish downward trend reversal. Traders look to take profits or open Short positions.

3. **Hidden Divergence**:
   - **Bullish Hidden Divergence**: Price makes a higher low while MACD makes a lower low (Trend continuation signal).
   - **Bearish Hidden Divergence**: Price makes a lower high while MACD makes a higher high.

## Entry Rules & Confirmation
- Never trade MACD divergence in isolation. Always seek confluence with key Support/Resistance levels or RSI oversold/overbought signals.
- Wait for a MACD signal line crossover confirmation before executing trades.
""",

    "02_rsi_overbought_oversold.md": """# Relative Strength Index (RSI) Master Class

## Understanding RSI Values
The Relative Strength Index (RSI) is a momentum oscillator developed by J. Welles Wilder that measures the speed and velocity of price movements on a scale from 0 to 100.

## Critical Thresholds
- **Overbought Level (>70)**: Indicates the asset has experienced rapid upward momentum and may be overextended. A pullback or consolidation is likely.
- **Oversold Level (<30)**: Indicates extreme selling pressure. The asset may be undervalued, presenting a potential buying opportunity.
- **Midline (50)**: Serves as the trend boundary. RSI > 50 indicates bullish dominance; RSI < 50 indicates bearish control.

## RSI Failure Swings
An RSI Failure Swing occurs when RSI breaches 70 or falls below 30, retraces, and fails to breach the extreme peak/trough on the next attempt. This signals strong trend exhaustion before price action reflects it.
""",

    "03_bollinger_bands_squeeze.md": """# Bollinger Bands Squeeze & Volatility Strategy

## Bollinger Bands Architecture
Developed by John Bollinger, Bollinger Bands consist of three lines:
1. **Middle Band**: 20-period Simple Moving Average (SMA).
2. **Upper Band**: 20 SMA + (2 * Standard Deviation).
3. **Lower Band**: 20 SMA - (2 * Standard Deviation).

## The Bollinger Squeeze Pattern
When the Upper and Lower bands contract tightly toward the Middle Band, volatility reaches historical lows. This setup precedes high-volatility breakouts.

## Trading Rules
- **Bullish Breakout**: Price closes above the Upper Band with expanding band width and high trading volume.
- **Bearish Breakout**: Price closes below the Lower Band with expanding band width.
""",

    "04_support_and_resistance_levels.md": """# Support and Resistance Identification & Execution

## Core Definitions
- **Support**: A price floor where buying interest is sufficiently strong to overcome selling pressure.
- **Resistance**: A price ceiling where selling interest overcomes buying pressure.

## Dynamic vs Static Support/Resistance
- **Static Levels**: Historical horizontal highs, lows, and round psychological numbers (e.g., $100,000 BTC, $3,000 ETH, 1.1000 EUR/USD).
- **Dynamic Levels**: Exponential Moving Averages (EMA 20, EMA 50, EMA 200) that adjust continuously as price action evolves.

## Role Reversal Principle
Once a Resistance level is convincingly broken to the upside, it flips to become a Support level during subsequent retests. Conversely, broken Support flips to Resistance.
""",

    "05_candlestick_patterns_mastery.md": """# Candlestick Patterns Manual for Crypto & Forex

## Bullish Reversal Candlesticks
1. **Hammer**: Small upper body, long lower shadow (wick) at least twice the length of the body. Signals rejection of lower prices.
2. **Bullish Engulfing**: A large green candle completely engulfs the real body of the preceding small red candle at market bottom.
3. **Morning Star**: Three-candle pattern featuring a long red candle, a indecisive doji/spinning top, followed by a strong green candle closing above 50% of the first candle.

## Bearish Reversal Candlesticks
1. **Shooting Star**: Long upper shadow, small lower body at market high.
2. **Bearish Engulfing**: A large red candle engulfs the preceding green candle body.
3. **Evening Star**: Three-candle top reversal pattern signaling intense distribution.
""",

    "06_chart_patterns_trading.md": """# Classical Chart Patterns Reference Guide

## Reversal Patterns
- **Head and Shoulders**: Features Left Shoulder, Head (highest peak), and Right Shoulder. A breakdown below the Neckline signals a major bearish trend shift. Target = Height from Head to Neckline.
- **Double Bottom (W Pattern)**: Two distinct troughs at roughly equal price levels. Breakout above the peak confirmation level triggers bullish entry.

## Continuation Patterns
- **Bull Flag**: Sharp upward pole followed by downward sloping rectangular channel consolidation. Breakout above flag resistance resumes upward trend.
- **Ascending Triangle**: Flat horizontal resistance with higher lows. Signals accumulation leading to bullish breakout.
""",

    "07_risk_management_1percent_rule.md": """# Risk Management & The 1% Rule

## The Golden Rule of Position Sizing
Never risk more than 1% to 2% of total trading account equity on any single trade.

## Position Sizing Formula
$$\\text{Position Size} = \\frac{\\text{Account Capital} \\times \\text{Risk Percentage}}{\\text{Entry Price} - \\text{Stop Loss Price}}$$

## Example Calculation
- **Account Balance**: $10,000
- **Max Risk (1%)**: $100
- **BTC Entry Price**: $100,000
- **Stop Loss Price**: $98,000 (Distance = $2,000)
- **Position Size**: $\$100 / \$2,000 = 0.05 \\text{ BTC}$

Following this formula guarantees that even a string of 10 consecutive losses reduces total capital by less than 9.5%.
""",

    "08_risk_reward_ratio_optimization.md": """# Risk-to-Reward Ratio (R:R) Optimization

## Understanding Risk-to-Reward Ratio
The Risk-to-Reward Ratio measures the potential loss against potential gain on a trade setup.

## Minimum R:R Threshold
- A minimum Risk-to-Reward ratio of **1:2** (risking $1 to make $2) is mandatory for profitable long-term trading systems.
- With a 1:2 R:R ratio, a trader needs a win rate of only **33.3%** to break even.

| Win Rate | R:R Ratio | Profitability Expectancy |
| :--- | :--- | :--- |
| 40% | 1:1 | Negative (-10R per 100 trades) |
| 40% | 1:2 | Positive (+20R per 100 trades) |
| 50% | 1:3 | Highly Profitable (+100R per 100 trades) |
""",

    "09_stop_loss_take_profit_atr.md": """# Dynamic Stop Loss & Take Profit Placement Using ATR

## Average True Range (ATR) Method
Static stop losses fail during volatile market expansion. Using ATR adjusts stop loss distance dynamically based on actual market volatility.

## ATR Placement Protocol
1. **Stop Loss Distance**: Set SL at $\\text{Entry Price} \\pm (1.5 \\times \\text{ATR})$.
2. **Take Profit Distance**: Set TP at $\\text{Entry Price} \\pm (3.0 \\times \\text{ATR})$ for a 1:2 R:R setup.

## Advantages
- Prevents premature stop-outs during market noise and spread widening.
- Automatically widens stops during high volatility and tightens stops in quiet markets.
""",

    "10_trading_psychology_fomo_control.md": """# Trading Psychology & Emotional Discipline

## Overcoming FOMO (Fear Of Missing Out)
FOMO causes traders to buy at market tops during green candles and sell at market bottoms.

## Core Rules for Emotional Control
1. **Never Chase Parabolic Moves**: If a price break has already moved more than 2x ATR without you, wait for a pull-back retest.
2. **Rule-Based Execution**: Execute entries only when pre-written plan conditions (Technical + Sentiment + Risk) are fulfilled.
3. **Accepting Loss as Operating Expense**: Losses are normal business expenses in trading, not personal failures.
""",

    "11_money_management_capital_preservation.md": """# Money Management & Capital Preservation Principles

## Capital Protection Guidelines
1. **Max Drawdown Limit**: If account drawdown reaches 10% in a month, halt trading for 48 hours to recalibrate.
2. **Leverage Control**: In Crypto Futures & Forex, limit real leverage to 3x-5x max. High leverage (20x-100x) amplifies liquidation risk exponentially.
3. **Profit Locking**: Scale out 50% of position size at Take Profit 1 and move Stop Loss to Breakeven.
""",

    "12_binance_futures_and_order_types.md": """# Binance API & Futures Order Types Guide

## Binance Order Types
- **Limit Order**: Executes at specified price or better. Lowers maker fees.
- **Market Order**: Executes immediately at current order book ask/bid price. Higher taker fees.
- **Stop-Limit / Stop-Market Order**: Triggers a buy/sell when stop price is touched. Essential for Stop Loss execution.
- **Trailing Stop Order**: Moves the stop loss price automatically as market price trends favorably.
""",

    "13_forex_market_fundamentals.md": """# Forex Market Architecture & Currency Pair Dynamics

## Major Currency Pairs
- **EUR/USD**: Euro / US Dollar (Most liquid global pair).
- **GBP/USD**: British Pound / US Dollar ("Cable" - known for high intraday volatility).
- **USD/JPY**: US Dollar / Japanese Yen (Highly sensitive to US Treasury Yields).

## Key Market Sessions
1. **Asian Session (Tokyo)**: 00:00 - 09:00 UTC. Lower volatility, consolidation range bound.
2. **London Session**: 08:00 - 17:00 UTC. Highest liquidity and major breakout movements.
3. **New York Session**: 13:00 - 22:00 UTC. Overlaps with London session; highest volume volatility.
""",

    "14_economic_calendar_events_nfp_fomc.md": """# Economic Calendar & Macroeconomic Indicators

## High-Impact Macroeconomic Events
1. **FOMC Interest Rate Decision & Fed Chair Speech**: Direct impact on US Dollar index (DXY), Gold, and Crypto assets.
2. **Non-Farm Payrolls (NFP)**: Released first Friday of every month. Measures US job creation.
3. **CPI (Consumer Price Index)**: Primary measure of inflation. Higher CPI = Hawkish interest rate policy = USD Strength.
""",

    "15_crypto_market_cycles_halving.md": """# Bitcoin Halving & Crypto Market Cycles

## The 4-Year Bitcoin Cycle
Bitcoin block reward halving occurs approximately every 210,000 blocks (roughly 4 years), cutting new BTC issuance in half.

## Four Phases of Crypto Market Cycle
1. **Accumulation Phase**: Smart money buys in quiet, sideways depressed market.
2. **Markup Phase (Bull Run)**: Parabolic price growth, retail inflow, all-time high breaks.
3. **Distribution Phase**: Whales scale out into extreme retail excitement.
4. **Markdown Phase (Bear Market)**: Sharp pullbacks of 70%-85% from peak.
""",

    "16_multi_timeframe_confluence_analysis.md": """# Multi-Timeframe Confluence Analysis

## The Top-Down Analysis Framework
1. **Higher Timeframe (Daily / 4H)**: Establishes overall macro trend direction and key major support/resistance zones.
2. **Intermediate Timeframe (1H)**: Identifies chart patterns, indicator setups (MACD/RSI), and structural entry zones.
3. **Execution Timeframe (15M / 5M)**: Fine-tunes precise entry timing, candle wicks, and tight stop loss placement.
""",

    "17_volume_spread_analysis.md": """# Volume Spread Analysis (VSA) & Order Flow

## Core VSA Principles
Price movements are valid only when validated by corresponding trading volume.

## Key VSA Signals
- **High Volume + Small Spread Candle**: Signals absorption by institutional market makers (Reversal imminent).
- **Low Volume Test**: Price dips into support with low volume, confirming lack of selling interest (Bullish confirmation).
""",

    "18_ema_moving_average_crossovers.md": """# Exponential Moving Average (EMA) Crossover Strategies

## Moving Average Configuration
- **Fast EMA**: 20-period EMA.
- **Medium EMA**: 50-period EMA.
- **Slow Macro EMA**: 200-period EMA.

## Signals
- **Golden Cross**: EMA 50 crosses above EMA 200. Major long-term bull market signal.
- **Death Cross**: EMA 50 crosses below EMA 200. Major long-term bear market signal.
""",

    "19_fibonacci_retracement_levels.md": """# Fibonacci Retracement & Golden Ratio Trading

## Key Fibonacci Levels
- **0.382 (38.2%)**: Shallow pullback in strong trends.
- **0.500 (50.0%)**: Psychological mid-point.
- **0.618 (61.8%)**: The Golden Ratio retracement level (Highest probability reversal zone).
- **0.786 (78.6%)**: Deep retracement level before structural invalidation.
""",

    "20_portfolio_diversification_crypto_forex.md": """# Portfolio Management & Asset Allocation

## Cross-Asset Asset Allocation
To protect capital against market-wide downturns, diversify across un-correlated asset classes:
- **Core Crypto Allocation**: 50% (Bitcoin & Ethereum).
- **Forex / Major Pairs**: 30% (EUR/USD, GBP/USD, USD/JPY).
- **Hedge / Commodities**: 20% (Gold & Cash Reserves).
""",

    "21_trade_journaling_performance_tracking.md": """# Trade Journaling & AI Analytics Framework

## Mandatory Log Fields for Professional Traders
Every trade execution must log:
1. Date & Time
2. Asset Pair & Direction (Long / Short)
3. Confluence Checklist (RSI, MACD, Support/Resistance, News)
4. Planned Entry, Stop Loss, Take Profit
5. Actual Execution Price & Exit Price
6. Emotional State & Lessons Learned

Analyzing journal logs over 50+ trades reveals actual win rates, average risk-to-reward ratios, and system expectancy.
"""
}

for filename, content in documents.items():
    filepath = CORPUS_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip())

print(f"Successfully generated {len(documents)} trading domain guides in {CORPUS_DIR}")
