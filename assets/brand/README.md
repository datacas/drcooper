# Marca de DrCooper

Propuesta vectorial completa. Todo es SVG editable; los PNG son exportaciones, no fuentes.

| Archivo | Uso |
|---|---|
| `logo.svg` | Lockup horizontal para fondo claro |
| `logo-dark.svg` | Lockup horizontal para fondo oscuro |
| `symbol.svg` | Símbolo suelto: tile navy con la chispa. Avatar de organización, app icon, favicon |
| `mascot.svg` | Mascota en disco navy. Avatar de GitHub y redes |
| `png/` | Exportaciones: logo 1600 px, símbolo 512, mascota 512, avatar 128/64, favicon 32 |

## Sistema

La marca tiene dos piezas con funciones distintas, y no se sustituyen entre sí:

- **Símbolo** — la chispa: un rayo trazado en tres segmentos entre dos nodos. Es lo que sobrevive a 16 px, lo que va en el favicon y lo que puede ir solo.
- **Mascota** — el personaje. Aporta carácter, no identificación a tamaño pequeño.

La mascota lleva el símbolo en la camiseta: el mismo trazo, no un rayo de cómic. Así el emblema del personaje y la marca son el mismo dibujo.

## Paleta

| Rol | Color | Contraste |
|---|---|---|
| Fondo / tinta | `#152238` | 15.9:1 sobre blanco |
| Acento | `#FFD43B` | 11.2:1 sobre navy · **1.4:1 sobre blanco** |
| Camiseta | `#E53935` | 4.2:1 con blanco encima |
| Secundario | `#2563EB` | 5.2:1 sobre blanco |
| Base | `#FFFFFF` | — |

El amarillo nunca va suelto sobre blanco: no alcanza contraste ni como texto ni como gráfico. Sobre navy sí. Si hace falta sobre claro, el símbolo va dentro del tile o con contorno navy.

## Reglas

- Área de respeto: el alto del tile a cada lado. Nada entra ahí.
- Tamaño mínimo del símbolo: 16 px. Del lockup: 96 px de ancho; por debajo, símbolo solo.
- No deformar, no rotar, no añadir sombras, degradados ni biseles.
- No recolorear fuera de la paleta. La versión monocroma es navy sobre transparente o blanco sobre transparente; nunca gris.
- El símbolo no lleva texto dentro. El wordmark se compone aparte, siempre en Space Grotesk o en un sustituto geométrico de peso y ancho equivalentes.
- La mascota no se recorta a la altura de los ojos ni se usa como icono pequeño.

## Regenerar

Los SVG son la fuente. No hay pipeline: se editan a mano o con el script que los generó, y se vuelven a exportar con `rsvg-convert`. Si se cambia la geometría de la chispa, hay que cambiarla en `symbol.svg`, en `logo.svg` y en la camiseta de `mascot.svg` a la vez, o la identidad se rompe.
