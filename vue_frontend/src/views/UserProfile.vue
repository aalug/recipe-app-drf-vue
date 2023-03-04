<template>
  <v-card
    class="mx-auto py-8 px-8"
    style="width: 50%"
  >
    <v-progress-linear
      v-if="loading"
      indeterminate
      :height="5"
      style="position: absolute;"
    ></v-progress-linear>

    <v-card-title class="mb-6">
      <span class="text-h4">Change account info</span>
    </v-card-title>

    <BasicAlert
      v-if="isSuccessful"
      title="Success!"
      color="success"
      text="You have successfully changed your information."
      class="mb-5 mt-2"
    />

    <v-form @submit.prevent="handleSubmit()">
      <v-text-field
        v-model="email"
        label="E-mail"
      ></v-text-field>
      <v-text-field
        v-model="name"
        label="Name"
      ></v-text-field>

      <v-text-field
        v-model="password"
        label="Password"
        :append-icon="showPass ? 'mdi-eye' : 'mdi-eye-off'"
        :type="showPass ? 'text' : 'password'"
        hint="At least 6 characters"
        @click:append="showPass = !showPass"
      ></v-text-field>

      <p v-if="errorMessage" class="text-error">{{ errorMessage }}</p>

      <v-btn
        type="submit"
        color="green-darken-2"
        :disabled="loading"
        block
        class="mt-2"
      >
        Save
      </v-btn>
    </v-form>
  </v-card>
</template>

<script setup lang="ts">
import {ref, onMounted} from 'vue';
import {storeToRefs} from "pinia"
import {useUserStore} from '@/store/users';
import BasicAlert from '@/components/alerts/BasicAlert.vue';

const userStore = useUserStore();
const {loading, errorMessage, isSuccessful, user} = storeToRefs(userStore);

const email = ref<string>('');
const name = ref<string>('');
const password = ref<string>('');
const showPass = ref<boolean>(false)

onMounted(async () => {
  /**
   * on mount, get the user data and set the values
   * so that the fields are prepopulated.
   */
  await userStore.getUserInfo()
  email.value = user.value.email
  name.value = user.value.name
})
const handleSubmit = async () => {
  await userStore.updateUserProfile(
    email.value,
    name.value,
    password.value
  )
}

</script>
