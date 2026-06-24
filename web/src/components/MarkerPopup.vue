<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { Restaurant } from '../types/restaurant'
import { lngLatToPixel } from '../utils/coordinates'

const props = defineProps<{ restaurant: Restaurant }>()
const emit = defineEmits<{ close: [] }>()
const router = useRouter()
const pos = lngLatToPixel(props.restaurant.longitude, props.restaurant.latitude)

function goDetail() { router.push(`/detail/${props.restaurant.id}`) }
</script>

<template>
  <div class="marker-popup" :style="{ left: pos.x + 'px', top: pos.y - 10 + 'px' }">
    <div class="popup-inner">
      <button class="popup-close" @click.stop="emit('close')">×</button>
      <h4 class="popup-name">{{ restaurant.name }}</h4>
      <div class="popup-meta">
        <span class="popup-district">{{ restaurant.district }}</span>
        <span v-if="restaurant.rating" class="popup-rating">⭐ {{ restaurant.rating }}</span>
      </div>
      <el-button size="small" type="danger" @click="goDetail" style="margin-top:8px;width:100%">查看详情</el-button>
    </div>
  </div>
</template>

<style scoped>
.marker-popup { position: absolute; z-index: 20; transform: translate(-50%, -100%); }
.popup-inner { background: white; border-radius: 8px; padding: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.15); min-width: 160px; position: relative; }
.popup-close { position: absolute; top: 4px; right: 8px; border: none; background: none; font-size: 18px; cursor: pointer; color: #999; line-height: 1; }
.popup-name { font-size: 14px; font-weight: 600; margin-bottom: 4px; padding-right: 16px; }
.popup-meta { display: flex; gap: 8px; font-size: 12px; color: #666; }
.popup-district { background: #FFF0F0; color: #C8102E; padding: 0 6px; border-radius: 3px; }
</style>
