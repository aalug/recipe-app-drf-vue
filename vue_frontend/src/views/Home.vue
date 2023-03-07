<template>
  <v-container>
    <span class="text-h3 mt-6 mb-16 text-center">Recipes app</span>
  <v-card
    class="d-flex mt-10 pt-7 px-4"
    style="width: 80%; height: 80vh;"
  >
    <v-card
      color="deep-orange"
      class="card"
      @click="changeRoute('list-recipes')"
    >
      <v-card-title class="d-flex justify-center align-center" style="height: 100%">
        <span class="text-h4">
          My Recipes
        </span>
      </v-card-title>
    </v-card>

    <v-card
      color="blue"
      class="card"
      @click="changeRoute('create-recipe')"
    >
      <v-card-title class="d-flex justify-center align-center" style="height: 100%">
        <span class="text-h4">
          Create
        </span>
      </v-card-title>
    </v-card>


  </v-card>
  </v-container>
</template>

<script setup lang="ts">
import {useRouter} from 'vue-router';

const router = useRouter()

const changeRoute = (pathName: string): void => {
  router.push({name: pathName});
}

</script>

<style scoped>
.card {
  width: 16rem;
  height: 10rem;
  margin: 1rem auto auto 2rem;
  transition: transform 0.2s ease-in-out;
  cursor: pointer;
  transform-origin: center;
}

.card:hover {
  transform: scale(1.05);
  box-shadow: 0 5px 10px 0 rgba(0, 0, 0, 0.8);
}
</style>
