<template>

  <ConfirmDialog
    v-if="showConfirmationDialog"
    :key="refreshConfirmDialog"
    title="Are you sure"
    :text="`you want to delete ${type}: ${name}?`"
    @confirm="handleConfirmingDelete"
  />

  <v-dialog
    v-model="showDialog"
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
        <span class="text-h6">Edit <span :style="`color: var(--${color})`">{{ name }}</span> {{ type }}</span>
      </v-card-title>

      <v-btn
        icon="mdi-close"
        variant="text"
        style="position: absolute; top: 0.3rem; right: 0.3rem;"
        @click="showDialog = false"
      >
      </v-btn>

      <v-form @submit.prevent="handleSubmit()">
        <v-text-field
          v-model="newName"
          :rules="[v => !!v || 'Name cannot be empty']"
          label="Name"
          required
        ></v-text-field>

        <p
          v-if="errorMessage"
          class="text-error"
        >
          {{ errorMessage }}
        </p>

        <div class="d-flex flex-column mt-10">
          <v-btn
            :color="`var(--${color})`"
            :disabled="loading"
            type="submit"
          >
            Save
          </v-btn>

          <v-btn
            color="error"
            class="mt-2"
            :disabled="loading"
            @click="startDeletingProcess()"
          >
            Delete
          </v-btn>

        </div>
      </v-form>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/store/users';
import ConfirmDialog from '@/components/ConfirmDialog.vue';

const props = defineProps<{
  id: number,
  name: string,
  type: string,
  color: string
}>();

const emit = defineEmits(['closeDialog', 'save', 'delete']);

const showDialog = ref<boolean>(true);
const newName = ref<string>(props.name);
const loading = ref<boolean>(false);
const errorMessage = ref<string>('');
const showConfirmationDialog = ref<boolean>(false);
const refreshConfirmDialog = ref<boolean>(false);

const token = useUserStore().token;

const handleSubmit = async () => {
  /**
   * Handle submitting the form.
   */
  // If the name has not changed, do not send a request, just close the dialog.
  if (newName.value === props.name) return showDialog.value = false;

  loading.value = true;
  try {
    await axios.patch(
      `${import.meta.env.VITE_API_BASE}/recipe/${props.type}s/${props.id}/`,
      {name: newName.value},
      {headers: {Authorization: `Token ${token}`}}
    );
    // Send info to the parent component to highlight element that
    // was here updated.
    emit('save', `${props.type}${props.id}`);
    showDialog.value = false;
  } catch (e) {
    console.error(e);
    // @ts-ignore
    errorMessage.value = `${e.message}. Please try again.`;
  } finally {
    loading.value = false;
  }
};

const deleteItem = async () => {
  /**
   * Delete the tag or ingredient by sending `delete` request to the server.
   */
  loading.value = true;
  try {
    await axios.delete(
      `${import.meta.env.VITE_API_BASE}/recipe/${props.type}s/${props.id}/`,
      {headers: {Authorization: `Token ${token}`}}
    );
    // Send info to the parent component to update the list without the deleted item.
    emit('delete', props.id);
    showDialog.value = false;
  } catch (e) {
    console.error(e);
    // @ts-ignore
    errorMessage.value = `${e.message}. Please try again.`;
  } finally {
    loading.value = false;
  }
};

const startDeletingProcess = () => {
  /**
   * Start deleting process. After the `delete` button is clicked, this function
   * will be called, and it will:
   * 1. Refresh the dialog component
   * 2. Display the confirmation dialog
   */
  showConfirmationDialog.value = true;
  refreshConfirmDialog.value = !refreshConfirmDialog.value;
};

const handleConfirmingDelete = async (isConfirmed: boolean) => {
  /**
   * This function is called when dialog has received a response (emit).
   * If the response is `OK` then it will proceed and delete the recipe.
   */
  if (isConfirmed) {
    await deleteItem();
  }
};

watch(showDialog, () => {
  /**
   * If the `showDialog` value changes, inform the parent component,
   * so it can refresh this component. It will allow to open EditAttributeDialog
   * of the same item more than one time in a row.
   */
  emit('closeDialog', false);
});

</script>
