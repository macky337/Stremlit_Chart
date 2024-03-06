import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


def calculate_moving_average(prices, window):
    return prices.rolling(window=window).mean()


def fetch_data(ticker_symbol, period):
    ticker = yf.Ticker(ticker_symbol)
    df = ticker.history(period=period)
    return df


def plot_data(df, ticker_symbol, ma_selections):
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Close'], label='Close Price', color='tab:blue')

    # 移動平均線の追加と凡例の復活
    for window in ma_selections:
        ma = calculate_moving_average(df['Close'], window)
        plt.plot(df.index, ma, label=f'{window}-day MA')

    plt.title(f'{ticker_symbol} - Closing Prices and Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()  # 凡例の表示
    st.pyplot(plt)


def main():
    st.sidebar.title('設定')
    symbol_options = ['^DJI', '^IXIC', '^GSPC', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'PYPL', 'NFLX',
                      'CRM', 'INTC', 'ARMH', 'CRWD', 'AMD', 'ADBE', '8411.T', '7735.T', '8035.T', '9984.T']
    default_symbols = ['AAPL', 'MSFT', 'GOOGL']

    if st.sidebar.button('全銘柄を選択'):
        selected_symbols = symbol_options
    else:
        selected_symbols = st.sidebar.multiselect('銘柄を選択してください', options=symbol_options,
                                                  default=default_symbols)

    # 期間の選択肢に3か月、6か月を追加
    period = st.sidebar.selectbox('期間', options=['1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd'], index=3)

    ma_options = [5, 25, 100, 200]
    ma_selections = st.sidebar.multiselect('移動平均線を選択', options=ma_options, default=[25, 100])

    for symbol in selected_symbols:
        df = fetch_data(symbol, period)
        if not df.empty:
            plot_data(df, symbol, ma_selections)
        else:
            st.write(f'{symbol}: データの取得に失敗しました。')


if __name__ == "__main__":
    main()
