import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def calculate_moving_average(prices, window):
    """指定されたウィンドウでの移動平均を計算します。"""
    return prices.rolling(window=window).mean()

def fetch_data(ticker_symbol, period):
    """指定された期間で銘柄のデータを取得します。"""
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.history(period=period)
    return df

def display_last_price_and_change(df):
    """最新の終値と前日比を計算します。"""
    last_price = df['Close'].iloc[-1]
    previous_price = df['Close'].iloc[-2]
    change = last_price - previous_price
    percent_change = (change / previous_price) * 100
    return last_price, change, percent_change

def plot_data(df, ticker_symbol, ma_selections):
    """株価、移動平均、および出来高をプロットします。"""
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:blue'
    ax1.plot(df.index, df['Close'], label='Close Price', color=color)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Close Price', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # 移動平均線の追加と凡例の表示
    for window in ma_selections:
        ma = calculate_moving_average(df['Close'], window)
        ax1.plot(df.index, ma, label=f'{window}-day MA')

    # 出来高の追加
    ax2 = ax1.twinx()
    ax2.fill_between(df.index, 0, df['Volume'], color='tab:gray', alpha=0.3)
    ax2.set_ylabel('Volume', color='tab:gray')
    ax2.tick_params(axis='y', labelcolor='tab:gray')

    ax1.legend(loc='upper left')
    plt.title(f'{ticker_symbol} - Closing Prices, Moving Averages, and Volume')
    st.pyplot(fig)

def main():
    st.sidebar.title('設定')

    # 銘柄追加のインプットボックス
    add_symbol = st.sidebar.text_input('銘柄コードを追加', '')

    symbol_options = ['^DJI', '^IXIC', '^GSPC', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'PYPL', 'NFLX', 'CRM', 'INTC', 'ARMH', 'CRWD', 'AMD', 'ADBE', '8411.T', '7735.T', '8035.T', '9984.T']

    if st.sidebar.button('追加') and add_symbol:
        symbol_options.append(add_symbol.upper())

    if st.sidebar.button('全銘柄を選択'):
        selected_symbols = symbol_options
    else:
        selected_symbols = st.sidebar.multiselect('銘柄を選択してください', options=symbol_options, default=['AAPL', 'MSFT', 'GOOGL'])

    period = st.sidebar.selectbox('期間', options=['1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd'], index=3)

    ma_options = [5, 25, 100, 200]
    ma_selections = st.sidebar.multiselect('移動平均線を選択', options=ma_options, default=[25, 100, 200])

    for symbol in selected_symbols:
        df = fetch_data(symbol, period)
        if not df.empty:
            plot_data(df, symbol, ma_selections)
            last_price, change, percent_change = display_last_price_and_change(df)
            st.write(f"最新の終値: {last_price:.2f}, 前日比: {change:.2f} ({percent_change:.2f}%)")
        else:
            st.error(f'{symbol}: データの取得に失敗しました。')

if __name__ == "__main__":
    main()
