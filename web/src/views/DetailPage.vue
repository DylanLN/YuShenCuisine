<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useRestaurantStore } from '../stores/restaurant'
import { ArrowLeft } from '@element-plus/icons-vue'
import NavButton from '../components/NavButton.vue'

const route = useRoute()
const router = useRouter()
const store = useRestaurantStore()

const restaurant = computed(() => store.getById(route.params.id as string))

onMounted(() => {
  if (!restaurant.value && !store.loading) store.fetchAll()
})
</script>

<template>
  <div class="detail-page">
    <el-button text @click="router.back()" class="back-btn"><el-icon><ArrowLeft /></el-icon>返回</el-button>

    <div v-if="store.loading && !restaurant" class="loading-state"><el-skeleton :rows="6" animated /></div>

    <div v-else-if="!restaurant" class="error-state">
      <el-result icon="warning" title="店铺不存在">
        <template #extra><el-button type="danger" @click="router.push('/list')">返回列表</el-button></template>
      </el-result>
    </div>

    <template v-else>
      <div class="detail-header">
        <div class="cover-placeholder" v-if="!restaurant.cover"><span class="cover-emoji">🥟</span></div>
        <h1 class="detail-name">{{ restaurant.name }}</h1>
      </div>

      <el-card shadow="never" class="info-card">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="区域"><el-tag type="danger" effect="light">{{ restaurant.district }}</el-tag></el-descriptions-item>
          <el-descriptions-item label="地址">{{ restaurant.address }}</el-descriptions-item>
          <el-descriptions-item label="电话" v-if="restaurant.phone"><a :href="`tel:${restaurant.phone}`" class="phone-link">{{ restaurant.phone }}</a></el-descriptions-item>
          <el-descriptions-item label="评分" v-if="restaurant.rating"><el-rate :model-value="restaurant.rating" disabled show-score :max="5" score-template="{value}" /></el-descriptions-item>
          <el-descriptions-item label="人均" v-if="restaurant.cost">¥{{ restaurant.cost }}</el-descriptions-item>
          <el-descriptions-item label="分类">
            <el-tag v-for="tag in restaurant.tags" :key="tag" type="danger" effect="light" style="margin-right:4px">{{ tag }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="收录来源"><span class="source-text">通过「{{ restaurant.source_keyword }}」收录</span></el-descriptions-item>
        </el-descriptions>
      </el-card>

      <el-card shadow="never" class="nav-card">
        <h3 class="nav-title">📍 位置与导航</h3>
        <p class="nav-address">{{ restaurant.address }}</p>
        <NavButton :longitude="restaurant.longitude" :latitude="restaurant.latitude" :address="restaurant.address" :name="restaurant.name" />
      </el-card>
    </template>
  </div>
</template>

<style scoped>
.detail-page { display: flex; flex-direction: column; gap: 16px; }
.back-btn { align-self: flex-start; }
.loading-state, .error-state { padding: 40px 0; }
.detail-header { text-align: center; }
.cover-placeholder { width: 80px; height: 80px; background: #FFF0F0; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px; }
.cover-emoji { font-size: 36px; }
.detail-name { font-size: 24px; font-weight: 700; color: #333; }
.info-card, .nav-card { border-radius: 12px; }
.phone-link { color: #C8102E; font-weight: 500; }
.source-text { color: #999; font-size: 13px; }
.nav-title { font-size: 16px; margin-bottom: 4px; }
.nav-address { font-size: 14px; color: #666; margin-bottom: 12px; }
</style>
