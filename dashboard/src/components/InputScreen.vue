<script setup>
import { reactive } from "vue";

const props = defineProps({ sliders: Array, categories: Object });
const emit = defineEmits(["predict", "update:sliders", "update:categories"]);

// local copy of sliders to avoid direct prop mutation
const localSliders = reactive(JSON.parse(JSON.stringify(props.sliders)));
const localCategories = reactive({ ...props.categories });

const keyOptions = [
  "C (Do)",
  "C♯ / D♭",
  "D (Re)",
  "D♯ / E♭",
  "E (Mi)",
  "F (Fa)",
  "F♯ / G♭",
  "G (Sol)",
  "G♯ / A♭",
  "A (La)",
  "A♯ / B♭",
  "B (Si)",
];

function formatValue(slider) {
  const decimalsMap = { duration_ms: 0, tempo: 1, loudness: 1 };
  const decimals = decimalsMap[slider.id] ?? 2;

  if (slider.id === "duration_ms") {
    // Intl.NumberFormat("es-CO") -> "2.654.000"
    return new Intl.NumberFormat("en-US").format(Math.round(slider.value));
  }

  return Number(slider.value).toFixed(decimals);
}

function updateValue() {
  emit("update:sliders", localSliders); // sync back to parent
}

function updateCategories() {
  emit("update:categories", localCategories);
}

function predict() {
  const values = {
    ...Object.fromEntries(localSliders.map((s) => [s.id, s.value])),
    ...localCategories,
  };
  emit("predict", values);
}
</script>

<style scoped>
.custom-select {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: url("data:image/svg+xml;utf8,<svg fill='%23008f11' height='20' viewBox='0 0 24 24' width='20' xmlns='http://www.w3.org/2000/svg'><path d='M7 10l5 5 5-5z'/></svg>");
  background-repeat: no-repeat;
  background-position: right 0.75rem center;
  background-size: 1.2em;
  padding-right: 2.5rem;
}
</style>

<template>
  <div class="bg-neutral-900 rounded-2xl shadow-2xl p-6 md:p-10 space-y-8">
    <div class="text-center">
      <h1 class="text-3xl md:text-4xl font-bold text-white">
        Song <span style="color: #008f11">Popularity</span> Predictor
      </h1>
      <p class="text-neutral-400 mt-2">
        Adjust the musical features to predict a song's popularity.
      </p>
    </div>

    <!-- SLIDERS -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-6">
      <div v-for="slider in localSliders" :key="slider.id" class="space-y-2">
        <div class="flex justify-between items-center">
          <label :for="slider.id" class="font-medium text-neutral-300">{{
            slider.label
          }}</label>
          <span
            class="text-white font-semibold bg-neutral-700 px-3 py-1 rounded-md text-sm"
          >
            {{ formatValue(slider) }}
          </span>
        </div>
        <input
          type="range"
          v-model.number="slider.value"
          :id="slider.id"
          :min="slider.min"
          :max="slider.max"
          :step="slider.step"
          style="background-color: #008f11"
          @input="updateValue"
        />
      </div>
    </div>

    <!-- Categorical -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
      <!-- Explicit -->
      <div class="flex items-center space-x-3">
        <input
          type="checkbox"
          v-model="localCategories.explicit"
          @change="updateCategories"
          class="w-5 h-5 accent-[#008f11] cursor-pointer"
          id="explicit"
        />
        <label for="explicit" class="text-neutral-300 font-medium"
          >Explicit</label
        >
      </div>

      <!-- Key -->
      <div class="space-y-2">
        <label for="key" class="font-medium text-neutral-300">Key</label>
        <select
          id="key"
          v-model.number="localCategories.key"
          @change="updateCategories"
          class="custom-select w-full bg-neutral-800 text-white font-bold rounded-lg px-3 py-2 focus:ring-2 focus:ring-[#008f11]"
        >
          <option
            v-for="(note, idx) in keyOptions"
            :key="idx"
            :value="idx"
            class="text-white"
          >
            {{ note }}
          </option>
        </select>
      </div>

      <!-- Mode -->
      <div>
        <label class="block text-neutral-300 mb-1">Mode</label>
        <select
          v-model.number="localCategories.mode"
          @change="updateCategories"
          class="custom-select w-full bg-neutral-800 text-white font-bold border border-neutral-700 rounded-md px-2 py-1 focus:outline-none focus:ring-2 focus:ring-[#008f11]"
        >
          <option :value="0" class="text-white">Minor</option>
          <option :value="1" class="text-white">Major</option>
        </select>
      </div>

      <!-- Time Signature -->
      <div>
        <label class="block text-neutral-300 mb-1">Time Signature</label>
        <select
          v-model.number="localCategories.time_signature"
          @change="updateCategories"
          class="custom-select w-full bg-neutral-800 text-white font-bold border border-neutral-700 rounded-md px-2 py-1 focus:outline-none focus:ring-2 focus:ring-[#008f11]"
        >
          <option :value="3" class="text-white">3/4</option>
          <option :value="4" class="text-white">4/4 (Most common)</option>
          <option :value="5" class="text-white">5/4</option>
          <option :value="0" class="text-white">Other (0)</option>
          <option :value="1" class="text-white">Other (1)</option>
          <option :value="2" class="text-white">Other (2)</option>
        </select>
      </div>

      <!-- Track Genre -->
      <div class="md:col-span-2">
        <label class="block text-neutral-300 mb-1">Track Genre</label>
        <input
          type="text"
          v-model="localCategories.track_genre"
          @input="updateCategories"
          placeholder="Search genre..."
          class="w-full bg-neutral-800 text-white font-bold border border-neutral-700 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#008f11]"
        />
        <small class="text-neutral-400"
          >Example: pop, rock, metal, hip hop...</small
        >
      </div>
    </div>

    <!-- Buttons -->
    <!-- Button + Link -->
    <div class="pt-6 space-y-4 text-center">
      <!-- Link a la pantalla de información -->
      <button
        @click="$emit('goInfo')"
        class="text-[#008f11] hover:text-[#00b51e] font-semibold hover:underline"
      >
        More information about the variables...
      </button>

      <!-- Botón de predicción -->
      <button
        @click="predict"
        class="w-full text-black font-bold py-3 px-4 rounded-full text-lg transition-transform duration-200 transform hover:scale-105 uppercase tracking-wider"
        style="background-color: #008f11"
      >
        Predict Popularity
      </button>
    </div>
  </div>
</template>
