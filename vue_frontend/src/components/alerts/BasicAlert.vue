<template>
  <v-alert
    border="start"
    variant="tonal"
    closable
    close-label="Close Alert"
    :color="color"
    :title="title"
  >
    {{ text }}
  </v-alert>
</template>

<script setup lang="ts">
defineProps<{
  title: string,
  text: string,
  color: string
}>();
</script>
