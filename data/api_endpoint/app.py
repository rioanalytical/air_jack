from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel, validator
import logging
import databases
import sqlalchemy

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(DATABASE_URL)
table = sqlalchemy.Table(
    "items",
    sqlalchemy.MetaData(),
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=100)),
)

class Item(BaseModel):
    name: str

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('Name must not be empty')
        return v

app = FastAPI()

@app.on_event("startup")
async def startup():
    logger.info("Connecting to the database...")
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    logger.info("Disconnecting from the database...")
    await database.disconnect()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    query = table.select().where(table.c.id == item_id)
    item = await database.fetch_one(query)
    if item is None:
        logger.error(f"Item with id {item_id} not found")
        raise HTTPException(status_code=404, detail="Item not found")
    logger.info(f"Fetched item: {item}")
    return item

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    query = table.insert().values(name=item.name)
    last_record_id = await database.execute(query)
    logger.info(f"Created item with id: {last_record_id}")
    return {"id": last_record_id, **item.dict()}