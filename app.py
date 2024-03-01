import streamlit as st
import matplotlib.pyplot as plt
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import datetime


# データ取得関数は変更なし
def fetch_data(ticker_symbol, period_years):
    # 以前と同じコード
    my_share = share.Share(ticker_symbol)
    try:
        symbol_data = my_share.get_historical(
            share.PERIOD_TYPE_YEAR,  # 期間タイプを年に変更
            period_years,  # 過去何年分のデータを取得するか
            share.FREQUENCY_TYPE_DAY,  # 日次データを取得
            1  # フリークエンシーの値(この場合は1日ごと)
        )
    except YahooFinanceError as e:
        print(e.message)
        return None
    return symbol_data


# データプロット関数は変更なし
def plot_data(symbol_data, ticker_symbol):
    # 以前と同じコード
    timestamps = symbol_data['timestamp']
    prices = symbol_data['close']
    volumes = symbol_data['volume']

    # 日付情報を使わずにインデックス(整数)を生成
    index = range(len(prices))

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Closing Price', color=color)
    ax1.plot(index, prices, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Volume', color=color)
    ax2.bar(index, volumes, color=color, alpha=0.3)
    ax2.tick_params(axis='y', labelcolor=color)

    # X軸にカスタムの日付ラベルを設定(オプショナル)
    dates = [datetime.datetime.fromtimestamp(ts / 1000).date() for ts in timestamps]
    ax1.set_xticks(index[::len(index) // 10])  # 適宜間隔を調整
    ax1.set_xticklabels([dates[i].strftime('%Y-%m-%d') for i in index[::len(index) // 10]], rotation=45, ha="right")

    # 最終値を注釈
    if prices:
        last_index = index[-1]
        last_price = prices[-1]
        ax1.annotate(f'Close: {last_price}',
                     xy=(last_index, last_price),
                     xytext=(last_index, last_price),
                     arrowprops=dict(facecolor='black', shrink=0.05),
                     horizontalalignment='right', verticalalignment='bottom')

    fig.tight_layout()
    plt.title(f'{ticker_symbol} - Closing Prices and Volumes')
    # plt.show()
    st.pyplot(fig)

# Streamlitアプリのメイン関数
def main():
    st.sidebar.title('設定')
    # サイドバーで銘柄の選択を可能にする
    default_symbols = ['AAPL', 'MSFT', 'GOOGL']
    symbols = st.sidebar.multiselect('銘柄を選択してください',
                                     options=['^DJI', '^IXIC', '^GSPC', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'meta', 'TSLA',
                                              'NVDA', 'PYPL', 'NFLX', 'CRM', 'INTC', 'ARM', 'CRWD', 'amd', 'adbe',
                                              '8411.T', '7735.T', '8035.T', '9984.T'], default=default_symbols)

    # サイドバーで期間の選択を可能にする1
    years = st.sidebar.slider('期間(年)', min_value=1, max_value=10, value=3)

    for symbol in symbols:
        data = fetch_data(symbol, years)
        if data is not None:
            plot_data(data, symbol)
        else:
            st.write(f'{symbol}: データの取得に失敗しました。')


if __name__ == "__main__":
    main()
