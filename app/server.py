from bottle import Bottle, JSONPlugin, run
from orjson import orjson

from parser import parse_dump_file

web_server = Bottle()

for plugin in web_server.plugins:
    if isinstance(plugin, JSONPlugin):
        plugin.json_dumps = orjson.dumps


@web_server.get("/parse")
def parse():
    return {"state": parse_dump_file(file_path="examples/losingmymind.txt")}


run(web_server, host="localhost", port=8069)
