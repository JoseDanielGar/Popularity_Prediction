<template>
  <div
    class="bg-[#1e1e1e] text-white flex items-center justify-center min-h-screen p-4"
  >
    <div class="w-full max-w-2xl mx-auto">
      <InputScreen
        v-if="screen === 'input'"
        :sliders="sliders"
        :categories="categories"
        @update:sliders="sliders = $event"
        @update:categories="categories = $event"
        @predict="handlePredict"
        @goInfo="screen = 'info'"
      />
      <InfoScreen v-else-if="screen === 'info'" @back="screen = 'input'" />
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
import { ref } from "vue";
import InputScreen from "./components/InputScreen.vue";
import ResultScreen from "./components/ResultScreen.vue";
import InfoScreen from "./components/InfoScreen.vue";

const screen = ref("input");
const result = ref(null);

const sliders = ref([
  {
    id: "danceability",
    label: "Danceability",
    min: 0,
    max: 1,
    step: 0.01,
  },
  { id: "energy", label: "Energy", min: 0, max: 1, step: 0.01 },
  {
    id: "acousticness",
    label: "Acousticness",
    min: 0,
    max: 1,
    step: 0.01,
  },
  {
    id: "instrumentalness",
    label: "Instrumentalness",
    min: 0,
    max: 1,
    step: 0.01,
  },
  { id: "valence", label: "Valence", min: 0, max: 1, step: 0.01 },
  {
    id: "speechiness",
    label: "Speechiness",
    min: 0,
    max: 1,
    step: 0.01,
  },
  { id: "liveness", label: "Liveness", min: 0, max: 1, step: 0.01 },
  { id: "tempo", label: "Tempo (BPM)", min: 0, max: 250, step: 0.1 },
  {
    id: "duration_ms",
    label: "Duration (ms)",
    min: 8000,
    max: 5300000,
    step: 1000,
  },

  {
    id: "loudness",
    label: "Loudness (dB)",
    min: -50,
    max: 5,
    step: 0.1,
  },
]);

const categories = ref({
  explicit: false,
  key: 0,
  mode: 1,
  time_signature: 4,
  track_genre: "acoustic",
});

sliders.value.forEach((f) => {
  const mid = (f.min + f.max) / 2;
  if (["duration_ms", "key", "mode", "time_signature"].includes(f.id)) {
    f.value = Math.round(mid / f.step) * f.step;
  } else {
    const decimals = f.id === "tempo" || f.id === "loudness" ? 1 : 2;
    f.value = Number(mid.toFixed(decimals));
  }
});

const weights = {
  danceability: 0.35,
  energy: 0.25,
  valence: 0.2,
  acousticness: 0.1,
  instrumentalness: -0.07,
  tempo: 0.03,
};

const relevanceData = [
  { characteristic: "Danceability", relevance: 35 },
  { characteristic: "Energy", relevance: 25 },
  { characteristic: "Valence", relevance: 20 },
  { characteristic: "Acousticness", relevance: 10 },
  { characteristic: "Instrumentalness", relevance: 7 },
  { characteristic: "Tempo", relevance: 3 },
];

function calculatePopularity(values) {
  const normalizedTempo = (values.tempo - 50) / 150;
  let score =
    values.danceability * weights.danceability +
    values.energy * weights.energy +
    values.valence * weights.valence +
    (1 - values.acousticness) * weights.acousticness +
    (1 - values.instrumentalness) * Math.abs(weights.instrumentalness) +
    normalizedTempo * weights.tempo;
  return Math.max(0, Math.min(1, score));
}

import { callApi } from "./composables/useApi.js";

async function handlePredict(values) {
  const apiResult = await callApi(values);
  if (apiResult && apiResult.score !== undefined) {
    result.value = { score: apiResult.score };
  } else {
    // fallback if API fails
    result.value = { score: calculatePopularity(values) };
  }
  screen.value = "result";
}
</script>
