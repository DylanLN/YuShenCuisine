<script setup lang="ts">
import { ElMessage } from 'element-plus'
import { Location, Guide, CopyDocument } from '@element-plus/icons-vue'

const props = defineProps<{ longitude: number; latitude: number; address: string; name: string }>()

function navigateByAmap() {
  window.location.href = `amap://route?from=&to=${props.longitude},${props.latitude}&name=${encodeURIComponent(props.name)}&mode=transit`
  setTimeout(() => {
    window.open(`https://uri.amap.com/navigation?to=${props.longitude},${props.latitude},${encodeURIComponent(props.name)}&mode=transit&coordinate=gaode`, '_blank')
  }, 3000)
}

function navigateByWeb() {
  window.open(`https://uri.amap.com/navigation?to=${props.longitude},${props.latitude},${encodeURIComponent(props.name)}&mode=transit&coordinate=gaode`, '_blank')
}

function copyAddress() {
  navigator.clipboard.writeText(props.address).then(() => ElMessage.success('地址已复制')).catch(() => ElMessage.warning('复制失败，请手动记下地址'))
}
</script>

<template>
  <div class="nav-actions">
    <el-button type="danger" size="large" @click="navigateByAmap" class="nav-btn"><el-icon style="margin-right:4px"><Location /></el-icon>导航到店（高德 APP）</el-button>
    <el-button plain size="large" @click="navigateByWeb" class="nav-btn"><el-icon style="margin-right:4px"><Guide /></el-icon>高德 Web 版</el-button>
    <el-button text size="large" @click="copyAddress"><el-icon style="margin-right:4px"><CopyDocument /></el-icon>复制地址</el-button>
  </div>
</template>

<style scoped>
.nav-actions { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.nav-btn { flex: 1; min-width: 120px; }
</style>
