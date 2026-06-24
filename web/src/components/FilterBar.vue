<script setup lang="ts">
import { useRestaurantStore } from '../stores/restaurant'

const store = useRestaurantStore()
</script>

<template>
  <div class="filter-bar">
    <div class="filter-section">
      <span class="filter-label">区域</span>
      <div class="filter-cbs">
        <el-checkbox :checked="store.filterDistricts.length === 0" :indeterminate="store.filterDistricts.length > 0" @change="store.filterDistricts = []" size="small">全部</el-checkbox>
        <el-checkbox v-for="d in store.districts" :key="d" :checked="store.filterDistricts.includes(d)" @change="store.toggleDistrict(d)" size="small">{{ d }}</el-checkbox>
      </div>
    </div>
    <div class="filter-section">
      <span class="filter-label">分类</span>
      <div class="filter-cbs">
        <el-checkbox :checked="store.filterCategories.length === 0" :indeterminate="store.filterCategories.length > 0" @change="store.filterCategories = []" size="small">全部</el-checkbox>
        <el-checkbox v-for="c in store.categories" :key="c" :checked="store.filterCategories.includes(c)" @change="store.toggleCategory(c)" size="small">{{ c }}</el-checkbox>
      </div>
    </div>
  </div>
</template>

<style scoped>
.filter-bar { background: white; border-bottom: 1px solid #eee; padding: 8px 16px; }
.filter-section { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.filter-section:last-child { margin-bottom: 0; }
.filter-label { font-size: 12px; color: #999; white-space: nowrap; width: 36px; }
.filter-cbs { display: flex; flex-wrap: wrap; gap: 4px 10px; }
</style>
