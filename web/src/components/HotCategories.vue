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
  store.filterCategories = [cat]
  store.searchKeyword = ''
  router.push('/list')
}
</script>

<template>
  <section class="hot-categories">
    <h3 class="section-title">热门分类</h3>
    <div class="category-grid">
      <div v-for="c in categories" :key="c.name" class="category-card" @click="goToCategory(c.name)">
        <span class="category-icon">{{ c.icon }}</span>
        <span class="category-name">{{ c.name }}</span>
      </div>
    </div>
  </section>
</template>

<style scoped>
.section-title { font-size: 16px; margin-bottom: 12px; color: #333; }
.category-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; }
.category-card { display: flex; flex-direction: column; align-items: center; padding: 20px 12px; background: white; border-radius: 12px; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
.category-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(200,16,46,0.12); }
.category-icon { font-size: 32px; margin-bottom: 8px; }
.category-name { font-size: 14px; font-weight: 500; color: #333; }
</style>
