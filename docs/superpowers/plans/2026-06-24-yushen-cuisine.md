# 深圳河南美食地图 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 开发一个可在 GitHub Pages 免费运行的深圳河南美食地图静态网站，包含数据采集、地图展示、搜索筛选、店铺详情和一键导航功能。

**Architecture:** 前端为 Vue3 + TypeScript + Vite 静态站点，部署在 GitHub Pages。数据通过 Python 脚本调用高德 Web API 一次性采集，存储为 JSON 静态文件。地图使用静态底图 + CSS 定位标记点，无需地图 API 调用。采用 Hash 路由避免 GitHub Pages 刷新 404。

**Tech Stack:** Vue 3, TypeScript, Vite, Pinia, Vue Router, Element Plus, lodash.debounce, Python 3.12, requests

**目录结构（产出目标）：**

```
/home/ln/data/Code/html/YuShenCuisine/
├── crawler/
│   ├── crawl.py
│   ├── config.py
│   └── output/
├── web/
│   ├── data/
│   │   ├── mock-restaurants.json     # 开发用模拟数据
│   │   ├── districts.json
│   │   └── categories.json
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.ts
│   │   ├── env.d.ts
│   │   ├── router/index.ts
│   │   ├── stores/restaurant.ts
│   │   ├── types/restaurant.ts
│   │   ├── utils/coordinates.ts
│   │   ├── utils/map-bounds.ts
│   │   ├── views/
│   │   │   ├── HomePage.vue
│   │   │   ├── MapPage.vue
│   │   │   ├── ListPage.vue
│   │   │   └── DetailPage.vue
│   │   ├── components/
│   │   │   ├── SearchBar.vue
│   │   │   ├── FilterBar.vue
│   │   │   ├── RestaurantCard.vue
│   │   │   ├── StaticMap.vue
│   │   │   ├── MapMarker.vue
│   │   │   ├── MarkerPopup.vue
│   │   │   └── NavButton.vue
│   │   └── assets/styles/main.css
│   ├── public/
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   ├── package.json
│   └── env.d.ts
├── scripts/
│   └── sync-data.sh
├── docs/
│   └── ...
├── .gitignore
└── README.md
```

---

### Task 1: 脚手架 Vue3 + Vite 项目

**Files:**
- Create: `web/package.json`
- Create: `web/vite.config.ts`
- Create: `web/tsconfig.json`
- Create: `web/tsconfig.node.json`
- Create: `web/index.html`
- Create: `web/src/env.d.ts`
- Create: `web/src/main.ts`
- Create: `web/src/App.vue`
- Create: `.gitignore`

- [ ] **Step 1: 创建 web/package.json**

```json
{
  "name": "shenzhen-henan-food",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.0",
    "vue-router": "^4.3.0",
    "pinia": "^2.1.0",
    "element-plus": "^2.7.0",
    "@element-plus/icons-vue": "^2.3.0",
    "lodash.debounce": "^4.0.8"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "typescript": "^5.4.0",
    "vite": "^5.4.0",
    "vue-tsc": "^2.0.0",
    "@types/lodash.debounce": "^4.0.9"
  }
}
```

- [ ] **Step 2: 创建 vite.config.ts**

```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: '/shenzhen-henan-food/'
})
```

- [ ] **Step 3: 创建 tsconfig.json**

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForCacheFields": true,
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "preserve",
    "strict": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noFallthroughCasesInSwitch": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*.ts", "src/**/*.tsx", "src/**/*.vue", "src/env.d.ts"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

- [ ] **Step 4: 创建 tsconfig.node.json**

```json
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
```

- [ ] **Step 5: 创建 web/index.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>深圳河南美食地图</title>
  <link rel="icon" type="image/svg+xml" href="/vite.svg" />
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/src/main.ts"></script>
</body>
</html>
```

- [ ] **Step 6: 创建 src/env.d.ts**

```typescript
/// <reference types="vite/client" />
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}
```

- [ ] **Step 7: 创建 src/main.ts**

```typescript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import App from './App.vue'
import router from './router'
import './assets/styles/main.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(ElementPlus, { locale: zhCn })
app.mount('#app')
```

- [ ] **Step 8: 创建 src/App.vue**

```vue
<script setup lang="ts">
import SearchBar from './components/SearchBar.vue'
import FilterBar from './components/FilterBar.vue'
</script>

<template>
  <div class="app-container">
    <header class="app-header">
      <div class="header-inner">
        <router-link to="/" class="logo">
          <span class="logo-icon">🥟</span>
          <span class="logo-text">深圳河南美食地图</span>
        </router-link>
        <SearchBar />
      </div>
    </header>

    <FilterBar />

    <main class="app-main">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  background: #F8F8F8;
}
.app-header {
  background: #C8102E;
  color: white;
  padding: 0 16px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 16px;
  height: 56px;
}
.logo {
  display: flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  color: white;
  white-space: nowrap;
}
.logo-icon {
  font-size: 24px;
}
.logo-text {
  font-size: 18px;
  font-weight: 600;
}
.app-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px;
}
</style>
```

- [ ] **Step 9: 创建 .gitignore**

```
node_modules/
dist/
.DS_Store
*.local
crawler/output/restaurants.json
.superpowers/
```

- [ ] **Step 10: 安装依赖**

Run: `cd /home/ln/data/Code/html/YuShenCuisine/web && npm install`
Expected: node_modules/ 创建成功，无报错

- [ ] **Step 11: 验证项目可构建**

Run: `cd /home/ln/data/Code/html/YuShenCuisine/web && npx vite build`
Expected: dist/ 目录生成成功，无报错

- [ ] **Step 12: Commit**

```bash
cd /home/ln/data/Code/html/YuShenCuisine
git add web/package.json web/vite.config.ts web/tsconfig.json web/tsconfig.node.json web/index.html web/src/ .gitignore
git commit -m "feat: scaffold Vue3 + Vite project"
```

---

### Task 2: 类型定义、路由、Store、Mock 数据

**Files:**
- Create: `web/src/types/restaurant.ts`
- Create: `web/src/router/index.ts`
- Create: `web/src/stores/restaurant.ts`
- Create: `web/data/mock-restaurants.json`
- Create: `web/data/districts.json`
- Create: `web/data/categories.json`
- Create: `web/src/assets/styles/main.css`
- Modify: `web/src/App.vue`（添加路由视图容器类）

- [ ] **Step 1: 创建 src/types/restaurant.ts**

```typescript
export interface Restaurant {
  id: string
  name: string
  district: string
  address: string
  phone: string
  longitude: number
  latitude: number
  rating: number | null
  cost: number | null
  tags: string[]
  cover: string
  source_keyword: string
  update_time: string
}
```

- [ ] **Step 2: 创建 src/router/index.ts**

```typescript
import { createRouter, createWebHashHistory } from 'vue-router'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomePage.vue')
    },
    {
      path: '/map',
      name: 'map',
      component: () => import('../views/MapPage.vue')
    },
    {
      path: '/list',
      name: 'list',
      component: () => import('../views/ListPage.vue')
    },
    {
      path: '/detail/:id',
      name: 'detail',
      component: () => import('../views/DetailPage.vue')
    }
  ]
})

export default router
```

- [ ] **Step 3: 创建 src/stores/restaurant.ts**

```typescript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Restaurant } from '../types/restaurant'

export const useRestaurantStore = defineStore('restaurant', () => {
  // 状态
  const all = ref<Restaurant[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const filterDistrict = ref('')
  const filterCategory = ref('')
  const searchKeyword = ref('')

  // 计算属性
  const filtered = computed(() => {
    let list = all.value

    if (searchKeyword.value) {
      const kw = searchKeyword.value.toLowerCase()
      list = list.filter(r =>
        r.name.toLowerCase().includes(kw) ||
        r.tags.some(t => t.toLowerCase().includes(kw)) ||
        r.district.includes(kw) ||
        r.address.toLowerCase().includes(kw)
      )
    }

    if (filterDistrict.value) {
      list = list.filter(r => r.district === filterDistrict.value)
    }

    if (filterCategory.value) {
      list = list.filter(r => r.tags.includes(filterCategory.value))
    }

    return list
  })

  const districts = computed(() => {
    const set = new Set(all.value.map(r => r.district))
    return Array.from(set).sort()
  })

  const categories = computed(() => {
    const set = new Set(all.value.flatMap(r => r.tags))
    return Array.from(set).sort()
  })

  // 操作
  async function fetchAll() {
    loading.value = true
    error.value = null
    try {
      const resp = await fetch('/shenzhen-henan-food/data/mock-restaurants.json')
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
      all.value = await resp.json()
    } catch (e: any) {
      error.value = e.message || '加载数据失败'
    } finally {
      loading.value = false
    }
  }

  function getById(id: string): Restaurant | undefined {
    return all.value.find(r => r.id === id)
  }

  return {
    all, loading, error,
    filterDistrict, filterCategory, searchKeyword,
    filtered, districts, categories,
    fetchAll, getById
  }
})
```

- [ ] **Step 4: 创建 web/data/mock-restaurants.json**

```json
[
  {
    "id": "B0FFF001",
    "name": "萧记烩面",
    "district": "南山",
    "address": "深圳市南山区创业路粤海小区1栋",
    "phone": "0755-88880001",
    "longitude": 113.9234,
    "latitude": 22.5345,
    "rating": 4.7,
    "cost": 35,
    "tags": ["烩面", "胡辣汤"],
    "cover": "",
    "source_keyword": "河南烩面",
    "update_time": "2026-06-24"
  },
  {
    "id": "B0FFF002",
    "name": "郑州烩面馆",
    "district": "福田",
    "address": "深圳市福田区华强北路赛格广场B1",
    "phone": "0755-88880002",
    "longitude": 114.0853,
    "latitude": 22.5478,
    "rating": 4.5,
    "cost": 28,
    "tags": ["烩面"],
    "cover": "",
    "source_keyword": "郑州烩面",
    "update_time": "2026-06-24"
  },
  {
    "id": "B0FFF003",
    "name": "老郑州烩面",
    "district": "宝安",
    "address": "深圳市宝安区西乡大道金海商务大厦1楼",
    "phone": "",
    "longitude": 113.8832,
    "latitude": 22.5651,
    "rating": null,
    "cost": null,
    "tags": ["烩面"],
    "cover": "",
    "source_keyword": "郑州烩面",
    "update_time": "2026-06-24"
  },
  {
    "id": "B0FFF004",
    "name": "方中山胡辣汤",
    "district": "龙华",
    "address": "深圳市龙华区民治大道嘉熙业广场1楼",
    "phone": "0755-88880004",
    "longitude": 114.0355,
    "latitude": 22.6198,
    "rating": 4.8,
    "cost": 25,
    "tags": ["胡辣汤"],
    "cover": "",
    "source_keyword": "胡辣汤",
    "update_time": "2026-06-24"
  },
  {
    "id": "B0FFF005",
    "name": "开封灌汤包",
    "district": "罗湖",
    "address": "深圳市罗湖区东门中路鸿基商业大厦1楼",
    "phone": "0755-88880005",
    "longitude": 114.1298,
    "latitude": 22.5483,
    "rating": 4.3,
    "cost": 45,
    "tags": ["灌汤包"],
    "cover": "",
    "source_keyword": "开封灌汤包",
    "update_time": "2026-06-24"
  },
  {
    "id": "B0FFF006",
    "name": "洛阳水席楼",
    "district": "南山",
    "address": "深圳市南山区科技南路高新公寓1楼",
    "phone": "0755-88880006",
    "longitude": 113.9532,
    "latitude": 22.5412,
    "rating": 4.4,
    "cost": 68,
    "tags": ["河南菜"],
    "cover": "",
    "source_keyword": "洛阳水席",
    "update_time": "2026-06-24"
  },
  {
    "id": "B0FFF007",
    "name": "信阳人家",
    "district": "龙岗",
    "address": "深圳市龙岗区龙岗大道万科天誉2楼",
    "phone": "0755-88880007",
    "longitude": 114.2478,
    "latitude": 22.7209,
    "rating": 4.6,
    "cost": 55,
    "tags": ["河南菜"],
    "cover": "",
    "source_keyword": "信阳菜",
    "update_time": "2026-06-24"
  },
  {
    "id": "B0FFF008",
    "name": "周口家乡菜",
    "district": "光明",
    "address": "深圳市光明区公明街道红花路1号",
    "phone": "",
    "longitude": 113.9355,
    "latitude": 22.7482,
    "rating": 4.2,
    "cost": 38,
    "tags": ["河南菜"],
    "cover": "",
    "source_keyword": "周口菜",
    "update_time": "2026-06-24"
  },
  {
    "id": "B0FFF009",
    "name": "安阳道口烧鸡",
    "district": "盐田",
    "address": "深圳市盐田区沙头角深盐路壹海城B1",
    "phone": "0755-88880009",
    "longitude": 114.2392,
    "latitude": 22.5563,
    "rating": 4.1,
    "cost": 42,
    "tags": ["河南菜"],
    "cover": "",
    "source_keyword": "安阳菜",
    "update_time": "2026-06-24"
  },
  {
    "id": "B0FFF010",
    "name": "大鹏胡辣汤店",
    "district": "大鹏",
    "address": "深圳市大鹏新区南澳街道海港路18号",
    "phone": "0755-88880010",
    "longitude": 114.4785,
    "latitude": 22.5923,
    "rating": null,
    "cost": 20,
    "tags": ["胡辣汤"],
    "cover": "",
    "source_keyword": "胡辣汤",
    "update_time": "2026-06-24"
  },
  {
    "id": "B0FFF011",
    "name": "豫见河南",
    "district": "福田",
    "address": "深圳市福田区车公庙泰然工业区203栋",
    "phone": "0755-88880011",
    "longitude": 114.0238,
    "latitude": 22.5351,
    "rating": 4.9,
    "cost": 72,
    "tags": ["河南菜", "烩面"],
    "cover": "",
    "source_keyword": "河南菜",
    "update_time": "2026-06-24"
  },
  {
    "id": "B0FFF012",
    "name": "老马家羊肉汤",
    "district": "坪山",
    "address": "深圳市坪山区坪山大道坪山影剧院旁",
    "phone": "0755-88880012",
    "longitude": 114.3502,
    "latitude": 22.6935,
    "rating": 4.0,
    "cost": 30,
    "tags": ["羊肉汤"],
    "cover": "",
    "source_keyword": "洛阳水席",
    "update_time": "2026-06-24"
  }
]
```

- [ ] **Step 5: 创建 web/data/districts.json**

```json
[
  "福田",
  "罗湖",
  "南山",
  "盐田",
  "宝安",
  "龙岗",
  "龙华",
  "坪山",
  "光明",
  "大鹏"
]
```

- [ ] **Step 6: 创建 web/data/categories.json**

```json
[
  "烩面",
  "胡辣汤",
  "灌汤包",
  "羊肉汤",
  "河南菜"
]
```

- [ ] **Step 7: 创建 src/assets/styles/main.css**

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
    'Helvetica Neue', Arial, 'Noto Sans SC', sans-serif;
  color: #333;
  background: #F8F8F8;
  -webkit-font-smoothing: antialiased;
}
a {
  color: #C8102E;
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
```

- [ ] **Step 8: 验证 TypeScript 编译通过**

Run: `cd /home/ln/data/Code/html/YuShenCuisine/web && npx vue-tsc --noEmit`
Expected: 无类型错误

- [ ] **Step 9: Commit**

```bash
cd /home/ln/data/Code/html/YuShenCuisine
git add web/src/types/ web/src/router/ web/src/stores/ web/data/ web/src/assets/styles/
git commit -m "feat: add types, router, store, and mock data"
```

---

### Task 3: SearchBar + FilterBar 组件

**Files:**
- Create: `web/src/components/SearchBar.vue`
- Create: `web/src/components/FilterBar.vue`

- [ ] **Step 1: 创建 SearchBar.vue**

```vue
<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useRestaurantStore } from '../stores/restaurant'
import debounce from 'lodash.debounce'

const store = useRestaurantStore()
const router = useRouter()
const keyword = ref(store.searchKeyword)

const debouncedSearch = debounce((val: string) => {
  store.searchKeyword = val
}, 300)

watch(keyword, (val) => {
  debouncedSearch(val)
})

function handleSearch() {
  if (keyword.value.trim()) {
    store.searchKeyword = keyword.value.trim()
    router.push('/list')
  }
}

function clearSearch() {
  keyword.value = ''
  store.searchKeyword = ''
}
</script>

<template>
  <div class="search-bar">
    <el-input
      v-model="keyword"
      placeholder="搜索店名、分类、区域..."
      clearable
      @clear="clearSearch"
      @keyup.enter="handleSearch"
    >
      <template #prefix>
        <el-icon><Search /></el-icon>
      </template>
    </el-input>
  </div>
</template>

<style scoped>
.search-bar {
  flex: 1;
  max-width: 400px;
}
.search-bar :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.15);
  border: none;
  box-shadow: none;
}
.search-bar :deep(.el-input__inner) {
  color: white;
}
.search-bar :deep(.el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.7);
}
.search-bar :deep(.el-input__prefix) {
  color: rgba(255, 255, 255, 0.7);
}
.search-bar :deep(.el-input__clear) {
  color: rgba(255, 255, 255, 0.7);
}
</style>
```

- [ ] **Step 2: 创建 FilterBar.vue**

```vue
<script setup lang="ts">
import { useRestaurantStore } from '../stores/restaurant'

const store = useRestaurantStore()

function setDistrict(d: string) {
  store.filterDistrict = d
}

function setCategory(c: string) {
  store.filterCategory = c
}

function clearAll() {
  store.filterDistrict = ''
  store.filterCategory = ''
  store.searchKeyword = ''
}
</script>

<template>
  <div class="filter-bar" v-if="store.districts.length > 0">
    <div class="filter-row">
      <span class="filter-label">区域</span>
      <div class="filter-tags">
        <el-tag
          :type="store.filterDistrict === '' ? 'danger' : 'info'"
          effect="plain"
          @click="setDistrict('')"
          style="cursor:pointer"
        >
          全部
        </el-tag>
        <el-tag
          v-for="d in store.districts"
          :key="d"
          :type="store.filterDistrict === d ? 'danger' : 'info'"
          effect="plain"
          @click="setDistrict(d)"
          style="cursor:pointer"
        >
          {{ d }}
        </el-tag>
      </div>
    </div>
    <div class="filter-row">
      <span class="filter-label">分类</span>
      <div class="filter-tags">
        <el-tag
          :type="store.filterCategory === '' ? 'danger' : 'info'"
          effect="plain"
          @click="setCategory('')"
          style="cursor:pointer"
        >
          全部
        </el-tag>
        <el-tag
          v-for="c in store.categories"
          :key="c"
          :type="store.filterCategory === c ? 'danger' : 'info'"
          effect="plain"
          @click="setCategory(c)"
          style="cursor:pointer"
        >
          {{ c }}
        </el-tag>
      </div>
    </div>
  </div>
</template>

<style scoped>
.filter-bar {
  background: white;
  border-bottom: 1px solid #eee;
  padding: 8px 16px;
}
.filter-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}
.filter-row:last-child {
  margin-bottom: 0;
}
.filter-label {
  font-size: 12px;
  color: #999;
  white-space: nowrap;
  width: 36px;
}
.filter-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
</style>
```

- [ ] **Step 3: Commit**

```bash
cd /home/ln/data/Code/html/YuShenCuisine
git add web/src/components/SearchBar.vue web/src/components/FilterBar.vue
git commit -m "feat: add SearchBar and FilterBar components"
```

---

### Task 4: HomePage 首页

**Files:**
- Create: `web/src/views/HomePage.vue`
- Create: `web/src/components/HotCategories.vue`

- [ ] **Step 1: 创建 views/HomePage.vue**

```vue
<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useRestaurantStore } from '../stores/restaurant'
import HotCategories from '../components/HotCategories.vue'

const store = useRestaurantStore()
const router = useRouter()

onMounted(() => {
  if (store.all.length === 0 && !store.loading) {
    store.fetchAll()
  }
})

function goToList() {
  router.push('/list')
}

function goToMap() {
  router.push('/map')
}
</script>

<template>
  <div class="home-page">
    <section class="hero">
      <h1 class="hero-title">🥟 深圳河南美食地图</h1>
      <p class="hero-subtitle">在深圳，找到家乡的味道</p>
      <div class="hero-actions">
        <el-button type="danger" size="large" @click="goToList">
          <el-icon style="margin-right:4px"><List /></el-icon>
          查看全部店铺
        </el-button>
        <el-button plain size="large" @click="goToMap">
          <el-icon style="margin-right:4px"><MapLocation /></el-icon>
          地图分布
        </el-button>
      </div>
    </section>

    <HotCategories />

    <section class="stats" v-if="!store.loading">
      <el-card shadow="never">
        <div class="stats-inner">
          <div class="stat-item">
            <span class="stat-num">{{ store.all.length }}</span>
            <span class="stat-label">收录店铺</span>
          </div>
          <div class="stat-item">
            <span class="stat-num">{{ store.districts.length }}</span>
            <span class="stat-label">覆盖区域</span>
          </div>
          <div class="stat-item">
            <span class="stat-num">{{ store.categories.length }}</span>
            <span class="stat-label">美食分类</span>
          </div>
        </div>
      </el-card>
    </section>

    <section class="about">
      <el-card shadow="never">
        <h3>关于本站</h3>
        <p>深圳聚集了大量河南籍人口，但寻找地道的河南菜馆却并不容易。本网站收录了深圳市各区河南餐馆信息，帮你快速找到家乡味道。</p>
        <p class="about-note">数据来源于高德地图，如有遗漏或错误欢迎反馈。</p>
      </el-card>
    </section>
  </div>
</template>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.hero {
  text-align: center;
  padding: 48px 16px 32px;
}
.hero-title {
  font-size: 32px;
  font-weight: 700;
  color: #C8102E;
  margin-bottom: 8px;
}
.hero-subtitle {
  font-size: 16px;
  color: #666;
  margin-bottom: 24px;
}
.hero-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
}
.stats-inner {
  display: flex;
  justify-content: space-around;
  text-align: center;
}
.stat-item {
  display: flex;
  flex-direction: column;
}
.stat-num {
  font-size: 28px;
  font-weight: 700;
  color: #C8102E;
}
.stat-label {
  font-size: 13px;
  color: #999;
  margin-top: 2px;
}
.about h3 {
  font-size: 16px;
  margin-bottom: 8px;
  color: #C8102E;
}
.about p {
  font-size: 14px;
  color: #555;
  line-height: 1.8;
}
.about-note {
  margin-top: 8px;
  font-size: 12px;
  color: #999;
}
</style>
```

- [ ] **Step 2: 创建 components/HotCategories.vue**

```vue
<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useRestaurantStore } from '../stores/restaurant'

const store = useRestaurantStore()
const router = useRouter()

const categories = [
  { name: '烩面', icon: '🍜' },
  { name: '胡辣汤', icon: '🥣' },
  { name: '灌汤包', icon: '🥟' },
  { name: '羊肉汤', icon: '🍲' },
  { name: '河南菜', icon: '🍳' }
]

function goToCategory(cat: string) {
  store.filterCategory = cat
  store.searchKeyword = ''
  router.push('/list')
}
</script>

<template>
  <section class="hot-categories">
    <h3 class="section-title">热门分类</h3>
    <div class="category-grid">
      <div
        v-for="c in categories"
        :key="c.name"
        class="category-card"
        @click="goToCategory(c.name)"
      >
        <span class="category-icon">{{ c.icon }}</span>
        <span class="category-name">{{ c.name }}</span>
      </div>
    </div>
  </section>
</template>

<style scoped>
.section-title {
  font-size: 16px;
  margin-bottom: 12px;
  color: #333;
}
.category-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
}
.category-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 12px;
  background: white;
  border-radius: 12px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.category-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(200,16,46,0.12);
}
.category-icon {
  font-size: 32px;
  margin-bottom: 8px;
}
.category-name {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}
</style>
```

- [ ] **Step 3: Commit**

```bash
cd /home/ln/data/Code/html/YuShenCuisine
git add web/src/views/HomePage.vue web/src/components/HotCategories.vue
git commit -m "feat: add HomePage with hero and hot categories"
```

---

### Task 5: ListPage 列表页 + RestaurantCard

**Files:**
- Create: `web/src/views/ListPage.vue`
- Create: `web/src/components/RestaurantCard.vue`

- [ ] **Step 1: 创建 components/RestaurantCard.vue**

```vue
<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { Restaurant } from '../types/restaurant'

const props = defineProps<{ restaurant: Restaurant }>()
const router = useRouter()

function goDetail() {
  router.push(`/detail/${props.restaurant.id}`)
}
</script>

<template>
  <div class="restaurant-card" @click="goDetail">
    <div class="card-body">
      <h3 class="card-name">{{ restaurant.name }}</h3>
      <div class="card-meta">
        <span class="meta-district">{{ restaurant.district }}</span>
        <span class="meta-rating" v-if="restaurant.rating">
          <el-icon style="color:#F59E0B;vertical-align:text-bottom"><StarFilled /></el-icon>
          {{ restaurant.rating }}
        </span>
        <span class="meta-cost" v-if="restaurant.cost">
          ¥{{ restaurant.cost }}/人
        </span>
      </div>
      <p class="card-address">{{ restaurant.address }}</p>
      <div class="card-tags">
        <el-tag
          v-for="tag in restaurant.tags"
          :key="tag"
          size="small"
          type="danger"
          effect="light"
        >
          {{ tag }}
        </el-tag>
      </div>
    </div>
  </div>
</template>

<style scoped>
.restaurant-card {
  background: white;
  border-radius: 8px;
  padding: 14px 16px;
  cursor: pointer;
  transition: box-shadow 0.2s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.restaurant-card:hover {
  box-shadow: 0 2px 8px rgba(200,16,46,0.10);
}
.card-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
}
.card-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: #666;
  margin-bottom: 6px;
}
.meta-district {
  background: #FFF0F0;
  color: #C8102E;
  padding: 1px 8px;
  border-radius: 4px;
  font-size: 12px;
}
.card-address {
  font-size: 13px;
  color: #999;
  margin-bottom: 8px;
  line-height: 1.4;
}
.card-tags {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}
</style>
```

- [ ] **Step 2: 创建 views/ListPage.vue**

```vue
<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { useRestaurantStore } from '../stores/restaurant'
import RestaurantCard from '../components/RestaurantCard.vue'

const store = useRestaurantStore()
const currentPage = ref(1)
const pageSize = 20

onMounted(() => {
  if (store.all.length === 0 && !store.loading) {
    store.fetchAll()
  }
})

const paginatedList = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return store.filtered.slice(start, start + pageSize)
})

const totalPages = computed(() => Math.ceil(store.filtered.length / pageSize))

function handlePageChange(page: number) {
  currentPage.value = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<template>
  <div class="list-page">
    <div class="list-header">
      <h2 class="list-title">
        全部店铺
        <span class="list-count" v-if="!store.loading">
          （{{ store.filtered.length }} 家）
        </span>
      </h2>
      <el-button
        v-if="store.filterDistrict || store.filterCategory || store.searchKeyword"
        text
        type="danger"
        @click="store.filterDistrict=''; store.filterCategory=''; store.searchKeyword=''"
      >
        清除筛选
      </el-button>
    </div>

    <div v-if="store.loading" class="loading-state">
      <el-skeleton :rows="5" animated />
    </div>

    <div v-else-if="store.error" class="error-state">
      <el-result icon="error" title="加载失败" :sub-title="store.error">
        <template #extra>
          <el-button type="danger" @click="store.fetchAll()">重试</el-button>
        </template>
      </el-result>
    </div>

    <div v-else-if="store.filtered.length === 0" class="empty-state">
      <el-result icon="info" title="没有找到相关店铺">
        <template #extra>
          <p class="empty-hint">试试其他关键词或清除筛选条件</p>
        </template>
      </el-result>
    </div>

    <template v-else>
      <div class="restaurant-grid">
        <RestaurantCard
          v-for="r in paginatedList"
          :key="r.id"
          :restaurant="r"
        />
      </div>

      <div class="pagination-wrap" v-if="totalPages > 1">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="store.filtered.length"
          layout="prev, pager, next"
          @current-change="handlePageChange"
        />
      </div>
    </template>
  </div>
</template>

<style scoped>
.list-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.list-title {
  font-size: 18px;
  font-weight: 600;
}
.list-count {
  font-size: 14px;
  color: #999;
  font-weight: 400;
}
.restaurant-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.loading-state, .error-state, .empty-state {
  padding: 40px 0;
}
.empty-hint {
  font-size: 14px;
  color: #999;
}
.pagination-wrap {
  display: flex;
  justify-content: center;
  padding: 16px 0;
}
</style>
```

- [ ] **Step 3: Commit**

```bash
cd /home/ln/data/Code/html/YuShenCuisine
git add web/src/views/ListPage.vue web/src/components/RestaurantCard.vue
git commit -m "feat: add ListPage with pagination and RestaurantCard"
```

---

### Task 6: DetailPage 详情页 + NavButton

**Files:**
- Create: `web/src/views/DetailPage.vue`
- Create: `web/src/components/NavButton.vue`

- [ ] **Step 1: 创建 components/NavButton.vue**

```vue
<script setup lang="ts">
import { ElMessage } from 'element-plus'

const props = defineProps<{
  longitude: number
  latitude: number
  address: string
  name: string
}>()

function navigateByAmap() {
  const url = `amap://route?from=&to=${props.longitude},${props.latitude}&name=${encodeURIComponent(props.name)}&mode=transit`
  window.location.href = url
  // 如果 APP 未安装，3 秒后跳转 Web 版
  setTimeout(() => {
    const webUrl = `https://uri.amap.com/navigation?to=${props.longitude},${props.latitude},${encodeURIComponent(props.name)}&mode=transit&coordinate=gaode`
    window.open(webUrl, '_blank')
  }, 3000)
}

function navigateByWeb() {
  const url = `https://uri.amap.com/navigation?to=${props.longitude},${props.latitude},${encodeURIComponent(props.name)}&mode=transit&coordinate=gaode`
  window.open(url, '_blank')
}

function copyAddress() {
  navigator.clipboard.writeText(props.address).then(() => {
    ElMessage.success('地址已复制')
  }).catch(() => {
    ElMessage.warning('复制失败，请手动记下地址')
  })
}
</script>

<template>
  <div class="nav-actions">
    <el-button type="danger" size="large" @click="navigateByAmap" class="nav-btn">
      <el-icon style="margin-right:4px"><Location /></el-icon>
      导航到店（高德 APP）
    </el-button>
    <el-button plain size="large" @click="navigateByWeb" class="nav-btn">
      <el-icon style="margin-right:4px"><Guide /></el-icon>
      高德 Web 版
    </el-button>
    <el-button text size="large" @click="copyAddress">
      <el-icon style="margin-right:4px"><CopyDocument /></el-icon>
      复制地址
    </el-button>
  </div>
</template>

<style scoped>
.nav-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}
.nav-btn {
  flex: 1;
  min-width: 120px;
}
</style>
```

- [ ] **Step 2: 创建 views/DetailPage.vue**

```vue
<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useRestaurantStore } from '../stores/restaurant'
import NavButton from '../components/NavButton.vue'

const route = useRoute()
const router = useRouter()
const store = useRestaurantStore()

const restaurant = computed(() => store.getById(route.params.id as string))

// 如果 store 还没加载，触发加载
import { onMounted } from 'vue'
onMounted(() => {
  if (!restaurant.value && !store.loading) {
    store.fetchAll()
  }
})
</script>

<template>
  <div class="detail-page">
    <el-button text @click="router.back()" class="back-btn">
      <el-icon><ArrowLeft /></el-icon>
      返回
    </el-button>

    <div v-if="store.loading && !restaurant" class="loading-state">
      <el-skeleton :rows="6" animated />
    </div>

    <div v-else-if="!restaurant" class="error-state">
      <el-result icon="warning" title="店铺不存在">
        <template #extra>
          <el-button type="danger" @click="router.push('/list')">
            返回列表
          </el-button>
        </template>
      </el-result>
    </div>

    <template v-else>
      <div class="detail-header">
        <div class="cover-placeholder" v-if="!restaurant.cover">
          <span class="cover-emoji">🥟</span>
        </div>
        <h1 class="detail-name">{{ restaurant.name }}</h1>
      </div>

      <el-card shadow="never" class="info-card">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="区域" label-class-name="desc-label">
            <el-tag type="danger" effect="light">{{ restaurant.district }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="地址">
            {{ restaurant.address }}
          </el-descriptions-item>
          <el-descriptions-item label="电话" v-if="restaurant.phone">
            <a :href="`tel:${restaurant.phone}`" class="phone-link">{{ restaurant.phone }}</a>
          </el-descriptions-item>
          <el-descriptions-item label="评分" v-if="restaurant.rating">
            <el-rate :model-value="restaurant.rating" disabled show-score :max="5" score-template="{value}" />
          </el-descriptions-item>
          <el-descriptions-item label="人均" v-if="restaurant.cost">
            ¥{{ restaurant.cost }}
          </el-descriptions-item>
          <el-descriptions-item label="分类">
            <el-tag
              v-for="tag in restaurant.tags"
              :key="tag"
              type="danger"
              effect="light"
              style="margin-right:4px"
            >
              {{ tag }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="收录来源">
            <span class="source-text">通过「{{ restaurant.source_keyword }}」收录</span>
          </el-descriptions-item>
        </el-descriptions>
      </el-card>

      <el-card shadow="never" class="nav-card">
        <h3 class="nav-title">📍 位置与导航</h3>
        <p class="nav-address">{{ restaurant.address }}</p>
        <NavButton
          :longitude="restaurant.longitude"
          :latitude="restaurant.latitude"
          :address="restaurant.address"
          :name="restaurant.name"
        />
      </el-card>
    </template>
  </div>
</template>

<style scoped>
.detail-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.back-btn {
  align-self: flex-start;
}
.loading-state, .error-state {
  padding: 40px 0;
}
.detail-header {
  text-align: center;
}
.cover-placeholder {
  width: 80px;
  height: 80px;
  background: #FFF0F0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
}
.cover-emoji {
  font-size: 36px;
}
.detail-name {
  font-size: 24px;
  font-weight: 700;
  color: #333;
}
.info-card, .nav-card {
  border-radius: 12px;
}
:deep(.desc-label) {
  font-weight: 500;
}
.phone-link {
  color: #C8102E;
  font-weight: 500;
}
.source-text {
  color: #999;
  font-size: 13px;
}
.nav-title {
  font-size: 16px;
  margin-bottom: 4px;
}
.nav-address {
  font-size: 14px;
  color: #666;
  margin-bottom: 12px;
}
</style>
```

- [ ] **Step 3: Commit**

```bash
cd /home/ln/data/Code/html/YuShenCuisine
git add web/src/views/DetailPage.vue web/src/components/NavButton.vue
git commit -m "feat: add DetailPage with navigation buttons"
```

---

### Task 7: StaticMap + MapMarker + MarkerPopup + MapPage

**Files:**
- Create: `web/src/utils/coordinates.ts`
- Create: `web/src/components/StaticMap.vue`
- Create: `web/src/components/MapMarker.vue`
- Create: `web/src/components/MarkerPopup.vue`
- Create: `web/src/views/MapPage.vue`

- [ ] **Step 1: 创建 utils/coordinates.ts**

```typescript
// 深圳地图边界（与底图截图对应）
export const SHENZHEN_BBOX = {
  minLng: 113.75,
  maxLng: 114.65,
  minLat: 22.40,
  maxLat: 22.85
}

// 地图图片尺寸（与 shenzhen-map.png 对应，CSS 像素）
export const MAP_IMAGE_WIDTH = 900
export const MAP_IMAGE_HEIGHT = 500

export interface PixelCoord {
  x: number
  y: number
}

/**
 * 将经纬度转换为静态地图上的像素坐标
 * 假设底图使用的坐标系与数据一致（推荐使用高德截图，均为 GCJ-02）
 */
export function lngLatToPixel(
  lng: number,
  lat: number
): PixelCoord {
  const { minLng, maxLng, minLat, maxLat } = SHENZHEN_BBOX
  const x = ((lng - minLng) / (maxLng - minLng)) * MAP_IMAGE_WIDTH
  const y = ((maxLat - lat) / (maxLat - minLat)) * MAP_IMAGE_HEIGHT
  return { x, y }
}

/**
 * 检查坐标是否在深圳地图边界内
 */
export function isInBounds(lng: number, lat: number): boolean {
  return (
    lng >= SHENZHEN_BBOX.minLng &&
    lng <= SHENZHEN_BBOX.maxLng &&
    lat >= SHENZHEN_BBOX.minLat &&
    lat <= SHENZHEN_BBOX.maxLat
  )
}
```

- [ ] **Step 2: 创建 components/MapMarker.vue**

```vue
<script setup lang="ts">
import type { Restaurant } from '../types/restaurant'
import { lngLatToPixel } from '../utils/coordinates'

const props = defineProps<{ restaurant: Restaurant }>()
const emit = defineEmits<{ click: [Restaurant] }>()

const pos = lngLatToPixel(props.restaurant.longitude, props.restaurant.latitude)
</script>

<template>
  <div
    class="map-marker"
    :style="{ left: pos.x + 'px', top: pos.y + 'px' }"
    @click.stop="emit('click', restaurant)"
    :title="restaurant.name"
  >
    🥟
  </div>
</template>

<style scoped>
.map-marker {
  position: absolute;
  font-size: 20px;
  cursor: pointer;
  transform: translate(-50%, -100%);
  transition: transform 0.15s;
  z-index: 2;
  filter: drop-shadow(0 1px 3px rgba(0,0,0,0.3));
  line-height: 1;
}
.map-marker:hover {
  transform: translate(-50%, -100%) scale(1.3);
  z-index: 10;
}
</style>
```

- [ ] **Step 3: 创建 components/MarkerPopup.vue**

```vue
<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { Restaurant } from '../types/restaurant'
import { lngLatToPixel } from '../utils/coordinates'

const props = defineProps<{ restaurant: Restaurant }>()
const emit = defineEmits<{ close: [] }>()
const router = useRouter()

const pos = lngLatToPixel(props.restaurant.longitude, props.restaurant.latitude)

function goDetail() {
  router.push(`/detail/${props.restaurant.id}`)
}
</script>

<template>
  <div
    class="marker-popup"
    :style="{ left: pos.x + 'px', top: pos.y - 10 + 'px' }"
  >
    <div class="popup-inner">
      <button class="popup-close" @click.stop="emit('close')">×</button>
      <h4 class="popup-name">{{ restaurant.name }}</h4>
      <div class="popup-meta">
        <span class="popup-district">{{ restaurant.district }}</span>
        <span v-if="restaurant.rating" class="popup-rating">
          ⭐ {{ restaurant.rating }}
        </span>
      </div>
      <el-button size="small" type="danger" @click="goDetail" style="margin-top:8px;width:100%">
        查看详情
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.marker-popup {
  position: absolute;
  z-index: 20;
  transform: translate(-50%, -100%);
}
.popup-inner {
  background: white;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
  min-width: 160px;
  position: relative;
}
.popup-close {
  position: absolute;
  top: 4px;
  right: 8px;
  border: none;
  background: none;
  font-size: 18px;
  cursor: pointer;
  color: #999;
  line-height: 1;
}
.popup-name {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 4px;
  padding-right: 16px;
}
.popup-meta {
  display: flex;
  gap: 8px;
  font-size: 12px;
  color: #666;
}
.popup-district {
  background: #FFF0F0;
  color: #C8102E;
  padding: 0 6px;
  border-radius: 3px;
}
</style>
```

- [ ] **Step 4: 创建 components/StaticMap.vue**

```vue
<script setup lang="ts">
import type { Restaurant } from '../types/restaurant'

defineProps<{ restaurants: Restaurant[] }>()
</script>

<template>
  <div class="static-map">
    <div class="map-wrapper">
      <img
        src="/shenzhen-henan-food/images/shenzhen-map.png"
        alt="深圳地图"
        class="map-image"
        @error="onImageError"
      />
      <div class="markers-layer">
        <slot :restaurants="restaurants" />
      </div>
      <div v-if="mapLoaded === false" class="map-error-overlay">
        <p>地图底图加载失败</p>
      </div>
    </div>
    <p class="map-attribution">© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap contributors</a></p>
  </div>
</template>

<script lang="ts">
import { ref } from 'vue'

export default {
  setup() {
    const mapLoaded = ref<boolean | null>(null)
    const onImageError = () => {
      mapLoaded.value = false
    }
    return { mapLoaded, onImageError }
  }
}
</script>

<style scoped>
.static-map {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.map-wrapper {
  position: relative;
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
}
.map-image {
  width: 100%;
  height: auto;
  display: block;
  border-radius: 8px;
}
.markers-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}
.markers-layer > * {
  pointer-events: auto;
}
.map-error-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border-radius: 8px;
  color: #999;
  font-size: 14px;
}
.map-attribution {
  text-align: right;
  font-size: 11px;
  color: #bbb;
}
.map-attribution a {
  color: #bbb;
  text-decoration: underline;
}
</style>
```

- [ ] **Step 5: 创建 views/MapPage.vue**

```vue
<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRestaurantStore } from '../stores/restaurant'
import StaticMap from '../components/StaticMap.vue'
import MapMarker from '../components/MapMarker.vue'
import MarkerPopup from '../components/MarkerPopup.vue'
import type { Restaurant } from '../types/restaurant'
import { useRouter } from 'vue-router'

const store = useRestaurantStore()
const router = useRouter()
const selectedRestaurant = ref<Restaurant | null>(null)

onMounted(() => {
  if (store.all.length === 0 && !store.loading) {
    store.fetchAll()
  }
})

function onMarkerClick(r: Restaurant) {
  selectedRestaurant.value = r
}

function closePopup() {
  selectedRestaurant.value = null
}
</script>

<template>
  <div class="map-page">
    <div class="map-header">
      <h2 class="map-title">深圳河南美食分布</h2>
      <p class="map-subtitle" v-if="!store.loading">共 {{ store.all.length }} 家店铺</p>
    </div>

    <div v-if="store.loading" class="loading-state">
      <el-skeleton :rows="3" animated />
    </div>

    <div v-else-if="store.error" class="error-state">
      <el-result icon="error" title="加载失败" :sub-title="store.error">
        <template #extra>
          <el-button type="danger" @click="store.fetchAll()">重试</el-button>
        </template>
      </el-result>
    </div>

    <template v-else>
      <StaticMap :restaurants="store.all">
        <template #default>
          <MapMarker
            v-for="r in store.all"
            :key="r.id"
            :restaurant="r"
            @click="onMarkerClick"
          />
          <MarkerPopup
            v-if="selectedRestaurant"
            :restaurant="selectedRestaurant"
            @close="closePopup"
          />
        </template>
      </StaticMap>
    </template>
  </div>
</template>

<style scoped>
.map-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.map-header {
  text-align: center;
}
.map-title {
  font-size: 20px;
  font-weight: 600;
}
.map-subtitle {
  font-size: 14px;
  color: #999;
  margin-top: 4px;
}
.loading-state, .error-state {
  padding: 40px 0;
}
</style>
```

- [ ] **Step 6: 生成占位底图（用于开发阶段）**

由于静态地图底图需要用户自行截图，先创建一个纯色占位图。用户后续替换即可。

Run:
```bash
cat > /home/ln/data/Code/html/YuShenCuisine/web/public/images/shenzhen-map.png << 'EOF'
PLACEHOLDER: Replace this file with a screenshot of Shenzhen map.
Recommended: Take a screenshot from 高德地图 (GCJ-02 coordinates match).
Save as PNG, suggested size ~900x500px.
EOF
```

> 注意：这只是占位文件。用户需要手动截取一张深圳地图保存到此路径。推荐使用高德地图截图（GCJ-02 坐标系，与 API 返回的坐标一致）。参考 `docs/豫深美食设计文档.md` 第 25 章附录说明。

- [ ] **Step 7: Commit**

```bash
cd /home/ln/data/Code/html/YuShenCuisine
git add web/src/utils/coordinates.ts web/src/components/StaticMap.vue web/src/components/MapMarker.vue web/src/components/MarkerPopup.vue web/src/views/MapPage.vue web/public/images/
git commit -m "feat: add static map page with markers and popup"
```

---

### Task 8: Python 数据采集脚本

**Files:**
- Create: `crawler/config.py`
- Create: `crawler/crawl.py`
- Create: `scripts/sync-data.sh`

- [ ] **Step 1: 创建 crawler/config.py**

```python
"""高德 API 配置与采集参数"""

# 高德 Web API Key
# 使用前请替换为你的实际 Key
AMAP_KEY = "your_amap_key_here"

# API 地址
AMAP_URL = "https://restapi.amap.com/v5/place/text"

# 采集行政区（短名称）
DISTRICTS = [
    "福田", "罗湖", "南山", "盐田", "宝安",
    "龙岗", "龙华", "坪山", "光明", "大鹏"
]

# 采集关键词
KEYWORDS = [
    "河南菜", "河南饭店", "河南餐馆", "河南面馆", "河南烩面",
    "郑州烩面", "羊肉烩面", "胡辣汤",
    "开封灌汤包", "洛阳水席", "信阳菜", "周口菜", "驻马店菜", "安阳菜"
]

# 标签推断规则
# key: 店名中包含的关键词, value: 对应标签
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
    """从店名推断分类标签"""
    tags = set()
    for keyword, tag in TAG_RULES.items():
        if keyword in name:
            tags.add(tag)
    if not tags:
        tags.add("河南菜")
    return sorted(tags)
```

- [ ] **Step 2: 创建 crawler/crawl.py**

```python
#!/usr/bin/env python3
"""
高德地图 POI 采集脚本

使用高德 Web API v5/place/text 搜索深圳河南菜馆。
一次性全量采集，输出到 output/restaurants.json。

用法：
    export AMAP_KEY="your_key"
    python crawler/crawl.py

或者直接修改 config.py 中的 AMAP_KEY。
"""

import json
import os
import sys
import time
from datetime import datetime

import requests

from config import AMAP_KEY, AMAP_URL, DISTRICTS, KEYWORDS, infer_tags

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "restaurants.json")


def fetch_pois(keyword: str, region: str) -> list:
    """调用高德 API 搜索 POI，返回店铺列表"""
    pois = []
    page_num = 1

    while True:
        params = {
            "key": AMAP_KEY,
            "keywords": keyword,
            "region": region,
            "page_size": 25,
            "page_num": page_num,
        }
        try:
            resp = requests.get(AMAP_URL, params=params, timeout=15)
            data = resp.json()
        except Exception as e:
            print(f"  [ERROR] 请求失败: {e}", file=sys.stderr)
            break

        if data.get("status") != "1":
            print(f"  [WARN] API 返回异常: {data.get('info', 'unknown')}", file=sys.stderr)
            break

        batch = data.get("pois", [])
        if not batch:
            break

        for poi in batch:
            # 只保留餐饮类 POI
            if "餐饮" not in poi.get("type", ""):
                continue

            # 解析坐标
            location = poi.get("location", "")
            if not location:
                continue
            try:
                lng, lat = map(float, location.split(","))
            except ValueError:
                continue

            # 解析评分和人均消费
            rating = poi.get("biz_ext", {}).get("rating", "")
            cost = poi.get("biz_ext", {}).get("cost", "")
            update_time = poi.get("update_time", "")

            restaurant = {
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
                "update_time": update_time or datetime.now().strftime("%Y-%m-%d"),
            }
            pois.append(restaurant)

        # 检查是否还有更多页
        total = int(data.get("count", 0))
        if page_num * 25 >= total:
            break
        page_num += 1
        time.sleep(0.3)  # 避免触发限流

    return pois


def deduplicate(pois: list) -> list:
    """按 poi_id 或 店名+地址 去重"""
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

    api_key = os.environ.get("AMAP_KEY") or AMAP_KEY
    if api_key == "your_amap_key_here":
        print("错误：请先设置 AMAP_KEY（环境变量或 config.py）", file=sys.stderr)
        sys.exit(1)

    all_pois = []
    total_queries = len(KEYWORDS) * len(DISTRICTS)
    current = 0

    print(f"开始采集，共 {total_queries} 个组合（{len(KEYWORDS)} 关键词 × {len(DISTRICTS)} 区）")
    print("-" * 40)

    for keyword in KEYWORDS:
        for region in DISTRICTS:
            current += 1
            print(f"[{current}/{total_queries}] {keyword} × {region}")
            pois = fetch_pois(keyword, region)
            all_pois.extend(pois)
            print(f"  → 获取 {len(pois)} 条")
            time.sleep(0.2)  # 请求间隔

    print("-" * 40)
    print(f"去重前: {len(all_pois)} 条")
    unique = deduplicate(all_pois)
    print(f"去重后: {len(unique)} 条")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(unique, f, ensure_ascii=False, indent=2)

    print(f"已保存到: {OUTPUT_FILE}")
    print("采集完成！")


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: 创建 scripts/sync-data.sh**

```bash
#!/bin/bash
# 数据同步脚本
# 将 crawler/output/restaurants.json 整理到 web/data/
# 并生成 districts.json 和 categories.json

set -e

CRAWLER_OUTPUT="crawler/output/restaurants.json"
DATA_DIR="web/data"

if [ ! -f "$CRAWLER_OUTPUT" ]; then
    echo "错误：未找到 $CRAWLER_OUTPUT"
    echo "请先运行 python crawler/crawl.py"
    exit 1
fi

mkdir -p "$DATA_DIR"

# 复制原始数据
cp "$CRAWLER_OUTPUT" "$DATA_DIR/restaurants.json"
echo "✔ 已复制 restaurants.json"

# 提取行政区列表（去重排序）
python3 -c "
import json

with open('$DATA_DIR/restaurants.json') as f:
    data = json.load(f)

districts = sorted(set(r['district'] for r in data if r.get('district')))
with open('$DATA_DIR/districts.json', 'w') as f:
    json.dump(districts, f, ensure_ascii=False, indent=2)

# 提取分类列表（去重排序）
categories = sorted(set(tag for r in data for tag in r.get('tags', [])))
with open('$DATA_DIR/categories.json', 'w') as f:
    json.dump(categories, f, ensure_ascii=False, indent=2)

print(f'✔ 已生成 districts.json（{len(districts)} 个区）')
print(f'✔ 已生成 categories.json（{len(categories)} 个分类）')
"
```

- [ ] **Step 4: 设置脚本执行权限**

Run:
```bash
chmod +x /home/ln/data/Code/html/YuShenCuisine/scripts/sync-data.sh
```

- [ ] **Step 5: Commit**

```bash
cd /home/ln/data/Code/html/YuShenCuisine
git add crawler/ scripts/
git commit -m "feat: add Python data collection script and sync script"
```

---

### Task 9: 样式统一 + App.vue 集成

**Files:**
- Modify: `web/src/App.vue`（添加骨架屏加载逻辑 + useRestaurantStore 初始化）
- Modify: `web/src/main.ts`（确保 store 初始化逻辑）

- [ ] **Step 1: 更新 App.vue 添加初始化逻辑**

```vue
<script setup lang="ts">
import { onMounted } from 'vue'
import { useRestaurantStore } from './stores/restaurant'
import SearchBar from './components/SearchBar.vue'
import FilterBar from './components/FilterBar.vue'

const store = useRestaurantStore()

onMounted(() => {
  if (store.all.length === 0 && !store.loading) {
    store.fetchAll()
  }
})
</script>

<template>
  <div class="app-container">
    <header class="app-header">
      <div class="header-inner">
        <router-link to="/" class="logo">
          <span class="logo-icon">🥟</span>
          <span class="logo-text">深圳河南美食地图</span>
        </router-link>
        <SearchBar />
      </div>
    </header>

    <FilterBar />

    <main class="app-main">
      <router-view />
    </main>

    <footer class="app-footer">
      <p>🥟 深圳河南美食地图 · 数据来源于高德地图</p>
    </footer>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #F8F8F8;
}
.app-header {
  background: #C8102E;
  color: white;
  padding: 0 16px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 16px;
  height: 56px;
}
.logo {
  display: flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  color: white;
  white-space: nowrap;
}
.logo-icon {
  font-size: 24px;
}
.logo-text {
  font-size: 18px;
  font-weight: 600;
}
.app-main {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px;
  width: 100%;
}
.app-footer {
  text-align: center;
  padding: 16px;
  font-size: 12px;
  color: #ccc;
  background: white;
  border-top: 1px solid #eee;
}
</style>
```

- [ ] **Step 2: 验证构建通过**

Run: `cd /home/ln/data/Code/html/YuShenCuisine/web && npx vue-tsc --noEmit && npx vite build`
Expected: 构建成功，无报错

- [ ] **Step 3: Commit**

```bash
cd /home/ln/data/Code/html/YuShenCuisine
git add web/src/App.vue
git commit -m "feat: integrate App.vue with data loading and footer"
```

---

### Task 10: GitHub Pages 部署配置 + README

**Files:**
- Create: `.github/workflows/deploy.yml`
- Create: `web/public/.nojekyll`
- Create: `README.md`

- [ ] **Step 1: 创建 .github/workflows/deploy.yml**

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}

    defaults:
      run:
        working-directory: web

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: web/package-lock.json

      - run: npm ci

      - name: Build
        run: npm run build

      - uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: web/dist

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 2: 创建 web/public/.nojekyll**

```
（空文件。创建此文件告知 GitHub Pages 不要用 Jekyll 处理站点。）
```

Run: `touch /home/ln/data/Code/html/YuShenCuisine/web/public/.nojekyll`

- [ ] **Step 3: 创建 README.md**

```markdown
# 🥟 深圳河南美食地图

在深圳，找到家乡的味道。

## 功能

- 查看深圳河南餐馆分布地图
- 搜索河南美食（店名 / 分类 / 区域）
- 筛选（区域 + 分类）
- 店铺详情（地址、电话、评分、导航）

## 技术栈

- **前端：** Vue 3 + TypeScript + Vite + Element Plus
- **数据采集：** Python 3 + 高德 Web API
- **地图：** 静态底图 + CSS 标记
- **部署：** GitHub Pages

## 数据

数据通过高德地图 Web API `v5/place/text` 采集。采集后手动更新，不设自动任务。

## 本地开发

```bash
cd web
npm install
npm run dev
```

## 数据更新流程

```bash
# 1. 设置 API Key
export AMAP_KEY="your_key"

# 2. 采集
python crawler/crawl.py

# 3. 整理数据
bash scripts/sync-data.sh
```

## 预览

[深圳河南美食地图](https://你的用户名.github.io/shenzhen-henan-food/)
```

- [ ] **Step 4: Commit**

```bash
cd /home/ln/data/Code/html/YuShenCuisine
git add .github/ web/public/.nojekyll README.md
git commit -m "feat: add GitHub Pages deploy workflow and README"
```

---

## 自检清单

对照设计文档检查每个需求是否有对应任务：

| 设计文档章节 | 需求 | 对应任务 |
|-------------|------|---------|
| 4. 数据采集策略 | 一次性采集 + 手动更新 | Task 8 |
| 5. 地图方案 | 静态地图图片 + CSS 标记 | Task 7 |
| 8. 数据结构 | restaurants/districts/categories JSON | Task 2, 8 |
| 9. TAG_RULES | 标签推断规则 | Task 8 |
| 11. 路由设计 | Hash 路由 4 条 | Task 2 |
| 12. 组件树 | 7 个组件 + 4 个页面 | Task 3~7 |
| 15. 列表页 | 分页、筛选、搜索 | Task 5 |
| 15. 详情页 | 信息展示 + 导航按钮 | Task 6 |
| 15. 地图页 | 静态图 + 标记 + 弹窗 | Task 7 |
| 17. 错误处理 | 加载/空/错误状态 | Task 5, 6, 7 |
| 20. 部署 | Vite base + GitHub Actions | Task 10 |

**查找缺失项：** 所有设计文档中的需求都已被覆盖。Markdown 附录中的坐标参考、API 参考等为参考信息，无需代码实现。
