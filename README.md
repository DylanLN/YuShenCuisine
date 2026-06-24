# 🥟 深圳河南美食地图

在深圳，找到家乡的味道。

**在线预览：** https://dylanln.github.io/YuShenCuisine/

## 功能

- 全屏高德地图展示深圳河南餐馆分布
- 多选筛选（区域 + 分类）
- 店铺详情（地址、电话、评分、导航）
- 输入地址定位到你的位置

## 本地开发

```bash
cd web
npm install
npm run dev
```

浏览器访问 `http://localhost:5173/YuShenCuisine/`

## 数据更新（一键）

```bash
# 先设置 Key
export AMAP_KEY="你的key"
# 一键采集+清洗+输出
bash scripts/sync-data.sh
```

## 高德 Key 配置

### Web API Key（数据采集）
```bash
export AMAP_KEY="你的key"
```

### JS API Key（地图展示）
在 `web/src/utils/amap.ts` 中已配置，需要在**高德开放平台 → 应用管理**添加「JS API 服务」，并白名单加入 `dylanln.github.io`
