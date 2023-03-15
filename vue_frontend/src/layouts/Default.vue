<template>
  <AppBar :isUserLoggedIn="token !== null"/>
  <v-layout class="layout mt-12">
    <router-view v-if="token !== null"/>
    <PleaseLogIn v-else/>
  </v-layout>

</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { useUserStore } from '@/store/users';
import AppBar from '@/components/bars/AppBar.vue';
import PleaseLogIn from '@/components/PleaseLogIn.vue';

const userStore = useUserStore();
const {token} = storeToRefs(userStore);

onMounted(async () => {
  await userStore.getUserInfo();
});

</script>

<style scoped>
.layout {
  width: 60%;
  margin: auto;
}
</style>
