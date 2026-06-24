<script setup lang="ts">
import { useRoute } from 'vue-router'
import { watch } from 'vue'
import { useRestaurantStore } from './stores/restaurant'
import SearchBar from './components/SearchBar.vue'
import FilterBar from './components/FilterBar.vue'
import AppHeader from './components/AppHeader.vue'

const route = useRoute()
const store = useRestaurantStore()

// 确保数据加载（在任何页面）
watch(() => route.path, () => {
  if (store.all.length === 0) store.fetchAll()
}, { immediate: true })
</script>

<template>
  <!-- 全屏模式（首页地图） -->
  <div v-if="route.meta?.fullscreen" class="fullscreen-layout">
    <router-view />
  </div>

  <!-- 普通模式（列表/详情/关于） -->
  <div v-else class="normal-layout">
    <AppHeader />
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
.fullscreen-layout {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}
.normal-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #F8F8F8;
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
