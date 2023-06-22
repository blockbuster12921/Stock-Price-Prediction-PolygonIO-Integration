from polygon import RESTClient
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sb

from datetime import date, datetime, timedelta
import time

import joblib
from tensorflow import keras

class RealTimePrediction:

    def __init__(self, apiKey, stockName, params, modelPath, scalerPath):
        # Initialize parameters
        self.apiKey = apiKey
        self.stockName = stockName
        self.params = params
        self.model = keras.models.load_model(modelPath)
        self.scaler = joblib.load(scalerPath)

    def pull_base_data(self, startDate, endDate):
        """
        This function pulls the stock from startDate to endDate
        """
        df = pd.DataFrame(columns=['time stamp', 'open', 'high', 'low', 'close', 'volume'])
        client = RESTClient(auth_key=self.apiKey)
        multiplier = 1
        timespan = "minute"
        bars = client.get_aggs(ticker=self.apiKey, multiplier=1, timespan="minute", \
                            from_=startDate, to=endDate)
        i = 0
        for bar in bars:
            df.loc[i] = [datetime.fromtimestamp(bar.timestamp / 1000), bar.open, bar.high, bar.low, bar.close,\
                        int(bar.volume)]
            i += 1
        return df
    
    def calcAdditionalFeatures(self, df):
        """This function calculates additional parameters"""


    
    def predict(self, df):
        """This function predicts the result automatically"""
        

    def autoUpdate(self):
        """This function updates the result automatically"""
        for i in range(1):
            today = datetime.now().date()
            yesterday = (datetime.today() - timedelta(days=1)).date()
            print(today, yesterday)
            baseDf = self.pull_base_data(yesterday, today)
            print(baseDf.tail(5))

        print("Update Complete")
    
    def visualizeResult(self):
        """This function visualizes the prediction result"""


apiKey = 'kOCHMwXaZkrC5ov6AcLslH4ZwqjP0won'
stockName = 'AMD'
params = ['open', 'high', 'low', 'close', 'volume']
modelPath = './RESULT/03_15_amd/model0.h5'
scalerPath = './SCALERS/scaler.save'
predictor = RealTimePrediction(apiKey=apiKey, stockName=stockName, params=params, \
                               modelPath=modelPath, scalerPath=scalerPath)
predictor.autoUpdate()