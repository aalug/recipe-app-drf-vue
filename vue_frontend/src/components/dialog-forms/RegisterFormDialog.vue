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
      <v-card-title>
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

      <v-form
        ref="form"
        :loading="loading"
        @submit.prevent="handleSubmit()"
      >
        <v-text-field
          v-model="email"
          :rules="[
            v => !!v || 'Email is required',
            v => validateEmail(v) || 'E-mail is invalid'
            ]"
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
          :rules="[
            v => !!v || 'Password is required',
            v => v.length > 5 || 'Password must be at least 6 characters'
            ]"
          label="Password"
          required
          :append-icon="showPass ? 'mdi-eye' : 'mdi-eye-off'"
          :type="showPass ? 'text' : 'password'"
          hint="At least 6 characters"
          @click:append="showPass = !showPass"
        ></v-text-field>

        <div class="d-flex flex-column">
          <v-btn
            color="teal-darken-3"
            class="mt-4"
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
import {ref} from 'vue'
import {validateEmail} from '@/utils/validate-email'

const email = ref<string>('')
const name = ref<string>('')
const password = ref<string>('')

const showPass = ref<boolean>(false)
const showDialog = ref<boolean>(true)
const loading = ref<boolean>(false)

const handleSubmit = async () => {
  loading.value = true
  try {
    console.log('start submitting')
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
    showDialog.value = false
  }
}

</script>
