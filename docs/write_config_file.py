#meta:tag=hide
import os
import json
with open(os.path.expanduser("~/.metaflowconfig/config_test.json"), "w") as outfile:
    outfile.write(json.dumps({"METAFLOW_DEFAULT_DATASTORE": "local"}, indent=4))
