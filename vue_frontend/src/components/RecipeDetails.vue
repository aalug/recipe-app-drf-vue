<template>
  <v-dialog
    v-model="showDialog"
    width="1000"
  >
    <v-card :loading="loading">
      <v-img
        v-if="image"
        :src="image"
      ></v-img>

      <v-card-title>
        <span class="text-h5">{{ title }}</span>
      </v-card-title>

      <v-card-text>
        <div class="d-flex justify-space-between">
          <div>
            <h4>Estimated price: <span class="text-decoration-underline"> ${{ price }}</span></h4>
            <h4>Estimated time: <span class="text-decoration-underline">{{ timeMinutes }} minutes </span></h4>
            <h4 v-if="link">
              <a :href="link">Click to see more</a>
            </h4>
          </div>
          <div>
            <div
              v-if="tags"
              class="mb-2"
            >
              <v-chip
                v-for="tag in tags"
                :key="tag.id"
                color="teal-lighten-2"
                class="mb-1 mr-1"
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
                class="mt-1 mr-1"
              >
                {{ ingredient.name }}
              </v-chip>
            </div>
          </div>
        </div>

        <v-divider class="mt-4 mb-6"></v-divider>

        {{ description }}
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>

        <v-btn
          color="blue"
          variant="text"
          @click="showDialog = false"
        >
          Edit
        </v-btn>
        <v-btn
          color="error"
          variant="text"
          @click="showDialog = false"
        >
          Close
        </v-btn>

      </v-card-actions>
    </v-card>
  </v-dialog>

</template>

<script setup lang="ts">
import {ref, onMounted} from 'vue';
import axios from 'axios';
import {useUserStore} from '@/store/users';
import {Tag} from '@/types/Tag';
import {Ingredient} from '@/types/Ingredient';

const props = defineProps<{
  recipeId: number,
}>();

const showDialog = ref<boolean>(true);
const loading = ref<boolean>(false);

const title = ref<string>('');
const timeMinutes = ref<number>(0);
const price = ref<string>('');
const link = ref<string>('');
const tags = ref<Tag[]>([]);
const ingredients = ref<Ingredient[]>([]);
const description = ref<string>('');
const image = ref<string>('');

const token = useUserStore().token;

onMounted(async () => {
  loading.value = true;
  try {
    const {data} = await axios.get(
      `${import.meta.env.VITE_API_BASE}/recipe/recipes/${props.recipeId}/`,
      {headers: {Authorization: `Token ${token}`}}
    )
    title.value = data.title;
    timeMinutes.value = data.timeMinutes;
    price.value = data.price;
    link.value = data.link;
    tags.value = data.tags;
    ingredients.value = data.ingredients;
    description.value = data.description;
    image.value = data.image;
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
});

</script>
