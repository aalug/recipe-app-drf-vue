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
import { Recipe } from '@/types/Recipe';
import RecipeCard from '@/components/RecipeCard.vue';

defineProps<{
  recipes: Recipe[]
}>();

const handleRemovedRecipe = (id: number) => {
  /**
   * Updates the recipes array to reflect deleting a recipe.
   */
  recipes.value = recipes.value.filter(r => r.id !== id);
};

</script>
