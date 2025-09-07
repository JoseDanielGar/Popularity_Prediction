<template>
  <div
    class="bg-[#1e1e1e] text-white min-h-screen flex items-center justify-center p-6"
  >
    <div class="w-full max-w-3xl bg-[#2a2a2a] rounded-2xl shadow-lg p-6">
      <h1
        class="text-4xl font-extrabold text-center bg-gradient-to-r from-white to-[#00b51e] text-transparent bg-clip-text mb-4 tracking-wider"
      >
        More information
      </h1>

      <p class="text-gray-200 text-lg leading-relaxed p-4 text-center">
        Ver el dataset utilizado en
        <a
          href="https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset"
          target="_blank"
          class="text-[#00ff41] hover:text-[#00b51e] font-semibold underline"
        >
          Kaggle.
        </a>
      </p>

      <div class="space-y-4">
        <div
          v-for="(variable, index) in variables"
          :key="index"
          class="p-4 bg-black rounded-xl shadow-md border border-black hover:border-[#00ff41] hover:shadow-lg hover:shadow-[#00ff41]/20 transition"
        >
          <h3
            class="text-xl md:text-xl text-[#008f11] font-bold underline mb-1"
          >
            {{ variable.name }}
          </h3>

          <p class="text-sm italic text-gray-300">Tipo: {{ variable.type }}</p>
          <p class="text-gray-200 mt-1">{{ variable.description }}</p>
        </div>
      </div>

      <div class="pt-6 space-y-4 text-center">
        <button
          @click="$emit('back')"
          class="w-full text-black font-bold py-3 px-4 rounded-full text-lg transition-transform duration-200 transform hover:scale-105 uppercase tracking-wider"
          style="background-color: #008f11"
        >
          Go Back
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
const variables = [
  {
    name: "Danceability",
    type: "float [0-1]",
    description:
      "Qué tan fácil es bailar la canción, considerando ritmo, tempo, fuerza del beat y regularidad. Valores cercanos a 1 indican alta bailabilidad.",
  },
  {
    name: "Energy",
    type: "float [0-1]",
    description:
      "Nivel de intensidad y actividad percibida en la canción. Valores altos suelen corresponder a canciones rápidas, fuertes y enérgicas. Valores bajos se relacionan a canciones suaves o tranquilas.",
  },
  {
    name: "Acousticness",
    type: "float [0-1]",
    description:
      "Confianza de que la pista es acústica. Valores cercanos a 1 indican alta probabilidad de ser completamente acústica.",
  },
  {
    name: "Instrumentalness",
    type: "float [0-1]",
    description:
      "Probabilidad de que la canción no contenga voces. Valores altos sugieren música puramente instrumental, mientras que valores bajos indican presencia de voces.",
  },
  {
    name: "Valence",
    type: "float [0-1]",
    description:
      "Sensación emocional de la pista. Valores altos indican música alegre o positiva, mientras que valores bajos representan música triste o negativa.",
  },
  {
    name: "Speechiness",
    type: "float [0-1]",
    description:
      "Detecta la presencia de palabras habladas. Valores altos corresponden a contenido principalmente hablado (podcast, rap, audiolibros), valores bajos a música.",
  },
  {
    name: "Liveness",
    type: "float [0-1]",
    description:
      "Probabilidad de que la canción haya sido grabada en vivo. Valores cercanos a 1 indican alta probabilidad de actuación en vivo.",
  },
  {
    name: "Tempo (BPM)",
    type: "float",
    description:
      "Velocidad promedio de la canción en beats por minuto (BPM). Indica el ritmo general de la pista.",
  },
  {
    name: "Duration (ms)",
    type: "int",
    description: "Duración total de la canción en milisegundos.",
  },
  {
    name: "Loudness (dB)",
    type: "float",
    description:
      "Volumen promedio de la canción medido en decibelios (dB). Valores más altos indican mayor sonoridad.",
  },
  {
    name: "Explicit",
    type: "boolean",
    description:
      "Indica si la canción contiene letras explícitas o lenguaje para adultos.",
  },
  {
    name: "Key",
    type: "int [1-12]",
    description:
      "Tono musical de la canción. Los valores van de 0 a 11, mapeados a notas musicales (0 = C, 1 = C♯/D♭, 2 = D, ...). -1 indica que no se detectó un tono.",
  },
  {
    name: "Mode",
    type: "int [0-1]",
    description: "Modalidad de la canción: 1 = escala mayor, 0 = escala menor.",
  },
  {
    name: "Time Signature",
    type: "int",
    description:
      "Compás de la canción, indicando cuántos beats hay por medida. Ejemplo: 3 = 3/4, 4 = 4/4.",
  },
  {
    name: "Track Genre",
    type: "category",
    description:
      "Género musical principal de la canción, como pop, rock, jazz, etc.",
  },
];
</script>
