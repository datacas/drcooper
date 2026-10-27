# Roadmap de DrCooper

Estado: revisión tras segunda auditoría, basada en especificación maestra v0.3.0. Se mantienen R0–R6, 52 issues y 69 incrementos. Bench y N-01–N-05 se integran en tareas existentes; no se inicia programación ni experimentos en esta entrega.

## Resultados que perseguimos

1. Una instalación y configuración coherente para los tres agentes en WSL2 Ubuntu.
2. Navegación y edición de código con cobertura y procedencia explícitas en PHP legado, TS/JS y Python.
3. Menor carga contextual conservando resultados íntegros y recuperables.
4. Decisiones recuperables entre agentes y sesiones sin mezcla entre proyectos o worktrees.
5. Conocimiento mantenido con evidencias, límites de gasto y reversión; cambios sensibles bajo consentimiento explícito.
6. Menor esfuerzo operativo que la combinación de herramientas actual, demostrado en un piloto.
7. JEV/LLM siempre opcionales, independientes y desactivados por defecto; funciones específicas ausentes no se anuncian disponibles ni generan error global.

## Entregas y puertas de salida

| Hito | Entrega utilizable | Issues | Puerta de salida |
|---|---|---|---|
| R0 — Discovery | Baseline, contrato Bench, clasificación común y decisiones | DC-001–006, DC-052 | Oráculos/umbrales, horizonte y eventos operativos definidos; criterio standalone/shared y compatibilidad por evidencia; ADR bloqueantes explícitos |
| R1 — Núcleo | CLI/MCP, memoria, recuperación y Bench mínimo | DC-007–016, DC-049–050 | Zero-Maintenance Installation, rollback, matriz servicio/operación/transporte; run/compare/report y gate CI de regresión sobre capacidades comprometidas |
| R2 — Inteligencia y memoria básica | LSP/AST gestionados, edición, docs y consolidación local sin grafo | DC-017–025, DC-051 | Semántica contrastada PHP/TS/Python; rollback LSP; mantenimiento local reversible, sin generar paráfrasis IA |
| R3 — Grafo y sesiones | Grafo esencial, impacto y obsolescencia | DC-026–030 | Utilidad medida antes de ampliar relaciones; impacto trazable; memoria obsoleta revisable; integración externa sin acoplamiento |
| R4 — KEE completo | Discover → Verify → Commit/Propose, idle y adaptadores IA opcionales | DC-031–038 | Núcleo completo sin IA; persistencia/reanudación; tres presupuestos, conservación semántica, linaje, gobernanza y rollback; capacidades opcionales correctamente expuestas |
| R5 — Aprendizaje y gobernanza | Revisión completa, preferencias y patrones | DC-039–042 | Feedback no altera permisos; rechazos no reaparecen sin evidencia nueva; propuestas obsoletas se revalidan; JEV permanece opcional y solo se incorpora si mejora métricas |
| R6 — Distribución | Paquetes/canales multiplataforma, TUI y piloto | DC-043–048 | Releases y canales verificables; ciclo de vida ampliado; piloto cumple R0 sin mantenimiento injustificado; migración preserva scope, fuentes y rollback |

R0–R6 expresan orden de madurez, no semanas. Cada hito exige una demostración reproducible y un registro de limitaciones antes de promoverlo.

## Fronteras de alcance

### R1: primer producto ejecutable

Incluye ejecución autorizada, salida íntegra, FTS, memoria con scope, sesiones y doctor. Añade actualización desde artefacto local verificado y recuperación de binario/DB compatibles. Seguridad, snapshots, observabilidad y separación de proyectos empiezan aquí.

Zero-Maintenance Installation es una prueba contractual desde R1: instalar, conectar los tres agentes, desinstalar preservando datos/configuración ajena, reinstalar, actualizar, fallar y recuperar. No permite editar manualmente configuraciones fuera de pasos declarados; registra consentimientos e intervenciones y se amplía en cada entrega. No promete ausencia literal de mantenimiento.

La matriz obligatoria por agente separa reinicios de core, puente y cliente. Servicio recuperado, operación resuelta y transporte MCP recuperado tienen comprobaciones distintas; una respuesta perdida no autoriza repetir una escritura a ciegas.

ADR-02 debe evaluar standalone para doctor, plan de reparación básica y lecturas autocontenidas cuando sea viable, frente a shared core para índices/sesiones/mantenimiento. Es un criterio pendiente de prueba, no obligación de levantar daemon para toda operación. La seguridad de locks/escrituras sigue siendo obligatoria en ambos modos.

No se anuncia reemplazo de Serena ni del conjunto completo de herramientas en esta entrega. Solo se anuncian capacidades efectivamente disponibles mediante negociación del contrato MCP.

### R2–R3: uso cotidiano sobre código

R2 añade proveedores por lenguaje con versiones fijadas, integridad y rollback, referencias y edición segura. DC-051 puede comenzar al estabilizar R1, sin esperar LSP/grafo: dedupe exacto, comprobación de fuentes y consolidación estructural que conserva literalmente decisiones y restricciones con reversión. No ejecuta inferencia externa.

R3 empieza con relaciones esenciales entre ficheros, símbolos y memoria. Más tipos solo se añaden con utilidad demostrada; incorpora impacto, recuperación y obsolescencia. Mantenimiento y memoria siguen siendo útiles sin grafo.

### R4: motor de evolución completo, con proveedores opcionales

Discover, Verify y Commit/Propose tienen estados/colas persistentes independientes en SQLite, no servicios separados. Fallo externo conserva candidatos y resultado de cada etapa; Commit revalida base y evita replay de cambios.

JEV y LLM son opcionales y se habilitan independientemente. R4 soporta adaptadores externos desde la primera versión funcional del KEE completo, pero pasa su puerta sin credenciales mediante base determinística y pruebas de contrato/dobles. Integraciones reales solo con proveedor disponible y autorizado; se informa cuáles no se probaron y no se anuncian como validadas.

Madurez explícita: `contract_tested`, `integration_verified` y `production_ready`. R4 puede acreditar solo contrato simulado de JEV; adoptar/verificar su API real sigue en DC-042. Solo `production_ready`, con evidencia operativa/seguridad/recuperación, permite anunciar soporte productivo pleno. Disponibilidad actual se registra aparte.

No hay sustituciones engañosas: sin LLM no se ofrece síntesis generativa; sin JEV no se ofrece su clasificación. Funciones multimotor solo usan motores autorizados y evaluados como equivalentes para esa operación. Ausencia/desactivación es válida; caída temporal degrada solo dependientes y requiere actualizar capacidades de forma compatible con cada cliente.

Cada proveedor externo respeta tres presupuestos: dinero, CPU/RAM/IO/tiempo local y volumen de conocimiento exportable. Datos, opt-in, preview y límites se verifican antes de enviar. Linaje a fuentes primarias evita verificar inferencias mediante inferencias solas.

R2 permite solo mantenimiento mecánico L0 auditado y reversible; interpretaciones quedan pendientes. R4 completa L0 automático, L1 solo como `derived` reversible con fuentes, L2 propuesta y L3 consentimiento explícito. Bandeja CLI mínima, agrupación/cuotas/caducidad y rollback llegan con esa autonomía; R5 mejora experiencia y preferencias.

### R6: producto capaz de sustituir el conjunto actual

Se contrasta el producto completo con el baseline sobre trabajo real. La retirada de herramientas anteriores es gradual por flujo validado. Una TUI, mascota o empaquetado adicional no compensan fallos en integridad, aislamiento o recuperación.

Windows/WSL2 Ubuntu es la plataforma inicial. Linux nativo se valida para distribución; Windows nativo y macOS se investigan y publican solo al superar su propia matriz. No se anuncia compatibilidad por el mero hecho de compilar.

## Orden de ejecución propuesto

1. **Primera tanda: DC-001, DC-002, DC-003.** Fijar escenarios, baseline, amenazas y objetivos comprobables; incluir ciclo de actualización y conservación semántica.
2. **Segunda tanda: DC-004, DC-005, DC-052 y DC-006.** Resolver runtime, capacidades opcionales, clasificación comparable y riesgos antes de adaptadores concretos.
3. **Tercera tanda: DC-007, DC-008, DC-009.** Crear base del producto, identidad/ownership y almacenamiento recuperable.
4. **Primer flujo vertical:** tras DC-010, ejecutar/artefactos y memoria avanzan según sus dependencias hasta DC-015. DC-011, DC-049 y DC-050 completan diagnóstico, recuperación y ciclo de vida antes de validar DC-016.
5. **Adelanto de memoria:** DC-051 tras R1, sin esperar R3. DC-031 puede ampliar esa base sin completar grafo; las capacidades de cada hito solo se anuncian tras su puerta. R5 y R6 consolidan experiencia y distribución.

Las dependencias completas viven en el backlog; los contenedores L se ejecutan mediante INCREMENTOS.md. Dependencias de entrega de adaptadores no obligan a configurar proveedores. Ninguna aceleración permite saltar permisos, opt-in, cuotas o reversión.

## Evaluación y promoción

DC-002 define baseline, corpus/oráculos y contrato [DrCooper Bench](BENCHMARKS.md); DC-005 formaliza CLI, DC-010/013 aportan interfaces/almacén y DC-016 implementa runner mínimo run/compare/report y gate CI. DC-025/030/038/041 amplían las suites con cada módulo; DC-043/044/047 exigen evidencia ligada al artefacto antes de promover releases.

Antes de retirar una herramienta se conserva baseline portable con versiones, condiciones y fuentes. Comparadores opcionales o ausentes no bloquean uso local ni cuentan como mejora probada. Gates aplican primero calidad/fidelidad, luego rendimiento; regresiones sobre límite o evidencia obligatoria insuficiente bloquean promoción.

El protocolo alterna orden, repite pares en copias limpias, separa caché fría/caliente y controla agente/modelo/carga. Historial incluye hashes, fallos y variabilidad; oráculos independientes evitan tratar salida de un competidor como verdad automática.

| Dimensión | Medida | Condición para promover |
|---|---|---|
| Configuración y mantenimiento | Pasos manuales, tiempo de setup/recuperación, fallos de inicio por cliente | Mejora frente al baseline según umbral acordado en R0 |
| Contexto | Bytes/tokens entregados y recuperación de evidencias omitidas | Ahorro frente al mismo escenario sin perder fallos o evidencia requerida |
| Código y grafo | Precisión/cobertura por lenguaje; p50/p95; incrementalidad | Superar umbrales de corpus y marcar cobertura incompleta |
| Memoria | Relevancia top-k, duplicados, revisiones y stale rate | Recuperar decisiones correctas; cero cruces no autorizados en pruebas de aislamiento |
| Conservación semántica | Pérdida de restricciones/excepciones/fechas/decisiones, afirmaciones sin evidencia y contradicciones nuevas | Superar umbrales del corpus DC-052 y reconstruir fuentes; no verificar derivados solo mediante otros derivados |
| Clasificación | Reglas/JEV/LLM sobre clases comunes; abstención, calidad, coste y latencia | Comparar motores disponibles; no exigir proveedores opcionales ni confundir dobles con integración real |
| Crecimiento y revisión | Bytes netos por clase/proyecto, amplificación, backlog y tiempo de revisión | Cuotas y archivado sin pérdida esencial; coste de revisión compatible con ganancia de utilidad |
| Fiabilidad | Arranque, reconexión, fallos inyectados y restauración | Componentes sanos operativos; ninguna pérdida irrecuperable en escenarios de fallo |
| KEE | Coste por lote/propuesta útil, falsos positivos, pausa y rollback | Cuotas respetadas; cero cambios L2/L3 autoaplicados sin autorización |
| Privacidad | Pruebas con secretos sintéticos, deny paths e inyección | Ningún dato prohibido sale en la suite; permisos nunca elevados por inferencia |

R0 fija objetivos cuantitativos y horizonte operativo más número mínimo de ciclos/eventos: instalar/actualizar, cambios de agente/LSP, reinicios WSL y recuperación provocada, junto a uso diario. Bench técnico inmediato y evaluación operativa se reportan por separado. Minutos manuales/mes requieren observación suficiente o extrapolación etiquetada; falta de fallos naturales en periodo corto no demuestra mejora sostenida. Integridad/autorización no dependen de una mejora estadística.

## Definición común de terminado de una issue

- Criterios de aceptación ejecutados con evidencia y versiones del entorno.
- Contrato CLI/MCP y documentación actualizados si cambian capacidades públicas.
- Casos de fallo relevantes, permisos, scope y concurrencia comprobados cuando el cambio los afecta.
- Sin introducir dependencia obligatoria de una herramienta que se pretende reemplazar.
- Migraciones y mutaciones con idempotencia y recuperación demostrables cuando corresponda.
- Limitaciones y elementos aún experimentales expuestos al consumidor.

## Riesgos que cambian el plan

Si el runtime compartido no es viable en un cliente, aplicar el modo autorizado en ADR con identidad y almacenamiento seguros. Context7 no viable conserva docs local/oficial. JEV o LLM no disponibles conservan funciones independientes; las exclusivas se desactivan, no se simulan. Aislamiento no viable restringe capacidad y publicidad; no se presenta un subprocess como sandbox.

Las ediciones semánticas dependen de cobertura real del proveedor. En PHP legado, validar sintaxis y runtime objetivo por separado de la versión del LSP. Los cambios amplios sin cobertura suficiente requieren una decisión explícita del usuario, no una promesa de seguridad basada solo en AST.
