import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from fastapi.middleware.cors import CORSMiddleware
from routers import future, option, strategies
from utils.helper_func import execute_query

app = FastAPI()

app.include_router(future.router)
app.include_router(option.router)
app.include_router(strategies.router)

# cors verification 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")


    
@app.get("/get_filter_data")
@cache(expire=60)
async def get_filter_data():
    
    fut_query = f'''SELECT symbol,expiry FROM fut_expiry'''

    opt_query = f'''SELECT symbol,expiry,strike_price FROM opt_expiry'''

    try:
        fut_result = execute_query(fut_query)
        opt_result = execute_query(opt_query)

   #query execution
    except Exception as e :
        print("database Error", e)


    fut_data = {item[0]: item[1] for item in fut_result}
    opt_data = {str(item[0]) + "_" + str(item[1]): item[2] for item in opt_result}


    return {"fut_expiry":fut_data,"opt_expiry":opt_data }


@app.get("/get_last_update_time")
@cache(expire=60)
async def get_last_update_time():
    query = f'''SELECT bucket FROM last_update_time'''

    try:
        result = execute_query(query)   #query execution
    except Exception as e :
        print("database Error", e) 

    return {"last_update_time" : result[0]}
    
    # return "Got the connection"

# server Exposure
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)