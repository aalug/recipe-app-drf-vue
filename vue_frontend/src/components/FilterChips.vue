<template>

  <v-chip-group
    column
    multiple
  >
    <v-chip
      v-for="chip in items"
      v-bind:key="chip.id"
      variant="outlined"
      :color="chipColor"
      @click="handleClick(chip.id)"
    >
      {{ chip.name }}
    </v-chip>
  </v-chip-group>

  <v-btn
    v-if="numberToShow < chipsArrayLength"
    variant="plain"
    color="blue"
    @click="numberToShow += 10"
  >
    Show more
  </v-btn>

</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { Ingredient } from '@/types/Ingredient';
import { Tag } from '@/types/Tag';

const props = defineProps<{
  chips: Tag[] | Ingredient[],
  chipColor: string
}>();

const emit = defineEmits(['selectChip']);

const selected = ref<number[]>([]);

const numberToShow = ref<number>(10);
const chipsArrayLength = computed(() => props.chips.length);

const items = computed(() => {
  return props.chips.slice(0, numberToShow.value);
});

const handleClick = (id: number) => {
  if (!selected.value.includes(id)) {
    selected.value.push(id);
  } else {
    selected.value = selected.value.filter(c => c !== id);
  }
  emit('selectChip', selected.value);
};

</script>
