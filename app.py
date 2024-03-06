import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf


def calculate_moving_average(prices, window):
    return prices.rolling(window=window).mean()


def fetch_data(ticker_symbol, period_years):
    ticker = yf.Ticker(ticker_symbol)
    # yfinanceで期間を設定するには、"1y", "2y"などの形式を使用します。
    # ここでは、入力された年数をこの形式に変換します。
    period_str = f"{period_years}y"
    df = ticker.history(period=period_str)
    return df


def plot_data(df, ticker_symbol, ma_selections):
    plt.figure(figsize=(10, 6))

    plt.plot(df.index, df['Close'], label='Close Price', color='tab:red')

    for window in ma_selections:
        ma = calculate_moving_average(df['Close'], window)
        plt.plot(df.index, ma, label=f'{window}D MA')

    plt.title(f'{ticker_symbol} - Closing Prices and Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    st.pyplot(plt)


def main():
    st.sidebar.title('設定')
    symbol_options = ['^DJI', '^IXIC', '^GSPC', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'PYPL', 'NFLX',
                      'CRM', 'INTC', 'ARMH', 'CRWD', 'AMD', 'ADBE', '8411.T', '7735.T', '8035.T', '9984.T']
    default_symbols = ['AAPL', 'MSFT', 'GOOGL']

    selected_symbols = st.sidebar.multiselect('銘柄を選択してください', options=symbol_options, default=default_symbols)

    years = st.sidebar.slider('期間(年)', min_value=1, max_value=10, value=3)

    ma_options = [5, 25, 100, 200]
    default_ma = [5, 25, 100, 200]
    ma_selections = st.sidebar.multiselect('移動平均線を選択', options=ma_options, default=default_ma)

    for symbol in selected_symbols:
        df = fetch_data(symbol, years)
        if not df.empty:
            plot_data(df, symbol, ma_selections)
        else:
            st.write(f'{symbol}: データの取得に失敗しました。')


if __name__ == "__main__":
    main()
