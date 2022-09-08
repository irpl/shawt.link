import os
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, HttpUrl, stricturl, Field
from datetime import datetime
from dotenv import load_dotenv
import shortuuid
import motor.motor_asyncio
from bson import ObjectId

load_dotenv()

app = FastAPI()

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.shawt

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="template")

def generate_link_id():
    return shortuuid.ShortUUID().random(length=6)

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class TallLink(BaseModel):
    url: HttpUrl

class ShawtLink(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    link_id: str = Field(default_factory=generate_link_id)
    url: HttpUrl
    visits: int = 0
    expiry: int = 7
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/test")
def test():
    return shawt_links

@app.get("/{link_id}")
async def get_link_id(link_id: str, response_class=RedirectResponse):
    if (shawt_link := await db["shawt_links"].find_one({"link_id": link_id})) is not None:
        update_shawt_link = await db["shawt_links"].update_one({"link_id": link_id}, {"$inc": { "visits": 1 }})
        return RedirectResponse(shawt_link["url"])
    raise HTTPException(status_code=404, detail=f"Shawt link {id} not found")

@app.post("/api", response_model=ShawtLink)
async def new_link_id(tall_link: TallLink):
    tall_link_dict = tall_link.dict()
    
    global shawt_links
    shawt_link = ShawtLink(**tall_link_dict)
    shawt_link_json = jsonable_encoder(shawt_link)
    # shawt_links.append(shawt_link)
    new_shawt_link = await db["shawt_links"].insert_one(shawt_link_json)
    created_shawt_link = await db["shawt_links"].find_one({"_id": new_shawt_link.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_shawt_link)