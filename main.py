import uvicorn
from fastapi import FastAPI, Query, Body


app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "Hotel Sochi"},
    {"id": 2, "title": "Dubai", "name": "Hotel Sochi"},
]


@app.get("/hotels")
def get_hotels(
    id_: int | None = Query(default=None, description="ID отеля"), 
    title: str | None = Query(default=None, description="Заголовок"),
):  
    hotels_ = []
    for hotel in hotels:
        if id_ and hotel["id"] == id_:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.post("/hotels")
def create_hotel(
    title: str = Body(description="Заголовок", embed=True),
    name: str = Body(description="Название отеля", embed=True),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
        "name": name
    })
    return {"status": "OK"}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}")
def update_hotel_put(
    hotel_id: int,
    title: str = Body(description="Заголовок", embed=True),
    name: str = Body(description="Название отеля", embed=True),
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return {"status": "OK"}
        
    return {"status": "NOT FOUND"}


@app.patch("/hotels/{hotel_id}")
def update_hotel_patch(
    hotel_id: int,
    title: str | None  = Body(default=None, description="Заголовок", embed=True),
    name: str | None = Body(default=None, description="Название отеля", embed=True),
):
    if title is None and name is None:
        return {"status": "ERROR"}
    
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title if title is not None else hotel["title"]
            hotel["name"] = name if name is not None else hotel["name"]
            return {"status": "OK"}
        
    return {"status": "NOT FOUND"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
