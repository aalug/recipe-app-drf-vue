<template>
  <AppBar/>
  <v-layout class="layout mt-12">
    <router-view/>
  </v-layout>

</template>

<script setup lang="ts">
import AppBar from '@/components/bars/AppBar.vue';

</script>

<style scoped>
.layout {
  width: 60%;
  margin: auto;
}
</style>
