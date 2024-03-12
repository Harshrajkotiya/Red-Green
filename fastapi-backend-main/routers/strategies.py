from fastapi import APIRouter, HTTPException
from utils.helper_func import execute_query,validate_data,check_if_strike_data
import pandas as pd
import numpy as np
from fastapi_cache.decorator import cache


router = APIRouter(
    prefix = "/strats"
)

interval = {"1min":["p2_cont_opt_pe_1_min","p2_cont_opt_ce_1_min"],"3min":["p2_cont_opt_pe_3_min","p2_cont_opt_ce_3_min"],"5min":["p2_cont_opt_pe_5_min","p2_cont_opt_ce_5_min"],"15min":["p2_cont_opt_pe_15_min","p2_cont_opt_ce_15_min"],"30min":["p2_cont_opt_pe_30_min","p2_cont_opt_ce_30_min"],"1hour":["p2_cont_opt_pe_1_hour","p2_cont_opt_ce_1_hour"]}   


@router.get("/straddle_snapshot")
@cache(expire=60)
async def get_straddle_snapshot(symbol:str, expiry:str):
    
    validate_data(None, None, symbol, expiry)

    query_pe = f'''SELECT symbol, strike_price, open, close, expiry, bucket FROM p2_cont_opt_pe_1_day WHERE expiry='{expiry}' AND symbol='{symbol}' AND date(bucket) = (SELECT date(bucket) FROM last_update_time) ORDER BY bucket'''
    query_ce = f'''SELECT symbol, strike_price, open, close, expiry, bucket FROM p2_cont_opt_ce_1_day WHERE expiry='{expiry}' AND symbol='{symbol}' AND date(bucket) = (SELECT date(bucket) FROM last_update_time) ORDER BY bucket'''

    try:
        result_pe = execute_query(query_pe)
        result_ce = execute_query(query_ce)
    except Exception as e :
        print("database Error", e)
    
    df_pe = pd.DataFrame(result_pe, columns=["symbol", "strike", "open", "close", "expiry", "bucket"])
    df_ce = pd.DataFrame(result_ce, columns=["symbol", "strike", "open", "close", "expiry", "bucket"])
    
    df_merged = pd.merge(df_pe, df_ce, how='inner',suffixes=('_pe', '_ce'),  on=['symbol','strike','expiry','bucket'] )

    df_merged["stradle_price"] = df_merged["close_ce"] + df_merged["close_pe"]
    df_merged["session_chng"] = df_merged["stradle_price"] - (df_merged["open_ce"] + df_merged["open_pe"])

    df_merged = df_merged.sort_values('strike', ascending=False)

    modified_data = df_merged.to_dict(orient="records")  
   
    return { "straddle_snapshot": modified_data }

@router.get("/straddle_strangle")
@cache(expire=60)
async def get_straddle_strangle(symbol:str, expiry:str,period:str, strike_price:int | None = None , pe_strike_price:int | None = None, ce_strike_price:int | None = None):
    
    validate_data(None, None, symbol, expiry)

    query_pe = f'''SELECT symbol, strike_price, open, high, low, close, open_interest, expiry, bucket FROM {interval.get(period)[0]} WHERE expiry='{expiry}' AND symbol='{symbol}' AND strike_price = {strike_price if strike_price != None else pe_strike_price} AND date(bucket) = (SELECT date(bucket) FROM last_update_time) ORDER BY bucket'''
    query_ce = f'''SELECT symbol, strike_price, open, high, low, close, open_interest, expiry, bucket FROM {interval.get(period)[1]} WHERE expiry='{expiry}' AND symbol='{symbol}' AND strike_price = {strike_price if strike_price != None else ce_strike_price } AND date(bucket) = (SELECT date(bucket) FROM last_update_time) ORDER BY bucket'''

    try:
        result_pe = execute_query(query_pe)
        result_ce = execute_query(query_ce)
    except Exception as e :
        print("database Error", e)
    
    df_pe = pd.DataFrame(result_pe, columns=["symbol", "strike", "open", "high", "low", "close", "open_interest", "expiry", "bucket"])
    df_ce = pd.DataFrame(result_ce, columns=["symbol", "strike", "open", "high", "low", "close", "open_interest", "expiry", "bucket"])
    
    on_arr = ['symbol','strike','expiry','bucket'] if strike_price != None else ['symbol','expiry','bucket']

    df_merged = pd.merge(df_pe, df_ce, how='inner',suffixes=('_pe', '_ce'),  on=on_arr )

    df_merged["stradle_price"] = df_merged["close_ce"] + df_merged["close_pe"]

    modified_data = df_merged.to_dict(orient="records")  
   
    return { "straddle_chart": modified_data }

@router.get("/straddle_chart_plus")
@cache(expire=60)
async def get_straddle_chart_plus(symbol: str, expiry: str, period: str, strike_list: str = None):
    if strike_list is None:
        return {"message": "Strike list is empty."}
    validate_data(None, None, symbol, expiry)
    
    response = []

    for strike in strike_list.split(","):
        straddle_data = await get_straddle_strangle(symbol, expiry, period, strike)
        response.append(straddle_data)
    
    return {"straddle_chart_plus" : response}

@router.get("/straddle_chart_combo")
@cache(expire=60)
async def get_straddle_chart_combo(symbol:str, expiry:str,period:str,strike_price:str):
    
    validate_data(None, None, symbol, expiry)

    query_pe = f'''SELECT close,strike_price,bucket FROM {interval.get(period)[0]} WHERE expiry='{expiry}' AND symbol='{symbol}' AND strike_price IN ({strike_price }) AND date(bucket) = (SELECT date(bucket) FROM last_update_time) ORDER BY bucket'''
    query_ce = f'''SELECT close,strike_price,bucket FROM {interval.get(period)[1]} WHERE expiry='{expiry}' AND symbol='{symbol}' AND strike_price IN ({strike_price}) AND date(bucket) = (SELECT date(bucket) FROM last_update_time) ORDER BY bucket'''

    strikes  = strike_price.split(",")

    try:
        result_pe = execute_query(query_pe)
        result_ce = execute_query(query_ce)
    except Exception as e :
        print("database Error", e)
 
    df_pe = pd.DataFrame(result_pe,columns=["close","strike","bucket"])
    df_ce = pd.DataFrame(result_ce,columns=["close","strike","bucket"])

    on_arr = ["strike","bucket"]

    df_merged = pd.merge(df_pe, df_ce,suffixes=('_pe', '_ce'),  on=on_arr, how="outer")

    straddle_close_pe = df_merged.groupby("bucket")["close_pe"].sum().fillna(0)
    straddle_close_ce = df_merged.groupby("bucket")["close_ce"].sum().fillna(0)

    df = straddle_close_pe + straddle_close_ce

    df = pd.DataFrame({'bucket': df.index, 'straddle_price': df.values})

    modified_data = df.to_dict(orient="records")
   
    return { "straddle_chart_combo": modified_data }

@router.get("/butterfly_chart")
@cache(expire=60)
async def get_butterfly_chart(type:str,symbol:str, expiry:str,period:str,lot_size:str,strike_price:str):
    
    validate_data(None, None, symbol, expiry)

    if type == "PE" :
        query = f'''SELECT close,strike_price,bucket FROM {interval.get(period)[0]} WHERE expiry='{expiry}' AND symbol='{symbol}' AND strike_price IN ({strike_price}) AND date(bucket) = (SELECT date(bucket) FROM last_update_time) ORDER BY bucket'''
    elif type == "CE" :    
        query = f'''SELECT close,strike_price,bucket FROM {interval.get(period)[1]} WHERE expiry='{expiry}' AND symbol='{symbol}' AND strike_price IN ({strike_price}) AND date(bucket) = (SELECT date(bucket) FROM last_update_time) ORDER BY bucket'''
    else :
        return { "butterfly_data": [], "message": "Please provie proper type" } 

    strikes  = strike_price.split(",")
    lots  = lot_size.split(",")

    try:
        result = execute_query(query)
    except Exception as e :
        print("database Error", e)
 
    df = pd.DataFrame(result,columns=["close","strike","bucket"])
    
    df_strike_1 =  df[df["strike"] == int(strikes[0])]
    df_strike_2 =  df[df["strike"] == int(strikes[1])]
    df_strike_3 =  df[df["strike"] == int(strikes[2])]

    df_strike_1["close"] = df_strike_1["close"] * int(lots[0]) 
    df_strike_2["close"] = df_strike_2["close"] * int(lots[1]) 
    df_strike_3["close"] = df_strike_3["close"] * int(lots[2]) 

    condition = True if len(df_strike_1) == len(df_strike_2) == len(df_strike_3) else False

    if condition :
        df_strike_1["straddle_price"] = df_strike_1["close"].values + df_strike_2["close"].values + df_strike_3["close"].values
    else :
        return { "butterfly_data": [] }

    df_data = df_strike_1[["bucket","straddle_price"]]

    modified_data = df_data.to_dict(orient="records")
   
    return { "butterfly_data": modified_data }

@router.get("/iron_condor_chart")
@cache(expire=60)
async def get_butterfly_chart(symbol:str, expiry:str,period:str,ce_lot_size:str,pe_lot_size:str,ce_strike_price:str,pe_strike_price:str):
    
    validate_data(None, None, symbol, expiry)
    
    query_pe = f'''SELECT close,strike_price,bucket FROM {interval.get(period)[0]} WHERE expiry='{expiry}' AND symbol='{symbol}' AND strike_price IN ({pe_strike_price}) AND date(bucket) = (SELECT date(bucket) FROM last_update_time) ORDER BY bucket'''
    query_ce = f'''SELECT close,strike_price,bucket FROM {interval.get(period)[1]} WHERE expiry='{expiry}' AND symbol='{symbol}' AND strike_price IN ({ce_strike_price}) AND date(bucket) = (SELECT date(bucket) FROM last_update_time) ORDER BY bucket'''

    ce_strikes  = ce_strike_price.split(",")
    ce_lots  = ce_lot_size.split(",")

    pe_strikes  = pe_strike_price.split(",")
    pe_lots  = pe_lot_size.split(",")

    try:
        result_pe = execute_query(query_pe)
        result_ce = execute_query(query_ce)
    except Exception as e :
        print("database Error", e)
 
    df_pe = pd.DataFrame(result_pe,columns=["close","strike","bucket"])
    df_ce = pd.DataFrame(result_ce,columns=["close","strike","bucket"])

    df_pe.loc[df_pe['strike'] == int(pe_strikes[0]), 'close'] *= int(pe_lots[0])
    df_pe.loc[df_pe['strike'] == int(pe_strikes[1]), 'close'] *= int(pe_lots[1])

    df_ce.loc[df_ce['strike'] == int(ce_strikes[0]), 'close'] *= int(ce_lots[0])
    df_ce.loc[df_ce['strike'] == int(ce_strikes[1]), 'close'] *= int(ce_lots[1])
    
    df_merged = pd.merge(df_pe, df_ce, how='outer',suffixes=('_pe', '_ce'),  on=['strike','bucket'])

    df_merged["close_pe"] = df_merged["close_pe"].fillna(0)
    df_merged["close_ce"] = df_merged["close_ce"].fillna(0)

    straddle_close_pe = df_merged.groupby("bucket")["close_pe"].sum().fillna(0)
    straddle_close_ce = df_merged.groupby("bucket")["close_ce"].sum().fillna(0)

    df = straddle_close_pe + straddle_close_ce

    df = pd.DataFrame({'bucket': df.index, 'straddle_price': df.values})

    modified_data = df.to_dict(orient="records")
   
    return { "iron_condor_data": modified_data }

@router.get("/spread_chart")
@cache(expire=60)
async def get_spread_chart(type:str, symbol:str,expiry_dates:str,period:str,lot_size:str,strike_price:str):
    
    validate_data(None, None, symbol, None)
    
    expiries = expiry_dates.split(",")
    
    query = f'''SELECT close,strike_price,expiry,bucket FROM {interval.get(period)[0] if type == "PE" else interval.get(period)[1]} WHERE expiry IN ('{expiries[0]}','{expiries[1]}') AND symbol='{symbol}' AND strike_price IN ({strike_price}) AND date(bucket) = (SELECT date(bucket) FROM last_update_time) ORDER BY bucket'''

    print(query)

    strikes  = strike_price.split(",")
    lots  = lot_size.split(",")

    try:
        result = execute_query(query) 
    except Exception as e :
        print("database Error", e)
 
    df = pd.DataFrame(result,columns=["close","strike","expiry","bucket"])

    df.loc[(df['strike'] == int(strikes[0])) & (df['expiry'] == pd.to_datetime(expiries[0]).date()), 'close'] *= int(lots[0])
    df.loc[(df['strike'] == int(strikes[1])) & (df['expiry'] == pd.to_datetime(expiries[1]).date()), 'close'] *= int(lots[1])

    straddle_close = df.groupby("bucket")["close"].sum().fillna(0)

    df_data = pd.DataFrame({'bucket': straddle_close.index, 'straddle_price': straddle_close.values})

    modified_data = df_data.to_dict(orient="records")
   
    return { "spread_chart_data": modified_data }

@router.get("/double_calendar_chart")
@cache(expire=60)
async def get_double_calendar_chart(symbol:str,expiry_dates:str,period:str,pe_lot_size:str,ce_lot_size:str,pe_strike_price:str,ce_strike_price:str):
    
    validate_data(None, None, symbol, None)

    expiries = expiry_dates.split(",")

    pe_strikes  = pe_strike_price.split(",")
    ce_strikes  = ce_strike_price.split(",")

    pe_lots  = pe_lot_size.split(",")
    ce_lots  = ce_lot_size.split(",")
    
    query_pe = f'''SELECT close,strike_price,expiry,bucket FROM {interval.get(period)[0]} WHERE expiry IN ('{expiries[0]}','{expiries[1]}') AND symbol='{symbol}' AND strike_price IN ({pe_strike_price}) AND date(bucket) = (SELECT date(bucket) FROM last_update_time) ORDER BY bucket'''
    query_ce = f'''SELECT close,strike_price,expiry,bucket FROM {interval.get(period)[1]} WHERE expiry IN ('{expiries[0]}','{expiries[1]}') AND symbol='{symbol}' AND strike_price IN ({ce_strike_price}) AND date(bucket) = (SELECT date(bucket) FROM last_update_time) ORDER BY bucket'''

    try:
        result_pe = execute_query(query_pe) 
        result_ce = execute_query(query_ce) 
    except Exception as e :
        print("database Error", e)
 
    df_pe = pd.DataFrame(result_pe,columns=["close","strike","expiry","bucket"])
    df_ce = pd.DataFrame(result_ce,columns=["close","strike","expiry","bucket"])

    condition_pe_short = (((df_pe['strike'] == int(pe_strikes[0])) & (df_pe['expiry'] == pd.to_datetime(expiries[0]).date())))

    condition_pe_long = (((df_pe['strike'] == int(pe_strikes[1])) & (df_pe['expiry'] == pd.to_datetime(expiries[1]).date())))

    condition_ce_short = (((df_ce['strike'] == int(ce_strikes[0])) & (df_ce['expiry'] == pd.to_datetime(expiries[0]).date()))) 
    
    condition_ce_long = (((df_ce['strike'] == int(ce_strikes[1])) & (df_ce['expiry'] == pd.to_datetime(expiries[1]).date()))) 
    
    df_pe_short = df_pe[condition_pe_short]
    df_pe_long = df_pe[condition_pe_long]
    
    df_ce_short = df_ce[condition_ce_short]
    df_ce_long = df_ce[condition_ce_long]

    df_pe_short.loc[((df_pe_short['strike'] == int(pe_strikes[0])) & (df_pe_short['expiry'] == pd.to_datetime(expiries[0]).date())), 'close'] *= int(pe_lots[0])
    
    df_pe_long.loc[((df_pe_long['strike'] == int(pe_strikes[1])) & (df_pe_long['expiry'] == pd.to_datetime(expiries[1]).date())), 'close'] *= int(pe_lots[1])
    
    df_ce_short.loc[((df_ce_short['strike'] == int(ce_strikes[0])) & (df_ce_short['expiry'] == pd.to_datetime(expiries[0]).date())), 'close'] *= int(ce_lots[0])
    
    df_ce_long.loc[((df_ce_long['strike'] == int(ce_strikes[1])) & (df_ce_long['expiry'] == pd.to_datetime(expiries[1]).date())), 'close'] *= int(ce_lots[1])
    

    combined_df = pd.concat([df_pe_short, df_pe_long, df_ce_short, df_ce_long], ignore_index=True)
    
    straddle_price = combined_df.groupby("bucket")["close"].sum().fillna(0)

    df = pd.DataFrame({'bucket': straddle_price.index, 'straddle_price': straddle_price.values})

    modified_data = df.to_dict(orient="records")
   
    return { "double_calendar_data": modified_data }

    