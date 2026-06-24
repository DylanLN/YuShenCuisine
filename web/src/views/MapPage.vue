<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useRestaurantStore } from '../stores/restaurant'
import AMapContainer from '../components/AMapContainer.vue'
import type { Restaurant } from '../types/restaurant'
import { Search, Filter, List } from '@element-plus/icons-vue'
import debounce from 'lodash.debounce'

const store = useRestaurantStore()
const router = useRouter()
const selectedRestaurant = ref<Restaurant | null>(null)
const showFilter = ref(false)
const showLocate = ref(false)
const keyword = ref('')
const locateKeyword = ref('')
const showDrawer = ref(false)
const myLocation = ref<{ address: string; lng: number; lat: number } | null>(null)

const debouncedSearch = debounce((val: string) => {
  store.searchKeyword = val
}, 300)

function onKeywordInput(val: string) {
  keyword.value = val
  debouncedSearch(val)
}

function clearKeyword() {
  keyword.value = ''
  store.searchKeyword = ''
}

function onMarkerClick(r: Restaurant) {
  selectedRestaurant.value = r
  showDrawer.value = true
}

function goDetail() {
  if (selectedRestaurant.value) router.push(`/detail/${selectedRestaurant.value.id}`)
}

function closeDrawer() {
  showDrawer.value = false
  selectedRestaurant.value = null
}

function setDistrict(d: string) {
  store.toggleDistrict(d)
}

function setCategory(c: string) {
  store.toggleCategory(c)
}

function onLocationReady(loc: { address: string; lng: number; lat: number }) {
  myLocation.value = loc
  showLocate.value = false
  locateKeyword.value = ''
}

function onLocationError(err: string) {
  alert(err)
}

function clearLocation() {
  myLocation.value = null
}

const markerCount = computed(() => store.filtered.length)
const hasFilter = computed(() => store.filterDistricts.length > 0 || store.filterCategories.length > 0 || store.searchKeyword !== '')
</script>

<template>
  <div class="map-page">
    <AMapContainer
      :restaurants="store.filtered"
      @marker-click="onMarkerClick"
      @location-ready="onLocationReady"
      @location-error="onLocationError"
    />

    <!-- 顶部浮动栏 -->
    <div class="float-top">
      <div class="float-top-left">
        <router-link to="/about" class="float-logo" title="关于本站">🥟</router-link>
        <div class="float-search">
          <el-input v-model="keyword" placeholder="搜索店名..." clearable size="small" @clear="clearKeyword" @input="onKeywordInput">
            <template #prefix><el-icon><Search /></el-icon></template>
          </el-input>
        </div>
        <button class="float-btn" :class="{ active: showFilter }" @click.stop="showFilter = !showFilter; showLocate = false" title="筛选">
          <el-icon><Filter /></el-icon>
        </button>
        <button class="float-btn" @click.stop="router.push('/list')" title="列表">
          <el-icon><List /></el-icon>
        </button>
        <button class="float-btn" :class="{ active: showLocate }" @click.stop="showLocate = !showLocate; showFilter = false" title="定位">
          📍
        </button>
        <button v-if="myLocation" class="float-btn float-btn-clear" @click.stop="clearLocation" title="清除定位">✕</button>
      </div>
      <div class="float-top-right">
        <span class="marker-badge" v-if="hasFilter">{{ markerCount }}/{{ store.all.length }}</span>
        <span class="marker-badge" v-else>{{ store.all.length }}</span>
      </div>
    </div>

    <!-- 定位输入 -->
    <div class="float-locate" v-if="showLocate" @click.stop>
      <p class="locate-label">输入你的位置</p>
      <el-input v-model="locateKeyword" placeholder="如：南山区科技园..." size="small" @keyup.enter="showLocate = false" />
      <p class="locate-hint">按回车定位</p>
    </div>

    <!-- 用户位置 -->
    <div class="float-my-location" v-if="myLocation" @click.stop>📍 {{ myLocation.address }}</div>

    <!-- 筛选面板 -->
    <div class="float-filter" v-if="showFilter" @click.stop>
      <div class="filter-row">
        <span class="filter-label">区域</span>
        <div class="filter-cbs">
          <el-checkbox :checked="store.filterDistricts.length === 0" :indeterminate="store.filterDistricts.length > 0" @change="store.filterDistricts = []" size="small">全部</el-checkbox>
          <el-checkbox v-for="d in store.districts" :key="d" :checked="store.filterDistricts.includes(d)" @change="store.toggleDistrict(d)" size="small">{{ d }}</el-checkbox>
        </div>
      </div>
      <div class="filter-row">
        <span class="filter-label">分类</span>
        <div class="filter-cbs">
          <el-checkbox :checked="store.filterCategories.length === 0" :indeterminate="store.filterCategories.length > 0" @change="store.filterCategories = []" size="small">全部</el-checkbox>
          <el-checkbox v-for="c in store.categories" :key="c" :checked="store.filterCategories.includes(c)" @change="store.toggleCategory(c)" size="small">{{ c }}</el-checkbox>
        </div>
      </div>
    </div>

    <!-- 底部提示 -->
    <div class="float-bottom" v-if="!showDrawer">
      <span>🥟 点击标记查看详情 · 深圳河南美食地图</span>
    </div>

    <!-- 标记详情抽屉 -->
    <el-drawer v-model="showDrawer" :title="selectedRestaurant?.name || ''" size="auto" @close="closeDrawer">
      <template v-if="selectedRestaurant">
        <el-descriptions :column="1" border size="small">
          <el-descriptions-item label="区域">{{ selectedRestaurant.district }}</el-descriptions-item>
          <el-descriptions-item label="地址">{{ selectedRestaurant.address }}</el-descriptions-item>
          <el-descriptions-item label="电话" v-if="selectedRestaurant.phone">{{ selectedRestaurant.phone }}</el-descriptions-item>
          <el-descriptions-item label="评分" v-if="selectedRestaurant.rating">⭐ {{ selectedRestaurant.rating }}</el-descriptions-item>
          <el-descriptions-item label="人均" v-if="selectedRestaurant.cost">¥{{ selectedRestaurant.cost }}</el-descriptions-item>
          <el-descriptions-item label="分类">
            <el-tag v-for="tag in selectedRestaurant.tags" :key="tag" type="danger" effect="light" style="margin-right:4px">{{ tag }}</el-tag>
          </el-descriptions-item>
        </el-descriptions>
        <div style="margin-top:12px;display:flex;gap:8px;">
          <el-button type="danger" @click="goDetail" style="flex:1">查看完整详情</el-button>
          <el-button @click="closeDrawer">关闭</el-button>
        </div>
      </template>
    </el-drawer>
  </div>
</template>

<style scoped>
.map-page { width: 100%; height: 100vh; height: 100dvh; position: relative; overflow: hidden; touch-action: manipulation; }

/* 顶部浮动栏 */
.float-top {
  position: absolute; top: 12px; left: 8px; right: 8px;
  z-index: 100; display: flex; justify-content: space-between;
  align-items: center; gap: 6px;
}
.float-top-left {
  display: flex; align-items: center; gap: 4px;
  background: rgba(255,255,255,0.96); padding: 4px 6px;
  border-radius: 10px; box-shadow: 0 2px 12px rgba(0,0,0,0.15);
}
.float-top-right { display: flex; align-items: center; }
.float-logo { font-size: 22px; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; text-decoration: none; }
.float-search { width: 130px; }
@media (min-width: 480px) { .float-search { width: 200px; } }
.float-btn {
  width: 36px; height: 36px; border: none; border-radius: 8px;
  background: transparent; cursor: pointer; display: flex;
  align-items: center; justify-content: center; font-size: 18px; color: #555;
  -webkit-tap-highlight-color: transparent; touch-action: manipulation;
}
.float-btn:hover { background: #f0f0f0; }
.float-btn:active { background: #e0e0e0; }
.float-btn.active { background: #FFF0F0; color: #C8102E; }
.float-btn-clear { color: #999; font-size: 14px; }
.marker-badge {
  background: rgba(200,16,46,0.9); color: white;
  padding: 4px 10px; border-radius: 20px; font-size: 13px; font-weight: 600;
  white-space: nowrap;
}

/* 定位面板 */
.float-locate {
  position: absolute; top: 60px; left: 8px; z-index: 100;
  background: rgba(255,255,255,0.97); padding: 12px 14px;
  border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.15);
  width: 280px; max-width: calc(100vw - 16px);
}
.locate-label { font-size: 14px; color: #333; margin-bottom: 6px; font-weight: 500; }
.locate-hint { font-size: 11px; color: #999; margin-top: 4px; }

.float-my-location {
  position: absolute; top: 60px; right: 8px; z-index: 100;
  background: rgba(255,255,255,0.92); padding: 8px 12px;
  border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  font-size: 13px; color: #333; max-width: 220px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}

/* 筛选面板 */
.float-filter {
  position: absolute; top: 60px; left: 8px; z-index: 100;
  background: rgba(255,255,255,0.97); padding: 10px 14px;
  border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.15);
  max-width: calc(100vw - 16px);
}
.filter-row { display: flex; align-items: flex-start; gap: 8px; margin-bottom: 6px; }
.filter-row:last-child { margin-bottom: 0; }
.filter-label { font-size: 12px; color: #999; white-space: nowrap; margin-top: 3px; }
.filter-cbs { display: flex; flex-wrap: wrap; gap: 4px 10px; }

/* 底部提示 */
.float-bottom {
  position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
  z-index: 100; background: rgba(0,0,0,0.6); color: white;
  padding: 8px 18px; border-radius: 24px; font-size: 13px; white-space: nowrap;
  max-width: calc(100vw - 32px); overflow: hidden; text-overflow: ellipsis;
}
</style>
