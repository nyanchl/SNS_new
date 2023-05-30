import { createRouter, createWebHistory } from 'vue-router';
import OneView from './components/OneView';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      name: 'One',
      path: '/one',
      component: OneView
    },
  ],
});

export default router;