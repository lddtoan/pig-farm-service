import asyncio
import os
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from src.client import run_simulation

app = FastAPI()


@app.get("/init")
async def run_experiment(id: str, name: str, path: str):
    asyncio.create_task(
        run_simulation(
            id=id,
            experiment_name=name,
            gaml_file_path_on_server=path,
        )
    )
    return Response()


@app.get("/gui")
def get_image(file: str):
    path = f"/app/pig-farm/includes/output/{file}"
    if os.path.isfile(path):
        return FileResponse(path)
    return Response(status_code=404)