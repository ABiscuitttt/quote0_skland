import requests

domain = "https://prts.wiki/api.php"


def cargo_tables():
    response = requests.get(f"{domain}?action=cargotables&format=json")
    return response.json()["cargotables"]


def cargo_fields(table: str):
    response = requests.get(f"{domain}?action=cargofields&format=json&table={table}")
    return response.json()["cargofields"]


def cargo_query(query: str):
    limit = 500
    offset = 0
    all_results = []
    url = f"{domain}?action=cargoquery&format=json&{query}"

    while True:
        url = f"{url}&limit={limit}&offset={offset}"
        response = requests.get(url).json()
        data = response.get("cargoquery", [])
        if not data:
            break  # 没有更多数据
        all_results.extend(data)

        if len(data) < limit:
            break
        else:
            offset += limit
    return all_results
