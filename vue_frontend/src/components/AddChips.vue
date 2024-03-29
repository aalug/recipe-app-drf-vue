<template>
  <v-container
    class="mx-auto"
    max-width="500"
  >

    <v-container>
      <v-row
        align="center"
        justify="start"
      >
        <v-col
          v-for="selection in selections"
          :key="selection"
          cols="auto"
          class="py-1 pe-0"
        >
          <v-chip
            :color="chipColor"
            closable
            @click:close="removeItem(selection)"
          >
            {{ selection }}
          </v-chip>
        </v-col>

        <v-col cols="12">
          <v-text-field
            :id="`${itemType}Id`"
            v-model="newItem"
            hide-details
            :label="`Add ${article} ${itemType}`"
            single-line
            @keyup.enter="addItem()"
            @focus="afterClear()"
          ></v-text-field>
        </v-col>
      </v-row>
    </v-container>

    <v-divider></v-divider>

    <v-card-actions>
      <v-spacer></v-spacer>

      <v-btn
        :color="chipColor"
        variant="text"
        @click="addItem()"
      >
        Add
      </v-btn>
    </v-card-actions>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

const props = defineProps<{
  itemType: string,
  chipColor: string,
  alreadySelected: string[],
  clearAllChips: boolean
}>();

const emit = defineEmits([
  'addChip', 'removeChip', 'afterClear'
]);

const selected = ref<string[]>([]);
const newItem = ref<string>('');
const clearAll = ref<boolean>(false);

let runClear = true;

onMounted(() => {
  if (props.alreadySelected) {
    selected.value = props.alreadySelected;
  }
  if (props.clearAllChips) clearAll.value = true;
});

const determineArticle = (word: string): string => {
  const vowels = ['a', 'e', 'i', 'o', 'u'];
  if (vowels.includes(word[0].toLowerCase())) {
    return 'an';
  } else {
    return 'a';
  }
};
const article: string = determineArticle(props.itemType);

const selections = computed(() => {
  const selections = [];
  if (!props.clearAllChips) {
    for (const selection of selected.value) {
      selections.push(selection);
    }
  }
  return selections;
});


const addItem = () => {
  /**
   * * If the item is not already in the selected list, add it, and emit an event
   * * to the parent component. The parent component needs this data to later send a request.
   */
  const trimmedValue = newItem.value.trim();
  if (!trimmedValue || selected.value.includes(newItem.value)) return;

  selected.value.push(trimmedValue);
  emit('addChip', {
    itemType: props.itemType,
    itemName: newItem.value
  });
  newItem.value = '';
  document.getElementById(`${props.itemType}Id`)?.focus();
};

const removeItem = (value: string) => {
  /**
   * Remove the item from the selected list and emit an event to the parent
   * component for it to do the same.
   */
  selected.value = selected.value.filter(v => v !== value);
  emit('removeChip', {
    itemType: props.itemType,
    itemName: value
  });
};

const afterClear = () => {
  if (runClear && props.clearAllChips) {
    clearAll.value = false;
    emit('afterClear');
    selected.value = [];
    runClear = false;
  }
};

</script>
