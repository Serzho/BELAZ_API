import sys

sys.path.append("../../../BELAZ_API/")

from core.server import fastAPI_app, dbController, parser
from fastapi.responses import FileResponse, JSONResponse
from requests_models import *
from core.service.logger import base_logger

app = fastAPI_app


def log(message: str) -> None:
    base_logger(msg = message, module_name="ENDPOINTS")


def json_resp(input_dict: dict) -> JSONResponse:
    return JSONResponse(content=input_dict)


@app.get("/database")  # получение файла базы данных пользователей
async def get_database() -> FileResponse:
    log("Getting database request")
    return FileResponse("../belaz.db")


@app.get("/test")
async def test() -> JSONResponse:
    log("Getting test request")
    return json_resp({"data": "Correct request to server!"})


@app.get("/get_all_items")
async def get_all_items() -> JSONResponse:
    # print(dbController.get_all_items())
    log("Getting all items from database request")
    return json_resp(
        dbController.get_all_items()
    )


@app.delete("/delete_item")
async def delete_item(delete_info: Item_reqeust) -> JSONResponse:
    log(f"Deleting item request with id = {delete_info.id} and name = {delete_info.title}")
    response_msg = dbController.delete_model(
        id= delete_info.id,
        title= delete_info.title
    )
    return json_resp({
        "msg": response_msg
    })


@app.post("/add_item")
async def add_item(add_info: Add_request) -> JSONResponse:
    log(f"Adding item request with name = {add_info.title}")
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
    log(f"Parse database request with remake = {parse_info.remake}")
    parser.parse(parse_info.remake)
    return json_resp({"msg": "Successfully parsing request!"})


@app.get("/get_item")
async def get_item(item_info: Item_reqeust) -> JSONResponse:  # TODO: не работает
    log(f"Getting item request with id = {item_info.id} and name = {item_info.title}")
    model = dbController.get_model(
        id=item_info.id, title=item_info.title
    )
    if model is not None:
        return json_resp({"msg": "Successfully getting item!", "data": model.get_dict()})
    else:
        return json_resp({"msg": "Item not found!"})


@app.post("/edit_item")
async def edit_item(edit_info: Edit_request) -> JSONResponse:
    log(f"Editing request with id = {edit_info.id} and changing fields = {edit_info.changing_fields}")
    response_msg = dbController.edit_model(edit_info.changing_fields, edit_info.id)
    return json_resp({"msg": response_msg})


@app.post("/filter")
async def get_filtered_items(filter_info: Filter_request) -> JSONResponse:
    log(f"Filter request with fields = {filter_info.filtered_fields}")
    response_data = dbController.filter_models(filter_info.filtered_fields)
    return json_resp(response_data)


@app.delete("/delete_series")  # TODO: Выбрасывает исключение при повторном удалении
async def delete_series(delete_series_info: Delete_series_request) -> JSONResponse:
    log(f"Deleting series request with name = {delete_series_info.name_series}")
    dbController.delete_series(id_series=None, name_series=delete_series_info.name_series)
    return json_resp({"msg": "Successfully deleting series request!"})

# uvicorn.run(app=app, host="localhost", port=9999)

