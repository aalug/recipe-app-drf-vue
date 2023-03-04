<template>
  <v-dialog
    v-model="showDialog"
    persistent
    width="1024"
  >
    <v-card
      class="py-8 px-5"
      style="width: 50%; margin: auto;"
    >

      <v-progress-linear
        v-if="loading"
        indeterminate
        :height="5"
        style="position: absolute;"
      ></v-progress-linear>

      <v-card-title class="mb-6">
        <span class="text-h4">Register</span>
      </v-card-title>

      <v-btn
        color="red"
        icon="mdi-close"
        variant="text"
        style="position: absolute; top: 0.3rem; right: 0.3rem;"
        @click="showDialog = false"
      >
      </v-btn>

      <BasicAlert
        v-if="isSuccessful"
        title="Success!"
        text="You have successfully created an account."
        color="success"
        class="mb-5 mt-2"
      />

      <v-form @submit.prevent="handleSubmit()">
        <v-text-field
          v-model="email"
          :rules="[v => !!v || 'Email is required']"
          label="E-mail"
          required
        ></v-text-field>

        <v-text-field
          v-model="name"
          :rules="[v => !!v || 'Name is required']"
          label="Name"
          required
        ></v-text-field>

        <v-text-field
          v-model="password"
          :rules="[v => !!v || 'Password is required']"
          label="Password"
          required
          :append-icon="showPass ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showPass ? 'text' : 'password'"
          hint="At least 6 characters"
          @click:append="showPass = !showPass"
        ></v-text-field>

        <p
          v-if="errorMessage"
          class="text-error"
        >
          {{ errorMessage }}
        </p>

        <div class="d-flex flex-column mt-10">
          <v-btn
            color="teal-darken-3"
            type="submit"
            :disabled="loading"
          >
            Submit
          </v-btn>

        </div>
      </v-form>
    </v-card>
  </v-dialog>

</template>

<script setup lang="ts">
import {ref} from 'vue';
import {storeToRefs} from 'pinia';
import {useUserStore} from '@/store/users';
import BasicAlert from '@/components/alerts/BasicAlert.vue';

const email = ref<string>('');
const name = ref<string>('');
const password = ref<string>('');

const showPass = ref<boolean>(false);
const showDialog = ref<boolean>(true);

const userStore = useUserStore();
const {loading, errorMessage, isSuccessful} = storeToRefs(userStore);

const handleSubmit = async () => {
  await userStore.handleRegister(
    email.value,
    name.value,
    password.value
  );
}

</script>
