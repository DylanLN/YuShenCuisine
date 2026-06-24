<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Restaurant } from '../types/restaurant'

defineProps<{ restaurants: Restaurant[] }>()

const mapImageSrc = '/shenzhen-henan-food/images/shenzhen-map.png'
const mapError = ref(false)
const zoom = ref(1)

function onImageError() { mapError.value = true }
function onImageLoad() { mapError.value = false }

function handleWheel(e: WheelEvent) {
  e.preventDefault()
  const delta = e.deltaY > 0 ? -0.1 : 0.1
  zoom.value = Math.max(0.5, Math.min(3, zoom.value + delta))
}

function zoomIn() { zoom.value = Math.min(3, zoom.value + 0.2) }
function zoomOut() { zoom.value = Math.max(0.5, zoom.value - 0.2) }
function resetZoom() { zoom.value = 1 }

const transformStyle = computed(() => ({
  transform: `scale(${zoom.value})`,
  transformOrigin: 'top left'
}))
</script>

<template>
  <div class="static-map">
    <div class="map-toolbar">
      <span class="zoom-label">{{ Math.round(zoom * 100) }}%</span>
      <button class="zoom-btn" @click="zoomIn" title="放大">＋</button>
      <button class="zoom-btn" @click="zoomOut" title="缩小">−</button>
      <button class="zoom-btn" @click="resetZoom" title="重置">⟲</button>
    </div>
    <div class="map-wrapper" @wheel.prevent="handleWheel">
      <div class="map-scroll" :style="transformStyle">
        <img :src="mapImageSrc" alt="深圳地图" class="map-image" @load="onImageLoad" @error="onImageError" />
        <div class="markers-layer"><slot :restaurants="restaurants" /></div>
      </div>
      <div v-if="mapError" class="map-error-overlay"><p>地图底图加载失败<br/><small>请将深圳地图截图保存到 web/public/images/shenzhen-map.png</small></p></div>
    </div>
    <p class="map-attribution">© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap contributors</a></p>
  </div>
</template>

<style scoped>
.static-map { display: flex; flex-direction: column; gap: 4px; }
.map-toolbar { display: flex; align-items: center; gap: 6px; padding: 4px 8px; background: white; border-radius: 8px 8px 0 0; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
.zoom-label { font-size: 12px; color: #999; min-width: 36px; }
.zoom-btn { width: 28px; height: 28px; border: 1px solid #ddd; border-radius: 4px; background: white; cursor: pointer; font-size: 16px; line-height: 1; display: flex; align-items: center; justify-content: center; color: #666; }
.zoom-btn:hover { background: #f5f5f5; }
.map-wrapper { position: relative; width: 100%; max-width: 900px; margin: 0 auto; overflow: auto; border-radius: 0 0 8px 8px; }
.map-scroll { position: relative; width: 1838px; height: 946px; }
.map-image { width: 1838px; height: 946px; display: block; }
.markers-layer { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }
.markers-layer > * { pointer-events: auto; }
.map-error-overlay { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; background: #f5f5f5; color: #999; font-size: 14px; border-radius: 8px; }
.map-error-overlay small { display: block; margin-top: 8px; color: #bbb; }
.map-attribution { text-align: right; font-size: 11px; color: #bbb; }
.map-attribution a { color: #bbb; text-decoration: underline; }
</style>
