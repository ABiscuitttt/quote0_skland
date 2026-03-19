import json

import src.skland_game_card as skland_game_card


def main():
    with open("user_info.json") as f:
        user_info = json.load(f)[0]

    uid = user_info["uid"]
    token = user_info["token"]

    print(f"uid: {uid}")
    print(f"token: {token}")

    skland_game_card.init_http_local(token)
    game_card = skland_game_card.get_game_card(uid)
    with open("game_card.json", "w") as f:
        json.dump(game_card, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
