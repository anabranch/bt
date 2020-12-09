from datetime import datetime
import json
import time
import anyscale.sdk.anyscale_client as anyscale_client
from anyscale.sdk.anyscale_client.api.default_api import DefaultApi

CLI_TOKEN = "sss_XXXXXXXX"
SESSION_ID = "ses_YYYYYYYY"

# Helpers
def _json_converter(o):
    if isinstance(o, datetime):
        return o.__str__()
def prettify_json(json_obj):
    return json.dumps(json_obj, default=_json_converter, sort_keys=True, indent=4)

# initialize API client
def initialize_api_client() -> DefaultApi:
    configuration = anyscale_client.Configuration(host="https://beta.anyscale.com/ext")
    api_client = anyscale_client.ApiClient(configuration, cookie=f"cli_token={CLI_TOKEN}")  
    return DefaultApi(api_client)

# initialize our API client
api = initialize_api_client()

# get status of a session
r = api.get_session(SESSION_ID)
print(prettify_json(r))

# start a session
r = api.start_session(SESSION_ID)
print(prettify_json(r))

# Scanning through commands
print(f"\nFetching first 3 Commands")
r = api.list_session_commands(SESSION_ID, count=3)
print(prettify_json(r.to_dict()))

print(f"\nFetching next 3 Commands")
r = api.list_session_commands(
    SESSION_ID, count=3, paging_token=r.metadata.next_paging_token
)
print(prettify_json(r.to_dict()))

# Run a shell command within the session
print("Create Command:")
r = api.create_session_command(anyscale_client.CreateSessionCommand(SESSION_ID, "echo ANYSCALE SDK DEMO"))
print(prettify_json(r.to_dict()))
command_id = r.id

# Wait for completion
r = api.get_session_command(command_id)
while r.result.finished_at is None:
    print("Waiting for Command to finish...")
    time.sleep(1)
    r = api.get_session_command(command_id)

print("Command Finished:")
print(prettify_json(r.to_dict()))

# Stop session, can be restarted quickly
r = api.stop_session(SESSION_ID)
print("Stopping Session:")
print(prettify_json(r.to_dict()))

# Terminate Session
r = api.terminate_session(SESSION_ID)
print("Terminating Session:")
print(prettify_json(r.to_dict()))