import streamlit as st
import matplotlib.pyplot as plt
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import datetime
import pandas as pd

def calculate_moving_average(prices, window):
    return prices.rolling(window=window).mean()

def fetch_data(ticker_symbol, period_years):
    my_share = share.Share(ticker_symbol)
    try:
        symbol_data = my_share.get_historical(
            share.PERIOD_TYPE_YEAR,  # 期間タイプを年に変更
            period_years,  # 過去何年分のデータを取得するか
            share.FREQUENCY_TYPE_DAY,  # 日次データを取得
            1  # フリークエンシーの値（この場合は1日ごと）
        )
    except YahooFinanceError as e:
        print(e.message)
        return None
    return symbol_data

def plot_data(symbol_data, ticker_symbol, moving_average_days):
    timestamps = symbol_data['timestamp']
    prices = symbol_data['close']
    volumes = symbol_data['volume']

    df = pd.DataFrame({'Price': prices}, index=pd.to_datetime(timestamps, unit='ms'))
    if moving_average_days > 0:
        df[f'{moving_average_days}-day MA'] = calculate_moving_average(df['Price'], moving_average_days)

    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Closing Price', color=color)
    ax1.plot(df.index, df['Price'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    if moving_average_days > 0:
        ax1.plot(df.index, df[f'{moving_average_days}-day MA'], label=f'{moving_average_days}-day MA')
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
    default_symbols = ['AAPL', 'MSFT', 'GOOGL']
    symbols = st.sidebar.multiselect('銘柄を選択してください', options=['^DJI', '^IXIC', '^GSPC', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'meta', 'TSLA', 'NVDA', 'PYPL', 'NFLX','CRM' ,'INTC','ARM','CRWD','amd','adbe','8411.T','7735.T','8035.T','9984.T'], default=default_symbols)

    years = st.sidebar.slider('期間(年)', min_value=1, max_value=10, value=3)

    # 移動平均線の選択
    moving_average_selection = st.sidebar.selectbox(
        '移動平均線を選択',
        options=[0, 5, 25, 100, 200],
        index=4,  # 200日線をデフォルトに設定
        format_func=lambda x: f'{x}-day MA' if x > 0 else 'None'
    )

    for symbol in symbols:
        data = fetch_data(symbol, years)
        if data is not None:
            plot_data(data, symbol, moving_average_selection)
        else:
            st.write(f'{symbol}: データの取得に失敗しました。')

if __name__ == "__main__":
    main()
