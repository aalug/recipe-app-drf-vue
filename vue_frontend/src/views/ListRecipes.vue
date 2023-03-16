<template>
  <v-container style="margin-bottom: 10rem;">
    <v-container>
      <h3>Filter by tags:</h3>
      <FilterChips
        :chips="tags"
        chipColor="teal"
        @selectChip="handleTagsFilter"
      />

      <br><br>

      <h3>Filter by ingredients:</h3>
      <FilterChips
        :chips="ingredients"
        chipColor="lime"
        @selectChip="handleIngredientsFilter"
      />

      <v-container
        class="d-flex justify-space-between mt-6 mb-5 "
      >
        <v-text-field
          label="Search..."
          v-model.trim="search"
          class="mr-4"
        ></v-text-field>

        <SortingPanel
          class="ml-4"
          @sortRecipes="handleSort"
        />
      </v-container>

    </v-container>
    <div v-if="loading" class="d-flex justify-center">
      <PageLoading/>
    </div>
    <v-container
      v-else
      class="d-flex justify-center"
    >
      <RecipesList
        v-if="recipes.length"
        :key="refreshRecipesList"
        :recipes="recipes"
      />
      <h2 v-else
      >No recipes
      </h2>
    </v-container>

  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/store/users';
import { Recipe } from '@/types/Recipe';
import { Tag } from '@/types/Tag';
import { Ingredient } from '@/types/Ingredient';
import { SortOption } from '@/types/SortOption.enum';
import RecipesList from '@/components/RecipesList.vue';
import FilterChips from '@/components/FilterChips.vue';
import PageLoading from '@/components/loading/PageLoading.vue';
import SortingPanel from '@/components/SortingPanel.vue';

const loading = ref<boolean>(false);
const recipes = ref<Recipe[]>([]);
const tags = ref<Tag[]>([]);
const ingredients = ref<Ingredient[]>([]);
const selectedTags = ref<number[]>([]);
const selectedIngredients = ref<number[]>([]);

const sortedBy = ref<SortOption>();
const search = ref<string>('');

// Exists to be a key of the v-container and to refresh it
const refreshRecipesList = ref<boolean>(false);

const token = useUserStore().token;

let allRecipes: Recipe[] = [];

onMounted(async () => {
  loading.value = true;
  try {
    const {data} = await axios.get(
      `${import.meta.env.VITE_API_BASE}/recipe/recipes/`,
      {headers: {Authorization: `Token ${token}`}}
    );
    allRecipes = data;
    recipes.value = allRecipes;
    // Get tags
    const tagsRes = await axios.get(
      `${import.meta.env.VITE_API_BASE}/recipe/tags/`,
      {headers: {Authorization: `Token ${token}`}}
    );
    tags.value = tagsRes.data;

    // Get ingredients
    const ingredientRes = await axios.get(
      `${import.meta.env.VITE_API_BASE}/recipe/ingredients/`,
      {headers: {Authorization: `Token ${token}`}}
    );
    ingredients.value = ingredientRes.data;
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
});

const filterRecipes = async () => {
  /**
   * Filter recipes by tags and ingredients by sending request to the server and
   * receiving filtered data.
   */
  refreshRecipesList.value = !refreshRecipesList.value;

  const tagsQuery = selectedTags.value.length ? `tags=${selectedTags.value}` : '';
  const ingredientsQuery = selectedIngredients.value.length ? `ingredients=${selectedIngredients.value}` : '';

  const twoQueries = ingredientsQuery && tagsQuery ? '&' : '';

  loading.value = true;
  try {
    const {data} = await axios.get(
      `${import.meta.env.VITE_API_BASE}/recipe/recipes?${tagsQuery}${twoQueries}${ingredientsQuery}`,
      {headers: {Authorization: `Token ${token}`}}
    );
    allRecipes = data;

    if (search.value) handleSearch();
    // Sort recipes by previously selected option
    if (sortedBy.value) handleSort(sortedBy.value);
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
};

const handleTagsFilter = async (selected: number[]) => {
  selectedTags.value = selected;
  await filterRecipes();
};

const handleIngredientsFilter = async (selected: number[]) => {
  selectedIngredients.value = selected;
  await filterRecipes();
};

const handleSearch = () => {
  /**
   * Filter recipes to ones that contain the given phrase.
   */
  refreshRecipesList.value = !refreshRecipesList.value;

  recipes.value = allRecipes.filter((recipe) => {
    let tags = recipe.tags ? [...recipe.tags] : [];
    let ingredients = recipe.ingredients ? [...recipe.ingredients] : [];
    tags = tags.filter((tag) => {
      return tag.name.toLowerCase().includes(search.value.toLowerCase());
    });
    ingredients = ingredients.filter((ingredient) => {
      return ingredient.name.toLowerCase().includes(search.value.toLowerCase());
    });
    if (
      tags.length ||
      ingredients.length ||
      recipe.title.toLowerCase().includes(search.value.toLowerCase())
    ) {
      return recipe;
    }
  });
};

watch(search, () => {
  handleSearch();
});

const handleSort = (sortBy: SortOption) => {
  /**
   * Get the chosen `sort by` value and run appropriate function.
   */
  sortedBy.value = sortBy;
  if (sortBy === SortOption.TITLE_ASCENDING) {
    sortByTitle('asc');
  } else if (sortBy === SortOption.TITLE_DESCENDING) {
    sortByTitle('desc');
  } else if (sortBy === SortOption.PRICE_ASCENDING) {
    sortByPrice('asc');
  } else if (sortBy === SortOption.PRICE_DESCENDING) {
    sortByPrice('desc');
  } else if (sortBy === SortOption.TIME_MINUTES_ASCENDING) {
    sortByTimeMinutes('asc');
  } else if (sortBy === SortOption.TIME_MINUTES_DESCENDING) {
    sortByTimeMinutes('desc');
  }
};

const sortByTitle = (direction: 'asc' | 'desc') => {
  /**
   * Sort recipes by title, in ascending order - if direction === 'asc',
   * in descending order - if direction === 'desc'.
   */
  recipes.value.sort((a, b) => {
    const titleA = a.title.toLowerCase();
    const titleB = b.title.toLowerCase();
    if (direction === 'asc') {
      if (titleA < titleB) {
        return -1;
      }
      if (titleA > titleB) {
        return 1;
      }
      return 0;
    } else if (direction === 'desc') {
      if (titleA > titleB) {
        return -1;
      }
      if (titleA < titleB) {
        return 1;
      }
      return 0;
    } else {
      throw new Error(`Invalid direction: ${direction}`);
    }
  });
  refreshRecipesList.value = !refreshRecipesList.value;
};

const sortByPrice = (direction: 'asc' | 'desc') => {
  /**
   * Sort recipes by price, in ascending order - if direction === 'asc',
   * in descending order - if direction === 'desc'.
   */
  recipes.value.sort((a, b) => {
    const priceA = parseFloat(a.price);
    const priceB = parseFloat(b.price);
    if (direction === 'asc') {
      if (priceA < priceB) {
        return -1;
      }
      if (priceA > priceB) {
        return 1;
      }
      return 0;
    } else if (direction === 'desc') {
      if (priceA > priceB) {
        return -1;
      }
      if (priceA < priceB) {
        return 1;
      }
      return 0;
    } else {
      throw new Error(`Invalid direction: ${direction}`);
    }
  });
  refreshRecipesList.value = !refreshRecipesList.value;
};

const sortByTimeMinutes = (direction: 'asc' | 'desc') => {
  /**
   * Sort recipes by timeMinutes, in ascending order - if direction === 'asc',
   * in descending order - if direction === 'desc'.
   */
  recipes.value.sort((a, b) => {
    if (direction === 'asc') {
      return a.timeMinutes - b.timeMinutes;
    } else if (direction === 'desc') {
      return b.timeMinutes - a.timeMinutes;
    } else {
      throw new Error(`Invalid direction: ${direction}`);
    }
  });
  refreshRecipesList.value = !refreshRecipesList.value;
};

</script>
