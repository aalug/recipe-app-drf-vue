<template>
  <RecipeDetails
    v-if="openDetails"
    :key="refresher"
    :recipeId="id"
  />

  <v-card
    class="mx-auto my-2"
    max-width="450"
  >
    <v-img
      cover
      height="270"
      width="400"
      :src="image"
    ></v-img>

    <v-card-item>
      <v-card-title>{{ title }}</v-card-title>
    </v-card-item>

    <v-card-text>

      <div class="my-4 text-subtitle-1">
        ${{ price }} <br> {{ timeMinutes }} minutes
      </div>

    </v-card-text>


    <div class="px-4">
      <div
        v-if="tags"
        class="mb-2"
      >
        <v-chip
          v-for="tag in tags"
          :key="tag.id"
          color="teal-lighten-2"
          class="mb-1"
        >
          {{ tag.name }}
        </v-chip>
      </div>

      <v-divider></v-divider>

      <div
        v-if="ingredients"
        class="mt-2"
      >
        <v-chip
          v-for="ingredient in ingredients"
          :key="ingredient.id"
          color="lime"
          class="mb-1"
        >
          {{ ingredient.name }}
        </v-chip>
      </div>
    </div>

    <v-card-actions class="d-flex justify-end">
      <v-btn
        color="pink"
        class="mt-4"
        variant="text"
        @click="showDetails()"
      >
        See details
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import { Tag } from '@/types/Tag';
import { Ingredient } from '@/types/Ingredient';
import { ref } from 'vue';
import RecipeDetails from '@/components/RecipeDetails.vue';

defineProps<{
  id: number,
  title: string,
  timeMinutes: number,
  price: string,
  tags: Tag[],
  ingredients: Ingredient[],
  image: string | null,
}>();

const openDetails = ref<boolean>(false);
const refresher = ref<boolean>(false);

const showDetails = () => {
  openDetails.value = true;
  refresher.value = !refresher.value;
};

</script>
