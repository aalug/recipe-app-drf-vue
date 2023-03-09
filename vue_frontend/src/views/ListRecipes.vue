<template>

  <v-container class="d-flex justify-space-between">
    <v-row>
      <v-col
        cols="4"
        sm="12"
        md="6"
        lg="4"
        v-for="recipe in recipes"
        :key="recipe.id"
      >
        <RecipeCard
          :id="recipe.id"
          :title="recipe.title"
          :timeMinutes="recipe.timeMinutes"
          :price="recipe.price"
          :tags="recipe.tags"
          :ingredients="recipe.ingredients"
          :image="recipe.image"
          @removedRecipe="handleRemovedRecipe"
        />
      </v-col>
    </v-row>

  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/store/users';
import { Recipe } from '@/types/Recipe';
import RecipeCard from '@/components/RecipeCard.vue';

const loading = ref<boolean>(false);
const recipes = ref<Recipe[]>([]);

const token = useUserStore().token;

onMounted(async () => {
  loading.value = true;
  try {
    const {data} = await axios.get(
      `${import.meta.env.VITE_API_BASE}/recipe/recipes/`,
      {headers: {Authorization: `Token ${token}`}}
    );
    recipes.value = data;
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
});

const handleRemovedRecipe = (id: number) => {
  recipes.value = recipes.value.filter(r => r.id !== id)
}

</script>
