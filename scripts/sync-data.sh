#!/bin/bash
# 一键数据更新流程
# 用法: bash scripts/sync-data.sh

set -e

echo "=== 深圳河南美食地图 - 数据更新 ==="
echo ""

# 1. 采集
echo "[1/3] 开始采集..."
python3 crawler/crawl.py
echo ""

# 2. 处理（过滤 + 重新分配区 + 去重 + 输出）
echo "[2/3] 开始处理..."
python3 crawler/process.py
echo ""

# 3. 提交
echo "[3/3] 提交到 git..."
git add web/src/assets/data/ web/public/data/
git commit -m "update: data refresh $(date +%Y-%m-%d)" || echo "  无变更，跳过提交"
echo ""

echo "=== 完成 ==="
echo "运行 npm run build 重新构建后即可预览"
