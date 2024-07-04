from typing import List
from fastapi import FastAPI, HTTPException
from app.database import get_database
from bson import ObjectId
import httpx

app = FastAPI()

# Get the MongoDB collection
db = get_database()
collection = db['student_details']

def convert_to_dict(document):
    document['_id'] = str(document['_id'])
    return document

@app.get("/student_details")
async def get_data():
    cursor = collection.find({})
    results = []
    async for document in cursor:
        results.append(convert_to_dict(document))
    return {"data": results}


@app.post("/addstudent")
async def add_studentData(student_name: str,student_id: int,last_name: str,maths:int,english: int,tamil: int):
    try:
        result = await collection.insert_one({
            "student_name": student_name,
            "student_id": student_id,
            "last_name": last_name,
            "maths": maths,
            "english": english,
            "tamil": tamil
        })
        return {"message": "Student added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/get-countries-from-bonds")
async def get_countries_from_bonds():
    url = "https://shibuimarkets.com/api/Common/GetCountriesFromBonds"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()

        return data

    except httpx.HTTPStatusError as http_exc:
        raise HTTPException(status_code=http_exc.response.status_code, detail=str(http_exc))
    except httpx.RequestError as req_exc:
        raise HTTPException(status_code=500, detail=f"Request error: {str(req_exc)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
