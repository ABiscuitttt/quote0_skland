import base64
import datetime
import json
import random
import re
import subprocess
import sys
from io import BytesIO

import requests
from PIL import Image, ImageDraw, ImageFont

import src.skland_game_card as skland_game_card
from src.dot_api import image
from src.get_img_url import get_role_img, roles_data
from src.image_process import crop_to_ratio_pil, webp_add_white_background


def main():
    # 使用当前的解释器运行“python ./skland_tool/src/main.py”
    subprocess.run([sys.executable, "./skland_tool/src/main.py"], check=True)

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

    # 随机挑选一个角色图片
    filtered_roles = list(
        filter(
            lambda role: (
                # role["title"]["org"] == "炎-岁" and role["title"]["rarity"] == "5"
                role["title"]["rarity"] == "5"
            ),
            roles_data,
        )
    )
    char_ids = [role["title"]["charId"] for role in filtered_roles]
    char_id = random.choice(char_ids)
    print(f"随机选择的角色ID: {char_id}")
    url = get_role_img(char_id, "CROPPED")
    with open("img.webp", "wb") as img:
        img.write(requests.get(url).content)

    res = read_res_from_log()

    webp_add_white_background("img.webp", "img.png")
    crop_to_ratio_pil("img.png", "img.png")
    img = Image.open("img.png")
    img = draw_text("今日已签到", res, img)
    img.save("img_with_text.png", format="PNG")

    print("正在推送图片...")
    push_img("img_with_text.png")


def read_res_from_log():
    # 读取签到内容
    d = datetime.datetime.now().strftime("%Y-%m-%d")
    pat = re.compile(r"\[明日方舟\]角色不闻竹幽#5397\(官服\)签到成功，获得了(.*?)\'")
    with open(f"logs/{d}.log", encoding="utf-8") as f:
        sign_in_content = f.read()
    match = pat.search(sign_in_content)
    res = match.group(1) if match else "None"
    pat2 = re.compile(r".*?×\d+")
    matches = pat2.findall(res)
    res = "\n".join(matches) if matches else "None"
    return res


def draw_text(text1, text2, img):
    draw = ImageDraw.Draw(img)

    # 分别设置不同大小的字体
    font_first = ImageFont.truetype("SarasaMonoSC-Bold.ttf", 80)  # 第一行字体较小
    font_second = ImageFont.truetype(
        "SarasaMonoSC-Bold.ttf", 90 if "\n" in text2 else 140
    )  # 第二行字体较大

    width, height = img.size
    first_line = text1
    second_line = text2

    # 计算两行文字各自的尺寸
    bbox_first = draw.textbbox((0, 0), first_line, font=font_first)
    text_height_first = bbox_first[3] - bbox_first[1]

    bbox_second = draw.textbbox((0, 0), second_line, font=font_second)
    text_height_second = bbox_second[3] - bbox_second[1]

    # 计算整体高度
    total_height = text_height_first + text_height_second + 20  # 20是两行之间的间距

    # 计算起始Y坐标，使两行文字整体垂直居中
    start_y = (height - total_height) // 2

    # 设置水平起点为靠左20%
    x_start = int(width * 0.05)  # 靠左20%的位置

    # 绘制文字（左对齐，起点在20%位置）
    draw.text((x_start, start_y), first_line, font=font_first, fill="black")
    draw.text(
        (x_start, start_y + text_height_first + 20),
        second_line,
        font=font_second,
        fill="black",
    )
    return img


def push_img(png_img_name):
    with open(png_img_name, "rb") as f:
        buffered = BytesIO(f.read())
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    with open("device_info.json") as f:
        device_info = json.load(f)
    ret = image(img_base64, device_info["device_id"], device_info["token"])
    print(ret)


if __name__ == "__main__":
    main()
