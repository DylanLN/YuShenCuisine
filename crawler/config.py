# 高德 Web API Key
# 方式1：设置环境变量 AMAP_KEY（推荐）
#   export AMAP_KEY="你的key"
#
# 方式2：直接修改下面这个值（注意不要提交到 git）
AMAP_KEY = "your_key"

AMAP_URL = "https://restapi.amap.com/v5/place/text"

DISTRICTS = [
    "福田", "罗湖", "南山", "盐田", "宝安",
    "龙岗", "龙华", "坪山", "光明", "大鹏"
]

KEYWORDS = [
    "河南菜", "河南饭店", "河南餐馆", "河南面馆", "烩面",
    "胡辣汤", "河南羊汤", "水煎包", "豫北饭店",
    "开封灌汤包", "洛阳水席", "信阳菜", "周口菜", "驻马店菜", "安阳菜"
]

TAG_RULES = {
    "烩面": "烩面",
    "胡辣汤": "胡辣汤",
    "灌汤包": "灌汤包",
    "开封灌汤包": "灌汤包",
    "羊肉汤": "羊肉汤",
    "河南菜": "河南菜",
    "豫菜": "河南菜",
    "信阳": "河南菜",
    "周口": "河南菜",
    "驻马店": "河南菜",
    "安阳": "河南菜",
    "洛阳": "河南菜",
    "开封": "河南菜",
    "扣碗": "河南菜",
    "大盘鸡": "河南菜",
}


def infer_tags(name: str) -> list:
    tags = set()
    for keyword, tag in TAG_RULES.items():
        if keyword in name:
            tags.add(tag)
    if not tags:
        tags.add("河南菜")
    return sorted(tags)
