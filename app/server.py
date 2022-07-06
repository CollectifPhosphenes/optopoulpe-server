from bottle import Bottle, JSONPlugin, run
from orjson import orjson

from parser import parse_dump_file

web_server = Bottle()

for plugin in web_server.plugins:
    if isinstance(plugin, JSONPlugin):
        plugin.json_dumps = orjson.dumps


@web_server.get("/parse")
def parse():
    state = parse_dump_file(file_path="examples/losingmymind.txt")
    if not state.current_selected_track_index:
        state.current_selected_track_index = 2
        state.current_selected_track = state.tracks[str(state.current_selected_track_index)]
    return {"state": state}


run(web_server, host="localhost", port=8069)
