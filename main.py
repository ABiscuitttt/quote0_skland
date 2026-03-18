import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "skland_tool", "src"))
import requests

from skland_tool.src import skyland as skland


def main():
    with open("user_info.json") as f:
        user_info = json.load(f)

    uid = user_info["uid"]
    token = user_info["token"]

    print(f"uid: {uid}")
    print(f"token: {token}")

    init_http_local(token)
    game_card = get_game_card(uid)
    with open("game_card.json", "w") as f:
        json.dump(game_card, f, indent=4, ensure_ascii=False)

    arknights_game_card = game_card["list"][0]
    # TODO: 解析游戏卡片，获取明日方舟的游戏数据


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


if __name__ == "__main__":
    main()
