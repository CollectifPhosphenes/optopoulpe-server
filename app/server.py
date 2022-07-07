from bottle import Bottle, JSONPlugin, run, response
from orjson import orjson

from parser import parse_dump_file
from utils import get_random_save

web_server = Bottle()

for plugin in web_server.plugins:
    if isinstance(plugin, JSONPlugin):
        plugin.json_dumps = orjson.dumps


@web_server.get("/parse")
def parse():
    # file_path = "/root/path/on/raspberry/"
    file_path = get_random_save()
    state = parse_dump_file(file_path)
    state.used_save = file_path
    return {"state": state}


@web_server.hook("after_request")
def enable_cors():
    response.headers["Access-Control-Allow-Origin"] = "*"


run(web_server, host="localhost", port=8069)
