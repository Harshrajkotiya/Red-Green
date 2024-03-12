from fastapi import APIRouter, HTTPException
from utils.helper_func import execute_query,lagging_fun,validate_data
import pandas as pd
import numpy as np
from fastapi_cache.decorator import cache


router = APIRouter(
    prefix = "/opt"
)

@router.get("/oi_breakup")
@cache(expire=60)
async def option_oi_breakup(expiry:str, pe_strike:str, ce_strike:str, symbol:str='NIFTY', period:str='3min' ):
    
    interval = {"3min":["p2_cont_opt_pe_3_min","p2_cont_opt_ce_3_min"],"5min":["p2_cont_opt_pe_5_min","p2_cont_opt_ce_5_min"],"15min":["p2_cont_opt_pe_15_min","p2_cont_opt_ce_15_min"],"30min":["p2_cont_opt_pe_30_min","p2_cont_opt_ce_30_min"],"1hour":["p2_cont_opt_pe_1_hour","p2_cont_opt_ce_1_hour"]}   

    validate_data(interval,period,symbol,expiry)
    

    if interval.get(period):
        query_pe = f'''SELECT symbol, open, high, low, close, volume, open_interest, strike_price, bucket, expiry FROM {interval.get(period)[0]} WHERE expiry='{expiry}' AND symbol='{symbol}' AND strike_price={pe_strike} ORDER BY bucket'''
        query_ce = f'''SELECT symbol, open, high, low, close, volume, open_interest, strike_price, bucket, expiry FROM {interval.get(period)[1]} WHERE expiry='{expiry}' AND symbol='{symbol}' AND strike_price={ce_strike} ORDER BY bucket'''

    else:
        return {"error": "Parameter is not passing properly."}
    
    try:
        result_pe = execute_query(query_pe)
        result_ce = execute_query(query_ce)
    except Exception as e :
        print("database Error", e)
    

    df_pe = pd.DataFrame(result_pe, columns=[ "symbol", "open", "high", "low", "close", "volume", "open_interest", "strike", "bucket", "expiry"])
    df_ce = pd.DataFrame(result_ce, columns=[ "symbol", "open", "high", "low", "close", "volume", "open_interest", "strike", "bucket", "expiry"])

    df_pe  = lagging_fun("opt", df_pe)
    df_ce  = lagging_fun("opt", df_ce)

    df_pe = df_pe[df_pe['bucket'].dt.date==df_pe['bucket'].dt.date.max()]
    df_ce = df_ce[df_ce['bucket'].dt.date==df_ce['bucket'].dt.date.max()]
    
    df_merged = pd.merge(df_pe, df_ce, how='inner',suffixes=('_pe', '_ce'),  on=['bucket'] )
    
    df_merged['pcr'] = (df_merged['open_interest_pe']/df_merged['open_interest_ce']).fillna(0).replace(np.inf, 0)
    df_merged['total_oi'] = df_merged['open_interest_pe']+df_merged['open_interest_ce']
    df_merged['total_price'] = df_merged['close_pe']+df_merged['close_ce']
    
    df_merged.sort_values('bucket',ascending=False)

    modified_data = df_merged.to_dict(orient="records")
    
    modified_data.reverse()
    
    return { 'data':modified_data }


@router.get("/get_option_chain")
@cache(expire=60)
async def get_option_chain(expiry:str, symbol:str='NIFTY' ):
    
    validate_data(None,None,symbol,expiry)
   
    query_pe = f'''SELECT symbol, close, volume, open_interest, strike_price, bucket, expiry FROM p2_cont_opt_pe_1_day WHERE expiry='{expiry}' AND symbol='{symbol}' ORDER BY bucket'''
    query_ce = f'''SELECT symbol, close, volume, open_interest, strike_price, bucket, expiry FROM p2_cont_opt_ce_1_day WHERE expiry='{expiry}' AND symbol='{symbol}' ORDER BY bucket'''
   
    try:
        result_pe = execute_query(query_pe)
        result_ce = execute_query(query_ce)
   #query execution
    except Exception as e :
        print("database Error", e)
    
    df_pe = pd.DataFrame(result_pe, columns=[ "symbol", "close", "volume", "open_interest", "strike", "bucket", "expiry"])
    df_ce = pd.DataFrame(result_ce, columns=[ "symbol", "close", "volume", "open_interest", "strike", "bucket", "expiry"])

    df_pe  = lagging_fun("opt", df_pe)
    df_ce  = lagging_fun("opt", df_ce)

    df_pe = df_pe[df_pe['bucket'].dt.date==df_pe['bucket'].dt.date.max()]
    df_ce = df_ce[df_ce['bucket'].dt.date==df_ce['bucket'].dt.date.max()]
    
    df_merged = pd.merge(df_pe, df_ce, how='inner',suffixes=('_pe', '_ce'),  on=['strike'] )

    modified_data = df_merged.to_dict(orient="records")
    
    return { "options_chain": modified_data }


@router.get("/get_ohl_scanners")
@cache(expire=60)
async def get_ohl_scanner(expiry:str, symbol:str='NIFTY' ):
    
    validate_data(None,None,symbol,expiry)

    query_pe = f'''SELECT symbol, open, high, low, close, volume, open_interest, strike_price, bucket, expiry FROM p2_cont_opt_pe_1_day WHERE expiry='{expiry}' AND symbol='{symbol}' AND (open = high OR open = low) ORDER BY bucket'''
    query_ce = f'''SELECT symbol, open, high, low, close, volume, open_interest, strike_price, bucket, expiry FROM p2_cont_opt_ce_1_day WHERE expiry='{expiry}' AND symbol='{symbol}' AND (open = high OR open = low) ORDER BY bucket'''
   
    try:
        result_pe = execute_query(query_pe)
        result_ce = execute_query(query_ce)
   #query execution
    except Exception as e :
        print("database Error", e)
    
    df_pe = pd.DataFrame(result_pe, columns=[ "symbol","open", "high", "low", "close", "volume", "open_interest", "strike", "bucket", "expiry"])
    df_ce = pd.DataFrame(result_ce, columns=[ "symbol","open", "high", "low", "close", "volume", "open_interest", "strike", "bucket", "expiry"])

    df_pe  = lagging_fun("opt", df_pe)
    df_ce  = lagging_fun("opt", df_ce)

    
    df_pe = df_pe[df_pe['bucket'].dt.date==df_pe['bucket'].dt.date.max()]
    df_pe_oh = df_pe[df_pe['open'] == df_pe['high']]
    df_pe_ol = df_pe[df_pe['open'] == df_pe['low']]

    
    df_ce = df_ce[df_ce['bucket'].dt.date==df_ce['bucket'].dt.date.max()]
    df_ce_oh = df_ce[df_ce['open'] == df_ce['high']]
    df_ce_ol = df_ce[df_ce['open'] == df_ce['low']]
    

    modified_data_pe_oh = df_pe_oh.to_dict(orient="records")
    modified_data_pe_ol = df_pe_ol.to_dict(orient="records")
    modified_data_ce_oh = df_ce_oh.to_dict(orient="records")
    modified_data_ce_ol = df_ce_ol.to_dict(orient="records")
    
    return { "pe_oh": modified_data_pe_oh, "pe_ol": modified_data_pe_ol, "ce_oh": modified_data_ce_oh, "ce_ol":modified_data_ce_ol }


@router.get("/pe_ce_diff")
@cache(expire=60)
async def pe_ce_diff(period:str, expiry:str, strike:str, symbol:str):
    interval = {"3min":["p2_cont_opt_pe_3_min","p2_cont_opt_ce_3_min"],"5min":["p2_cont_opt_pe_5_min","p2_cont_opt_ce_5_min"],"15min":["p2_cont_opt_pe_15_min","p2_cont_opt_ce_15_min"],"30min":["p2_cont_opt_pe_30_min","p2_cont_opt_ce_30_min"],"1hour":["p2_cont_opt_pe_1_hour","p2_cont_opt_ce_1_hour"]}
    
    validate_data(interval, period, symbol, expiry)

    if interval.get(period):
        query_pe = f'''SELECT symbol, open_interest, strike_price, bucket, expiry FROM {interval.get(period)[0]} WHERE expiry='{expiry}' AND symbol='{symbol}' AND strike_price={strike} ORDER BY bucket'''
        query_ce = f'''SELECT symbol, open_interest, strike_price, bucket, expiry FROM {interval.get(period)[1]} WHERE expiry='{expiry}' AND symbol='{symbol}' AND strike_price={strike} ORDER BY bucket'''

    else:
        return {"error": "Parameter is not passing properly."}

    try:
        result_pe = execute_query(query_pe)
        result_ce = execute_query(query_ce)
   #query execution
    except Exception as e :
        print("database Error", e)
    
    df_pe = pd.DataFrame(result_pe, columns=[ "symbol", "open_interest", "strike", "bucket", "expiry"])
    df_ce = pd.DataFrame(result_ce, columns=[ "symbol", "open_interest", "strike", "bucket", "expiry"])
    

    group_oi = df_pe['open_interest']
    df_pe['pe_oi_chng'] = group_oi.diff().fillna(0)
    # df_pe['oi_chng_per'] = (group_oi.pct_change().fillna(0).replace(np.inf, 0))*100

    group_oi = df_ce['open_interest']
    df_ce['ce_oi_chng'] = group_oi.diff().fillna(0)
    # df_ce['oi_chng_per'] = (group_oi.pct_change().fillna(0).replace(np.inf, 0))*100


    df_pe = df_pe[df_pe['bucket'].dt.date==df_pe['bucket'].dt.date.max()].replace(np.inf, 0)
    df_ce = df_ce[df_ce['bucket'].dt.date==df_ce['bucket'].dt.date.max()].replace(np.inf, 0)
    

    df_merged = pd.merge(df_pe, df_ce, how='inner',suffixes=('_pe', '_ce'),  on=['bucket'] )

    df_merged["pcr"] = (df_merged['open_interest_pe']/df_merged['open_interest_ce'].replace(0, np.nan)).fillna('-')         

    df_merged['pe_ce_diff'] = df_merged['open_interest_pe']-df_merged['open_interest_ce']

    df_merged['diff_pe_ce_per'] = (((df_merged['open_interest_pe']-df_merged['open_interest_ce'])/(df_merged['open_interest_pe']+df_merged['open_interest_ce']))*100).fillna('-')

    modified_data = df_merged.to_dict(orient="records") 
    
    modified_data.reverse() 
   
    return { "pe_ce_diff": modified_data }



@router.get("/get_oi_stats")
@cache(expire=60)
async def get_oi_stats(symbol:str, expiry:str):
    
    validate_data(None, None, symbol, expiry)

    query_pe = f'''SELECT strike_price,open_interest FROM p2_cont_opt_pe_1_day WHERE symbol='{symbol}' AND expiry='{expiry}' AND date(bucket) = (SELECT date(bucket) FROM last_update_time) ORDER BY strike_price'''
    query_ce = f'''SELECT strike_price,open_interest FROM p2_cont_opt_ce_1_day WHERE symbol='{symbol}' AND expiry='{expiry}' AND date(bucket) = (SELECT date(bucket) FROM last_update_time) ORDER BY strike_price'''


    try:
        result_pe = execute_query(query_pe)
        result_ce = execute_query(query_ce)
    except Exception as e :
        print("database Error", e)
    
    df_pe = pd.DataFrame(result_pe, columns=["strike", "open_interest"])
    df_ce = pd.DataFrame(result_ce, columns=["strike", "open_interest"])
    
    df_merged = pd.merge(df_pe, df_ce, how='outer',suffixes=('_pe', '_ce'),  on=['strike'] )
    
    df_merged["strike"] = df_merged["strike"].fillna(0)
    df_merged["open_interest_ce"] = df_merged["open_interest_ce"].fillna(0)
    df_merged["open_interest_pe"] = df_merged["open_interest_pe"].fillna(0)

    modified_data = df_merged.to_dict(orient="records") 
   
    return { "oi_stats": modified_data,
             "total_ce_oi" :  df_merged["open_interest_ce"].values.sum(),
             "total_pe_oi" :  df_merged["open_interest_pe"].values.sum()
           }

@router.get("/get_oi_chng")
@cache(expire=60)
async def get_oi_chng(symbol:str, expiry:str):
    
    validate_data(None, None, symbol, expiry)

    query_pe = f'''SELECT strike_price,open_interest,bucket FROM p2_cont_opt_pe_1_day WHERE symbol='{symbol}' AND expiry='{expiry}' ORDER BY bucket'''
    query_ce = f'''SELECT strike_price,open_interest,bucket FROM p2_cont_opt_ce_1_day WHERE symbol='{symbol}' AND expiry='{expiry}' ORDER BY bucket'''

    try:
        result_pe = execute_query(query_pe)
        result_ce = execute_query(query_ce)
    except Exception as e :
        print("database Error", e)
    
    df_pe = pd.DataFrame(result_pe, columns=["strike", "open_interest","bucket"])
    df_ce = pd.DataFrame(result_ce, columns=["strike", "open_interest","bucket"])

    group_ce_oi = df_ce.groupby(['strike'])['open_interest']
    group_pe_oi = df_pe.groupby(['strike'])['open_interest']

    df_ce['oi_chng'] = group_ce_oi.diff()
    df_pe['oi_chng'] = group_pe_oi.diff()
    
    df_pe = df_pe[df_pe['bucket'].dt.date==df_pe['bucket'].dt.date.max()]
    df_ce = df_ce[df_ce['bucket'].dt.date==df_ce['bucket'].dt.date.max()]

    df_merged = pd.merge(df_pe, df_ce, how='outer',suffixes=('_pe', '_ce'),  on=['strike','bucket'] )
    
    df_merged["strike"] = df_merged["strike"].fillna(0)

    df_merged['pcr'] = (df_merged['open_interest_pe'].fillna(0).astype("int")/df_merged['open_interest_ce'].fillna(0).astype("int")).replace(np.inf, 0)

    df_merged["oi_chng_ce"] = df_merged["oi_chng_ce"].fillna(0)
    df_merged["oi_chng_pe"] = df_merged["oi_chng_pe"].fillna(0)
    df_merged["open_interest_ce"] = df_merged["open_interest_ce"].fillna(0)
    df_merged["open_interest_pe"] = df_merged["open_interest_pe"].fillna(0)

    modified_data = df_merged.sort_values("strike",ascending=True).to_dict(orient="records") 
   
    return { "oi_chng": modified_data,
             "total_ce_oi_chng" :  df_merged["oi_chng_ce"].values.sum(),
             "total_pe_oi_chng" :  df_merged["oi_chng_pe"].values.sum()
           }

@router.get("/get_expiries")
@cache(expire=60)
async def get_expiries(symbol : str):

    validate_data(None,None,symbol,None)

    if symbol:
        query = f'''SELECT DISTINCT ON (expiry) expiry FROM opt_expiry WHERE symbol='{symbol}' '''
    
    try:
        result = execute_query(query)
   #query execution
    except Exception as e :
        print("database Error", e)
    

    expiry_list = [row[0].strftime('%Y-%m-%d') for row in result]

    return {"expiry": expiry_list}
  
    
@router.get("/get_strike_price")
@cache(expire=60)
async def get_strike_price(symbol : str,expiry : str):

    validate_data(None,None,symbol,expiry)

    
    query = f'''SELECT strike_price FROM opt_expiry WHERE symbol = '{symbol}' AND expiry = '{expiry}' '''

    try:
        result = execute_query(query)
    except Exception as e :
        print("database Error", e)

    return result[0][0]


@router.get("/get_filter_data")
@cache(expire=1800)
async def get_filter_data():
    
    query = f'''SELECT symbol,expiry,strike_price FROM opt_expiry'''
   
    try:
        result = execute_query(query)
   #query execution
    except Exception as e :
        print("database Error", e)

    filter_data = {str(item[0]) + "_" + str(item[1]): item[2] for item in result}

    return {"filter_data":filter_data}


@router.get("/get_multi_strike_oi")
@cache(expire=60)
async def get_multi_strike_oi(symbol:str, period:str, expiry:str, pe_strike_list:str | None="0000",ce_strike_list:str | None="0000"):
    
    validate_data(None, None, symbol, expiry)

    interval = {"1min":["p2_cont_opt_pe_1_min","p2_cont_opt_ce_1_min"],"3min":["p2_cont_opt_pe_3_min","p2_cont_opt_ce_3_min"],"5min":["p2_cont_opt_pe_5_min","p2_cont_opt_ce_5_min"],"15min":["p2_cont_opt_pe_15_min","p2_cont_opt_ce_15_min"],"30min":["p2_cont_opt_pe_30_min","p2_cont_opt_ce_30_min"],"1hour":["p2_cont_opt_pe_1_hour","p2_cont_opt_ce_1_hour"]}

    query_pe = f'''SELECT open_interest, strike_price, bucket FROM {interval.get(period)[0]} WHERE expiry='{expiry}' AND symbol='{symbol}' AND strike_price IN ({pe_strike_list}) AND date(bucket) = (SELECT date(bucket) FROM last_update_time) ORDER BY bucket'''
   
    query_ce = f'''SELECT open_interest, strike_price, bucket FROM {interval.get(period)[1]} WHERE expiry='{expiry}' AND symbol='{symbol}' AND strike_price IN ({ce_strike_list}) AND date(bucket) = (SELECT date(bucket) FROM last_update_time) ORDER BY bucket'''

    try:
        result_pe = execute_query(query_pe)
        result_ce = execute_query(query_ce)
    except Exception as e :
        print("database Error", e)

    df_pe = pd.DataFrame(result_pe, columns=["open_interest", "strike", "bucket"])
    df_ce = pd.DataFrame(result_ce, columns=["open_interest", "strike", "bucket"])

    group_by = ['strike']
    
    df_pe['open_interest'] = df_pe['open_interest'].astype('float')
    group_oi = df_pe.groupby(group_by)['open_interest']
    df_pe['oi_chng'] = group_oi.diff().fillna(0)

    df_ce['open_interest'] = df_ce['open_interest'].astype('float')
    group_oi = df_ce.groupby(group_by)['open_interest']
    df_ce['oi_chng'] = group_oi.diff().fillna(0)

    passing = {}
    # passing['pe_'] = {}
    # passing['ce'] = {}
    bucket_list = []
    if pe_strike_list != "0000":    
        for strike in pe_strike_list.split(","):
            passing[strike+ ' PE'] = df_pe[df_pe['strike'] == int(strike)].to_dict(orient="records")
            if len(passing[strike+ ' PE'])>0 and len(bucket_list)==0:    
                bucket_list = df_pe[df_pe['strike'] == int(strike)]['bucket'].to_list()

    if ce_strike_list != "0000":     
        for strike in ce_strike_list.split(","):
            passing[strike+ ' CE'] = df_ce[df_ce['strike'] == int(strike)].to_dict(orient="records")
            if len(passing[strike+ ' CE'])>0 and len(bucket_list)==0:    
                bucket_list = df_ce[df_ce['strike'] == int(strike)]['bucket'].to_list()

    return {"multi_strike_oi":passing , "bucket": bucket_list}

    
    
    




