<template>
  <v-container class="d-flex justify-space-between">
    <v-row>
      <v-col
        cols="4"
        sm="12"
        md="6"
        lg="4"
        v-for="recipe in recipesList"
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
import { ref } from 'vue';
import { Recipe } from '@/types/Recipe';
import RecipeCard from '@/components/RecipeCard.vue';

const props = defineProps<{
  recipes: Recipe[]
}>();

const recipesList = ref<Recipe[]>([...props.recipes])
const handleRemovedRecipe = (id: number) => {
  /**
   * Updates the recipes array to reflect deleting a recipe.
   */
  recipesList.value = recipesList.value.filter(r => r.id !== id);
};

</script>
