import sys
from pathlib import Path

skland_tool_path = (Path(__file__).parent / "../skland_tool/src").resolve()

sys.path.append(skland_tool_path.__str__())
sys.dont_write_bytecode = True

import requests  # noqa: E402

from skland_tool.src import skyland as skland  # noqa: E402


def init_http_local(token):
    cred_resp = skland.get_cred_by_token(token)
    skland.http_local.token = cred_resp["token"]
    skland.http_local.header = skland.header.copy()
    skland.http_local.header["cred"] = cred_resp["cred"]


def get_game_card(uid):
    url = f"https://zonai.skland.com/api/v1/game/cards?uid={uid}"
    headers = skland.get_sign_header(url, "get", None, skland.http_local.header)
    resp = requests.get(url, headers=headers).json()
    if resp["code"] != 0:
        print(f"get game card failed: {resp}")
        return None
    return resp["data"]
