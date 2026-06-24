import { createRouter, createWebHashHistory } from 'vue-router'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      name: 'map',
      component: () => import('../views/MapPage.vue'),
      meta: { fullscreen: true }
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/HomePage.vue')
    },
    {
      path: '/list',
      name: 'list',
      component: () => import('../views/ListPage.vue')
    },
    {
      path: '/detail/:id',
      name: 'detail',
      component: () => import('../views/DetailPage.vue')
    }
  ]
})

export default router
