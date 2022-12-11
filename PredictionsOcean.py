import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
class Model:
    def __init__(self, path):
        self.df = pd.read_csv(path)
        self.df['rsi_perc'] -= 0.5
        self.df['williams_r_perc'] -= 0.5
        self.df[['macd_diff', 'rsi_perc', 'williams_r_perc', 'close', 'Y']].to_csv("Test/visualizations.csv")
        #print(self.df[['close', 'Y']])
    def linear_with_MACD(self):
        self.df = self.df.dropna(subset = ['macd_diff', 'close', 'Y'])
        X = self.df[['macd_diff', 'close']]  
        Y = self.df[['Y']]
        reg = LinearRegression().fit(X, Y)
        print(reg.coef_, reg.intercept_, reg.score(X, Y))
        self.reg = reg
    def check_stat_sense(self):
        rsi_big_count = 0
        total_big_count = 0
        rsi_low_count = 0
        total_low_count = 0
        for index, row in self.df.iterrows():
            if (self.df['rsi_perc'].iloc[index] > 0.45 and 
                self.df['close'].iloc[index] > self.df['Y'].iloc[index]):
                rsi_big_count += 1
                total_big_count += 1
            elif self.df['rsi_perc'].iloc[index] > 0.45:
                total_big_count += 1
            if (self.df['rsi_perc'].iloc[index] < -0.45 and 
                self.df['close'].iloc[index] < self.df['Y'].iloc[index]):
                rsi_low_count += 1
                total_low_count += 1
            elif self.df['rsi_perc'].iloc[index] < -0.45:
                total_low_count += 1
        print(rsi_big_count / total_big_count)
    def linear_with_rsi_perc(self):
        tempdf = self.df.dropna(subset = ['rsi_perc', 'close', 'Y', 'williams_r_perc'])
        X = tempdf[['close']]
        #X['rsi_perc'] -= 0.5
        #X['williams_r_perc'] -= 0.5
        Y = tempdf[['Y']]
        reg = LinearRegression().fit(X, Y)
        #print(reg.coef_, reg.intercept_, reg.score(X, Y))
        self.reg = reg
    def linear_reg(self):
        tempdf = self.df.dropna(subset = ['close', 'Y'])
        X = tempdf[['close']]
        Y = tempdf[['Y']]
        self.breg = LinearRegression().fit(X, Y)
    def pred(self, val):
        l = [0] * 12
        l[0] = self.reg.predict(val)
        for i in range(1, 12):
            l[i] = self.breg.predict(l[i - 1])
        try:
            open('pred.csv', 'x')
        except:
            pass
        with open('pred.csv', 'w') as file:
            file.write(','.join([str(n) for n in l]))
class Metrics:
    def __init__(self, df):
        self.df = df
        self.df['time'] = pd.to_datetime(self.df['time'])
    def process_time(self):
        for index, row in self.df.iterrows():
            if self.df['time'].iloc[index].hour != 23 and self.df['time'].iloc[index].minute != 30:
                continue
            if index + 13 * 60 > len(self.df['close']):
                break
    def get_stats(self):
        average = 0
        total = 0
        for index, row in self.df.iterrows():
            if self.df['time'].iloc[index].hour != 23 or self.df['time'].iloc[index].minute != 30:
                continue
            if index + 13 * 60 + 30 > len(self.df['close']):
                break
            temp_sum = 0
            for i in range(60 * 1 + 30, 60 * 13 + 30, 60):
                temp_sum += (self.df['close'].iloc[index + i] - self.df['50_ema'].iloc[index]) ** 2
            average += temp_sum
            total += 1
        print(average / total)
    def alternate_stats(self):
        average = 0
        total = 0
        for index, row in self.df.iterrows():
            if self.df['time'].iloc[index].hour != 23 or self.df['time'].iloc[index].minute != 30:
                continue
            if index + 13 * 60 + 30 > len(self.df['close']):
                break
            #print(index)
            temp_sum = 0
            for i in range(60 * 1 + 30, 60 * 13 + 30, 60):
                temp_sum += (self.df['close'].iloc[index + i] - self.df['100_ema'].iloc[index]) ** 2
            average += temp_sum
            total += 1
        print(average / total)
    def stats(self):
        average = 0
        total = 0
        for index, row in self.df.iterrows():
            if self.df['time'].iloc[index].hour != 23 or self.df['time'].iloc[index].minute != 30:
                continue
            if index + 13 * 60 + 1 > len(self.df['close']):
                break
            temp_sum = 0
            if index + 13 * 60 + 1> len(self.df['close']):
                break
            for i in range(60 * 1 + 30, 60 * 13 + 30, 60):
                temp_sum += (self.df['close'].iloc[index + i] - self.df['close'].iloc[index]) ** 2
            average += temp_sum
            total += 1
        print(average / total)
model = Model("ETH_DATA/eth_1_minute_price_techs_time.csv")
model.linear_reg()
model.pred()