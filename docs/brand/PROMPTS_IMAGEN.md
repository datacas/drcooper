# Prompts de marca — revisión y versión corregida

`brief_identidad.md` es un buen brief y unos prompts flojos. El brief describe el personaje, la paleta y las restricciones con precisión. Los tres prompts que lo cierran cometen errores que ningún modelo puede resolver por sí solo.

Este documento no sustituye al brief: lo traduce a instrucciones que un generador puede ejecutar.

## Veredicto

Los prompts actuales sirven para explorar direcciones, no para producir el logo. Tres cosas los rompen:

1. **Piden texto.** `Include the exact text DrCooper in a modern geometric sans-serif wordmark` es la petición más fiable para obtener basura tipográfica. Los modelos de imagen no componen letras: las dibujan. Aun cuando aciertan una palabra corta, el resultado no es un logotipo, es un dibujo de un logotipo.
2. **Piden «un rayo amarillo».** El rayo sin geometría definida converge al rayo de Flash, que es justo lo que la sección 5 prohíbe. La prohibición no ayuda: el modelo no tiene un catálogo negativo de marcas, tiene una distribución, y «red shirt + yellow lightning bolt» está saturada de ese referente.
3. **Describen tres personajes distintos.** Medio cuerpo, busto y cabeza-y-hombros con encuadres y detalles diferentes producen tres caras diferentes. Sin una ficha de personaje fija, la mascota no es un personaje: es una coincidencia.

Dos problemas menores: mencionar a Sheldon Cooper en el prompt *aumenta* el parecido, porque el nombre es una señal semántica fuerte; y `gafas obligatorias` no es una instrucción, es una ambigüedad que el modelo resuelve añadiendo gafas y bata.

## Las siete correcciones

| # | Qué falla | Corrección |
|---|---|---|
| 1 | Texto dentro de la imagen | Generar sin texto. El wordmark se compone en vector con una tipografía real |
| 2 | Rayo genérico | Definir el pictograma por geometría: tres segmentos, dos nodos, trazo redondeado |
| 3 | Tres personajes distintos | Una ficha de personaje idéntica en los tres prompts, y la misma semilla |
| 4 | Nombrar lo prohibido | Describir rasgos positivos; los negativos, sin nombrar marcas ni personas |
| 5 | Accesorios ambiguos | Negar explícitamente gafas, bata, pajarita y gadgets |
| 6 | Sin formato de entrega | Fijar proporción, resolución, fondo y número de variantes |
| 7 | Logo y mascota mezclados | Separar: el símbolo identifica, la mascota ilustra. Un personaje no funciona a 32 px |

## Ficha de personaje

Este bloque es fijo. Va literalmente en los tres prompts, y no se toca entre generaciones.

> Original character, not based on any existing person or fictional character. Male, late twenties, slim build, oversized cartoon head roughly one third of total height. Short dark brown hair (#3A2A22) with a clean side part on his right and a single small cowlick at the crown. Warm mid-tone skin (#F2C6A0). Large almond eyes with dark navy irises and a single highlight dot, thick straight eyebrows, straight nose, asymmetric closed-mouth half-smile with the left corner slightly higher. Calm, analytical, faintly amused expression. Bright red crew-neck t-shirt (#E53935) with a darker red collar band (#C62828). No glasses, no lab coat, no bow tie, no badge, no lanyard, no text anywhere. Flat vector cartoon, clean 4 px navy outlines (#152238), flat fills, no gradients, no texture, no photorealism.

La chispa que lleva en el pecho, descrita para que no salga el rayo de Flash:

> On the chest, one small emblem: a lightning mark drawn as a single rounded stroke with three straight segments — down-right, a short back-step left, then down-right again — ending in two rounded terminals. It reads as a spark, not as a comic-book bolt silhouette. Solid #FFD43B, no outline, no double stroke.

## Prompt 1 — mascota (medio cuerpo, sin texto)

```
[FICHA DE PERSONAJE]

Half-body composition, three-quarter view turned slightly to his left, looking at the viewer.
Centered with generous margin. Flat solid background #152238, no gradient, no vignette.
Behind him, at very low opacity, a sparse knowledge graph: four small #2563EB nodes
joined by thin lines, clearly secondary and never overlapping the face.
Style: modern flat vector cartoon for a developer tool, confident geometric shapes,
restrained shading limited to one soft shadow tone, crisp edges.
Square 1:1 canvas, 2048 px. No text, no letters, no watermark, no frame.
```

## Prompt 2 — avatar de GitHub (busto, 1:1)

```
[FICHA DE PERSONAJE]

Bust portrait, head and shoulders, facing the viewer, symmetrical framing,
head occupying 70% of the canvas height, small margin above the hair.
Flat solid #152238 background filling the square. The composition must survive
being cropped to a circle: nothing important outside the central 90%.
High contrast between skin, hair and background. Eyes readable when the image
is scaled down to 64 px.
Square 1:1 canvas, 1024 px. No text, no letters, no border, no badge.
```

## Prompt 3 — símbolo (sin personaje)

```
Minimal app icon for a developer intelligence tool. A single lightning mark drawn
as one rounded stroke with three straight segments: long diagonal down-right,
a short horizontal back-step to the left, then a second long diagonal down-right.
Rounded line caps and joins, stroke weight 12% of the icon width.
Solid #FFD43B on a #152238 rounded square, corner radius 23%.
Perfectly centered, generous padding of 22% on each side.
Flat vector, no gradient, no shadow, no outline, no 3D, no text, no letters.
Must remain legible at 16 px: thick stroke, no thin details, no decoration.
Square 1:1 canvas, 1024 px.
```

## Negativos

Se pasan en el campo negativo, no dentro del prompt positivo:

```
text, letters, words, typography, watermark, signature, logo of an existing brand,
comic-book bolt silhouette, superhero insignia, glasses, spectacles, lab coat,
bow tie, pocket protector, graduation cap, stethoscope, clipboard, 3D render,
gradient, glow, neon, drop shadow, photorealism, photograph, anime, chibi,
extra fingers, deformed hands, two heads, asymmetric eyes, cropped head
```

## Parámetros

- **Semilla fija** mientras se ajusta el personaje; cambiarla solo para explorar.
- **Referencia de imagen** para las variantes 2 y 3: partir del retrato elegido y pedir el nuevo encuadre. Es la única forma fiable de mantener la misma cara.
- **Fondo sólido**, nunca «transparent». Los modelos fingen transparencia con un damero o un halo, y luego hay que recortar a mano.
- **Cuatro variantes por prompt** como mínimo. La primera suele ser la media.
- **No pedir el logo completo.** Pedir el símbolo y el personaje por separado; el lockup se compone después en vector.

## Checklist de aceptación

- [ ] La cara es la misma en las tres imágenes.
- [ ] No hay texto ni letras, ni siquiera deformadas, en ningún borde.
- [ ] El emblema del pecho se lee como chispa y no como el rayo de un superhéroe.
- [ ] Sin gafas, sin bata, sin accesorios no pedidos.
- [ ] El avatar sigue leyéndose a 64 px y no se corta al recortarlo en círculo.
- [ ] El símbolo es distinguible a 16 px.
- [ ] Ningún elemento se parece a una marca registrada existente.

Cuando una imagen pase el checklist, se vectoriza: se traza a mano o se usa un trazador y se limpia. Un PNG generado no es un activo de marca: no escala, no se recolorea y no se puede ajustar el trazo.
