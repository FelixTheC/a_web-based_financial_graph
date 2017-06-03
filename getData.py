#! /usr/env/python3
from pandas_datareader import data
import datetime

def getData(name='TSLA', start=datetime.datetime(2017,3,1), end=datetime.datetime.today()):
    df = data.DataReader(name=name, data_source="google", start=start, end=end)
    return df