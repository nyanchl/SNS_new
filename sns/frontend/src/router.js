import { createRouter, createWebHistory } from 'vue-router';
import OneView from './components/OneView';
import TwoView from './components/TwoView';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      name: 'One',
      path: '/one',
      component: OneView
    },
    {
      name: 'Two',
      path: '/two',
      component: TwoView
    },
  ],
});

export default router;