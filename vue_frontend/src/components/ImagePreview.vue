<template>
  <div
    v-if="image"
    class="text-center"
  >
    <v-menu
      v-model="show"
      :close-on-content-click="false"
      location="end"
    >
      <template v-slot:activator="{ props }">
        <v-btn
          v-bind="props"
          variant="plain"
          class="btnImage"
        >
          <img :src="image" alt="" class="btnImage"/>
        </v-btn>


      </template>

      <v-card min-width="300">

        <v-img :src="image"></v-img>

      </v-card>
    </v-menu>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

defineProps<{
  image: string
}>();

const show = ref<boolean>(false);

</script>

<style scoped>
.btnImage {
  width: 3rem;
  height: 3rem;
  border-radius: 10%;
}
</style>
