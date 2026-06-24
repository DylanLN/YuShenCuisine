<script setup lang="ts">
import SearchBar from './SearchBar.vue'
</script>

<template>
  <header class="app-header">
    <div class="header-inner">
      <router-link to="/" class="logo">
        <span class="logo-icon">🥟</span>
        <span class="logo-text">深圳河南美食地图</span>
      </router-link>
      <SearchBar />
    </div>
  </header>
</template>

<style scoped>
.app-header { background: #C8102E; color: white; padding: 0 16px; position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 8px rgba(0,0,0,0.15); }
.header-inner { max-width: 1200px; margin: 0 auto; display: flex; align-items: center; gap: 16px; height: 56px; }
.logo { display: flex; align-items: center; gap: 6px; text-decoration: none; color: white; white-space: nowrap; }
.logo-icon { font-size: 24px; }
.logo-text { font-size: 22px; font-weight: 700; }
</style>
