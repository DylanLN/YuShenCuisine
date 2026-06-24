<script setup lang="ts">
import type { Restaurant } from '../types/restaurant'
import { lngLatToPixel } from '../utils/coordinates'

const props = defineProps<{ restaurant: Restaurant }>()
const emit = defineEmits<{ click: [Restaurant] }>()
const pos = lngLatToPixel(props.restaurant.longitude, props.restaurant.latitude)
</script>

<template>
  <div class="map-marker" :style="{ left: pos.x + 'px', top: pos.y + 'px' }" @click.stop="emit('click', restaurant)" :title="restaurant.name">🥟</div>
</template>

<style scoped>
.map-marker { position: absolute; font-size: 20px; cursor: pointer; transform: translate(-50%, -100%); transition: transform 0.15s; z-index: 2; filter: drop-shadow(0 1px 3px rgba(0,0,0,0.3)); line-height: 1; }
.map-marker:hover { transform: translate(-50%, -100%) scale(1.3); z-index: 10; }
</style>
