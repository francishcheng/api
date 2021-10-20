from os import sep
from typing import Optional, List
from judge import judge_youxiao
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, HTMLResponse
from datetime import datetime
import pymongo
from starlette.responses import FileResponse
class Item(BaseModel):
    C_ygz: int
    Ce: int
    points: List[int]

class Data(BaseModel):
    data: List[Item]
app = FastAPI()
client = pymongo.MongoClient('localhost')
db = client['api']
table = db['data']
@app.post("/data/")
async def create_item(data: Data):
    # try:
    ret =   {
        'result': []
    } 
    data = data.data
    print(data)
    for item in data:

        youxiao, reason, reason_s, _ = judge_youxiao(item.points, item.C_ygz, item.Ce) 
        ret['result'].append(dict({
            'if_youxiao': youxiao,
            'reason': reason_s,
            'explain': reason_s
        }))
        query = {
            'time': datetime.now(),
            'points':item.points,
            'Ce':item.Ce,
            'C_ygz':item.C_ygz,
            'if_youxiao':youxiao,
            'reason':reason_s,
            'explain':reason_s
        }
        db_res = table.find_one(query)
        if db_res is None:
            table.update_one(query, {'$set':query}, upsert=True)
    # except Exception:
    #       raise HTTPException(status_code=404, detail="参数错误")
    return JSONResponse(content=ret)


@app.get("/download")
async def read_item():
    with open('data.csv', 'w') as f:
        f.write('time, C_ygz, Ce, explain, if_youxiao, reason, points\n')
        for data in table.find():
            data = dict(data)
            f.write(str(data['time']) + ',')
            f.write(str(data['C_ygz']) + ',')
            f.write(str(data['Ce']) + ',')
            f.write(str(data['explain']) + ',')
            f.write(str(data['if_youxiao']) + ',')
            f.write(str(data['reason']) + ',')
            f.write(','.join( list([str(i) for i in data['points']])))
            f.write('\n')
    file_location = 'data.csv'
    return FileResponse(file_location, media_type='application/octet-stream',filename='data.csv')



@app.get("/")
async def read_item():
    return HTMLResponse(
        '<button "><a href="/download"> download</a> </button>'
    )

