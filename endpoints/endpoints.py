from server import app, dbController, parser
from fastapi.responses import FileResponse, JSONResponse
from requests_models import *


def json_resp(input_dict: dict) -> JSONResponse:
    return JSONResponse(content=input_dict)


@app.get("/database")  # получение файла базы данных пользователей
async def get_database() -> FileResponse:
    return FileResponse("../belaz.db")


@app.get("/test")
async def test() -> JSONResponse:
    return json_resp({"data": "Correct request to server!"})


@app.get("/get_all_items")
async def get_all_items() -> JSONResponse:
    return json_resp(
        dbController.get_all_items()
    )


@app.delete("/delete_item")
async def delete_item(delete_info: Item_reqeust) -> JSONResponse:
    response_msg = dbController.delete_model(
        id= delete_info.id,
        title= delete_info.title
    )
    return json_resp({
        "msg": response_msg
    })


@app.post("/add_item")
async def add_item(add_info: Add_request) -> JSONResponse:
    model_dict = {
        "title": add_info.title,
        "load_capacity": add_info.load_capacity,
        "engine_power": add_info.engine_power,
        "transmission": add_info.transmission,
        "torque": add_info.torque,
        "fuel_consumption": add_info.fuel_consumption,
        "tires": add_info.tires,
        "max_speed": add_info.max_speed,
        "turning_radius": add_info.turning_radius,
        "weight": add_info.weight
    }
    response_msg = dbController.add_model(
        model_dict=model_dict,
        name_series=add_info.name_series,
        name_author="USER"
    )
    return json_resp({"msg": response_msg})


@app.post("/parse")
async def parse_database(parse_info: Parse_request) -> JSONResponse:
    parser.parse(parse_info.remake)
    return json_resp({"msg": "Successfully parsing request!"})


@app.get("/get_item")
async def get_item(item_info: Item_reqeust) -> JSONResponse:
    model = dbController.get_model(
        id=item_info.id, title=item_info.title
    )
    if model is not None:
        return json_resp({"msg": "Successfully getting item!", "data": model.get_dict()})
    else:
        return json_resp({"msg": "Item not found!"})


@app.post("/edit_item")
async def edit_item() -> JSONResponse:
    # TODO: сделать функцию
    pass


@app.get("/filter")
async def get_filtered_items() -> JSONResponse:
    # TODO: сделать функцию
    pass


@app.delete("/delete_series")
async def delete_series(delete_series_info: Delete_series_request) -> JSONResponse:
    dbController.delete_series(id_series=None, name_series=delete_series_info.name_series)
    return json_resp({"msg": "Successfully deleting series request!"})
