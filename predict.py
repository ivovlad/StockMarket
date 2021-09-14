if __name__ == '__main__':
    import pandas as pd
    from datetime import datetime
    import numpy as np
    
    data = pd.read_csv('sphist.csv')
    data['Date']=pd.to_datetime(data['Date'])
    data = data.sort_values('Date', ascending=True)
    data = data.reset_index(drop=True)
    # data['Avg_365'] = data['Close'].rolling(365,min_periods = 365).mean()
    # data['Avg_30'] = data['Close'].rolling(30,min_periods = 30).mean()
    # data['Stdev_30'] = data['Close'].rolling(30,min_periods = 30).std()
    # data['Stdev_365'] = data['Close'].rolling(365,min_periods = 365).std()
    # data[['Avg_365','Avg_30','Stdev_30', 'Stdev_365']] = data[['Avg_365','Avg_30','Stdev_30', 'Stdev_365']].shift(periods = 1)
    
    def calc_indicator(t, func, col_name, dframe, col_target_name):
        x = dframe.iterrows()
        prices = []
        col = []

        for _ in range(len(dframe)):
            tup = next(x)
            if len(prices)<t:
                prices.append(tup[1][col_target_name])
                col.append(0)
            else:
                col.append(func(prices))
                prices.pop(0)
                prices.append(tup[1][col_target_name])
        dframe[col_name] = col
    calc_indicator(30,np.mean,'Avg_30', data, 'Close')
    calc_indicator(365,np.mean,'Avg_365',data, 'Close')
    calc_indicator(30, np.std, 'Stdev_30',data, 'Close')
    calc_indicator(365, np.std, 'Stdev_365',data, 'Close')
    calc_indicator(30,np.mean, 'Avg_Vol30',data,'Volume')
    calc_indicator(365,np.mean,'Avg_Vol365',data,'Volume')
    data['Ratio_price_30_365'] = data['Avg_30']/data['Avg_365']
    data['Ratio_std_30_365']=data['Stdev_30']/data['Stdev_365']
    data['Ratio_vol_30_365']=data['Avg_Vol30']/data['Avg_Vol365']
                          
    data = data[data['Stdev_365']!=0]
    data = data.dropna(axis=0)
    train = data[data['Date']<datetime(year=2013,month=1,day=1)]
    test = data[data['Date']>=datetime(year=2013,month=1,day=1)]
    
    from sklearn.linear_model import LinearRegression
    labels = ['Avg_30','Avg_365', 'Stdev_30', 'Stdev_365',
             'Avg_Vol30', 'Avg_Vol365', 'Ratio_price_30_365',
             'Ratio_std_30_365', 'Ratio_vol_30_365']
    reg = LinearRegression().fit(train[labels],train['Close'])
    pred = reg.predict(test[labels])
    mae = np.mean(np.abs(test['Close'] - pred))
    print(mae)
    
    