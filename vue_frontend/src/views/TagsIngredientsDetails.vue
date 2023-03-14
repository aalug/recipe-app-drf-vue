<template>

  <v-container class="d-flex justify-space-between">
    <v-container>
      <v-card
        class="mx-auto py-8 px-7"
        width="80%"
        style="border: solid 2px var(--teal-lighter-2);"
      >
        <h2 class="mb-10">Tags</h2>

        <v-row
          align="center"
          justify="space-between"
          class="mx-auto mb-6"
        >
          <v-col
            v-for="tag in tags"
            v-bind:key="tag.id"
            cols="auto"
            class="py-1 pe-0"
          >
            <EditAttributeDialog
              v-if="openDialogId === `tag${tag.id}`"
              :id="tag.id"
              :name="tag.name"
              type="tag"
              color="teal-lighter-2"
              @closeDialog="openDialogId = ''"
              @save="handleOnSave"
              @delete="handleOnDeleteTag"
            />
            <v-chip
              size="x-large"
              class="mb-2 mx-1"
              :style="newlyEditedId === `tag${tag.id}` ? 'outline: solid 2px green': ''"
              @click="handleShowEditDialog(`tag${tag.id}`)"
            >
              {{ tag.name }}
            </v-chip>

          </v-col>
        </v-row>
      </v-card>
    </v-container>

    <v-container>
      <v-card
        class="mx-auto py-8 px-7"
        width="80%"
        style="border: solid 2px var(--lime);"
      >
        <h2 class="mb-10">Ingredients</h2>

        <v-row
          align="center"
          justify="space-between"
          class="mx-auto mb-6"
        >
          <v-col
            v-for="ingredient in ingredients"
            v-bind:key="ingredient.id"
            cols="auto"
            class="py-1 pe-0"
          >
            <v-chip
              size="x-large"
              class="mb-2 mx-1"
              :style="newlyEditedId === `ingredient${ingredient.id}` ? 'outline: solid 2px green': ''"
              @click="handleShowEditDialog(`ingredient${ingredient.id}`)"
            >
              {{ ingredient.name }}
            </v-chip>
            <EditAttributeDialog
              v-if="openDialogId === `ingredient${ingredient.id}`"
              :id="ingredient.id"
              :name="ingredient.name"
              type="ingredient"
              color="lime"
              @closeDialog="openDialogId = ''"
              @save="handleOnSave"
              @delete="handleOnDeleteIngredient"
            />
          </v-col>
        </v-row>
      </v-card>
    </v-container>
  </v-container>

</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/store/users';
import { Tag } from '@/types/Tag';
import { Ingredient } from '@/types/Ingredient';
import EditAttributeDialog from '@/components/EditAttributeDialog.vue';

const loading = ref<boolean>(false);
const errorMessage = ref<string>('');
const ingredients = ref<Ingredient[]>([]);
const tags = ref<Tag[]>([]);
const openDialogId = ref<string>('');
const newlyEditedId = ref<string>('');

const token = useUserStore().token;
const headers = {headers: {Authorization: `Token ${token}`}};

const loadData = async () => {
  /**
   * Send a get request to fetch tags and ingredients.
   */
  loading.value = true;
  try {
    const ingredientsResponse = await axios.get(
      `${import.meta.env.VITE_API_BASE}/recipe/ingredients/`,
      headers
    );
    ingredients.value = ingredientsResponse.data;

    const tagsResponse = await axios.get(
      `${import.meta.env.VITE_API_BASE}/recipe/tags/`,
      headers
    );
    tags.value = tagsResponse.data;
  } catch (e) {
    errorMessage.value = 'Could not load data properly. Please try again.';
    console.log(e);
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await loadData();
});

const handleShowEditDialog = (id: string) => {
  /**
   * Show an edit dialog for an appropriate tag / ingredient.
   */
  openDialogId.value = id;
};
const handleOnSave = async (updatedItem: string) => {
  await loadData();
  newlyEditedId.value = updatedItem;
};

const handleOnDeleteTag = (id: number) => {
  /**
   * Remove a tag with given `id` from the tags list.
   */
  tags.value = tags.value.filter(t => t.id !== id);
};

const handleOnDeleteIngredient = (id: number) => {
    /**
   * Remove an ingredient with given `id` from the ingredients list.
   */
  ingredients.value = ingredients.value.filter(i => i.id !== id);
};

</script>
