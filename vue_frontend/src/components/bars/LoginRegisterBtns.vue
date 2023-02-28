<template>
  <RegisterFormDialog
    v-if="showRegisterDialog"
    :key="refreshingRegisterDialog"
  />
  <LoginFormDialog
    v-if="showLoginDialog"
    :key="refreshingLoginDialog"
  />

  <div>
    <v-btn
      variant="outlined"
      prepend-icon="mdi-login-variant"
      color="cyan-darken-3"
      rounded="lg"
      class="mr-3"
      @click="showLoginDialog = true;
      refreshingLoginDialog = !refreshingLoginDialog"
    >
      Login
    </v-btn>

    <v-btn
      variant="outlined"
      prepend-icon="mdi-account-plus"
      color="teal-darken-3"
      rounded="lg"
      @click="showRegisterDialog = true;
      refreshingRegisterDialog = !refreshingRegisterDialog"
    >
      Register
    </v-btn>
  </div>
</template>

<script setup lang="ts">
import {ref} from 'vue'
import RegisterFormDialog from '@/components/dialog-forms/RegisterFormDialog.vue'
import LoginFormDialog from '@/components/dialog-forms/LoginFormDialog.vue'

const showRegisterDialog = ref<boolean>(false)
const showLoginDialog = ref<boolean>(false)
const refreshingRegisterDialog = ref<boolean>(false)
const refreshingLoginDialog = ref<boolean>(false)

</script>
