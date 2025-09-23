# 🎵 Manual de Usuario

- **Proyecto:** Popularity Prediction Dashboard
- **Versión:** 1.0
- **Fecha:** 2025-09

---

## Introducción

Este manual describe cómo usar el **Popularity Prediction Dashboard**, una herramienta web que permite ingresar características de una canción y obtener una predicción categórica de su popularidad (Low / Medium / High).

## Requisitos

- Navegador moderno: Chrome, Firefox o Edge (versiones recientes).
- Conexión a Internet para acceder a la URL del dashboard.
- URL de acceso.

## Pantallas

### 1. Input Screen

**Función:** ingresar las características de la canción para realizar la predicción.

**Elementos principales**:

- **Sliders**: ajustar valores numéricos (Danceability, Acousticness, Valence, Liveness, Duration, Energy, Instrumentalness, Speechiness, Tempo y Loudness).

- **Selectores**: opciones categóricas (Key, Mode, Time Signature y Track Genre).

- **Botón _Predict Popularity_**: envía los valores al modelo y muestra la predicción.

- **Botón _More information about the variables_**: abre la pantalla que contiene una descripción de las variables.

![Input Screen](<img/Input Screen.png>)

### 2. Info Screen

Función: consultar la descripción y el tipo de cada variable empleada por el modelo.

Contenido:

- Lista de variables con su **definición**, **rango** y **tipo de dato**.

- Enlace al dataset original (Kaggle) para referencia adicional.

- **Botón _Go back_**: vuelve a la pantaña de inicio.

![Info Screen](<img/Info Screen.png>)

![Info Screen 2](<img/Info Screen 2.png>)

### 3. Result Screen

Función: presentar el resultado de la predicción y explicar las variables más relevantes.

Elementos:

- **Resultado Categórico**: `Low`, `Medium` o `High`.
- **Tabla de características relevantes**: columnas con el nombre de la variable y su importancia o contribución al resultado.
- **Botón _Try again_** volver a la pantalla de inicio y probar otra canción.

Interpretación rápida:

- **Low**: probabilidad baja de alta popularidad.
- **Medium**: probabilidad moderada.
- **High**: probabilidad alta de que la canción tenga fuerte aceptación.

![Result Screen](<img/Result Screen.png>)

## Ejemplo paso a paso

1. Abrir la URL del dashboard en el navegador.
2. En la **Input Screen**, ajustar los sliders y selecciones.
3. Pulsar **Predict Popularity**.
4. Revisar la **Result Screen**: leer la categoría y la tabla con las variables más influyentes.
5. Si se desea, volver a la Input Screen y modificar parámetros.

A continuación, se muestran ejemplos de casos de prediciones: alta, media y baja.

### 1. Ejemplo de una predicción alta

En la pantalla de Input Screen se utilizaron los siguientes valores:

| Variable         | Valor    |
| ---------------- | -------- |
| Duration         | 210000   |
| Explicit         | No check |
| Danceability     | 0.35     |
| Energy           | 0.25     |
| Key              | C (DO)   |
| Loudness         | -12.0    |
| Mode             | Major    |
| Speechiness      | 0.04     |
| Acousticness     | 0.85     |
| Instrumentalness | 0.0000   |
| Liveness         | 0.12     |
| Valence          | 0.30     |
| Tempo            | 72.0     |
| Time Signature   | 3/4      |
| Track Genre      | acoustic |

#### Input Screen:

![Input Screen para la predicción alta](<img/Input Screen - High values.png>)

#### Result Screen:

![Result Screen para la predicción alta](<img/Result Screen - high prediction.png>)

### 2. Ejemplo de una predicción media

En la pantalla de Input Screen se utilizaron los siguientes valores:

| Variable         | Valor    |
| ---------------- | -------- |
| Duration         | 320000   |
| Explicit         | No check |
| Danceability     | 0.92     |
| Energy           | 0.97     |
| Key              | A (La)   |
| Loudness         | -2.0     |
| Mode             | Minor    |
| Speechiness      | 0.03     |
| Acousticness     | 0.02     |
| Instrumentalness | 0.85     |
| Liveness         | 0.35     |
| Valence          | 0.55     |
| Tempo            | 128.0    |
| Time Signature   | 4/4      |
| Track Genre      | metal    |

#### Input Screen:

![Input Screen para la predicción media](<img/Input Screen - medium values.png>)

#### Result Screen:

![Result Screen para la predicción media](<img/Result Screen - medium prediction.png>)

### 3. Ejemplo de una predicción baja

En la pantalla de Input Screen se utilizaron los siguientes valores:

| Variable         | Valor    |
| ---------------- | -------- |
| Duration         | 250000   |
| Explicit         | No check |
| Danceability     | 0.75     |
| Energy           | 0.88     |
| Key              | G (sol)  |
| Loudness         | -4.5     |
| Mode             | Major    |
| Speechiness      | 0.06     |
| Acousticness     | 0.12     |
| Instrumentalness | 0.0001   |
| Liveness         | 0.18     |
| Valence          | 0.65     |
| Tempo            | 124.0    |
| Time Signature   | 4/4      |
| Track Genre      | pop      |

#### Input Screen:

![Input Screen para la predicción baja](<img/Input Screen - low values.png>)

#### Result Screen:

![Result Screen para la predicción baja](<img/Result Screen - low prediction.png>)

## Descripción de las variables

### Danceability

Qué tan fácil es bailar la canción, considerando ritmo, tempo, fuerza del beat y regularidad. Valores cercanos a 1 indican alta bailabilidad.

### Energy

Nivel de intensidad y actividad percibida en la canción. Valores altos suelen corresponder a canciones rápidas, fuertes y enérgicas. Valores bajos se relacionan a canciones suaves o tranquilas.

### Acousticness

Confianza de que la pista es acústica. Valores cercanos a 1 indican alta probabilidad de ser completamente acústica.

### Instrumentalness

Probabilidad de que la canción no contenga voces. Valores altos sugieren música puramente instrumental, mientras que valores bajos indican presencia de voces.

### Valence

Sensación emocional de la pista. Valores altos indican música alegre o positiva, mientras que valores bajos representan música triste o negativa.

### Speechiness

Detecta la presencia de palabras habladas. Valores altos corresponden a contenido principalmente hablado, valores bajos a música.

### Liveness

Probabilidad de que la canción haya sido grabada en vivo. Valores cercanos a 1 indican alta probabilidad de actuación en vivo.

### Tempo

Velocidad promedio de la canción en beats por minuto (BPM). Indica el ritmo general de la pista.

### Duration

Duración total de la canción en milisegundos.

### Loudness

Volumen promedio de la canción medido en decibelios (dB). Valores más altos indican mayor sonoridad.

### Explicit

Si la canción tiene contenido explícito, como lenguaje o referencias sexuales, violencia o temas para adultos.

### Key

Tonalidad musical de la canción.

| Nota    | Descripción breve                                                 |
| ------- | ----------------------------------------------------------------- |
| C (Do)  | Tonalidad mayor de Do. Base común en música occidental.           |
| C♯ / D♭ | Do sostenido o Re bemol. Sonoridad brillante y tensa.             |
| D (Re)  | Tonalidad de Re. Muy usada en música folk y clásica.              |
| D♯ / E♭ | Re sostenido o Mi bemol. Usada en jazz y música romántica.        |
| E (Mi)  | Tonalidad de Mi. Frecuente en guitarra por la afinación estándar. |
| F (Fa)  | Tonalidad de Fa. Muy empleada en música coral y clásica.          |
| F♯ / G♭ | Fa sostenido o Sol bemol. Tonalidad con mucha tensión.            |
| G (Sol) | Tonalidad de Sol. Muy común en rock y música popular.             |
| G♯ / A♭ | Sol sostenido o La bemol. Rica en color armónico.                 |
| A (La)  | Tonalidad de La. Muy frecuente en música pop y rock.              |
| A♯ / B♭ | La sostenido o Si bemol. Usada en jazz y orquestal.               |
| B (Si)  | Tonalidad de Si. Brillante, con sonoridad abierta.                |

### Mode

Modalidad de la canción.

| Modalidad | Descripción breve                                    |
| --------- | ---------------------------------------------------- |
| Major     | Escala mayor, relacionada con alegría.               |
| Minor     | Escala menor, relacionada con tristeza o melancolía. |

### Time Signature

Compás o asignatura del tiempo, indica el patrón rítmico o la estructura métrica de la canción.

| Compás          | Descripción breve                                                                            |
| --------------- | -------------------------------------------------------------------------------------------- |
| 4/4             | El más común en la música occidental. 4 tiempos por compás, usado en pop, rock, jazz, etc.   |
| 3/4             | Compás de vals. 3 tiempos por compás, frecuente en música clásica y baladas.                 |
| 5/4             | Métrica irregular con 5 tiempos por compás. Ejemplo famoso: _Take Five_ de Dave Brubeck.     |
| 1/4             | Compás con 1 tiempo por compás. Muy poco común, suele aparecer en fragmentos experimentales. |
| No especificado | Representa un compás no estándar.                                                            |

### Track Genre

Género musical principal de la canción.

| Género            | Descripción breve                                                      |
| ----------------- | ---------------------------------------------------------------------- |
| acoustic          | Música con instrumentos acústicos, sin efectos electrónicos.           |
| punk-rock         | Subgénero del rock con ritmos rápidos y agresivos.                     |
| progressive-house | Estilo de música electrónica con progresiones largas y ambientales.    |
| power-pop         | Rock con melodías pegadizas y estructuras cercanas al pop.             |
| pop               | Género popular con estructuras simples y gran alcance comercial.       |
| pop-film          | Música pop usada en bandas sonoras de películas.                       |
| piano             | Piezas centradas en el piano como instrumento principal.               |
| party             | Música animada y rítmica para ambientes de fiesta.                     |
| pagode            | Subgénero del samba brasileño con letras románticas y festivas.        |
| opera             | Música vocal clásica con acompañamiento orquestal.                     |
| new-age           | Música instrumental relajante y atmosférica, usada en meditación.      |
| mpb               | Música Popular Brasileña, mezcla de samba, bossa nova y otros estilos. |
| minimal-techno    | Estilo de techno con estructuras repetitivas y minimalistas.           |
| metalcore         | Fusión de heavy metal y hardcore punk, con voces agresivas.            |
| metal             | Género con guitarras distorsionadas, baterías potentes y alta energía. |
