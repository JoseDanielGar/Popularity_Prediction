<script setup>
import { reactive } from 'vue'

const props = defineProps({ sliders: Array })
const emit = defineEmits(['predict', 'update:sliders'])

// local copy of sliders to avoid direct prop mutation
const localSliders = reactive(JSON.parse(JSON.stringify(props.sliders)))

function formatValue(slider) {
  return slider.id === 'tempo' ? parseInt(slider.value) : slider.value.toFixed(2)
}

function updateValue() {
  emit('update:sliders', localSliders) // sync back to parent
}

function predict() {
  const values = Object.fromEntries(localSliders.map(s => [s.id, s.value]))
  emit('predict', values)
}
</script>

<template>
  <div class="bg-neutral-900 rounded-2xl shadow-2xl p-6 md:p-10 space-y-8">
    <div class="text-center">
      <h1 class="text-3xl md:text-4xl font-bold text-white">
        Song <span style="color: #008F11">Popularity</span> Predictor
      </h1>
      <p class="text-neutral-400 mt-2">Adjust the musical features to predict a song's popularity.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-6">
      <div v-for="slider in localSliders" :key="slider.id" class="space-y-2">
        <div class="flex justify-between items-center">
          <label :for="slider.id" class="font-medium text-neutral-300">{{ slider.label }}</label>
          <span class="text-white font-semibold bg-neutral-700 px-3 py-1 rounded-md text-sm">
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
          style="background-color: #008F11;"
          @input="updateValue"
        />
      </div>
    </div>

    <div class="pt-6">
      <button @click="predict" class="w-full text-black font-bold py-3 px-4 rounded-full text-lg transition-transform duration-200 transform hover:scale-105 uppercase tracking-wider" style="background-color: #008F11;">
        Predict Popularity
      </button>
    </div>
  </div>
</template>