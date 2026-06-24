<script setup lang="ts">
import { onMounted, computed, ref } from 'vue'
import { useRestaurantStore } from '../stores/restaurant'
import RestaurantCard from '../components/RestaurantCard.vue'

const store = useRestaurantStore()
const currentPage = ref(1)
const pageSize = 20

onMounted(() => {
  if (store.all.length === 0 && !store.loading) store.fetchAll()
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
      <h2 class="list-title">全部店铺<span class="list-count" v-if="!store.loading">（{{ store.filtered.length }} 家）</span></h2>
      <el-button v-if="store.filterDistricts.length || store.filterCategories.length || store.searchKeyword" text type="danger" @click="store.clearFilters()">清除筛选</el-button>
    </div>

    <div v-if="store.loading" class="loading-state"><el-skeleton :rows="5" animated /></div>

    <div v-else-if="store.error" class="error-state">
      <el-result icon="error" title="加载失败" :sub-title="store.error">
        <template #extra><el-button type="danger" @click="store.fetchAll()">重试</el-button></template>
      </el-result>
    </div>

    <div v-else-if="store.filtered.length === 0" class="empty-state">
      <el-result icon="info" title="没有找到相关店铺"><template #extra><p class="empty-hint">试试其他关键词或清除筛选条件</p></template></el-result>
    </div>

    <template v-else>
      <div class="restaurant-grid"><RestaurantCard v-for="r in paginatedList" :key="r.id" :restaurant="r" /></div>
      <div class="pagination-wrap" v-if="totalPages > 1">
        <el-pagination v-model:current-page="currentPage" :page-size="pageSize" :total="store.filtered.length" layout="prev, pager, next" @current-change="handlePageChange" />
      </div>
    </template>
  </div>
</template>

<style scoped>
.list-page { display: flex; flex-direction: column; gap: 16px; }
.list-header { display: flex; justify-content: space-between; align-items: center; }
.list-title { font-size: 18px; font-weight: 600; }
.list-count { font-size: 14px; color: #999; font-weight: 400; }
.restaurant-grid { display: flex; flex-direction: column; gap: 10px; }
.loading-state, .error-state, .empty-state { padding: 40px 0; }
.empty-hint { font-size: 14px; color: #999; }
.pagination-wrap { display: flex; justify-content: center; padding: 16px 0; }
</style>
