from fastapi import APIRouter
from utils.helper_func import lagging_fun,execute_query,is_valid_date,validate_data
import pandas as pd
from fastapi_cache.decorator import cache
import datetime
import numpy as np

router = APIRouter(prefix = "/fut")

@router.get("/get_by_expiry")
@cache(expire=60)
async def get_by_expiry(expiry:str):

    validate_data(None,None,None,expiry)

    query = f'''SELECT 
                    bucket, symbol, open, high, low, close, volume, open_interest, expiry 
            FROM p2_fut_1_day WHERE expiry='{expiry}' ORDER BY bucket'''
    try:
        result = execute_query(query)   #query execution
    except Exception as e :
        print("database Error", e)


    df = pd.DataFrame(result, columns=[ "bucket", "symbol", "open", "high", "low", "close", "volume", "open_interest", "expiry"])  # data frame formation of result data

    df = lagging_fun("fut", df)

    modified_data = df[df['bucket'].dt.date==df['bucket'].dt.date.max()].to_dict(orient="records")
    
    return modified_data


@router.get("/get_by_perd_symb_exp")
@cache(expire=60)
async def get_by_perd_symb_exp(period: str, symbol: str , expiry: str):

    interval = {"3min":"p2_cont_fut_3_min","5min":"p2_cont_fut_5_min","15min":"p2_cont_fut_15_min","30min":"p2_cont_fut_30_min","1hour":"p2_cont_fut_1_hour","1day": "cont_fut_1_day"}
    
    validate_data(interval,period,symbol,expiry)

    query = f'''SELECT 
                    bucket, symbol, open, high, low, close, volume, open_interest, expiry 
            FROM {interval.get(period)} WHERE symbol = '{symbol}' AND expiry ='{expiry}' ORDER BY bucket'''
    
    try:
        result = execute_query(query)
    except Exception as e :
        print("database Error", e)

    df = pd.DataFrame(result, columns=[ "bucket", "symbol", "open", "high", "low", "close", "volume", "open_interest", "expiry"])  # data frame formation of result data

    df = lagging_fun("fut", df)

    if period != "1day" :
        df = df[df['bucket'].dt.date==df['bucket'].dt.date.max()]

    df.sort_values('bucket',ascending=False)

    modified_data = df.to_dict(orient="records")

    modified_data.reverse()
    
    return modified_data


@router.get("/get_ohl_scanner")
@cache(expire=60)
async def get_ohl_scanner(expiry:str):
    
    validate_data(None,None,None,expiry)

    query = f'''SELECT 
                    bucket, symbol, open, high, low, close, volume, open_interest, expiry 
            FROM p2_fut_1_day WHERE expiry='{expiry}' AND (open = high OR open = low) ORDER BY bucket'''
   
    try:
        result_pe = execute_query(query)
   #query execution
    except Exception as e :
        print("database Error", e)
    
    df = pd.DataFrame(result_pe, columns=[ "bucket", "symbol", "open", "high", "low", "close", "volume", "open_interest", "expiry"])

    df  = lagging_fun("fut", df)

    
    df = df[df['bucket'].dt.date==df['bucket'].dt.date.max()]
    df_oh = df[df['open'] == df['high']]
    df_ol = df[df['open'] == df['low']]

    modified_data_oh = df_oh.to_dict(orient="records")
    modified_data_ol = df_ol.to_dict(orient="records")
    
    return { "open_high": modified_data_oh, "open_low": modified_data_ol}

@router.get("/get_oi_scan")
@cache(expire=60)
async def get_oi_scan(expiry: str, symbol:str | None=None):
    
    validate_data(None,None,None,expiry)

    # modified_data = []
    if symbol == None:  
        query = f'''SELECT 
                            bucket, symbol, expiry, price_1_day, open_interest_1_day, price_15_min, open_interest_15_min,price_30_min, open_interest_30_min,price_1_hour, open_interest_1_hour   
                        FROM fut_oi_scan WHERE expiry ='{expiry}' ORDER BY bucket'''
    else:
        query = f'''SELECT 
                                    bucket, symbol, expiry, price_1_day, open_interest_1_day, price_15_min, open_interest_15_min,price_30_min, open_interest_30_min,price_1_hour, open_interest_1_hour   
                                FROM fut_oi_scan WHERE expiry ='{expiry}' AND symbol='{symbol}' ORDER BY bucket'''


    try:
        result = execute_query(query)   #query execution
    except Exception as e :
        print("database Error", e)

    view = pd.DataFrame(result, columns=["bucket", "symbol", "expiry", "price_1_day", "open_interest_1_day", "price_15_min", "open_interest_15_min", "price_30_min", "open_interest_30_min", "price_1_hour", "open_interest_1_hour"])  # data frame formation of result data

    # view = lagging_fun("fut_oi_scan", view)
    group_close_1day = view.groupby(['symbol','expiry'])['price_1_day']
    group_oi_1day = view.groupby( ['symbol','expiry'])['open_interest_1_day']
    group_close_15min = view.groupby(['symbol','expiry'])['price_15_min']
    group_oi_15min = view.groupby( ['symbol','expiry'])['open_interest_15_min']
    group_close_30min = view.groupby(['symbol','expiry'])['price_30_min']
    group_oi_30min = view.groupby( ['symbol','expiry'])['open_interest_30_min']
    group_close_1hour = view.groupby(['symbol','expiry'])['price_1_hour']
    group_oi_1hour = view.groupby( ['symbol','expiry'])['open_interest_1_hour']
    

    view['price_chng_1_day'] = group_close_1day.diff().fillna(0)
    view['price_chng_per_1_day'] = (group_close_1day.pct_change(fill_method='ffill').fillna(0).replace(np.inf, 0))*100

    view['oi_chng_1_day'] = group_oi_1day.diff().fillna(0)
    view['oi_chng_per_1_day'] = (group_oi_1day.pct_change(fill_method='ffill').fillna(0).replace(np.inf, 0))*100
    
    view['price_chng_15_min'] = group_close_15min.diff().fillna(0)
    view['price_chng_per_15_min'] = (group_close_15min.pct_change(fill_method='ffill').fillna(0).replace(np.inf, 0))*100

    view['oi_chng_15_min'] = group_oi_15min.diff().fillna(0)
    view['oi_chng_per_15_min'] = (group_oi_15min.pct_change(fill_method='ffill').fillna(0).replace(np.inf, 0))*100
    
    view['price_chng_30_min'] = group_close_30min.diff().fillna(0)
    view['price_chng_per_30_min'] = (group_close_30min.pct_change(fill_method='ffill').fillna(0).replace(np.inf, 0))*100

    view['oi_chng_30_min'] = group_oi_30min.diff().fillna(0)
    view['oi_chng_per_30_min'] = (group_oi_30min.pct_change(fill_method='ffill').fillna(0).replace(np.inf, 0))*100
    
    view['price_chng_1_hour'] = group_close_1hour.diff().fillna(0)
    view['price_chng_per_1_hour'] = (group_close_1hour.pct_change(fill_method='ffill').fillna(0).replace(np.inf, 0))*100

    view['oi_chng_1_hour'] = group_oi_1hour.diff().fillna(0)
    view['oi_chng_per_1_hour'] = (group_oi_1hour.pct_change(fill_method='ffill').fillna(0).replace(np.inf, 0))*100
    
    modified_data = view[view['bucket'].dt.date==view['bucket'].dt.date.max()].to_dict(orient="records")
    
    return modified_data

@router.get("/get_expiries")
@cache(expire=60)
async def get_expiries():
    
    query = f'''SELECT expiry FROM fut_expiry WHERE symbol = 'NIFTY';'''

    try:
        result = execute_query(query)
    except Exception as e :
        print("database Error", e)

    return {"expiries": result[0][0]}

    
@router.get("/get_filter_data")
@cache(expire=60)
async def get_filter_data():
    
    query = f'''SELECT symbol,expiry FROM fut_expiry'''
   
    try:
        result = execute_query(query)
   #query execution
    except Exception as e :
        print("database Error", e)

    filter_data = {item[0]: item[1] for item in result}

    return {"filter_data":filter_data}



 
@router.get("/get_rollover")
async def get_rollover():
    query = f'''SELECT symbol, oi_array, sum FROM public.rollover_data'''
   
    try:
        result = execute_query(query)
   #query execution
    except Exception as e :
        print("database Error", e)

    key_value_pairs = []

    for item in result:
        key_value_pairs.append({
            "symbol":item[0], 
            "rollover" :  (sum(item[1][:-1])/item[2])*100
        })

    return {"rollover": key_value_pairs}

