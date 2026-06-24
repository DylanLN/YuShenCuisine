#!/usr/bin/env python3
"""
数据清洗与整理脚本

从 crawler/output/restaurants.json 读取原始采集数据：
1. 按坐标过滤（只保留深圳范围内的记录）
2. 按坐标重新分配行政区
3. 去重
4. 输出到 web/src/assets/data/ 和 web/public/data/

用法：
    python crawler/process.py
"""

import json
import os
import sys
from datetime import datetime
from collections import Counter

# 深圳坐标范围
SZ_MIN_LNG, SZ_MAX_LNG = 113.75, 114.48
SZ_MIN_LAT, SZ_MAX_LAT = 22.48, 22.85

# 各区坐标范围（先检查小区域，后检查大区域，避免覆盖）
DISTRICT_BOUNDS = [
    ("盐田", 114.22, 114.28, 22.54, 22.60),
    ("罗湖", 114.10, 114.18, 22.53, 22.60),
    ("福田", 114.00, 114.12, 22.51, 22.58),
    ("南山", 113.90, 114.00, 22.48, 22.56),
    ("大鹏", 114.35, 114.55, 22.55, 22.65),
    ("坪山", 114.30, 114.48, 22.62, 22.80),
    ("光明", 113.85, 114.00, 22.68, 22.82),
    ("龙华", 113.98, 114.10, 22.58, 22.76),
    ("宝安", 113.78, 113.98, 22.55, 22.80),
    ("龙岗", 114.05, 114.48, 22.58, 22.82),
]


def assign_district(lng: float, lat: float) -> str:
    """根据坐标判断所属行政区"""
    for name, min_lng, max_lng, min_lat, max_lat in DISTRICT_BOUNDS:
        if min_lng <= lng <= max_lng and min_lat <= lat <= max_lat:
            return name
    return "其他"


def main():
    input_file = os.path.join(os.path.dirname(__file__), "output", "restaurants.json")
    if not os.path.exists(input_file):
        print(f"错误：未找到 {input_file}", file=sys.stderr)
        print("请先运行 python crawler/crawl.py", file=sys.stderr)
        sys.exit(1)

    with open(input_file, "r", encoding="utf-8") as f:
        raw = json.load(f)

    print(f"原始数据: {len(raw)} 条")

    # 第一步：按坐标过滤（只保留深圳范围内）
    in_sz = []
    for r in raw:
        lng, lat = r["longitude"], r["latitude"]
        if SZ_MIN_LNG <= lng <= SZ_MAX_LNG and SZ_MIN_LAT <= lat <= SZ_MAX_LAT:
            in_sz.append(r)

    print(f"深圳范围内: {len(in_sz)} 条（过滤掉 {len(raw) - len(in_sz)} 条）")

    # 第二步：重新分配行政区（基于坐标，不信任API返回的区名）
    for r in in_sz:
        new_district = assign_district(r["longitude"], r["latitude"])
        old_district = r["district"]
        if new_district != old_district and new_district != "其他":
            r["district"] = new_district

    # 第三步：去重（优先 poi_id，次选 店名+地址）
    seen = set()
    unique = []
    for r in in_sz:
        key = r["id"] if r["id"] else f"{r['name']}|{r['address']}"
        if key not in seen:
            seen.add(key)
            unique.append(r)

    print(f"去重后: {len(unique)} 条（去重 {len(in_sz) - len(unique)} 条）")

    # 第四步：统计各区分布
    districts = Counter(r["district"] for r in unique)
    print("\n各区分布:")
    for d, c in sorted(districts.items()):
        print(f"  {d}: {c} 家")

    # 第五步：输出到前端目录
    targets = [
        os.path.join(os.path.dirname(__file__), "..", "web", "src", "assets", "data", "restaurants.json"),
        os.path.join(os.path.dirname(__file__), "..", "web", "public", "data", "restaurants.json"),
    ]

    for target in targets:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            json.dump(unique, f, ensure_ascii=False, indent=2)
        print(f"已输出: {target}")

    # 同步生成 districts.json 和 categories.json
    district_list = sorted(set(r["district"] for r in unique if r.get("district")))
    categories = sorted(set(tag for r in unique for tag in r.get("tags", [])))

    for base_dir in [
        os.path.join(os.path.dirname(__file__), "..", "web", "src", "assets", "data"),
        os.path.join(os.path.dirname(__file__), "..", "web", "public", "data"),
    ]:
        with open(os.path.join(base_dir, "districts.json"), "w", encoding="utf-8") as f:
            json.dump(district_list, f, ensure_ascii=False, indent=2)
        with open(os.path.join(base_dir, "categories.json"), "w", encoding="utf-8") as f:
            json.dump(categories, f, ensure_ascii=False, indent=2)

    print(f"\n已生成 districts.json（{len(district_list)} 个区）")
    print(f"已生成 categories.json（{len(categories)} 个分类）")
    print("\n✅ 处理完成！")


if __name__ == "__main__":
    main()
