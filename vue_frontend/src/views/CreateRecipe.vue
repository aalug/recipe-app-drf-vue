<template>

  <v-card
    style="width: 60%; margin: 2rem auto 7rem auto"
    class="py-10 px-8"
  >

    <v-progress-linear
      v-if="loading"
      indeterminate
      :height="6"
      style="position: absolute;"
    ></v-progress-linear>

    <v-card-title>
      <span id="title" class="text-h4">Create a new recipe</span>
    </v-card-title>

    <BasicAlert
      v-if="isSuccessful"
      title="Success!"
      text="You have successfully created a new recipe."
      color="green"
      class="mt-5 mb-8"
    />

    <v-form
      @submit.prevent="handleSubmit()"
      @keydown.enter.prevent
    >
      <v-text-field
        v-model="recipeDetails.title"
        :error-messages="errorMessages.title"
        label="Title"
        class="mt-3"
        required
      ></v-text-field>
      <v-text-field
        v-model="recipeDetails.timeMinutes"
        :error-messages="errorMessages.timeMinutes"
        label="Time in minutes"
        class="mt-3"
        type="number"
        min="1"
        :rules="[v => v > 0 || 'Time must be at least 1']"
        required
      >
      </v-text-field>

      <v-text-field
        v-model="recipeDetails.price"
        :error-messages="errorMessages.price"
        label="Price"
        :rules="[isValidPrice() || 'Invalid value']"
        class="mt-3"
        required
      >
      </v-text-field>

      <v-text-field
        v-model="recipeDetails.link"
        label="Link"
        class="mt-3"
      >
      </v-text-field>

      <AddChips
        itemType="tag"
        chipColor="teal-lighten-2"
        @addChip="handleAddChip"
        @removeChip="handleRemoveChip"
        class="mt-3"
      />
      <AddChips
        itemType="ingredient"
        chipColor="lime"
        @addChip="handleAddChip"
        @removeChip="handleRemoveChip"
        class="mt-3"
      />

      <v-textarea
        v-model="recipeDetails.description"
        label="Description"
        class="mt-3"
      >
      </v-textarea>

      <v-file-input
        accept="image/png, image/jpeg, image/bmp"
        placeholder="Image"
        prepend-icon="mdi-camera"
        label="Image"
        @change="onFileSelected"
      ></v-file-input>

      <p v-if="nonFieldErrorMessage" class="text-error">{{ nonFieldErrorMessage }}</p>

      <div class="d-flex flex-column">
        <v-btn
          type="submit"
          color="cyan"
          class="mt-6 mb-3"
          :disabled="loading"
          block
        >
          Save
        </v-btn>
      </div>
    </v-form>
  </v-card>
</template>


<script setup lang="ts">
import {reactive, ref} from 'vue';
import axios from 'axios';
import {useUserStore} from '@/store/users';
import AddChips from '@/components/AddChips.vue';
import BasicAlert from '@/components/alerts/BasicAlert.vue';
import {Recipe} from '@/types/Recipe';

const loading = ref<boolean>(false);
const nonFieldErrorMessage = ref<string>('');
const isSuccessful = ref<boolean>(false);
const recipeImage = ref<File | null>(null);

const initialRecipeDetails: Recipe = {
  title: '',
  timeMinutes: 1,
  price: '',
  link: '',
  tags: [],
  ingredients: [],
  description: '',
}
const recipeDetails: Recipe = reactive({...initialRecipeDetails});

const errorMessages = reactive({
  title: '',
  timeMinutes: '',
  price: ''
});

const token = useUserStore().token;

interface InputFileEvent extends Event {
  target: HTMLInputElement;
}

const onFileSelected = (event: InputFileEvent) => {
  if (event.target.files)
    recipeImage.value = event.target.files[0];
}

type chipData = {
  itemType: string;
  itemName: string;
}

const handleAddChip = (data: chipData) => {
  if (data.itemType === 'tag') {
    recipeDetails.tags?.push({name: data.itemName});
  } else if (data.itemType === 'ingredient') {
    recipeDetails.ingredients?.push({name: data.itemName});
  }
}

const handleRemoveChip = (data: chipData) => {
  if (data.itemType === 'tag') {
    recipeDetails.tags = recipeDetails.tags?.filter(tag => tag.name !== data.itemName);
  } else if (data.itemType === 'ingredient') {
    recipeDetails.ingredients = recipeDetails.ingredients?.filter(ingredient => ingredient.name !== data.itemName);
  }
}

const isValidPrice = async () => {
  /**
   * Validate price as a number with up to 2 decimal places
   */
  return /^-?\d+(\.\d{0,2})?$/.test(recipeDetails.price);
}

const handleSubmit = async () => {
  /**
   * Validate the data and send POST request to create a new recipe.
   */
  // Validation
  if (!recipeDetails.title) {
    errorMessages.title = 'Title is required';
  }
  if (!recipeDetails.timeMinutes) {
    errorMessages.timeMinutes = 'Time is required';
  } else if (recipeDetails.timeMinutes < 1) {
    errorMessages.timeMinutes = 'Time must be at least 1';
  }
  if (!recipeDetails.price) {
    return errorMessages.price = 'Price is required';
  } else if (!await isValidPrice()) {
    return errorMessages.price = 'Invalid value';
  }

  const requestBody: Recipe = {
    'title': recipeDetails.title,
    'timeMinutes': recipeDetails.timeMinutes,
    'price': recipeDetails.price
  }

  if (recipeDetails.link) requestBody['link'] = recipeDetails.link;
  if (recipeDetails.description) requestBody['description'] = recipeDetails.description;
  if (recipeDetails.tags) requestBody['tags'] = recipeDetails.tags;
  if (recipeDetails.ingredients) requestBody['ingredients'] = recipeDetails.ingredients;

  // POST request
  try {
    const {data} = await axios.post(
      `${import.meta.env.VITE_API_BASE}/recipe/recipes/`,
      requestBody,
      {headers: {Authorization: `Token ${token}`}}
    )
    if (recipeImage.value) {
      const formData = new FormData();
      formData.append('image', recipeImage.value);

      await axios.post(
        `${import.meta.env.VITE_API_BASE}/recipe/recipes/${data.id}/upload-image/`,
        formData,
        {headers: {Authorization: `Token ${token}`}}
      )
    }
    isSuccessful.value = true;

    // Clear the form
    Object.assign(recipeDetails, initialRecipeDetails);

    // Scroll to the top of the page to see the success alert
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });

  } catch (e) {
    console.error(e)
    // @ts-ignore
    nonFieldErrorMessage.value = `${e.message}. Try again.`;
  } finally {
    loading.value = false;
  }
}

</script>
