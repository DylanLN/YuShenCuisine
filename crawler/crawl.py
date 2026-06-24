#!/usr/bin/env python3
"""
高德地图 POI 采集脚本
用法：
    export AMAP_KEY="your_key"
    python crawler/crawl.py
"""

import json
import os
import re
import sys
import time
from datetime import datetime

import requests

# 从 .env 文件加载环境变量（不提交到 git）
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip())

# 先从环境变量取 Key，没有则从 config.py 取
AMAP_KEY = os.environ.get("AMAP_KEY") or "your_amap_key_here"

from config import AMAP_URL, DISTRICTS, KEYWORDS, infer_tags

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "restaurants.json")


def fetch_pois(keyword: str, region: str) -> list:
    pois = []
    page_num = 1
    while True:
        params = {
            "key": AMAP_KEY, "keywords": keyword, "region": region,
            "page_size": 25, "page_num": page_num,
        }
        try:
            resp = requests.get(AMAP_URL, params=params, timeout=15)
            data = resp.json()
        except Exception as e:
            print(f"  [ERROR] {e}", file=sys.stderr)
            break

        if data.get("status") != "1":
            print(f"  [WARN] {data.get('info', 'unknown')}", file=sys.stderr)
            break

        batch = data.get("pois", [])
        if not batch:
            break

        for poi in batch:
            if "餐饮" not in poi.get("type", ""):
                continue
            location = poi.get("location", "")
            if not location:
                continue
            try:
                lng, lat = map(float, location.split(","))
            except ValueError:
                continue
            rating = poi.get("biz_ext", {}).get("rating", "")
            cost = poi.get("biz_ext", {}).get("cost", "")
            pois.append({
                "id": poi.get("id", ""),
                "name": poi.get("name", "").strip(),
                "district": region,
                "address": poi.get("address", "").strip(),
                "phone": poi.get("tel", "").strip(),
                "longitude": lng,
                "latitude": lat,
                "rating": float(rating) if rating else None,
                "cost": int(float(cost)) if cost else None,
                "tags": infer_tags(poi.get("name", "")),
                "cover": "",
                "source_keyword": keyword,
                "update_time": poi.get("update_time", "") or datetime.now().strftime("%Y-%m-%d"),
            })

        total = int(data.get("count", 0))
        if page_num * 25 >= total:
            break
        page_num += 1
        time.sleep(0.3)

    return pois


def deduplicate(pois: list) -> list:
    seen = set()
    unique = []
    for p in pois:
        key = p["id"] if p["id"] else f"{p['name']}|{p['address']}"
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return unique


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if AMAP_KEY == "your_amap_key_here":
        print("错误：请先创建 crawler/.env，写入 AMAP_KEY=你的key（不要提交到 git）", file=sys.stderr)
        sys.exit(1)

    all_pois = []
    total_queries = len(KEYWORDS) * len(DISTRICTS)
    current = 0

    print(f"开始采集，共 {total_queries} 个组合")
    for keyword in KEYWORDS:
        for region in DISTRICTS:
            current += 1
            print(f"[{current}/{total_queries}] {keyword} × {region}")
            all_pois.extend(fetch_pois(keyword, region))
            time.sleep(0.2)

    print(f"去重前: {len(all_pois)} 条")
    unique = deduplicate(all_pois)
    print(f"去重后: {len(unique)} 条")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)
    print(f"已保存到: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
