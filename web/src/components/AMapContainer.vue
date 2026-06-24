<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import type { Restaurant } from '../types/restaurant'
import { loadAMap } from '../utils/amap'

const props = defineProps<{
  restaurants: Restaurant[]
  userAddress?: string
}>()
const emit = defineEmits<{
  markerClick: [Restaurant]
  locationReady: [{ address: string; lng: number; lat: number }]
  locationError: [string]
}>()

const container = ref<HTMLDivElement>()
const mapReady = ref(false)
const mapError = ref(false)

const TAG_ICONS: Record<string, string> = {
  '烩面': '🍜', '胡辣汤': '🥣', '灌汤包': '🥟',
  '羊肉汤': '🍲', '河南菜': '🍳'
}
function getIcon(r: Restaurant): string {
  for (const tag of r.tags) if (TAG_ICONS[tag]) return TAG_ICONS[tag]
  return '🥟'
}

let map: any = null
let cluster: any = null
let markers: any[] = []
let userMarker: any = null

async function initMap() {
  if (!container.value) return
  try {
    const AMap = await loadAMap()
    map = new AMap.Map(container.value, {
      zoom: 11,
      center: [114.05, 22.55],
      viewMode: '2D',
      mapStyle: 'amap://styles/light'
    })
    mapReady.value = true
    await nextTick()
    renderMarkers()
  } catch {
    mapError.value = true
  }
}

function renderMarkers() {
  if (!map) return
  clearMarkers()
  if (!props.restaurants.length) return

  const AMap = (window as any).AMap
  markers = props.restaurants.map(r => {
    const m = new AMap.Marker({
      position: [r.longitude, r.latitude],
      content: `<div class="amap-marker-icon"><span class="amap-marker-touch">${getIcon(r)}</span></div>`,
      offset: new AMap.Pixel(-18, -36),
      zIndex: 10
    })
    m.on('mousedown', () => emit('markerClick', r))
    return m
  })

  // 先把标记直接加上，保证能看见
  map.add(markers)
}

function clearMarkers() {
  if (cluster) { cluster.clearMarkers(); cluster = null }
  if (map && markers.length) { map.remove(markers); markers = [] }
}

watch(() => props.restaurants, () => { if (mapReady.value) renderMarkers() })
onMounted(() => initMap())
onUnmounted(() => { clearMarkers(); map?.destroy(); map = null })
</script>

<template>
  <div class="amap-wrap">
    <div v-if="!mapReady && !mapError" class="map-loading"><el-skeleton :rows="3" animated /></div>
    <div v-if="mapError" class="map-error">
      <el-result icon="error" title="地图加载失败" sub-title='请配置 Key'>
        <template #extra><p style="font-size:12px;color:#999;line-height:1.8">请在高德后台 → 应用管理 → 添加「JS API」服务<br/>并在域名白名单加入：dylanln.github.io 和 localhost</p></template>
      </el-result>
    </div>
    <div ref="container" class="amap-container"></div>
  </div>
</template>

<style scoped>
.amap-wrap { width: 100%; height: 100vh; height: 100dvh; position: absolute; top: 0; left: 0; z-index: 1; }
.amap-container { width: 100%; height: 100vh; height: 100dvh; }
.map-loading { height: 100vh; display: flex; align-items: center; justify-content: center; background: #f5f5f5; }
.map-error { height: 100vh; display: flex; align-items: center; justify-content: center; background: #f5f5f5; }
</style>

<style>
.amap-marker-icon { font-size: 26px; line-height: 1; }
.amap-marker-touch { display: block; padding: 8px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.35)); transition: transform .15s; }
.amap-marker-touch:active { transform: scale(1.3); }
</style>
