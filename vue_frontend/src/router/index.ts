// Composables
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/Default.vue'),
    children: [
      {
        path: '',
        name: 'home',
        component: () => import('@/views/Home.vue'),
      },
      {
        path: '/profile',
        name: 'profile',
        component: () => import('@/views/UserProfile.vue'),
      },
      {
        path: '/create-recipe',
        name: 'create-recipe',
        component: () => import('@/views/CreateRecipe.vue'),
      },
      {
        path: '/edit-recipe/:recipeId',
        name: 'edit-recipe',
        component: () => import('@/views/CreateRecipe.vue'),
      },
      {
        path: '/my-recipes',
        name: 'list-recipes',
        component: () => import('@/views/ListRecipes.vue'),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
