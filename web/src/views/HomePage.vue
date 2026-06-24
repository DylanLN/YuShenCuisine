<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useRestaurantStore } from '../stores/restaurant'
import { List, MapLocation } from '@element-plus/icons-vue'
import HotCategories from '../components/HotCategories.vue'

const store = useRestaurantStore()
const router = useRouter()

onMounted(() => {
  if (store.all.length === 0 && !store.loading) store.fetchAll()
})

function goToList() { router.push('/list') }
function goToMap() { router.push('/') }
</script>

<template>
  <div class="home-page">
    <section class="hero">
      <h1 class="hero-title">🥟 深圳河南美食地图</h1>
      <p class="hero-subtitle">在深圳，找到家乡的味道</p>
      <div class="hero-actions">
        <el-button type="danger" size="large" @click="goToList"><el-icon style="margin-right:4px"><List /></el-icon>查看全部店铺</el-button>
        <el-button plain size="large" @click="goToMap"><el-icon style="margin-right:4px"><MapLocation /></el-icon>地图分布</el-button>
      </div>
    </section>
    <HotCategories />
    <section class="stats" v-if="!store.loading">
      <el-card shadow="never">
        <div class="stats-inner">
          <div class="stat-item"><span class="stat-num">{{ store.all.length }}</span><span class="stat-label">收录店铺</span></div>
          <div class="stat-item"><span class="stat-num">{{ store.districts.length }}</span><span class="stat-label">覆盖区域</span></div>
          <div class="stat-item"><span class="stat-num">{{ store.categories.length }}</span><span class="stat-label">美食分类</span></div>
        </div>
      </el-card>
    </section>
    <section class="about">
      <el-card shadow="never">
        <h3>关于本站</h3>
        <p>深圳聚集了大量河南籍人口，但寻找地道的河南菜馆却并不容易。本网站收录了深圳市各区河南餐馆信息，帮你快速找到家乡味道。</p>
        <p class="about-note">数据来源于高德地图，如有遗漏或错误欢迎反馈。</p>
      </el-card>
    </section>
  </div>
</template>

<style scoped>
.home-page { display: flex; flex-direction: column; gap: 20px; }
.hero { text-align: center; padding: 48px 16px 32px; }
.hero-title { font-size: 32px; font-weight: 700; color: #C8102E; margin-bottom: 8px; }
.hero-subtitle { font-size: 16px; color: #666; margin-bottom: 24px; }
.hero-actions { display: flex; justify-content: center; gap: 12px; }
.stats-inner { display: flex; justify-content: space-around; text-align: center; }
.stat-item { display: flex; flex-direction: column; }
.stat-num { font-size: 28px; font-weight: 700; color: #C8102E; }
.stat-label { font-size: 13px; color: #999; margin-top: 2px; }
.about h3 { font-size: 16px; margin-bottom: 8px; color: #C8102E; }
.about p { font-size: 14px; color: #555; line-height: 1.8; }
.about-note { margin-top: 8px; font-size: 12px; color: #999; }
</style>
