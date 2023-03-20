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
      :text="recipeId ? 'You have successfully updated the recipe.' : 'You have successfully created a new recipe.'"
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
        :key="clearAllTags"
        itemType="tag"
        chipColor="teal-lighten-2"
        :alreadySelected="oldTags"
        :clearAllChips="clearAllTags"
        @addChip="handleAddChip"
        @removeChip="handleRemoveChip"
        @afterClear="clearOldNewTags();"
        class="mt-3"
      />
      <v-btn
        icon="mdi-trash-can"
        color="red"
        size="small"
        variant="text"
        style="margin-top: -7rem;"
        @click="clearAllTags = true"
      ></v-btn>
      <AddChips
        :key="clearAllIngredients"
        itemType="ingredient"
        chipColor="lime"
        :alreadySelected="oldIngredients"
        :clearAllChips="clearAllIngredients"
        @addChip="handleAddChip"
        @removeChip="handleRemoveChip"
        @afterClear="clearOldNewIngredients();"
        class="mt-3"
      />
      <v-btn
        icon="mdi-trash-can"
        color="red"
        size="small"
        variant="text"
        style="margin-top: -7rem;"
        @click="clearAllIngredients = true"
      ></v-btn>

      <v-textarea
        v-model="recipeDetails.description"
        label="Description"
        class="mt-3"
      >
      </v-textarea>

      <div class="d-flex">
        <v-file-input
          accept="image/png, image/jpeg, image/bmp"
          placeholder="Image"
          prepend-icon="mdi-camera"
          label="Image"
          style="width: 80%"
          @change="onFileSelected"
        ></v-file-input>

        <div class="d-flex justify-space-between">
          <ImagePreview
            :image="recipeImage"
            :key="imgRefresher"
          />
        </div>

      </div>

      <p v-if="nonFieldErrorMessage" class="text-error">{{ nonFieldErrorMessage }}</p>

      <div class="d-flex align-center">
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
import { reactive, ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { useUserStore } from '@/store/users';
import AddChips from '@/components/AddChips.vue';
import BasicAlert from '@/components/alerts/BasicAlert.vue';
import ImagePreview from '@/components/ImagePreview.vue';
import { Recipe } from '@/types/Recipe';

const loading = ref<boolean>(false);
const nonFieldErrorMessage = ref<string>('');
const isSuccessful = ref<boolean>(false);
const recipeImage = ref<File | null>(null);
const clearAllIngredients = ref<boolean>(false);
const clearAllTags = ref<boolean>(false);

const imgRefresher = ref<boolean>(false);
const fileChanged = ref<boolean>(false);

const initialRecipeDetails: Recipe = {
  title: '',
  timeMinutes: 1,
  price: '',
  link: '',
  tags: [],
  ingredients: [],
  description: '',
};
const recipeDetails: Recipe = reactive({...initialRecipeDetails});

const errorMessages = reactive({
  title: '',
  timeMinutes: '',
  price: ''
});
// To send them to the `AddChip` component so they can be displayed in a proper way
const oldTags = ref<string[]>([]);
const oldIngredients = ref<string[]>([]);

const token = useUserStore().token;

const {params} = useRoute();
const recipeId = params.recipeId;

onMounted(async () => {
  /**
   * Check if `recipeId` exists. If it does, that means that user is editing
   * the recipe, not creating one.
   * If user is editing, fetch the recipe details and update the form with its values.
   */
  if (recipeId) {
    loading.value = true;
    try {
      const {data} = await axios.get(
        `${import.meta.env.VITE_API_BASE}/recipe/recipes/${recipeId}/`,
        {headers: {Authorization: `Token ${token}`}}
      );
      initialRecipeDetails.title = data.title;
      initialRecipeDetails.timeMinutes = data.timeMinutes;
      initialRecipeDetails.price = data.price;
      initialRecipeDetails.tags = data.tags;
      initialRecipeDetails.ingredients = data.ingredients;
      initialRecipeDetails.description = data.description;
      recipeImage.value = data.image;

      // It's done this way, because later, `initialRecipeDetails` and `recipeDetails`
      // will be compared to send an appropriate request with the appropriate data.
      Object.assign(recipeDetails, initialRecipeDetails);


      // If tags and/ or ingredients exist, set the values accordingly.
      // Values will be sent to the `AddChips` component which will display them
      // the same way they are displayed while creating a new recipe.
      const tags = recipeDetails.tags;
      if (tags) {
        for (const tag of tags) {
          oldTags.value.push(tag.name);
        }
      }
      const ingredients = recipeDetails.ingredients;
      if (ingredients) {
        for (const ingredient of ingredients) {
          oldIngredients.value.push(ingredient.name);
        }
      }
    } catch (e) {
      console.error(e);
      nonFieldErrorMessage.value = 'Could not load the recipe details. Please try again.';
    } finally {
      loading.value = false;
    }
  }
});

interface InputFileEvent extends Event {
  target: HTMLInputElement;
}

const onFileSelected = (event: InputFileEvent) => {
  if (event.target.files) {
    recipeImage.value = event.target.files[0];
    imgRefresher.value = !imgRefresher.value;
    fileChanged.value = true;
  }
};

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
};

const handleRemoveChip = (data: chipData) => {
  if (data.itemType === 'tag') {
    recipeDetails.tags = recipeDetails.tags?.filter(tag => tag.name !== data.itemName);
  } else if (data.itemType === 'ingredient') {
    recipeDetails.ingredients = recipeDetails.ingredients?.filter(ingredient => ingredient.name !== data.itemName);
  }
};

const isValidPrice = async () => {
  /**
   * Validate price as a number with up to 2 decimal places
   */
  return /^-?\d+(\.\d{0,2})?$/.test(recipeDetails.price);
};

const handleSubmit = async () => {
  /**
   * Validate the data and:
   * a) Send a POST request to create a new recipe
   * b) Send a PUT or a PATCH request to edit an existing recipe
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
  };

  if (recipeDetails.link) requestBody['link'] = recipeDetails.link;
  if (recipeDetails.description) requestBody['description'] = recipeDetails.description;
  if (recipeDetails.tags) requestBody['tags'] = recipeDetails.tags;
  if (recipeDetails.ingredients) requestBody['ingredients'] = recipeDetails.ingredients;

  // If user is editing, not creating a new recipe
  if (recipeId) {
    const initRecipeEntries = Object.entries(initialRecipeDetails);
    const recipeEntries = Object.entries(recipeDetails);
    type Payload = {
      [key: string]: string | number;
    }
    const payload: Payload = {};

    for (let i = 0; i < recipeEntries.length; i++) {
      // If the values are the same, that means that user did not make a change
      const [key, value] = recipeEntries[i];
      if (initRecipeEntries[i][1] !== value) {
        payload[key] = value;
      }
    }
    if (recipeImage.value && fileChanged.value) {
      loading.value = true;
      try {
        const formData = new FormData();
        formData.append('image', recipeImage.value);

        await axios.post(
          `${import.meta.env.VITE_API_BASE}/recipe/recipes/${recipeId}/upload-image/`,
          formData,
          {headers: {Authorization: `Token ${token}`}}
        );
      } catch (e) {
        console.error(e);
        nonFieldErrorMessage.value = 'Could not upload new image. Please try again.';
      } finally {
        loading.value = false;
      }
    }

    // If the length of the payload is 0 that means that only the image was supported
    // to be updated, and it was handled above.
    // If lengths are not the same, that means that not all the fields were changed
    // so the request should be PATCH.
    if (payload.length !== 0 && payload.length !== recipeEntries.length) {
      loading.value = true;
      try {
        await axios.patch(
          `${import.meta.env.VITE_API_BASE}/recipe/recipes/${recipeId}/`,
          payload,
          {headers: {Authorization: `Token ${token}`}}
        );
        isSuccessful.value = true;
      } catch (e) {
        console.error(e);
        // @ts-ignore
        nonFieldErrorMessage.value = `${e.message}. Please try again.`;
      } finally {
        loading.value = false;
      }
    }
  } else {
    // POST request
    loading.value = true;
    try {
      const {data} = await axios.post(
        `${import.meta.env.VITE_API_BASE}/recipe/recipes/`,
        requestBody,
        {headers: {Authorization: `Token ${token}`}}
      );
      if (recipeImage.value) {
        const formData = new FormData();
        formData.append('image', recipeImage.value);

        await axios.post(
          `${import.meta.env.VITE_API_BASE}/recipe/recipes/${data.id}/upload-image/`,
          formData,
          {headers: {Authorization: `Token ${token}`}}
        );
      }
      isSuccessful.value = true;

      // Clear the form
      Object.assign(recipeDetails, initialRecipeDetails);
      recipeDetails.tags = [];
      recipeDetails.ingredients = [];
      clearAllIngredients.value = true;
      clearAllTags.value = true;

      errorMessages.title = '';
      errorMessages.timeMinutes = '';
      errorMessages.price = '';
    } catch (e) {
      console.error(e);
      // @ts-ignore
      nonFieldErrorMessage.value = `${e.message}. Try again.`;
    } finally {
      loading.value = false;
    }
  }
  // Scroll to the top of the page to see the success alert
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
};

const clearOldNewIngredients = () => {
  clearAllIngredients.value = true;
  oldIngredients.value = [];
  recipeDetails.ingredients = [];
}

const clearOldNewTags = () => {
  clearAllTags.value = true;
  oldTags.value = [];
  recipeDetails.tags = [];
}
</script>
