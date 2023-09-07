import asyncio
from asyncio import Future
from typing import Dict
from gama_client.base_client import GamaBaseClient
from gama_client.command_types import CommandTypes
from gama_client.message_types import MessageTypes

SERVER_URL = "gama-server"
SERVER_PORT = 6868

async def run_simulation(id: str, experiment_name: str, gaml_file_path_on_server: str):
    experiment_future: Future
    play_future: Future
    pause_future: Future
    expression_future: Future
    step_future: Future
    stop_future: Future


    async def _message_handler(message: Dict):
        print("received", message)
        if "command" in message:
            if message["command"]["type"] == CommandTypes.Load.value:
                experiment_future.set_result(message)
            elif message["command"]["type"] == CommandTypes.Play.value:
                play_future.set_result(message)
            elif message["command"]["type"] == CommandTypes.Pause.value:
                pause_future.set_result(message)
            elif message["command"]["type"] == CommandTypes.Expression.value:
                expression_future.set_result(message)
            elif message["command"]["type"] == CommandTypes.Step.value:
                step_future.set_result(message)
            elif message["command"]["type"] == CommandTypes.Stop.value:
                stop_future.set_result(message)

    init_parameters = [{"type": "string", "name": "experiment_id", "value": id}]

    client = GamaBaseClient(SERVER_URL, SERVER_PORT, _message_handler)
    print("connecting to Gama server")
    await client.connect()

    print("initialize a gaml model")
    experiment_future = asyncio.get_running_loop().create_future()
    await client.load(gaml_file_path_on_server, experiment_name, True, True, True, True, init_parameters)
    gama_response = await experiment_future
    
    try:
        experiment_id = gama_response["content"]
    except Exception as e:
        print("error while initializing", gama_response, e)
        return

    print("initialization successful, running the model")
    for _ in range(0, 60 * 24 * 55, 10):
        step_future = asyncio.get_running_loop().create_future()
        await client.step(experiment_id, 10, True)
        gama_response = await step_future
        if gama_response["type"] != MessageTypes.CommandExecutedSuccessfully.value:
            print("Unable to execute 10 new steps in the experiment", gama_response)
            raise Exception("Unable to execute 10 new steps in the experiment")
        
    await client.exit()
