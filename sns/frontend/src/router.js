import { createRouter, createWebHistory } from 'vue-router';
import OneView from './components/OneView';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      name: 'Home',
      path: '/home',
      component: OneView
    },
  ],
});

export default router;