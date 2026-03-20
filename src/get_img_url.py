from typing import Literal

import requests

from .prts_api import cargo_query

roles_data = cargo_query("tables=chara&fields=cn,charId,org,rarity")


def get_role_img(
    char_id: str,
    type: Literal["FULL", "CROPPED"],
    *,
    rank: Literal["#0", "#1", "#2"] = "#0",
    skin_id: str | None = None,
):
    if type == "FULL":
        cn = list(filter(lambda role: role["title"]["charId"] == char_id, roles_data))
        assert len(cn) == 1, f"角色ID {char_id} 不唯一或不存在"
        cn = cn[0]["title"]["cn"]
        if skin_id:
            url = __query_img_url_prts(cn + "_skin" + skin_id)[0]["url"]
            print(url)
            return url
        else:
            rank_suffix = {
                "#0": "1",
                "#1": "1",
                "#2": "2",
            }[rank]
            if cn == "阿米娅" and rank == "#1":
                rank_suffix = "1+"
            url = __query_img_url_prts(cn + "_" + rank_suffix)
            assert len(url) > 0, f"未找到角色 {cn} 的图片，rank={rank}"
            url = url[0]["url"]
            print(url)
            return url
    elif type == "CROPPED":
        rank_suffix = {
            "#0": "",
            "#1": "",
            "#2": "#2",
        }[rank]
        url_base = "https://bbs.hycdn.cn/skland-fe-static/assets/arknights/char_illustration/{{charId}}.png?x-oss-process=style/arknightsCardDecorationChar2"
        url = url_base.replace("{{charId}}", char_id + rank_suffix)
        print(url)
        return url


def __query_img_url_prts(cn: str):
    base_url = "https://prts.wiki/api.php?action=query&list=allimages&aiprefix=立绘_{{prefix}}.png&prop=imageinfo&iiprop=url&format=json&ailimit=50"
    url = base_url.replace("{{prefix}}", cn)
    response = requests.get(url).json()
    return response["query"]["allimages"]
