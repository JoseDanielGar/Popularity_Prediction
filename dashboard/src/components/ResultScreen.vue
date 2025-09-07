<template>
  <div class="bg-neutral-900 rounded-2xl shadow-2xl p-6 md:p-10 space-y-8">
    <div class="text-center">
      <h1 class="text-3xl md:text-4xl font-bold text-white">Prediction Result</h1>
    </div>

    <div :class="['text-center p-6 rounded-lg', colorClasses]">
      <p class="text-5xl font-extrabold">{{ classification }}</p>
    </div>

    <div>
      <h2 class="text-xl font-semibold text-center mb-4 text-neutral-300">Influential Characteristics</h2>
      <div class="overflow-x-auto">
        <table class="min-w-full bg-neutral-800 rounded-lg">
          <thead class="border-b border-neutral-700">
            <tr>
              <th class="text-left py-3 px-4 font-semibold text-sm text-neutral-400 uppercase tracking-wider">Characteristic</th>
              <th class="text-right py-3 px-4 font-semibold text-sm text-neutral-400 uppercase tracking-wider">Relevance</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in relevanceData" :key="index" class="border-t border-neutral-700">
              <td class="py-3 px-4 text-neutral-300">{{ item.characteristic }}</td>
              <td class="py-3 px-4 text-right font-mono text-neutral-400">{{ item.relevance }}%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="pt-6">
      <button @click="$emit('back')" class="w-full bg-transparent hover:bg-white/10 border-2 border-white/50 text-white font-bold py-3 px-4 rounded-full text-lg transition-all duration-200 uppercase tracking-wider">
        Try Again
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({ result: Object, relevanceData: Array })

const score = props.result?.score ?? 0
let classification = ''
let colorClasses = ''

if (score < 0.45) {
  classification = 'Low'
  colorClasses = 'bg-red-900/50 text-red-400'
} else if (score < 0.70) {
  classification = 'Medium'
  colorClasses = 'bg-yellow-900/50 text-yellow-400'
} else {
  classification = 'High'
  colorClasses = 'bg-green-900/50 text-green-400'
}
</script>
