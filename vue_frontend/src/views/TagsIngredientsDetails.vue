<template>

  <ConfirmDialog
    v-if="showConfirmationDialog"
    :key="refreshConfirmDialog"
    title="Are you sure"
    text="you want to delete these attributes?"
    @confirm="handleConfirmingDelete"
  />

  <v-container>
    <h2
      v-if="!deletingMultiple"
      class="text-center mb-6"
    >Click a chip to edit
    </h2>
    <h2
      v-else
      class="text-center text-error mb-6"
    >
      Click a chip to add to deletion list
    </h2>

    <div
      v-if="loading"
      class="d-flex justify-center mb-16"
    >
      <PageLoading/>
    </div>
    <v-container
      v-else
      class="d-flex justify-space-between"
    >
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
                :class="selectedToDeleteTags.includes(tag.id) ? 'selectedToDelete' : ''"
                :style="newlyEditedId === `tag${tag.id}` ? 'outline: solid 2px green': ''"
                @click="!deletingMultiple ? handleShowEditDialog(`tag${tag.id}`) : handleDeleteTagList(tag.id)"
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
                :class="selectedToDeleteIngredients.includes(ingredient.id) ? 'selectedToDelete' : ''"
                :style="newlyEditedId === `ingredient${ingredient.id}` ? 'outline: solid 2px green': ''"
                @click="!deletingMultiple ?
                handleShowEditDialog(`ingredient${ingredient.id}`) :
                handleDeleteIngredientList(ingredient.id)"
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
    <div class="d-flex justify-center">
      <v-btn
        v-if="!deletingMultiple"
        color="error"
        :disabled="loading"
        @click="deletingMultiple = true"
      >
        Delete multiple
      </v-btn>
      <div
        v-else
        style="display: flex; flex-direction: column;"
      >
        <v-btn
          color="brown-darken-3 mb-3"
          :disabled="loading"
          @click="stopMultipleDeletion()"
        >
          Stop multiple deletion
        </v-btn>
        <v-btn
          v-if="selectedToDeleteTags.length || selectedToDeleteIngredients.length"
          color="red-darken-4"
          :disabled="loading"
          @click="startDeletingProcess()"
        >
          Delete selected attributes
        </v-btn>
      </div>
    </div>
  </v-container>

</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/store/users';
import { Tag } from '@/types/Tag';
import { Ingredient } from '@/types/Ingredient';
import EditAttributeDialog from '@/components/EditAttributeDialog.vue';
import PageLoading from '@/components/loading/PageLoading.vue';
import ConfirmDialog from '@/components/ConfirmDialog.vue';

const loading = ref<boolean>(false);
const errorMessage = ref<string>('');
const ingredients = ref<Ingredient[]>([]);
const tags = ref<Tag[]>([]);
const openDialogId = ref<string>('');
const newlyEditedId = ref<string>('');
const selectedToDeleteTags = ref<number[]>([]);
const selectedToDeleteIngredients = ref<number[]>([]);
const deletingMultiple = ref<boolean>(false);
const showConfirmationDialog = ref<boolean>(false);
const refreshConfirmDialog = ref<boolean>(false);

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
    console.error(e);
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

const stopMultipleDeletion = () => {
  /**
   * Stop multiple deletion and reset values of selected
   * to delete tags and ingredients.
   */
  deletingMultiple.value = false;
  selectedToDeleteTags.value = [];
  selectedToDeleteIngredients.value = [];
};

const handleDeleteTagList = (tagId: number) => {
  /**
   * If the tagId is not in the 'to delete' array, add it.
   * If it is, remove it.
   */
  if (!selectedToDeleteTags.value.includes(tagId)) {
    selectedToDeleteTags.value.push(tagId);
  } else {
    selectedToDeleteTags.value = selectedToDeleteTags.value.filter(id => id !== tagId);
  }
};

const handleDeleteIngredientList = (ingredientId: number) => {
  /**
   * If the ingredientId is not in the 'to delete' array, add it.
   * If it is, remove it.
   */
  if (!selectedToDeleteIngredients.value.includes(ingredientId)) {
    selectedToDeleteIngredients.value.push(ingredientId);
  } else {
    selectedToDeleteIngredients.value = selectedToDeleteIngredients.value.filter(id => id !== ingredientId);
  }
};

const startDeletingProcess = () => {
  /**
   * Start deleting process. After the `delete` button is clicked, this function
   * will be called, and it will:
   * 1. Refresh the dialog component
   * 2. Display the confirmation dialog
   */
  showConfirmationDialog.value = true;
  refreshConfirmDialog.value = !refreshConfirmDialog.value;
};

const handleConfirmingDelete = async (isConfirmed: boolean) => {
  /**
   * This function is called when dialog has received a response (emit).
   * If the response is `OK` then it will proceed and delete attributes.
   */
  if (isConfirmed) {
    await deleteSelected();
  }
};

const deleteSelected = async () => {
  /**
   * Loop through the selected to delete tags and ingredients
   * and delete them.
   */
  loading.value = true;
  try {
    for (const tagId of selectedToDeleteTags.value) {
      await axios.delete(
        `${import.meta.env.VITE_API_BASE}/recipe/tags/${tagId}/`,
        {headers: {Authorization: `Token ${token}`}}
      );
    }
    for (const ingredientId of selectedToDeleteIngredients.value) {
      await axios.delete(
        `${import.meta.env.VITE_API_BASE}/recipe/ingredients/${ingredientId}/`,
        {headers: {Authorization: `Token ${token}`}}
      );
    }
  } catch (e) {
    console.error(e);
    errorMessage.value = 'Error occurred while deleting selected attributes. Please try again.';
  } finally {
    loading.value = false;
    await loadData();
    deletingMultiple.value = false;
  }
};

</script>

<style scoped>
.selectedToDelete {
  outline: solid 2px var(--dark-red);
  color: var(--light-red)
}
</style>
