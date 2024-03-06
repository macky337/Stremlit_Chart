import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError


def calculate_moving_average(prices, window):
    return prices.rolling(window=window).mean()

def fetch_data(ticker_symbol, period_years):
    my_share = share.Share(ticker_symbol)
    try:
        symbol_data = my_share.get_historical(
            share.PERIOD_TYPE_YEAR,
            period_years,
            share.FREQUENCY_TYPE_DAY,
            1
        )
    except YahooFinanceError as e:
        st.error(f"データの取得中にエラーが発生しました: {e.message}")
        return None
    return symbol_data

def plot_data(symbol_data, ticker_symbol, ma_selections):
    timestamps = symbol_data['timestamp']
    prices = symbol_data['close']
    volumes = symbol_data['volume']

    df = pd.DataFrame({'Price': prices}, index=pd.to_datetime(timestamps, unit='ms'))

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Closing Price', color=color)
    ax1.plot(df.index, df['Price'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # 移動平均線の描画
    for ma in ma_selections:
        df[f'{ma}D MA'] = calculate_moving_average(df['Price'], ma)
        ax1.plot(df.index, df[f'{ma}D MA'], label=f'{ma}D MA')

    ax1.legend()

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Volume', color=color)
    ax2.bar(df.index, volumes, color=color, alpha=0.3)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.title(f'{ticker_symbol} - Closing Prices and Volumes')
    st.pyplot(fig)

def main():
    st.sidebar.title('設定')
    symbol_options = ['^DJI', '^IXIC', '^GSPC', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'meta', 'TSLA',
                      'NVDA', 'PYPL', 'NFLX', 'CRM', 'INTC', 'ARM', 'CRWD', 'amd', 'adbe',
                      '8411.T', '7735.T', '8035.T', '9984.T']
    default_symbols = ['AAPL', 'MSFT', 'GOOGL']

    if st.sidebar.button('登録銘柄を全部選択'):
        selected_symbols = symbol_options
    else:
        selected_symbols = default_symbols

    symbols = st.sidebar.multiselect('銘柄を選択してください',
                                     options=symbol_options,
                                     default=selected_symbols)

    years = st.sidebar.slider('期間(年)', min_value=1, max_value=10, value=3)

    ma_options = [5, 25, 100, 200]
    default_ma = [5, 25, 200]
    ma_selections = st.sidebar.multiselect('移動平均線を選択',
                                           options=ma_options,
                                           default=default_ma)

    for symbol in symbols:
        data = fetch_data(symbol, years)
        if data is not None:
            plot_data(data, symbol, ma_selections)
        else:
            st.write(f'{symbol}: データの取得に失敗しました。')

if __name__ == "__main__":
    main()
