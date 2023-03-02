<template>
  <v-app-bar
    elevation="6"
    class="pr-11">

    <v-app-bar-nav-icon
      variant="text"
      @click.stop="showDrawer = !showDrawer"
    >
    </v-app-bar-nav-icon>

    <v-app-bar-title>Recipe app</v-app-bar-title>
    <template v-slot:append>
      <LoginRegisterBtns v-if="!token"/>
    </template>
  </v-app-bar>

  <v-navigation-drawer
    v-model="showDrawer"
    location="left"
    temporary
  >
    <v-list>
      <v-list-item
        v-if="user"
        :title="user.email"
        :subtitle="user.name"
      />
      <v-divider></v-divider>
    </v-list>

    <v-list>
      <v-list-item @click="changeRoute('home')">
        <v-icon>mdi-home</v-icon>
        Home
      </v-list-item>
      <v-list-item @click="changeRoute('profile')">
        <v-icon>mdi-account</v-icon>
        My Profile
      </v-list-item>

    </v-list>
  </v-navigation-drawer>

</template>

<script setup lang="ts">
import {ref, onMounted} from 'vue';
import {useRouter} from 'vue-router';
import {storeToRefs} from 'pinia';
import {useUserStore} from '@/store/users';
import LoginRegisterBtns from '@/components/bars/LoginRegisterBtns.vue';

const showDrawer = ref<boolean>(false);

const userStore = useUserStore();
const {token, user} = storeToRefs(userStore);

const router = useRouter();

onMounted(async () => {
  await userStore.getUserInfo();
});

const changeRoute = (pathName: string) => {
  router.push({name: pathName});
}

</script>
