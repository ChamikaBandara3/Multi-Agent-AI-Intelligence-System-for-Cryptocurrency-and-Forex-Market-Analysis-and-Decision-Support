# Dynamic Stop Loss & Take Profit Placement Using ATR

## Average True Range (ATR) Method
Static stop losses fail during volatile market expansion. Using ATR adjusts stop loss distance dynamically based on actual market volatility.

## ATR Placement Protocol
1. **Stop Loss Distance**: Set SL at $\text{Entry Price} \pm (1.5 \times \text{ATR})$.
2. **Take Profit Distance**: Set TP at $\text{Entry Price} \pm (3.0 \times \text{ATR})$ for a 1:2 R:R setup.

## Advantages
- Prevents premature stop-outs during market noise and spread widening.
- Automatically widens stops during high volatility and tightens stops in quiet markets.