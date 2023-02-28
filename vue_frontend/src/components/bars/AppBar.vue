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
      <LoginRegisterBtns v-if="!isUserLoggedIn"/>
    </template>
  </v-app-bar>

  <v-navigation-drawer
    v-model="showDrawer"
    location="left"
    temporary
  >
    <v-list>
      <v-list-item @click="changeRoute('home')">
        <v-icon>mdi-home</v-icon>
        Home
      </v-list-item>

    </v-list>
  </v-navigation-drawer>

</template>

<script setup lang="ts">
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import LoginRegisterBtns from '@/components/bars/LoginRegisterBtns.vue'

const showDrawer = ref<boolean>(false)
const isUserLoggedIn = ref<boolean>(false)

const router = useRouter()

const changeRoute = (pathName: string) => {
  router.push({name: pathName})
}

</script>
