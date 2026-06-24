<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useRestaurantStore } from '../stores/restaurant'
import { Search } from '@element-plus/icons-vue'
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
.search-bar { flex: 1; max-width: 400px; }
.search-bar :deep(.el-input__wrapper) { background: rgba(255,255,255,0.15); border: none; box-shadow: none; }
.search-bar :deep(.el-input__inner) { color: white; }
.search-bar :deep(.el-input__inner::placeholder) { color: rgba(255,255,255,0.7); }
.search-bar :deep(.el-input__prefix) { color: rgba(255,255,255,0.7); }
.search-bar :deep(.el-input__clear) { color: rgba(255,255,255,0.7); }
</style>
