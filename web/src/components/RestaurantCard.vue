<script setup lang="ts">
import { useRouter } from 'vue-router'
import { StarFilled } from '@element-plus/icons-vue'
import type { Restaurant } from '../types/restaurant'

const props = defineProps<{ restaurant: Restaurant }>()
const router = useRouter()
function goDetail() { router.push(`/detail/${props.restaurant.id}`) }
</script>

<template>
  <div class="restaurant-card" @click="goDetail">
    <div class="card-body">
      <h3 class="card-name">{{ restaurant.name }}</h3>
      <div class="card-meta">
        <span class="meta-district">{{ restaurant.district }}</span>
        <span class="meta-rating" v-if="restaurant.rating"><el-icon style="color:#F59E0B;vertical-align:text-bottom"><StarFilled /></el-icon> {{ restaurant.rating }}</span>
        <span class="meta-cost" v-if="restaurant.cost">¥{{ restaurant.cost }}/人</span>
      </div>
      <p class="card-address">{{ restaurant.address }}</p>
      <div class="card-tags">
        <el-tag v-for="tag in restaurant.tags" :key="tag" size="small" type="danger" effect="light">{{ tag }}</el-tag>
      </div>
    </div>
  </div>
</template>

<style scoped>
.restaurant-card { background: white; border-radius: 8px; padding: 14px 16px; cursor: pointer; transition: box-shadow 0.2s; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
.restaurant-card:hover { box-shadow: 0 2px 8px rgba(200,16,46,0.10); }
.card-name { font-size: 16px; font-weight: 600; color: #333; margin-bottom: 6px; }
.card-meta { display: flex; align-items: center; gap: 10px; font-size: 13px; color: #666; margin-bottom: 6px; }
.meta-district { background: #FFF0F0; color: #C8102E; padding: 1px 8px; border-radius: 4px; font-size: 12px; }
.card-address { font-size: 13px; color: #999; margin-bottom: 8px; line-height: 1.4; }
.card-tags { display: flex; gap: 4px; flex-wrap: wrap; }
</style>
