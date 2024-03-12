import psycopg2
from config.database import get_db_connection
from datetime import datetime
from fastapi import HTTPException
import numpy as np


def execute_query(query) :
     
     conn = get_db_connection()

     with conn.cursor() as cur :
        try:
            cur.execute(query)
            results = cur.fetchall()
            conn.close()
            return results
        except psycopg2.Error as e:
            print("Unable to Select Data : ")
            print(e)
            conn.rollback()
            exit(1)
        finally :
            conn.close()


def lagging_fun(type, df):
    try:
        if type=="fut" or type =="fut_oi_scan":
            group_by = ['symbol','expiry']
        elif type=="opt":  
            group_by = ['symbol','expiry', 'strike']

        df['open_interest'] = df['open_interest'].astype('float')
        df['close'] = df['close'].astype('float')
            
        group_close = df.groupby(group_by)['close']
        group_oi = df.groupby(group_by)['open_interest']
        

        df['price_chng'] = group_close.diff().fillna(0)
        df['price_chng_per'] = (group_close.pct_change(fill_method='ffill').fillna(0).replace(np.inf, 0))*100

        df['oi_chng'] = group_oi.diff().fillna(0)
        df['oi_chng_per'] = (group_oi.pct_change(fill_method='ffill').fillna(0).replace(np.inf, 0))*100

        if not type =="fut_oi_scan":
            df['volume'] = df['volume'].astype('float')
            group_volume = df.groupby(group_by)['volume']
            df['volume_chng'] = group_volume.diff().fillna(0)
            df['volume_chng_per'] = (group_volume.pct_change(fill_method='ffill').fillna(0).replace(np.inf, 0))*100

        return df

    except Exception as e:
        print("dataframe is not proper ", e)


def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except Exception:
        return False


def validate_data(interval, period, symbol, expiry):

    is_error = False
    details = []

    if period is not None and interval is not None and not interval.get(period):
        is_error = True
        details.append("period")

    if symbol is not None and len(symbol) == 0:
        is_error = True
        details.append("symbol")

    if expiry is not None and not is_valid_date(expiry):
        is_error = True
        details.append("expiry")
    
    if is_error :
        raise HTTPException(status_code=400, detail=f"Please provide a proper {','.join(str(x) for x in details)} for futures")


def check_if_strike_data(result_pe_1,result_ce_1,strikes) :

    flag_pe = False
    flag_ce = False
    flag = True

    for strike in strikes :
        if not flag_pe and not flag_ce :
            for list_pe in result_pe_1 :
                if list_pe[1] == int(strike) :
                    flag_pe = True
                    break
            for list_ce in result_ce_1 :
                if list_ce[1] == int(strike) :
                    flag_ce = True
                    break
        if (not flag_pe or not flag_ce) :
            flag = False 
            break
        if flag_pe and flag_ce :
            flag_pe = False
            flag_ce = False

    return flag