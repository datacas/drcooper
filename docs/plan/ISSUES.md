# Backlog de implementación

52 issues padre propuestas. Se conservan DC-001–048 y se añaden DC-049–052 tras la auditoría. Referencias a la [especificación maestra](../../drcooper_ESPECIFICACION_MAESTRA.md). Prioridades, tamaños y reglas de cierre en [README](README.md). Ninguna está publicada. R0 está autorizado como alcance; aún no hay implementación o discovery ejecutado.

Cada bloque puede copiarse como una issue padre. El hito sirve como milestone y área/prioridad como etiquetas. Las dependencias son IDs locales estables. Las 23 issues L se descomponen en [69 incrementos revisables](INCREMENTOS.md); son contenedores de aceptación y no se asignan como un único cambio. El orden numérico no determina hito: DC-052 es R0, DC-049/050 son R1 y DC-051 es R2.

Dependencia de implementación no equivale a dependencia operativa: entregar un adaptador opcional o su prueba de contrato nunca obliga al usuario a configurar el proveedor. Sin JEV ni LLM el producto y el KEE determinístico siguen siendo válidos.

## R0 — Discovery

### DC-001 — Definir flujos reales, límites del producto y corpus inicial

**Área:** producto · **Prioridad:** P0 · **Tamaño:** M · **Depende de:** ninguna · **Fuente:** §§1–4, 18, 22.

**Trabajo:** inventariar herramientas actuales y escenarios diarios por agente; seleccionar repositorios o muestras congeladas PHP legado, TS/JS y Python sin datos sensibles. Separar capacidades imprescindibles, experimentos y exclusiones.

**Aceptación:**
- Cada flujo incluye entrada, resultado esperado, herramienta actual, agente y fallo que se busca evitar.
- El corpus cubre worktrees, monorepo, referencias entre archivos y al menos un fallo de proveedor por lenguaje.
- Objetivo, entregas R1/R4/R6 y lista de exclusiones quedan revisados; identidad visual no bloquea el núcleo.

### DC-002 — Crear baseline y protocolo de evaluación reproducible

**Área:** evaluación · **Prioridad:** P0 · **Tamaño:** M · **Depende de:** DC-001 · **Fuente:** §§2.3, 17, 18, 22.

**Trabajo:** medir el conjunto actual y definir objetivos de contexto, precisión, latencia, recursos, fiabilidad y mantenimiento. Acordar duración y criterios del piloto.

**Contrato Bench:** definir `bench run/compare/report`, manifiestos versionados, oráculos y adaptadores de comparación conforme a [BENCHMARKS.md](BENCHMARKS.md). DC-005 formaliza interfaces; DC-010/013 aportan CLI e historial; DC-016 implementa el primer runner y gate CI. Ampliaciones en las validaciones existentes, sin nueva issue padre.

**Aceptación:**
- Protocolo versionado identifica corpus, hardware/WSL, versiones, repeticiones y método de contabilización de tokens/bytes.
- Existe una ejecución baseline con resultados recuperables; los umbrales de promoción están escritos antes de evaluar DrCooper.
- Incluye relevancia de memoria, cobertura semántica, falsos positivos KEE y coste por propuesta útil; distingue métricas aún no medibles de resultados cero.
- Incluye conservación de restricciones/excepciones/fechas/decisiones, afirmaciones sin evidencia, contradicciones introducidas, reconstrucción de fuentes y límite de propagación de inferencias.
- Baseline de instalación/actualización/recuperación, crecimiento neto por clase y esfuerzo de revisar propuestas; ninguna capacidad se promueve si aumenta mantenimiento sin ganancia medible.
- Baseline actual de RTK, Serena/LSP, Context Mode, AgentMemory, Graphify y Context7, según disponibilidad, se conserva con versiones, corpus, evidencias y exportación antes de retirar cada herramienta. Celda ausente se declara no evaluada, nunca victoria.
- Bench separa calidad/fidelidad y rendimiento; protocolo fija oráculos, no inferioridad, repeticiones, orden alternado/aleatorio, caché y variabilidad por agente/modelo. Incluye LSP directo con igual proveedor para no atribuir su semántica al motor.
- Fijar horizonte operativo y mínimo de ciclos/eventos (instalar/actualizar, reinicio WSL, cambios de agente/LSP y fallos provocados) antes del piloto. Minutos manuales/mes distinguen periodo observado de extrapolación y se separan de espera automatizada.

### DC-003 — Modelar amenazas y definir fronteras de autorización y datos

**Área:** seguridad · **Prioridad:** P0 · **Tamaño:** M · **Depende de:** DC-001 · **Fuente:** §§4, 6.4, 11, 13.

**Trabajo:** definir ownership, permisos de comandos/IPC, límites de workspace, aislamiento real, contenido no confiable y política de datos locales/externos.

**Aceptación:**
- Matriz amenaza → control → prueba cubre symlinks, paths externos, ejecución, contaminación de scope, inyección, agentes concurrentes y exfiltración.
- Se separan salida íntegra local, contenido indexable y datos exportables; se especifican exclusiones clínicas, secretos, cuotas y retención.
- Lectura degradada y escritura sensible tienen políticas explícitas; no existe fallback que eluda controles obligatorios.
- Se definen tres presupuestos independientes (dinero, recursos locales y volumen exportable), linaje a fuentes primarias y cuota/retención de memorias, derivados y propuestas.

### DC-004 — Validar runtime compartido, puentes stdio y modo standalone

**Área:** arquitectura · **Prioridad:** P0 · **Tamaño:** M · **Depende de:** DC-001, DC-003 · **Fuente:** §§5, 14, 20.

**Trabajo:** realizar una prueba técnica desechable de procesos, transporte y concurrencia en WSL2 y los tres clientes; registrar ADR con alternativa y límites.

**Aceptación:**
- Dos clientes concurrentes mantienen proyectos/worktrees distintos sin mezclar cwd o sesión.
- El ADR documenta startup, cierre, locks, IPC protegido, pérdida del core y capacidades seguras standalone.
- Las capacidades de hooks y transports se contrastan con documentación vigente y una prueba real por cliente; se registran versiones y pendientes.
- Matriz por agente separa caída/reinicio de core, puente y cliente, resolución de operaciones en curso y recuperación del transporte; define cuándo reconectar y cómo resolver resultados ambiguos sin repetir escrituras.
- Comparar modos standalone/shared core: doctor, plan de reparación básica y lecturas viables sin daemon; mutaciones conservan permisos, locks y seguridad. Documentar qué operaciones realmente precisan core, sin declararlo obligatorio para todo ni dar el diseño por probado.

### DC-005 — Definir contratos CLI/MCP, capacidades y errores

**Área:** contratos · **Prioridad:** P0 · **Tamaño:** M · **Depende de:** DC-003, DC-004 · **Fuente:** §§6, 7, 11, 14.

**Trabajo:** diseñar esquemas versionados de las diez tools propuestas y suboperaciones de docs, grafo, contexto, sesión y gobernanza; decidir exposición incremental por hito.

**Aceptación:**
- Ejemplos válidos y negativos cubren `status`, estrategia, ubicaciones, cobertura, expansión, warnings, correlation ID y tiempos.
- CLI y MCP usan el mismo modelo de operación y permisos; se especifican cancelación, límites, errores y negociación de capacidades.
- Lo no implementado no se anuncia como disponible; los cambios incompatibles tienen política de versión explícita.
- Contrato de capacidades contempla sin IA, solo LLM, solo JEV y ambos; ausencia/desactivación no es error. Una caída temporal afecta solo funciones dependientes y se revalida disponibilidad al invocar.
- Define etapas persistentes Discover → Verify → Commit/Propose con estados/reintentos independientes y clasificación común de DC-052; no obliga a tres servicios.
- Formalizar CLI Bench run/compare/report y veredictos `pass/regression/inconclusive/incomparable`, códigos CI y esquema de runs/evidencias. Versión ambigua exige run IDs y no compara corpus/entornos incompatibles como equivalentes.
- Disponibilidad actual y madurez de soporte son campos distintos: `contract_tested`, `integration_verified`, `production_ready`, con evidencias y versiones; solo el último permite anunciar soporte productivo pleno.

### DC-006 — Resolver proveedores, dependencias y decisiones de discovery

**Área:** arquitectura · **Prioridad:** P0 · **Tamaño:** M · **Depende de:** DC-002, DC-003, DC-004, DC-005, DC-052 · **Fuente:** §§5.2, 10.6–10.7, 20.

**Trabajo:** evaluar SDK MCP Rust, SQLite, gramáticas, LSP por lenguaje, Context7, proveedores LLM y viabilidad de JEV. Registrar decisiones de aislamiento, retención, naming, plataformas y UI.

**Aceptación:**
- Matriz documenta versión evaluada, licencia, coste/restricción, compatibilidad y alternativa; las APIs se verifican con documentación actual antes de concretar integración.
- Adaptador LLM inicialmente soportado y contratos JEV/Context7 se evalúan sin exigir configurar proveedor real; ambos proveedores IA están desactivados por defecto y son independientes. JEV no viable se documenta sin bloquear el producto.
- Registro de decisiones de este plan actualizado: cada pendiente tiene dueño por issue y fecha/hito de resolución; R0 deja revisados baseline, contratos y amenazas.

### DC-052 — Definir clasificación comparable y corpus de conservación semántica

**Área:** evaluación · **Prioridad:** P0 · **Tamaño:** M · **Depende de:** DC-002, DC-003, DC-005 · **Fuente:** §§7.4, 10.5–10.7, 17; H-05–H-07.

**Trabajo:** contrato común para reglas, JEV y LLM con opciones cerradas, abstención, evidencias, versión, latencia y coste; corpus etiquetado de clasificación y consolidación. Forma parte de R0, aunque su ID sea posterior.

**Aceptación:**
- Mismas entradas/clases para motores comparables; evidencia desconocida y salida fuera de esquema se rechazan; indisponible no se puntúa como predicción incorrecta.
- Casos incluyen excepciones, fechas, restricciones y decisiones; se fijan umbrales de pérdida semántica, afirmaciones nuevas y reconstrucción, no solo reducción de tokens.
- Reglas tienen baseline; proveedores opcionales se prueban con dobles o, si están autorizados, llamadas reales identificadas. Un derivado sin fuente primaria no puede certificar otro derivado.

## R1 — Núcleo

### DC-007 — Crear base Rust, configuración validada y observabilidad

**Área:** runtime · **Prioridad:** P0 · **Tamaño:** M · **Depende de:** DC-006 · **Fuente:** §§5, 7.2, 13, 15, 17.

**Trabajo:** crear proyecto, estructura modular, CI inicial, configuración y logs estructurados. El TOML orientativo no se publica como contrato sin validación.

**Aceptación:**
- Binario arranca con configuración mínima; claves desconocidas o inválidas producen diagnóstico accionable.
- Precedencia global/proyecto/sesión y restricciones de seguridad están documentadas y comprobadas; configuración del repo no eleva permisos.
- `[ai.llm]` y `[ai.jev]` están desactivados por defecto; activación, consentimiento y disponibilidad son independientes; mantenimiento determinístico no requiere claves.
- Logs incluyen correlación y tiempos sin credenciales; CI compila y ejecuta las comprobaciones acordadas en R0.
- CI documental valida inventario canónico, hashes, enlaces y ausencia de referencias a copias exportadas ambiguas según DOCUMENTOS_CANONICOS.json. Revisión intencional de docs exige actualizar versión/hashes; un enlace existente a otra revisión no se acepta como correcto solo por existir.

### DC-008 — Implementar identidad canónica, scopes, worktrees y sesiones concurrentes

**Área:** identidad · **Prioridad:** P0 · **Tamaño:** L · **Depende de:** DC-003, DC-007 · **Fuente:** §§5.1, 9.2, 13, 16.3, 16.5.

**Trabajo:** resolver identidad persistida, remotos y alias; manejar monorepos, proyectos sin remoto y contexto de cliente. Usar IDs estables, nunca el cwd como única autorización.

**Aceptación:**
- Worktrees comparten identidad de proyecto y conservan sesiones distintas; mover el checkout no crea otra identidad por accidente.
- Ante identidad ambigua no se escribe hasta resolver propietario; lecturas cruzadas requieren scope intencional.
- Pruebas concurrentes impiden escritura en otro proyecto por cambio de cwd, alias conflictivo, symlink o contexto de cliente mal resuelto.

### DC-009 — Implementar SQLite, migraciones, snapshots y recuperación

**Área:** almacenamiento · **Prioridad:** P0 · **Tamaño:** L · **Depende de:** DC-007, DC-008 · **Fuente:** §§9, 12, 14.

**Trabajo:** esquema inicial de proyectos/sesiones/memoria/artefactos/auditoría y migraciones extensibles; WAL cuando proceda, busy timeout, IDs estables y cuotas.

**Aceptación:**
- Escrituras concurrentes son idempotentes; contención produce reintento acotado sin pérdida ni cambio de scope.
- Snapshot se verifica antes de migrar; versión incompatible se rechaza; interrupción simulada permite recuperar el estado compatible anterior.
- Corrupción simulada produce plan de reparación y restauración verificable; no hay reparación destructiva silenciosa. Exportación conserva IDs y procedencia.
- Cuotas por clase/proyecto incluyen fuentes, derivados, propuestas y auditoría; se mide crecimiento neto. Cuota llena frena derivaciones o archiva conforme a política sin borrar memoria esencial silenciosamente.

### DC-010 — Implementar adaptadores CLI/MCP y ciclo de vida del runtime

**Área:** integración · **Prioridad:** P0 · **Tamaño:** L · **Depende de:** DC-005, DC-007, DC-008, DC-009 · **Fuente:** §§5.1, 7, 14.2.

**Trabajo:** implementar transporte y core según ADR, negociación, cancelación y operaciones disponibles de R1 con inicialización automática por sesión.

**Aceptación:**
- CLI y MCP completan el mismo caso sobre un proyecto y devuelven el contrato común con correlación.
- Reconexión no duplica sesiones o procesos; stdout de stdio no contiene logs ajenos al protocolo.
- Pérdida del core devuelve estado claro y habilita solo las operaciones standalone autorizadas; no se promete continuidad de un transporte roto.
- Pruebas separan servicio recuperado, operación resuelta y transporte MCP recuperado; token de operación/consulta de estado evita repetir a ciegas una escritura tras respuesta perdida. Cliente incompatible con actualización de capacidades recibe instrucción de reconectar.
- Reservar comandos Bench según DC-005 sin anunciar ejecución hasta DC-016; disponibilidad del runner no depende de IA o comparadores instalados. Estado de madurez impide anunciar soporte productivo por pasar solo dobles.

### DC-011 — Entregar doctor y status con diagnóstico parcial

**Área:** fiabilidad · **Prioridad:** P1 · **Tamaño:** M · **Depende de:** DC-010 · **Fuente:** §§14.1–14.2, 17.

**Trabajo:** diagnóstico humano/JSON y registro ampliable de checks de protocolo, path, cliente, IPC, DB, scope y componentes.

**Aceptación:**
- Fallos inyectados de permisos IPC, DB bloqueada y cliente incompatible identifican componente y solución sin declarar caído todo el producto.
- Componentes de hitos posteriores aparecen como no implementados o no configurados; su ausencia opcional no bloquea operaciones sanas.
- JEV/LLM desactivados o sin configurar son estados válidos; configurado pero caído degrada solo capacidades dependientes y permite desactivarlo independientemente.
- Reparaciones potencialmente destructivas se presentan como plan separado de su aplicación autorizada.
- Core que no arranca permite doctor/plan de reparación y lecturas standalone que el ADR haya validado; si se escribe, se comprueban locks/permisos sin eludirlos por indisponibilidad del daemon.

### DC-012 — Ejecutar comandos con permisos, captura íntegra y cancelación

**Área:** ejecución · **Prioridad:** P0 · **Tamaño:** L · **Depende de:** DC-003, DC-010 · **Fuente:** §§6.4, 13, 16.2.

**Trabajo:** implementar `dev_execute`: cwd fijado, autorización del cliente, controles de red/disco, timeout y limpieza del árbol de procesos. Separar proceso ordinario, procesamiento de solo lectura y sandbox real.

**Aceptación:**
- Se conservan comando, cwd, stdout/stderr, exit code, duración y estado de captura; un límite nunca se oculta como salida completa.
- Cancelación/timeout terminan descendientes según la política probada; comandos y escapes por symlink fuera de permisos se rechazan.
- Una prueba de escritura/red acredita cada nivel anunciado de aislamiento; plataformas sin soporte restringen capacidad y explican límites.

### DC-013 — Crear artefactos recuperables, filtros y búsqueda FTS de contexto

**Área:** contexto · **Prioridad:** P0 · **Tamaño:** L · **Depende de:** DC-009, DC-012 · **Fuente:** §§6.4, 7, 12, 16.2.

**Trabajo:** conservar salidas y chunks, filtrar Git/tests/builds/diagnósticos/logs, buscar por scope y entregar resultados progresivos. Implementar consulta por ID y modalidad raw/proxy conforme al contrato.

**Aceptación:**
- Fixtures demuestran que compresión conserva fallos y estado; recuperación íntegra coincide byte a byte durante retención autorizada.
- Búsqueda devuelve IDs y fragmentos expandibles sin recapturar salida; lotes conservan resultado individual y dependencias de ejecución.
- Artefactos locales sensibles tienen acceso y retención explícitos; indexación excluye datos prohibidos sin confundir redacción con bytes originales.
- El mismo almacén conserva manifiestos/runs e historial Bench con IDs/hashes, evidencias y retención explícita; export/import valida esquema e integridad, nunca ejecuta instrucciones del informe ni requiere comparadores residentes.

### DC-014 — Implementar memoria tipada, scoped y con revisiones

**Área:** memoria · **Prioridad:** P0 · **Tamaño:** L · **Depende de:** DC-008, DC-009, DC-010 · **Fuente:** §§6.3, 9, 16.3.

**Trabajo:** save/search por scope, `topic_key`, fingerprints, estados, fuentes y revisiones; selección de conocimiento no deducible del repo y exclusión automática de datos sensibles/clínicos.

**Aceptación:**
- Misma decisión guardada por dos agentes en el mismo proyecto no crea duplicado exacto; decisiones de proyectos distintos permanecen separadas.
- Nueva revisión conserva fuente e historial; búsqueda compacta permite expandir evidencia y recuperar archivados autorizados.
- Memorias sin propietario o con contenido prohibido no se guardan; contenido recordado no adquiere prioridad sobre instrucciones actuales.

### DC-015 — Configurar Codex, Claude Code y OpenCode de forma reversible

**Área:** clientes · **Prioridad:** P0 · **Tamaño:** L · **Depende de:** DC-010, DC-011, DC-013, DC-014 · **Fuente:** §§2.2, 5.1, 6.3, 7.3, 14.

**Trabajo:** setup por cliente, backups de configuración, detección de versiones y adaptadores/hooks disponibles. Documentar acceso manual cuando no exista hook compatible.

**Aceptación:**
- Instalación, segunda ejecución y reversión preservan configuración ajena; no elevan permisos globales.
- En cada cliente se demuestra ejecutar → expandir artefacto → buscar contexto → guardar/recuperar memoria.
- Hooks de inicio/fin permiten recall acotado y guardado selectivo; fallo del core no bloquea trabajo nativo salvo controles obligatorios.
- Setup se integra con Zero-Maintenance Installation; detecta instalación previa y conserva copia verificable para recuperación por cada agente.

### DC-049 — Actualizar y recuperar binario/DB de forma segura desde R1

**Área:** fiabilidad · **Prioridad:** P0 · **Tamaño:** M · **Depende de:** DC-006, DC-009, DC-010 · **Fuente:** §§14.3, 16.5; H-01.

**Trabajo:** actualización básica desde artefacto local verificado, staging, prueba de arranque/handshake, sustitución atómica y vuelta a binario/DB compatibles. Canales remotos y multiplataforma se amplían en DC-044.

**Aceptación:**
- Firma/checksum y origen de confianza se verifican; artefacto inválido no reemplaza binario. `check` y `apply` son operaciones separadas y no forzosas.
- Fallos inyectados antes/después de migrar o sustituir recuperan combinación compatible de binario y snapshot; se verifica contenido persistido.
- Sesiones/locks activos tienen política explícita; rollback de binario no abre DB incompatible ni pisa escrituras nuevas sin plan de recuperación.

### DC-050 — Contratar Zero-Maintenance Installation como prueba transversal

**Área:** instalación · **Prioridad:** P0 · **Tamaño:** M · **Depende de:** DC-002, DC-015, DC-049 · **Fuente:** §§2.3, 14.3, 16.5; H-03–H-04.

**Trabajo:** escenario versionado instalar → conectar tres agentes → desinstalar preservando datos → reinstalar → actualizar → fallar → recuperar. Primera ejecución en R1; se repite con capacidades nuevas por entrega.

**Aceptación:**
- En entorno limpio, los tres agentes completan el flujo sin editar configuraciones manualmente fuera de pasos declarados y consentimientos iniciales; configuración ajena y datos sobreviven.
- Matriz por agente cubre reinicio de core/puente/cliente, conexiones abiertas, operaciones concurrentes y resultado de escritura ambiguo; distingue servicio, operación y transporte.
- Se contabilizan intervenciones y tiempo frente al baseline; actualización fallida recupera versión funcional y setup previo. El nombre de la prueba no implica garantía de mantenimiento literalmente cero.

### DC-016 — Entregar Bench mínimo y validar salida de R1

**Área:** evaluación · **Prioridad:** P0 · **Tamaño:** M · **Depende de:** DC-002, DC-011, DC-012, DC-013, DC-014, DC-015, DC-049, DC-050 · **Fuente:** §§14, 16.2–16.3, 16.5, 18.

**Trabajo:** implementar runner nativo mínimo `bench run/compare/report` sobre CLI y artefactos existentes, con suites sintéticas de ejecución/contexto/memoria/ciclo de vida. Usarlo para validar R1 en WSL2/tres agentes y añadir gate CI; adaptar comparadores disponibles sin volverlos dependencias del producto. Las suites posteriores se incorporan en DC-025/030/038/041/047/048.

**Aceptación:**
- Dos agentes y dos worktrees trabajan simultáneamente sin mezclar resultados, memoria o locks.
- Arranque, caída del core, contención SQLite, timeout y recuperación de snapshot están probados con evidencia.
- Informe compara con baseline, declara limitaciones y decide si la puerta R1 está superada; no declara funciones semánticas aún ausentes.
- Zero-Maintenance Installation y matriz de reinicio/reconexión pasan en los tres clientes; ningún estado ambiguo provoca replay automático de escrituras.
- `run` produce ID/manifiesto/evidencias, `compare` aplica primero calidad y luego rendimiento, `report` recupera historial y estado de sustitución por flujo. Regresión sintética conocida se detecta y bloquea el gate; muestra insuficiente o comparador ausente no se presenta como aprobación.
- Cada candidata R1 ejecuta suites pertinentes en CI, con hash del binario/corpus y baseline aprobado; baseline previo a primera release es explícito. Gates no exigen red, JEV ni LLM; pruebas reales y dobles quedan diferenciados.

## R2 — Inteligencia

### DC-017 — Gestionar servidores LSP por proyecto y lenguaje

**Área:** código · **Prioridad:** P0 · **Tamaño:** L · **Depende de:** DC-006, DC-016 · **Fuente:** §§5.2, 8.1, 14.

**Trabajo:** cliente JSON-RPC stdio, ciclo de vida, sincronización de documentos, capacidades, cancelación y proveedores configurables; instalación gestionada solo bajo política definida.

**Aceptación:**
- Timeouts, crash y reinicio del servidor no dejan diagnósticos obsoletos presentados como actuales ni bloquean memoria/ejecución.
- Versiones, configuración y capacidades del proveedor aparecen en doctor y evidencias.
- Dos worktrees con configuración distinta no comparten estado LSP incorrectamente; descargas verifican integridad y licencia.
- Instalador gestionado fija versión, verifica artefacto, usa staging y conserva proveedor anterior para rollback. Actualización fallida se revierte sin cambiar configuración del usuario ni bloquear el núcleo.

### DC-018 — Indexar AST y símbolos de forma incremental

**Área:** índice · **Prioridad:** P0 · **Tamaño:** L · **Depende de:** DC-006, DC-008, DC-009, DC-016 · **Fuente:** §§5.2, 8.2, 12.

**Trabajo:** gramáticas de los lenguajes objetivo, identidades/rangos/hash de contenido y reindexación; distinguir sintaxis de semántica.

**Aceptación:**
- Modificar, borrar o mover un archivo actualiza símbolos afectados sin reutilizar rangos de otra revisión/worktree.
- Cambio de configuración/dependencias invalida conservadoramente; cambios ordinarios no fuerzan escaneo completo sin necesidad.
- Sintaxis no soportada devuelve cobertura parcial y fallback, nunca relaciones semánticas inventadas; consumo se mide con el corpus.

### DC-019 — Validar proveedor TypeScript/JavaScript

**Área:** código · **Prioridad:** P1 · **Tamaño:** M · **Depende de:** DC-017, DC-018 · **Fuente:** §§8.1, 16.1.

**Trabajo:** adaptar definiciones, implementaciones, referencias y diagnósticos al proyecto TS/JS real y su configuración.

**Aceptación:**
- Fixtures incluyen exports, referencias entre módulos, aliases y monorepo con `tsconfig`/`jsconfig`.
- Ubicaciones y cobertura contrastan con golden fixtures; diagnósticos conservan severidad, rango, proveedor y versión.
- Sin servidor, AST/texto responde con limitaciones y no etiqueta búsqueda literal como referencia semántica.

### DC-020 — Validar proveedor PHP incluido legado 7.x

**Área:** código · **Prioridad:** P1 · **Tamaño:** M · **Depende de:** DC-017, DC-018 · **Fuente:** §§2.2, 8.1, 16.1.

**Trabajo:** integrar proveedor configurable y validar sintaxis legacy, autoload y referencias según configuración real.

**Aceptación:**
- Corpus incluye clases, herencia, namespaces/autoload y limitaciones dinámicas explícitas.
- Runtime PHP objetivo y versión/capacidades del analizador se registran por separado; no se exige modernizar el proyecto para analizarlo.
- Definiciones/referencias/diagnósticos cumplen umbrales acordados; cobertura dinámica insuficiente se comunica antes de editar.

### DC-021 — Validar proveedor Python con BasedPyright o compatible

**Área:** código · **Prioridad:** P1 · **Tamaño:** M · **Depende de:** DC-017, DC-018 · **Fuente:** §§2.2, 8.1, 16.1.

**Trabajo:** integrar análisis respetando entorno e importación del proyecto, configuración Pyright y proveedores alternativos.

**Aceptación:**
- Imports, clases, referencias y diagnósticos se verifican en fixtures con entorno y configuración propios.
- Se diferencia análisis LSP de ejecución CLI del type checker y no se atribuyen operaciones no ejecutadas.
- Falta de entorno o proveedor devuelve límites accionables y fallback; no modifica configuración para esconder errores.

### DC-022 — Enrutar búsqueda, inspección, referencias y diagnósticos

**Área:** políticas · **Prioridad:** P0 · **Tamaño:** M · **Depende de:** DC-005, DC-019, DC-020, DC-021 · **Fuente:** §§6.1, 7, 16.1.

**Trabajo:** implementar tools de código con semántica primero, expansión progresiva e inicialización automática.

**Aceptación:**
- Para símbolo resoluble se usa LSP/AST y no se repite búsqueda textual si ya hay respuesta suficiente.
- Logs, SQL sin soporte, configuración y consultas literales usan búsqueda textual apropiada.
- Cada respuesta identifica estrategia, versión del índice, fuentes y cobertura; IDs de expansión reutilizan el trabajo válido.

### DC-023 — Editar símbolos con preview, referencias y verificación de base

**Área:** edición · **Prioridad:** P0 · **Tamaño:** L · **Depende de:** DC-003, DC-022 · **Fuente:** §§6.1, 7, 13, 16.1.

**Trabajo:** `dev_code_edit` para rename e inserción/sustitución simbólica con plan, permisos y recuperación ante aplicación parcial.

**Aceptación:**
- Preview muestra archivos, diff, referencias y cobertura antes de una mutación compartida.
- Cambio de hash/base tras preview invalida el plan; ningún archivo fuera del workspace autorizado se modifica por path o symlink.
- Fallo a mitad de edición permite recuperar el estado anterior; checks aplicables al lenguaje verifican el resultado y exponen errores preexistentes por separado.

### DC-024 — Resolver documentación por versión con caché y procedencia

**Área:** documentación · **Prioridad:** P1 · **Tamaño:** L · **Depende de:** DC-006, DC-013, DC-022 · **Fuente:** §§6.2, 7, 20.

**Trabajo:** detectar versiones instaladas/lockfiles, documentación local fiable, adaptador Context7 si es viable y fallback oficial; caché indexada.

**Aceptación:**
- Resultado indica versión detectada, fuente, fecha/caché y cualquier discrepancia; versión ambigua pide resolver o marca incertidumbre.
- Caída o falta de autorización Context7 activa la alternativa documentada; modo offline devuelve solo fuentes disponibles con límites.
- Código propio no dispara consultas externas; una discrepancia reproducible con docs se registra sin inventar opciones de API.

### DC-025 — Validar salida de R2 en PHP, TS/JS y Python

**Área:** evaluación · **Prioridad:** P0 · **Tamaño:** M · **Depende de:** DC-002, DC-023, DC-024, DC-051 · **Fuente:** §§16.1, 17, 18.

**Trabajo:** ejecutar corpus y escenarios reales de navegación, edición, documentación y degradación; comparar con baseline.

**Aceptación:**
- Informe publica precisión/cobertura, p50/p95, RSS, CPU e indexación incremental por lenguaje con versiones y artefactos.
- Fallo LSP → AST → texto está probado y marcado; edición con base obsoleta no se aplica.
- Los tres agentes consumen el contrato sin perder procedencia; regresiones críticas bloquean promoción R2.
- Se repite Zero-Maintenance Installation con instalación/rollback LSP y mantenimiento básico; informe distingue consolidación estructural local de síntesis semántica no disponible sin LLM.
- Ampliar Bench con suites semántica/docs y comparadores Serena/LSP directo/Context7 disponibles; oráculos independientes, misma versión LSP/configuración y desglose por lenguaje/agente. Gate release cubre las nuevas capacidades comprometidas.

### DC-051 — Mantener y consolidar memoria local sin depender del grafo

**Área:** memoria · **Prioridad:** P0 · **Tamaño:** M · **Depende de:** DC-014, DC-016, DC-052 · **Fuente:** §§9.4, 10.3, 16.3–16.4; H-02, H-05, H-07.

**Trabajo:** incremento temprano R2 tras estabilizar memoria R1: dedupe exacto, verificación básica de existencia/hash, agrupación por topic y consolidación estructural reversible. Cola lógica persistente Discover → Verify → Commit/Propose; ejecución explícita y acotada, sin scheduler idle ni proveedor externo.

**Aceptación:**
- Funciona sin índice semántico, grafo, JEV o LLM; conservación literal de excepciones, fechas y restricciones con fuentes reconstruibles. No ofrece paráfrasis generativa.
- Discover no modifica canónico; Verify registra evidencias y candidatos pendientes; Commit revalida base y solo realiza mantenimiento L0 auditado. Cambios interpretativos se dejan como candidatos sin aplicar.
- Reintento/reinicio no duplica cambios; dry-run, cuota por clase y rollback de lote están probados. Fallo de fuente queda pendiente/rechazado con motivo, nunca verificado por mera repetición.

## R3 — Grafo y sesiones

### DC-026 — Persistir grafo incremental con evidencia por relación

**Área:** grafo · **Prioridad:** P0 · **Tamaño:** L · **Depende de:** DC-009, DC-025 · **Fuente:** §§8.2–8.3, 12.

**Trabajo:** empezar con fichero/símbolo/memoria y `contains`, `imports`, `references`, `relates_to_memory`; `calls` solo con cobertura comprobada. Esquema extensible para más tipos tras demostrar utilidad, sin exigir poblar todo el modelo de la especificación.

**Aceptación:**
- Cada arista conserva proveedor, evidencia, versión de índice y fiabilidad cualitativa; inferencias se distinguen de relaciones observadas.
- Cambio/borrado de archivo actualiza relaciones sin mezclar revisiones o worktrees; reindexar dos veces no duplica aristas.
- Un fallo del grafo deja operativas memoria, ejecución y navegación que no lo necesita.
- Informe de utilidad del grafo esencial precede a añadir nodos/aristas; relaciones no soportadas se declaran no disponibles en consultas.

### DC-027 — Consultar callers, rutas, impacto y hotspots

**Área:** grafo · **Prioridad:** P1 · **Tamaño:** M · **Depende de:** DC-022, DC-026 · **Fuente:** §§7, 8.3, 17.

**Trabajo:** dependencia inversa, callers/callees, rutas entre símbolos, impacto y puntos de acoplamiento con expansión acotada.

**Aceptación:**
- Fixtures con ciclos y dependencias entre módulos devuelven rutas justificadas y resultados finitos.
- Impacto separa lo observado de lo inferido y explica límites de cobertura; hotspots no afirman causalidad por frecuencia.
- CLI/MCP respetan presupuesto de resultado y devuelven IDs para expandir sin repetir el recorrido válido.

### DC-028 — Recuperar sesiones, timeline y contexto de tarea progresivo

**Área:** sesiones · **Prioridad:** P1 · **Tamaño:** M · **Depende de:** DC-014, DC-015, DC-026 · **Fuente:** §§6.3, 7, 9, 16.3.

**Trabajo:** enlazar tareas, operaciones, artefactos y decisiones; recuperar contexto pertinente al inicio y cerrar sesiones con selección de aprendizaje.

**Aceptación:**
- Otra sesión/agente recupera una decisión con fuente y timeline sin cargar toda la conversación.
- Recall respeta límites y scope; indisponibilidad de memoria no bloquea la tarea; guardar al cierre es selectivo y no duplica código/ADR versionado.
- Worktrees comparten conocimiento canónico sin compartir tareas activas; orden actual del usuario prevalece sobre memoria anterior.

### DC-029 — Marcar conocimiento obsoleto por cambios de código y fuentes

**Área:** memoria · **Prioridad:** P0 · **Tamaño:** M · **Depende de:** DC-014, DC-026 · **Fuente:** §§9.3–9.4, 10.3–10.4, 16.3.

**Trabajo:** enlazar recuerdos a símbolos/commits/docs y encolar revisión incremental tras cambios relevantes.

**Aceptación:**
- Cambiar o borrar una fuente puede marcar memoria `pending_review` manteniendo versión y evidencia originales.
- Recuerdos no afectados no se revalidan sin motivo; cambios de rama/configuración invalidan con criterio conservador documentado.
- Conflictos muestran ambas fuentes y condiciones; lo más reciente no se convierte automáticamente en verdad.

### DC-030 — Integrar Code Cycle por contratos y validar salida de R3

**Área:** integración · **Prioridad:** P0 · **Tamaño:** M · **Depende de:** DC-002, DC-027, DC-028, DC-029 · **Fuente:** §§17–19.

**Trabajo:** ejemplo de consumo MCP/CLI para inspección/impacto y recuperación de una tarea; medir grafo y sesiones contra objetivos R0.

**Aceptación:**
- Flujo externo puede citar correlation IDs, evidencias y contexto sin importar módulos internos de Orca/Toolkit.
- Issue/PR son enlaces de procedencia; el núcleo no adquiere responsabilidad de orquestación.
- Informe R3 valida impacto, incrementalidad, recuperación y degradación con corpus y umbrales; documentación explica el modo independiente.
- Zero-Maintenance Installation se repite con migraciones del grafo; ampliar esquema exige ganancia medida y no bloquea mantenimiento básico de memoria.
- Ampliar Bench con grafo/impacto y comparador Graphify cuando disponible; informes de sustitución no extrapolan relaciones no cubiertas. Gate release compara también sesiones/continuidad comprometidas.

## R4 — Knowledge Evolution Engine completo con IA opcional

### DC-031 — Planificar mantenimiento en inactividad con pausa cooperativa

**Área:** KEE · **Prioridad:** P0 · **Tamaño:** L · **Depende de:** DC-016, DC-051 · **Fuente:** §§10.1–10.3, 12, 16.4.

**Trabajo:** ampliar etapas persistentes de DC-051 con scheduler idle, locks, leases, intervalos, límites de CPU/RAM/IO y checkpoints. No requiere completar R3; grafo se usa cuando está disponible.

**Aceptación:**
- El scheduler comprueba trabajo activo y carga, además de ausencia de llamadas MCP; no compite con otro mantenedor por el mismo lote.
- Nueva interacción pausa en checkpoint sin cortar transacción; reinicio recupera trabajo pendiente de forma idempotente.
- Core apagado no se anuncia como mantenimiento activo; `knowledge status` explica pendiente, pausa y consumo.
- Discover, Verify y Commit/Propose conservan estados e intentos independientes; perder proveedor/cuota en Verify mantiene descubrimientos pendientes sin reiniciar el análisis completo.

### DC-032 — Mantener conocimiento con reglas determinísticas locales

**Área:** KEE · **Prioridad:** P1 · **Tamaño:** M · **Depende de:** DC-031, DC-051, DC-052 · **Fuente:** §§9.4, 10.3–10.4, 16.4.

**Trabajo:** ampliar mantenimiento básico con FTS/topics y señales opcionales de símbolos/grafo, comprobación de fuentes y propuestas de archivado. La aplicación avanzada pasa por gobernanza y lote reversible.

**Aceptación:**
- Sin red/clave se seleccionan candidatos, deduplican exactamente y revisan fuentes con evidencia; similitud no se trata como identidad.
- Segunda ejecución no repite cambios ya aplicados; memoria esencial conserva originales recuperables.
- Dry-run lista cambios propuestos sin aplicarlos; reglas no producen síntesis atribuida a un LLM que no se ha ejecutado.
- Derivados mantienen linaje a fuentes primarias; ciclos o profundidad excedida detienen derivación. Un derivado solo no verifica otro; cuotas limitan crecimiento neto por clase.

### DC-033 — Integrar inferencia remota con salida estructurada y evidencia

**Área:** LLM opcional · **Prioridad:** P1 · **Tamaño:** L · **Depende de:** DC-006, DC-031, DC-052 · **Fuente:** §§7.4, 10.3, 10.5–10.6.

**Trabajo:** soporte opcional de adaptador inicial evaluado en R0 y contratos para OpenAI, Anthropic y endpoint compatible; síntesis, contradicciones y clasificación cerrada. Desactivado por defecto; todo envío real queda bloqueado hasta DC-034/DC-035. No se exige configurar/contratar proveedor para usar KEE.

**Aceptación:**
- Respuesta JSON referencia IDs de evidencia suministrados, incertidumbres y cambios propuestos; IDs inventados/esquema inválido se rechazan.
- Timeout, rate limit y errores de proveedor tienen reintentos acotados; no generan lote duplicado ni se presentan como éxito.
- Hay pruebas de contrato por adaptador comprometido; se expone cuáles están disponibles, sin asumir equivalencia de APIs. Síntesis queda `derived`, no hecho verificado.
- Sin proveedor no se anuncian funciones generativas disponibles ni se marca error global; caída temporal degrada solo esas funciones. Activación LLM es independiente de JEV; no se sustituye silenciosamente por heurística.
- Publicar evidencia de madurez por proveedor/versión/operación: dobles acreditan `contract_tested`, API real `integration_verified`; operación/seguridad/recuperación comprobadas permiten `production_ready`. Solo esta última acredita soporte productivo pleno.
- Corpus DC-052 mide pérdida de restricciones/excepciones/fechas/decisiones, novedades sin evidencia y reconstrucción; linaje prohíbe verificar una inferencia solo con otra.

### DC-034 — Aplicar opt-in por proyecto, redacción y controles de salida

**Área:** privacidad · **Prioridad:** P0 · **Tamaño:** L · **Depende de:** DC-003, DC-008, DC-033 · **Fuente:** §§6.3, 10.6, 13, 16.5.

**Trabajo:** egress gate para cualquier proveedor externo LLM/JEV, deny paths, clasificación, preview del payload y claves vía entorno/gestor seguro. No enviar repositorios completos; opt-in y revocación independientes por proveedor/proyecto.

**Aceptación:**
- Sin consentimiento explícito vigente del proyecto no se hace ninguna llamada externa; cambiar scope no reutiliza consentimiento ajeno.
- Secretos sintéticos, contenido clínico y rutas prohibidas quedan fuera del payload y logs; si no puede garantizarse redacción se omite llamada.
- Inyección en memoria/docs/logs no altera políticas ni extrae credenciales; claves no aparecen en SQLite, TOML versionado, MCP ni informes.
- Límite persistente de volumen exportable por lote/periodo (bytes/tokens, memorias y fuentes) se reserva antes del envío y no se elude fraccionando llamadas o cambiando proveedor.

### DC-035 — Controlar dinero, recursos locales y volumen de salida

**Área:** costes · **Prioridad:** P0 · **Tamaño:** M · **Depende de:** DC-009, DC-033 · **Fuente:** §§10.6, 15, 17.

**Trabajo:** tres presupuestos independientes: dinero diario/mensual; CPU/RAM/IO/tiempo local; volumen de conocimiento enviado. Contabilidad por lote, proveedor y proyecto; distinguir estimación de uso real. Comparte gate de datos con DC-034.

**Aceptación:**
- Concurrencia reserva presupuesto antes del envío; reiniciar no reinicia el consumo; agotamiento bloquea nuevas llamadas y conserva mantenimiento local.
- Reintentos y respuestas con uso desconocido tienen tratamiento conservador documentado, sin asumir coste cero.
- Stats muestra periodo, modelo/proveedor, estimación, uso real disponible y discrepancias; precios/versiones usados son trazables.
- Pruebas agotan cada presupuesto por separado y con concurrencia/reinicio; cambiar motor no elude límites agregados. Sin proveedores no hay reservas/costes externos ficticios.

### DC-036 — Aplicar matriz L0–L3 y bandeja CLI mínima

**Área:** gobernanza · **Prioridad:** P0 · **Tamaño:** L · **Depende de:** DC-005, DC-032, DC-033 · **Fuente:** §§11, 16.4.

**Trabajo:** política central de aplicación, propuestas con fingerprint, evidencias, diff, estado y consentimiento. CLI mínima para listar, inspeccionar, aprobar/rechazar y consultar historial.

**Aceptación:**
- L0 se audita; L1 solo se aplica como derivado reversible con fuentes; L2 permanece propuesta; L3 requiere consentimiento explícito verificable.
- Score o texto de un proveedor no amplían permisos; propuesta global requiere confirmación adicional y no hereda una aprobación solo de proyecto.
- Estado base cambiado invalida aprobación antigua; decisiones y transiciones son idempotentes y auditadas; no hay aplicación productiva antes de DC-037.
- Bandeja mínima agrupa, prioriza y limita propuestas, con caducidad y digest opcional; cuota llena no produce interrupciones ilimitadas ni aplicación automática.

### DC-037 — Aplicar lotes atómicos con auditoría, history y rollback

**Área:** integridad · **Prioridad:** P0 · **Tamaño:** L · **Depende de:** DC-009, DC-034, DC-035, DC-036 · **Fuente:** §§10.3, 11.3, 12, 16.4.

**Trabajo:** unir selección, inferencia, controles y aplicación en lotes versionados con diffs, fuentes, costes, dry-run e inversión segura.

**Aceptación:**
- Cada cambio tiene lote, versión del modelo/reglas, evidencias y estado anterior; ningún original se destruye por consolidar.
- Fallo o cancelación en cada checkpoint no deja cambios parciales invisibles; repetir el lote no duplica efectos.
- Rollback restaura relaciones/revisiones/estados previstos; si hay cambios posteriores conflictivos no los pisa, presenta conflicto y ruta de recuperación.
- Etapas persistentes reanudan desde su último estado válido; resultado externo incierto conserva intento/coste sin prometer exactamente una llamada, y Commit nunca duplica cambios por replay.

### DC-038 — Validar KEE completo sin IA y con proveedores opcionales

**Área:** evaluación · **Prioridad:** P0 · **Tamaño:** M · **Depende de:** DC-002, DC-031, DC-032, DC-033, DC-034, DC-035, DC-036, DC-037 · **Fuente:** §§16.4–16.5, 17–18.

**Trabajo:** validar base determinística y matriz sin IA/solo LLM/solo JEV/ambos mediante contratos y dobles controlados; integración real únicamente con proveedor disponible y autorizado. Extender doctor y repetir Zero-Maintenance Installation.

**Aceptación:**
- Base sin JEV/LLM completa Discover → Verify → Commit/Propose, revisión local y rollback sin error de configuración. Funciones exclusivas ausentes no se anuncian disponibles.
- Cuando hay proveedor autorizado, evidencia distingue llamada real de doble, coste, salida con fuentes y permisos. Integración real no ejecutada queda explícita y no impide promover el núcleo sin IA; capacidad real no verificada no se anuncia validada.
- Sin API key/red, con respuesta malformada, presupuesto agotado o nueva interacción, se mantiene coherencia y utilidad local.
- Suite de fuga/inyección, concurrencia y permisos pasa; informe mide falsas propuestas y coste útil y decide promoción R4.
- Pruebas de pérdida semántica, linaje y tres presupuestos cumplen umbrales. Pausa/reinicio/fallo en cada etapa conserva candidatos y evita duplicar commits; grafo ausente no impide mantenimiento local.
- Matriz simulada R4 acredita contrato, no JEV real: adopción sigue en DC-042. Resultados Bench y publicidad distinguen `contract_tested`, `integration_verified` y `production_ready`; sin evidencia no hay nivel asignado.
- Ampliar Bench knowledge con conservación semántica, clasificación, linaje y coste; fallos de calidad bloquean gate de release sin exigir activar IA. Celdas generativas no ejecutadas permanecen no evaluadas.

## R5 — Aprendizaje y gobernanza avanzada

### DC-039 — Detectar patrones y contradicciones sin convertir hipótesis en normas

**Área:** aprendizaje · **Prioridad:** P1 · **Tamaño:** M · **Depende de:** DC-038 · **Fuente:** §§10.4–10.5, 11, 17.

**Trabajo:** identificar recurrencia de errores, verificaciones útiles, alternativas rechazadas y condiciones de contradicción.
- Separar patrones contables determinísticos de detección semántica que requiera proveedor: esta última no se ofrece sin motor válido.

**Aceptación:**
- Patrón cita observaciones independientes y condiciones; repetir una misma hipótesis no aumenta artificialmente su verificación.
- Recomendaciones nuevas o de gran impacto crean propuestas, sin modificar código, permisos o reglas por inferencia.
- Fixtures con contradicciones aparentes y reales miden precisión; se conservan incertidumbres y fuentes opuestas.

### DC-040 — Completar bandeja de revisión y ciclo de vida de propuestas

**Área:** gobernanza · **Prioridad:** P1 · **Tamaño:** M · **Depende de:** DC-036, DC-038 · **Fuente:** §§11.2–11.3.

**Trabajo:** agrupación, `snooze`, evidencia, aprobación por proyecto/global, verificación, reversión y expiración; exposición por agente conforme al contrato.

**Aceptación:**
- Todas las transiciones válidas se auditan y las inválidas se rechazan; propuestas obsoletas se revalidan antes de aplicar.
- Rechazo evita repetición del mismo fingerprint; reapertura exige evidencia nueva material visible para el usuario.
- Resúmenes no interrumpen por cada hallazgo; acciones globales conservan confirmación adicional y vista del impacto.

### DC-041 — Aprender preferencias de presentación y validar salida de R5

**Área:** aprendizaje · **Prioridad:** P0 · **Tamaño:** M · **Depende de:** DC-002, DC-039, DC-040 · **Fuente:** §§11.2, 17–18.

**Trabajo:** ajustar ranking y frecuencia según feedback explícito, con posibilidad de revisar/restablecer preferencias; medir calidad y fatiga.

**Aceptación:**
- Aprobaciones/rechazos cambian orden o frecuencia de sugerencias, nunca controles obligatorios, permisos o alcance de consentimiento.
- Preferencias de proyecto no se promueven globalmente por inferencia; usuario puede inspeccionar y revertir ajustes.
- Informe R5 muestra utilidad, falsas propuestas y repetición frente al baseline; pruebas de autonomía demuestran cero escaladas indebidas.
- Tiempo de revisión, cola neta y caducidad se miden; se repite Zero-Maintenance Installation y matriz de capacidades sin obligar a activar IA.
- Bench histórico compara falsas propuestas/carga de revisión y crecimiento por versión; el gate impide compensar peor calidad mediante menos tokens o una media global favorable.

### DC-042 — Evaluar JEV como clasificador opcional

**Área:** experimento · **Prioridad:** P2 · **Tamaño:** M · **Depende de:** DC-006, DC-038 · **Fuente:** §§10.7, 17, 20.

**Trabajo:** verificar API/despliegue reales y comparar clasificación cerrada con reglas y LLM sobre el corpus. No bloquea la salida R5.
- Implementar el contrato común DC-052 solo si la API resulta viable; JEV se activa independientemente del LLM y aplica controles externos si necesita red.

**Aceptación:**
- Informe compara precisión, calibración, latencia y coste; si no hay mejora o API viable, decisión documentada de no integrar.
- Si se incorpora, se puede desactivar/fallar sin bloquear KEE; solo clasifica opciones cerradas y conserva procedencia.
- Ningún score permite aprobar cambios sensibles; límites de privacidad y presupuesto se mantienen.
- Sin JEV no se anuncia su clasificación como disponible ni hay error global. Comparativa incluye abstención y calibración, identifica dobles vs llamadas reales y no exige ambos proveedores para evaluar reglas.
- Adoptar API real solo acredita `integration_verified`; anunciar `production_ready` requiere además operación, seguridad y recuperación contrastadas. Contrato simulado de DC-038 no implica adopción ni soporte real.

## R6 — Distribución y sustitución validada

### DC-043 — Publicar paquetes verificables y matriz de plataformas

**Área:** distribución · **Prioridad:** P0 · **Tamaño:** L · **Depende de:** DC-006, DC-041, DC-049 · **Fuente:** §§2.2, 5.2, 13, 14.3.

**Trabajo:** builds de release, instalación/desinstalación documentadas, checksums/firmas, lockfile, SBOM y auditoría de dependencias/licencias. Documentar evaluación del nombre antes de publicar.

**Aceptación:**
- Instalación limpia en WSL2 Ubuntu y Linux nativo arranca sin servicios de las herramientas sustituidas, salvo proveedores externos documentados.
- Artefacto manipulado falla verificación; gramáticas y componentes distribuidos tienen licencias incluidas.
- Windows nativo/macOS se etiquetan soportados solo con pruebas de su matriz; desinstalar preserva datos salvo borrado explícito.
- Cada release incorpora informe Bench ligado al hash del artefacto, corpus y matriz comprometida; regresión de calidad o evidencia obligatoria insuficiente bloquea promoción/publicación. Sin comparadores externos no se proclama superioridad.

### DC-044 — Ampliar actualización a canales remotos y multiplataforma

**Área:** fiabilidad · **Prioridad:** P0 · **Tamaño:** L · **Depende de:** DC-009, DC-043, DC-049 · **Fuente:** §§12, 14.3, 16.5.

**Trabajo:** ampliar recuperación básica de DC-049 con canales remotos verificados, distribución multiplataforma y compatibilidad entre varias versiones publicadas; conservar separación check/apply, staging y coordinación con sesiones.

**Aceptación:**
- Fallos de descarga, firma, arranque, migración y cambio de binario conservan una combinación binario/DB recuperable comprobada.
- Sesiones y locks activos se gestionan según política explícita; binario viejo no abre un esquema incompatible.
- No hay actualización automática forzosa; usuario puede consultar estado, aplicar conscientemente y volver a versión compatible.
- Comparación Bench baseline/candidate inequívoca antes de promover candidata; evidencia de otro binario no vale. Ensayar versiones antiguas usa copias de datos, sin abrir DB personal con esquema incompatible.

### DC-045 — Entregar TUI de observabilidad y propuestas

**Área:** interfaz · **Prioridad:** P1 · **Tamaño:** L · **Depende de:** DC-011, DC-040, DC-041 · **Fuente:** §§3.1, 11.2, 17–18; brief de identidad.

**Trabajo:** estado por proyecto, actividad, recursos, costes, propuestas, evidencias e historial usando los mismos contratos CLI. Aplicar identidad cuando exista un sistema visual aprobado.

**Aceptación:**
- Usuario distingue disponible, degradado, pendiente y experimental; ve scope y coste antes de aprobar.
- Acciones de TUI conservan exactamente permisos, confirmaciones y auditoría de CLI; no exponen secretos.
- Navegación por teclado, terminal estrecho y ausencia de color están comprobados; CLI sigue ofreciendo las operaciones esenciales.

### DC-046 — Migrar memoria de forma asistida, portable e idempotente

**Área:** migración · **Prioridad:** P0 · **Tamaño:** L · **Depende de:** DC-014, DC-037, DC-041 · **Fuente:** §§3.2, 9.4, 12, 20.

**Trabajo:** import/export portable y adaptador AgentMemory basado en formato verificado; preview, mapeo canónico de proyectos, consentimiento y registro de importación.

**Aceptación:**
- Memorias sin scope no reciben proyecto inferido silenciosamente: se aíslan para resolución explícita; datos sensibles quedan excluidos.
- Reimportar no duplica; IDs de origen, fuentes/revisiones y estado se preservan o su pérdida se declara antes de importar.
- Export/import funciona sin servicio original activo si hay exportación; cancelar o revertir importación no daña conocimiento anterior.

### DC-047 — Completar matriz E2E de clientes, plataformas y recuperación

**Área:** compatibilidad · **Prioridad:** P0 · **Tamaño:** L · **Depende de:** DC-025, DC-030, DC-038, DC-041, DC-043, DC-044, DC-045, DC-046, DC-050 · **Fuente:** §§14, 16–18, 22.

**Trabajo:** congelar versiones candidatas y verificar setup, reconexión, sesiones activas, fallos parciales, límites y restauración en plataformas soportadas.

**Aceptación:**
- Codex/Claude/OpenCode pasan los flujos comprometidos y negociación MCP en WSL2; plataformas adicionales cumplen su matriz publicada.
- Caídas de LSP/grafo/LLM/red y transporte no corrompen memoria ni ocultan pérdida de capacidad; restauración de binario y DB está ejecutada.
- Informe registra resultados, versiones, incompatibilidades y problemas abiertos; ninguna regresión crítica se disfraza de pendiente menor.
- Zero-Maintenance Installation ejecuta ciclo completo por plataforma soportada; matriz de capacidades incluye proveedores ausentes, desactivados y caídos sin errores globales espurios.
- Bench consolida suites por cliente/plataforma y madurez de cada integración; `contract_tested` no se anuncia como soporte productivo. CI sintética y pruebas reales disponibles se registran por separado.

### DC-048 — Ejecutar piloto diario y decidir sustitución de herramientas

**Área:** producto · **Prioridad:** P0 · **Tamaño:** L · **Depende de:** DC-002, DC-047 · **Fuente:** §§2.3, 17–18, 22.

**Trabajo:** usar DrCooper en los proyectos/periodo acordados, comparar resultados con baseline y documentar sustitución por flujo validado.

**Aceptación:**
- Informe demuestra ahorro contextual o esfuerzo operativo según umbrales R0, con calidad, fiabilidad, costes y feedback del usuario.
- Se documenta qué herramientas/flujos ya se sustituyen, cuáles siguen siendo necesarios y cómo volver al entorno previo.
- Solo se declara producto inicial terminado si se cumplen los seis puntos de §22 y no quedan regresiones críticas; de lo contrario se abren tareas correctivas concretas y se mantiene la convivencia necesaria.
- No requiere configurar JEV/LLM; evalúa capacidades activas y marca las no disponibles. La memoria R4 debe demostrar mejor recuperación/conservación de decisiones y menos trabajo repetido, sin aumento de mantenimiento carente de ganancia medible.
- Evaluación operativa cumple horizonte y cobertura de eventos fijados en DC-002: actualizaciones, reinicios WSL, cambios de agente y recuperación provocada, además de uso diario. Tiempo manual activo, espera y extrapolación mensual son métricas separadas; horizonte insuficiente produce conclusión pendiente.
- `bench report` entrega `ready/keep/not_evaluated` por herramienta/flujo/lenguaje/agente con condiciones de vuelta; retirada parcial no espera a sustituir todas las capacidades ni elimina dependencias LSP/API aún usadas.
