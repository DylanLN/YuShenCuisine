import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Restaurant } from '../types/restaurant'
import rawData from '../assets/data/restaurants.json'

export const useRestaurantStore = defineStore('restaurant', () => {
  const all = ref<Restaurant[]>(rawData as Restaurant[])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const filterDistricts = ref<string[]>([])
  const filterCategories = ref<string[]>([])
  const searchKeyword = ref('')

  const filtered = computed(() => {
    let list = all.value
    if (searchKeyword.value) {
      const kw = searchKeyword.value.toLowerCase()
      list = list.filter(r =>
        r.name.toLowerCase().includes(kw) ||
        r.tags.some(t => t.toLowerCase().includes(kw)) ||
        r.district.includes(kw) ||
        r.address.toLowerCase().includes(kw)
      )
    }
    if (filterDistricts.value.length > 0) {
      list = list.filter(r => filterDistricts.value.includes(r.district))
    }
    if (filterCategories.value.length > 0) {
      list = list.filter(r => filterCategories.value.some(c => r.tags.includes(c)))
    }
    return list
  })

  const districts = computed(() => {
    const set = new Set(all.value.map(r => r.district))
    return Array.from(set).sort()
  })

  const categories = computed(() => {
    const set = new Set(all.value.flatMap(r => r.tags))
    return Array.from(set).sort()
  })

  function toggleDistrict(d: string) {
    const idx = filterDistricts.value.indexOf(d)
    if (idx >= 0) {
      filterDistricts.value.splice(idx, 1)
    } else {
      filterDistricts.value.push(d)
    }
  }

  function toggleCategory(c: string) {
    const idx = filterCategories.value.indexOf(c)
    if (idx >= 0) {
      filterCategories.value.splice(idx, 1)
    } else {
      filterCategories.value.push(c)
    }
  }

  function clearFilters() {
    filterDistricts.value = []
    filterCategories.value = []
    searchKeyword.value = ''
  }

  function fetchAll() {}

  function getById(id: string): Restaurant | undefined {
    return all.value.find(r => r.id === id)
  }

  return {
    all, loading, error,
    filterDistricts, filterCategories, searchKeyword,
    filtered, districts, categories,
    toggleDistrict, toggleCategory, clearFilters,
    fetchAll, getById
  }
})
