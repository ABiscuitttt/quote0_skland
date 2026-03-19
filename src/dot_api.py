from typing import Literal, TypeAlias

import requests

DitherType: TypeAlias = Literal["DIFFUSION", "ORDERED", "NONE"]
DitherKernel: TypeAlias = Literal[
    "THRESHOLD",
    "ATKINSON",
    "BURKES",
    "FLOYD_STEINBERG",
    "SIERRA2",
    "STUCKI",
    "JARVIS_JUDICE_NINKE",
    "DIFFUSION_ROW",
    "DIFFUSION_COLUMN",
    "DIFFUSION_2D",
]


def devices(token: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    response = requests.get(
        "https://dot.mindreset.tech/api/authV2/open/devices",
        headers=headers,
    )
    return response.json()


def status(device_id: str, token: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    response = requests.get(
        f"https://dot.mindreset.tech/api/authV2/open/device/{device_id}/status",
        headers=headers,
    )
    return response.json()


def next(device_id: str, token: str):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        f"https://dot.mindreset.tech//api/authV2/open/device/{device_id}/next",
        headers=headers,
    )
    return response.json()


def list_content(
    device_id: str, token: str, taskType: Literal["loop", "fixed"] = "loop"
):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    response = requests.get(
        f"https://dot.mindreset.tech/api/authV2/open/device/{device_id}/{taskType}/list",
        headers=headers,
    )
    return response.json()


def text(
    device_id: str,
    token: str,
    *,
    refreshNow=True,
    title=None,
    message=None,
    signature=None,
    icon_base64=None,
    link=None,
    taskKey=None,
):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "refreshNow": refreshNow,
    }
    if title:
        payload["title"] = title
    if message:
        payload["message"] = message
    if signature:
        payload["signature"] = signature
    if icon_base64:
        payload["icon"] = icon_base64
    if link:
        payload["link"] = link
    if taskKey:
        payload["taskKey"] = taskKey
    response = requests.post(
        f"https://dot.mindreset.tech/api/authV2/open/device/{device_id}/text",
        headers=headers,
        json=payload,
    )
    return response.json()


def image(
    img_base64: str,
    device_id: str,
    token: str,
    *,
    refreshNow=True,
    link=None,
    border=0,
    ditherType: DitherType = "DIFFUSION",
    ditherKernel: DitherKernel = "FLOYD_STEINBERG",
    taskKey=None,
):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "image": img_base64,
        "refreshNow": refreshNow,
        "border": border,
        "ditherType": ditherType,
    }
    if ditherType == "DIFFUSION":
        payload["ditherKernel"] = ditherKernel

    if link:
        payload["link"] = link
    if taskKey:
        payload["taskKey"] = taskKey

    response = requests.post(
        f"https://dot.mindreset.tech/api/authV2/open/device/{device_id}/image",
        headers=headers,
        json=payload,
    )
    return response.json()
