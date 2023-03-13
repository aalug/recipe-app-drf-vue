<template>

  <v-select
    clearable
    label="Sort by"
    :items="sortOptions"
    v-model="sortBy"
    @update:modelValue="onSortSelected()"
  ></v-select>

</template>

<script setup lang="ts">
import { ref } from 'vue';
import { SortOption } from '@/types/SortOption.enum';

const emit = defineEmits(['sortRecipes']);

const sortBy = ref<SortOption>();
const sortOptions: string[] = Object.values(SortOption);

const onSortSelected = () => {
  emit('sortRecipes', sortBy.value);
};

</script>
