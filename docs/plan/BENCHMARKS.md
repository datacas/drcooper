# DrCooper Bench — contrato de evaluación continua

Estado: diseño de capacidad nativa, integrado en las issues existentes; no hay motor implementado ni mediciones de superioridad. Fecha: 2026-10-26. Responsables: DC-002/005 para diseño, DC-010/013/016 para primera entrega y validaciones posteriores en [ISSUES.md](ISSUES.md). No se añaden issues padre ni incrementos.

## Objetivo y alcance

`drcooper bench` debe permitir ejecutar, comparar y consultar evaluaciones históricas en cualquier momento, sin depender del piloto final. Se integra como módulo del mismo producto, con ejecución explícita, almacenamiento local y los controles de autorización, recursos y datos del runtime. No requiere otro daemon, una cuenta externa ni las herramientas competidoras para funcionar.

Hay dos comparaciones distintas: DrCooper contra su propia versión anterior, obligatoria antes de cada release sobre capacidades comprometidas; y DrCooper contra herramientas actuales para decidir sustituciones por flujo. Un benchmark demuestra resultados sobre versiones, corpus y condiciones concretas, nunca superioridad universal.

JEV y LLM siguen siendo opcionales e independientes. El núcleo de Bench y las suites locales funcionan sin ambos. Un proveedor ausente no es fallo del producto; una celda no evaluada no cuenta como victoria, equivalencia ni validación de una integración.

## Modalidades

### Suites reproducibles

Corpus sintético y muestras reales autorizadas, versionados por hash, con entradas, resultados esperados, oracle, recursos y política de repetición. Los resultados esperados se establecen independientemente del candidato; salida de Serena, LSP o cualquier otra herramienta no es por sí sola verdad de referencia.

Cada escenario tiene identificador estable, capacidad, lenguaje/versión, agente si procede, estado inicial, acciones permitidas, aserciones de calidad y condiciones de finalización. Seeds y presupuestos quedan fijados antes de comparar. Separar casos de desarrollo de un conjunto reservado para evitar optimizar únicamente los ejemplos del benchmark.

### Evaluación de uso real

Tareas equivalentes sobre copias limpias de una misma revisión, con configuración de agente/modelo/razonamiento, proveedor, herramientas y límites registrados. Alternar o aleatorizar el orden y repetir pares de tareas; no reutilizar resultados ni memoria de la primera ejecución en la segunda.

No se ejecuta evaluación sobre datos productivos por defecto ni se captura automáticamente contenido privado. Consentimiento por proyecto, redacción y política de retención se aplican también a prompts, traces e informes. El modo real requiere autorización explícita para comandos que escriban o envíen datos y usa workspace/datos de prueba aislados.

En tareas con modelos externos se conserva identificador de modelo y revisión si está disponible, configuración, coste, uso real y variación entre repeticiones. Si el proveedor no permite fijar revisión o seed, se declara esa incertidumbre. No atribuir a las herramientas una mejora que no pueda distinguirse de variación del modelo.

Separar benchmark técnico inmediato de evaluación operativa. DC-002 fija antes del piloto duración, número mínimo de ciclos y cobertura de eventos: instalación, actualización del producto/LSP/agente, reinicio de WSL, reconexión concurrente y recuperación de fallos provocados. Uso diario y fallos inyectados se reportan por separado. Si falta horizonte o eventos representativos, no se certifica mejora mensual de mantenimiento aunque los microbenchmarks pasen.

## Matriz de suites y comparadores

| Suite | Comparadores posibles | Calidad obligatoria | Rendimiento/operación |
|---|---|---|---|
| `execution` | Salida sin filtrar, RTK y DrCooper | Exit status, fallos visibles, fidelidad de stdout/stderr y evidencia raw | Tokens/bytes entregados, latencia, CPU/RSS y errores ocultos |
| `context` | Salida directa, Context Mode y DrCooper | Recuperación íntegra dentro de retención, resultados pertinentes y scopes | Tokens, volumen indexado, latencia y coste de expansión |
| `semantic` | Serena con LSP, LSP directo y DrCooper con proveedor equivalente | Precisión y recall de definiciones/referencias/diagnósticos; edición segura por lenguaje | Latencia p50/p95, indexación fría/incremental, CPU/RSS |
| `memory` | Dataset/oracle común, AgentMemory y DrCooper | Recall@k, precision@k, revisiones, dedupe, aislamiento y continuidad entre agentes | Latencia, crecimiento, recuperación y coste de mantenimiento |
| `graph` | Relaciones etiquetadas, Graphify y DrCooper | Precisión/cobertura de relaciones, rutas y conjunto de impacto | Construcción/incrementalidad, latencia, tamaño y recursos |
| `docs` | Documentación oficial versionada, Context7 y DrCooper | Versión correcta, afirmación respaldada por fuente y abstención si no hay evidencia | Latencia, caché, llamadas y coste externo |
| `knowledge` | Reglas, JEV o LLM disponibles y revisiones previas de DrCooper | Conservación semántica, falsas conclusiones, linaje, vigencia y rollback | Coste por propuesta útil, recursos, volumen exportado y carga de revisión |
| `lifecycle` | Conjunto actual y DrCooper; versiones consecutivas | Instalación, reconexión, aislamiento, recuperación y fidelidad de datos/config | Intervenciones y minutos manuales, fallos de MCP por exposición, tiempo de recuperación |
| `workflow` | Conjunto actual y DrCooper por agente | Tareas completas según oracle, decisiones conservadas, ausencia de fallos críticos | Tiempo total, contexto, recursos agregados, coste y trabajo repetido |

Las métricas se definen por escenario: una salida deliberadamente compacta no necesita coincidir con el texto raw, pero debe conservar hechos requeridos y permitir recuperar el original cuando el contrato lo exija. Un error oculto es un fallo de calidad, no ahorro.

DrCooper utiliza LSP: comparar además con el mismo servidor/versión/configuración directamente permite separar cobertura del proveedor y sobrecoste del motor. Las mejoras del runtime no se presentan como capacidad semántica superior a su proveedor. Ensayos con otro servidor se reportan en otra celda.

## Metodología y metadatos mínimos

Cada run produce un manifiesto versionado e inmutable con `run_id`, versión/esquema de Bench, versión/build/commit del ejecutable, suite/corpus/oracle y hashes, scenario IDs, baseline/candidate, plataformas y parámetros. Una corrección crea nueva revisión, no reescribe resultados históricos.

Registrar también:

- Hardware, límites WSL/contenedor, OS/kernel, carga de fondo, filesystem, versión de Git, runtime y dependencias relevantes.
- Agente/versión/modelo, configuración y permisos; LSP/versión/configuración; comparador/adaptador y capacidades activas, incluido IA ausente o simulada.
- Estado frío/caliente de caché, índice y memoria; orden/seed, repeticiones, warm-up y timeout. Nunca mezclar frío y caliente en un promedio sin desglose.
- Comando/operación/cwd de prueba, timestamps, duración, exit code, estado de captura, correlation IDs y artefactos redactados recuperables bajo su retención autorizada.
- Método de medición de tokens y tokenizer/versión, límites del conteo (entrada/salida/total); bytes aparte. No convertir bytes a tokens con un ratio fijo sin marcar estimación.
- Recursos del árbol completo de procesos atribuible a la tarea: core, puentes, LSP y auxiliares. Distinguir pico/residencia, CPU acumulada y costes compartidos; no comparar core solo contra seis servicios completos.
- Número de repeticiones válidas, intentos fallidos, timeouts y variabilidad. Fallos y outliers no se eliminan por favorecer al candidato; exclusiones justificadas y visibles.

Definir denominadores: éxito sobre tareas intentadas; fallos MCP por sesiones/operaciones y horas observadas; recall@k sobre evidencia relevante etiquetada. Métricas sin oráculo o muestra suficiente quedan indeterminadas. Latencia p95 y diferencias de precisión incluyen tamaño muestral e incertidumbre, no solo una cifra redondeada.

**Intervención manual:** registrar minutos activos dedicados a instalación, diagnóstico, reparación, actualización y restauración, separados de espera automatizada y trabajo de desarrollo. Minutos por mes solo se informan con periodo observado o extrapolación explícita, ventana y supuestos. No presentar una prueba corta como observación mensual real.

## Contrato CLI propuesto

Los comandos son diseño, no comandos disponibles actualmente. DC-002/DC-005 fijarán sus esquemas exactos; DC-016 entrega la primera implementación sobre CLI y artefactos existentes.

```bash
drcooper bench run --suite semantic
drcooper bench run --suite memory
drcooper bench run --suite context
drcooper bench run --suite graph
drcooper bench compare --baseline <run-id> --candidate <run-id>
drcooper bench compare --baseline 0.8.0 --candidate 0.9.0
drcooper bench report
```

- `run` ejecuta solo suites seleccionadas y capacidades implementadas; anuncia plan, dependencias, coste y permisos antes de operaciones sensibles. Devuelve run ID y resultados estructurados, con originales recuperables.
- `compare` no instala herramientas ni ejecuta código automáticamente: compara runs compatibles ya registrados. Una versión es alias válido solo si resuelve inequívocamente a runs con corpus/entorno/configuración compatibles; si hay ambigüedad exige IDs.
- `report` consulta historial local, diferencias, regresiones y preparación para sustituir herramientas. Exportación JSON y Markdown en archivos; TUI posterior puede consumir el mismo contrato.
- Comparación sin argumentos solo se permite si baseline/candidate están seleccionados explícita e inequívocamente; nunca escoger el par que produzca mejor resultado.
- Estados por caso: `passed`, `failed`, `skipped`, `unavailable` o `invalid`. Estados del veredicto comparativo: `pass`, `regression`, `inconclusive` o `incomparable` con motivos y evidencias. No ejecutar un escenario no lo convierte en aprobado.
- `compare` y modo CI distinguen por código de salida veredicto aprobado, regresión, insuficiencia/incompatibilidad y error de ejecución; valores exactos se congelan en DC-002/DC-005.

## Calidad antes que rendimiento

1. Validar comparabilidad: mismo escenario/oracle, corpus, configuración relevante, capacidades y política de caché. Incompatibilidad crea informe `incomparable`, no porcentaje de mejora.
2. Aplicar invariantes: cero pérdidas de evidencia exigida, cruces de scope o elevación de permisos, más criterios funcionales definidos. Fallo crítico bloquea promoción aunque mejore rendimiento.
3. Aplicar umbrales de calidad preacordados por capacidad/lenguaje/agente: precisión, cobertura, recall y conservación. Márgenes de no inferioridad, repeticiones y tratamiento de incertidumbre quedan fijados antes del candidato. Muestra insuficiente produce `inconclusive`, nunca equivalencia por defecto.
4. Solo después comparar recursos, tokens, latencia y mantenimiento. Informar todas las métricas y el intercambio entre ellas; no esconder un lenguaje peor detrás de una media global.

El baseline no puede sustituirse después de observar una regresión para borrarla. Cambios de corpus/oracle/umbrales tienen revisión y motivo; si rompen comparabilidad se exige recalcular ambos lados. Una corrección demostrada del oracle conserva evidencia histórica y justificación.

## Regresiones y releases

Desde R1, cada versión candidata debe ejecutar las suites sintéticas/offline pertinentes y comparar contra la última release aceptada sobre capacidades comprometidas. Antes de la primera release se usa el baseline de referencia validado en R0 y sus oráculos, declarando que aún no hay versión anterior.

La matriz obligatoria y sus umbrales quedan en un manifiesto de release versionado. CI archiva resultados y hashes del artefacto probado. Una regresión de calidad por encima del límite o falta de evidencia en una celda obligatoria bloquea promoción/publicación; una mejora de velocidad no la compensa. Si no se dispone del comparador externo, su comparación es indeterminada, no una razón para impedir el funcionamiento del producto ni declarar superioridad.

Pruebas reales de clientes, comparadores o proveedores se ejecutan cuando estén disponibles y autorizadas, separadas de simulaciones. Compatibilidad por proveedor/versiones/operación tiene tres niveles: `contract_tested` (dobles), `integration_verified` (API real) y `production_ready` (validación operativa, seguridad y recuperación). Sin evidencia queda sin verificar. Solo `production_ready` permite anunciar soporte productivo pleno; pasar cuatro combinaciones simuladas en R4 no integra JEV real, cuya adopción sigue en DC-042.

No se puede eludir la puerta convirtiendo en opcional una capacidad ya comprometida para esa release. Releases sin IA no necesitan activar JEV/LLM. Cambios de versión/configuración invalidan o exigen revalidar las evidencias afectadas; disponibilidad actual y madurez de compatibilidad son dimensiones distintas.

Antes de distribuir o recomendar una actualización, verificar que el informe corresponde al binario candidato y corpus aprobados. El actualizador sigue siendo explícito y recuperable; un informe Bench no autoriza por sí solo instalar, modificar permisos ni saltar rollback. Ensayos de versiones antiguas usan copias aisladas, nunca abren la DB personal productiva con un esquema incompatible.

## Preparación para sustituir herramientas

Informe por herramienta/capacidad/lenguaje/agente/plataforma con estado `ready`, `keep` o `not_evaluated`. Cada `ready` requiere calidad y fiabilidad aceptadas, evidencia reproducible y ganancia de utilidad/coste operativo conforme al protocolo; no obliga a ganar todas las métricas.

| Herramienta | Condición de sustitución por flujo |
|---|---|
| RTK | Fidelidad de fallos/estado, raw recuperable y ahorro contextual competitivo |
| Serena y LSP actuales | Precisión/cobertura aceptadas por lenguaje, configuración y operación; proveedor necesario permanece gestionado o instalado |
| Context Mode | Contexto reducido con recuperación íntegra y búsqueda pertinente |
| AgentMemory | Recall y revisiones aceptados, aislamiento, continuidad entre agentes y migración recuperable |
| Graphify | Relaciones/impacto precisos y útiles sobre los casos cubiertos |
| Context7 | Consultas fiables por versión/fuente; si DrCooper sigue usando su API, se puede retirar el MCP separado, no eliminar esa dependencia remota |

Una herramienta puede retirarse de TS y conservarse para PHP dinámico. `ready` informa una decisión; no desinstala ni borra configuraciones automáticamente. Registrar límites, rutas de vuelta y revisiones que invalidan el dictamen (cambios de versión, proveedor o escenario).

## Entrega progresiva y simplicidad operativa

| Hito | Compromiso de Bench |
|---|---|
| R0 | DC-002 fija baseline, contrato Bench, corpus/manifiestos/oráculos y matriz de adaptadores; DC-005 formaliza CLI; DC-052 aporta clasificación y conservación semántica |
| R1 | DC-010 expone CLI, DC-013 conserva/indexa runs e historial; DC-016 implementa runner mínimo run/compare/report y gate CI usando suites de ejecución/contexto/memoria/ciclo de vida |
| R2 | DC-025 añade semántica/docs y memoria básica a suites y comparadores implementados, incluidos LSP directos |
| R3 | DC-030 amplía grafo/impacto y continuidad |
| R4–R5 | DC-038/041 añaden KEE, linaje, tres cuotas, clasificación y carga de revisión, con IA opcional |
| R6 | DC-043/044/047 exigen evidencia por release/plataforma; DC-048 consolida piloto operativo con horizonte/eventos y decisión de sustitución |

No es un sistema de competición que mantiene seis servicios residentes. Los adaptadores son opcionales y de ejecución explícita, usan versiones detectadas/fijadas y corpus portable; resultados exportados verificables pueden servir como baseline cuando las herramientas anteriores ya se retiraron. Metadatos ausentes o artefactos expirados reducen verificabilidad y se declaran. Un formato importado debe validar esquema/procedencia/integridad y nunca ejecutar instrucciones del informe.

Bench no se ejecuta continuamente en background ni fuerza uso de red. Cuotas, limpieza, exportación y retención de informes deben evitar que medir el ahorro introduzca más mantenimiento que el que se pretende eliminar.
