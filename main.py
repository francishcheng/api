from os import sep
from typing import Optional, List
from judge import judge_youxiao
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
class Item(BaseModel):
    C_ygz: int
    Ce: int
    points: List[int]

class Data(BaseModel):
    data: List[Item]
app = FastAPI()


@app.post("/data/")
async def create_item(data: Data):
    try:
        ret =   {
            'result': []
        } 
        data = data.data
        for item in data:

            # print(item.points, item.C_ygz, item.Ce)
            youxiao, reason, _, _ = judge_youxiao(item.points, item.C_ygz, item.Ce) 
            ret['result'].append(dict({
                'if_youxiao': youxiao,
                'reason': reason.tolist()
            }))
    except Exception:
          raise HTTPException(status_code=404, detail="参数错误")
    return JSONResponse(content=ret)