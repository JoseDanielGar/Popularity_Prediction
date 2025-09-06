<template>
  <div class="bg-[#1e1e1e] text-white flex items-center justify-center min-h-screen p-4">
    <div class="w-full max-w-2xl mx-auto">
      <InputScreen
        v-if="screen === 'input'"
        :sliders="sliders"
        @update:sliders="sliders = $event"
        @predict="handlePredict"
      />
      <ResultScreen 
        v-else
        :result="result"
        :relevance-data="relevanceData"
        @back="screen = 'input'"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import InputScreen from './components/InputScreen.vue'
import ResultScreen from './components/ResultScreen.vue'

const screen = ref('input')
const result = ref(null)

const sliders = ref([
  { id: 'danceability', label: 'Danceability', min: 0, max: 1, step: 0.01, value: 0.5 },
  { id: 'energy', label: 'Energy', min: 0, max: 1, step: 0.01, value: 0.5 },
  { id: 'acousticness', label: 'Acousticness', min: 0, max: 1, step: 0.01, value: 0.5 },
  { id: 'instrumentalness', label: 'Instrumentalness', min: 0, max: 1, step: 0.01, value: 0.5 },
  { id: 'valence', label: 'Valence', min: 0, max: 1, step: 0.01, value: 0.5 },
  { id: 'tempo', label: 'Tempo (BPM)', min: 50, max: 200, step: 1, value: 120 }
])

const weights = {
  danceability: 0.35,
  energy: 0.25,
  valence: 0.20,
  acousticness: 0.10,
  instrumentalness: -0.07,
  tempo: 0.03
}

const relevanceData = [
  { characteristic: 'Danceability', relevance: 35 },
  { characteristic: 'Energy', relevance: 25 },
  { characteristic: 'Valence', relevance: 20 },
  { characteristic: 'Acousticness', relevance: 10 },
  { characteristic: 'Instrumentalness', relevance: 7 },
  { characteristic: 'Tempo', relevance: 3 }
]

function calculatePopularity(values) {
  const normalizedTempo = (values.tempo - 50) / 150
  let score = values.danceability * weights.danceability
    + values.energy * weights.energy
    + values.valence * weights.valence
    + (1 - values.acousticness) * weights.acousticness
    + (1 - values.instrumentalness) * Math.abs(weights.instrumentalness)
    + normalizedTempo * weights.tempo
  return Math.max(0, Math.min(1, score))
}

import { callApi } from './composables/useApi.js'

async function handlePredict(values) {
  const apiResult = await callApi(values)
  if (apiResult && apiResult.score !== undefined) {
    result.value = { score: apiResult.score }
  } else {
    // fallback if API fails
    result.value = { score: calculatePopularity(values) }
  }
  screen.value = 'result'
}
</script>
