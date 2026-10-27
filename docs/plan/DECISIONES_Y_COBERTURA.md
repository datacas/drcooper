# Decisiones pendientes y trazabilidad

Estado: revisado tras segunda auditoría; R0 autorizado como alcance, sin discovery técnico ejecutado. Este registro desarrolla §20 de especificación v0.3.0 sin convertir sugerencias en decisiones verificadas. No se inicia programación ni prototipos. «Responsable» identifica la issue que resuelve/documenta la decisión; no hay asignaciones personales.

## Registro de decisiones

| ID | Decisión | Responsable | Resolver antes de | Evidencia exigida |
|---|---|---|---|---|
| ADR-01 | Nombre final y disponibilidad | DC-006; cierre de publicación en DC-043 | Publicar paquetes o identidad definitiva | Comprobación de repositorio, registro de paquetes y restricciones de nombre/marca; fecha de consulta |
| ADR-02 | Core compartido, stdio y standalone por cliente/OS | DC-004 | DC-010 | Comparar standalone sin daemon para doctor/plan de reparación/lecturas viables y shared core para índices/sesiones; permisos/locks obligatorios. Matriz servicio/operación/transporte por agente en DC-050/016 |
| ADR-03 | Crates, SDK MCP, SQLite y gramáticas | DC-006 | DC-007 y DC-018 | Compatibilidad, licencias, mantenibilidad, pin de versión y build de prueba |
| ADR-04 | Contrato autorizado de Context7 y fallback oficial | DC-006 | DC-024 | API/documentación vigente, condiciones de uso, autenticación, límites y alternativa |
| ADR-05 | Viabilidad y valor de JEV opcional | DC-006 evalúa; DC-052 define comparación; DC-042 decide adopción | Integración opcional | Contrato común reglas/JEV/LLM con abstención, calidad, coste y latencia; no integrar/no configurar es válido |
| ADR-06 | Adaptador LLM opcional y tres cuotas | DC-006; controles DC-034/035 | Cualquier envío externo | Soporte no exige uso real; dinero, CPU/RAM/IO/tiempo y volumen exportable; opt-in por proveedor/proyecto y contabilidad |
| ADR-07 | Hooks, scopes y setup por cliente | DC-004; implementación DC-015 | Promoción R1 | Documentación vigente y prueba de setup/reversión por versión; límites sin hooks |
| ADR-08 | Similitud, conservación semántica y propagación | DC-002/052 fijan evaluación; DC-032/039 implementan | Aplicar selección o inferencias | Corpus con restricciones/excepciones/fechas/decisiones, omisiones y afirmaciones nuevas; fuentes primarias, profundidad máxima y bloqueo de ciclos |
| ADR-09 | Retención y cuotas por clase/proyecto | DC-003/DC-006; implementación DC-009/013/051 | Persistencia productiva R1 | Raw, caches, fuentes, derivados, propuestas y auditoría separados; crecimiento neto/amplificación y recuperación medidos |
| ADR-10 | Formato y automatización de migración | DC-006 delimita; DC-046 concreta | Importación real | Exportación de prueba, preview de mapeos/scope, idempotencia y rollback; consentimiento explícito |
| ADR-11 | Aislamiento real de ejecución por plataforma | DC-003/DC-004; validación DC-012 | Exponer ejecución R1 | Pruebas de escritura/red/procesos y escape por symlinks; límites de sandbox demostrados |
| ADR-12 | CLI, bandeja por agente y TUI | DC-005/DC-006; DC-040/045 amplían | Congelar contratos de interfaz | CLI mínima en R4; TUI en R6; pruebas de ergonomía y mismo modelo de permisos |
| ADR-13 | Etapas persistentes y linaje del mantenimiento | DC-005/DC-052; DC-051 inicia, DC-031/037 amplían | Mantenimiento R2 y KEE R4 | Discover/Verify/Commit-Propose independientes en SQLite; fingerprints, leases, reintentos, idempotencia y no verificación circular |
| ADR-14 | Recuperación básica y contrato de instalación | DC-004/DC-006; DC-049/050 implementan | Puerta R1 | Artefacto local verificado, binario/DB compatibles, Zero-Maintenance Installation por agente; DC-044 amplía canales en R6 |
| ADR-15 | Contrato Bench, calidad y promoción por release | DC-002/DC-005; entrega DC-010/013/016 | Puerta R1 y cada release | Run/compare/report, oráculos, hashes, baseline portable, comparabilidad y umbrales previos; regresión de calidad bloquea promoción |
| ADR-16 | Madurez de compatibilidad por proveedor | DC-005; DC-033/038/042/047 validan | Anunciar soporte productivo | contract_tested, integration_verified, production_ready; disponibilidad separada, versiones/evidencias y revalidación; JEV R4 simulado no implica API integrada |

Cada ADR final debe incluir contexto, opciones, decisión, evidencia/versiones, consecuencias y condición de revisión. El usuario decide alcance, presupuesto y preferencias de producto; la implementación no debe inventar esas aprobaciones.

## Decisiones operativas previas al arranque

- **Gestión de issues:** preparación local solicitada por el usuario; no se crea un repositorio remoto ni se publican tickets.
- **Conjunto canónico:** DC-DOCSET-0.3.0 con inventario/versiones/hashes en DOCUMENTOS_CANONICOS.json. Las copias adjuntas con sufijos o nombres anteriores no son referencias normativas de este paquete; validación en CI futura dentro de DC-007.
- **Bench:** capacidad nativa incorporada a DC-002/005/010/013/016 y validaciones por módulo, conservando 52 issues y 69 incrementos. DC-049 conserva actualización básica; no se reutiliza su ID para Bench.
- **Opcionalidad IA:** decisión obligatoria del usuario ya incorporada; LLM y JEV independientes, desactivados por defecto. Ausencia válida, funciones exclusivas no disponibles, fallos aislados. No se reabre esta decisión como requisito de contratar proveedor.
- **Implementación:** aún no iniciada. Este trabajo entrega planificación; las issues describen verificaciones futuras, no pruebas ejecutadas del producto.
- **Identidad en agentmemory:** falta slug canónico declarado. Antes de guardar aprendizaje de este proyecto, pedir el valor, declararlo y verificar que coincide con `session/start`; guardar por REST con scope y no por `memory_save` MCP.
- **Calendario y responsables:** no definidos. Tras R0, estimar con capacidad real y dividir las issues L; no deducir fechas a partir de los tamaños orientativos.
- **División del trabajo:** 52 padres; los 23 de tamaño L ya tienen 69 subtareas en INCREMENTOS.md. Asignar incrementos, no contenedores completos; mantener aceptación de integración del padre.
- **Plataformas:** WSL2 Ubuntu inicial; Linux nativo en distribución; Windows nativo/macOS sujetos a evaluación y aceptación propia.

## Cobertura por sección de especificación

| Sección | Resultado que debe quedar cubierto | Issues |
|---|---|---|
| §1 Resumen | Nueve capacidades, IA opcional, utilidad y coste operativo medidos | DC-001, DC-004, DC-005, DC-048; desarrollo R1–R6 |
| §2 Contexto/objetivos | Tres agentes, lenguajes objetivo, WSL2 y baseline | DC-001, DC-002, DC-015, DC-019–021, DC-047 |
| §3 Alcance/exclusiones | Núcleo propio sin orquestador ni cloud obligatorios | DC-001, DC-006, DC-030 |
| §4 Principios | Procedencia, local-first, determinismo y control explícito | DC-003, DC-005, DC-014, DC-036, DC-037 |
| §5 Arquitectura | Rust, transportes, proveedores externos gestionados | DC-004, DC-006–010, DC-017–018 |
| §6.1 Política semántica | Semántica primero, referencias antes de editar | DC-022, DC-023, DC-025 |
| §6.2 Documentación | Versión instalada, local/Context7/oficial, caché | DC-006, DC-024 |
| §6.3 Memoria por tarea | Recall acotado, guardado selectivo, exclusiones y prioridad del usuario | DC-014, DC-015, DC-028, DC-034 |
| §6.4 Ejecución/contexto | Captura íntegra, filtrado, lotes y aislamiento honesto | DC-003, DC-012, DC-013 |
| §7 Contratos | Capacidades dinámicas, CLI Bench y madurez separada de disponibilidad | DC-002, DC-005, DC-007, DC-010, DC-033, DC-038, DC-042 |
| §8 Código/grafo | LSP/AST, índices, evidencia, rutas e impacto | DC-017–023, DC-026–027 |
| §9 Memoria | Capas, scopes, revisiones, cuotas y mantenimiento temprano sin grafo | DC-008, DC-014, DC-028–029, DC-032, DC-046, DC-051 |
| §10 KEE | Tres etapas persistentes, reglas, IA opcional y linaje | DC-031–035, DC-037–039, DC-042, DC-051–052 |
| §11 Gobernanza | Autonomía, propuestas, feedback y transiciones | DC-036–037, DC-040–041 |
| §12 Almacenamiento | SQLite, migraciones, recovery, export y cuotas | DC-009, DC-013, DC-026, DC-031, DC-037, DC-046 |
| §13 Seguridad | Threat model, permisos, datos, IPC y supply chain | DC-003, DC-008, DC-010, DC-012, DC-023, DC-034, DC-043 |
| §14 Fiabilidad | Recuperación R1, LSP fijado R2 y canales remotos R6 | DC-011, DC-016, DC-017, DC-038, DC-044, DC-047, DC-049–050 |
| §15 Configuración | Validación de opciones; valores de ejemplo no congelados | DC-006, DC-007, DC-031, DC-034–036 |
| §16 Aceptación | Pruebas funcionales y de seguridad por capacidad | Matriz detallada inferior |
| §17 Métricas/Bench | Run/compare/report, calidad previa, regresión por release y horizonte operativo | DC-002/005 diseño, DC-010/013/016 entrega; DC-025/030/038/041 amplían; DC-043/044/047/048 validan; DC-052 corpus |
| §18 Roadmap | R0–R6 y puertas observables | ROADMAP.md y validaciones DC-006/016/025/030/038/041/048 |
| §19 Code Cycle | Integración por interfaces públicas, sin acoplamiento | DC-030 |
| §20 Pendientes | Decisiones con evidencia y dueño por issue | Registro ADR anterior |
| §21 Inspiraciones | Referencias orientan diseño; no dependencias obligatorias | DC-001, DC-006, DC-043 |
| §22 Terminado | Sustitución cotidiana validada sin regresiones críticas | DC-047, DC-048 |

El brief de identidad se considera en DC-001, ADR-01 y DC-045. Los entregables gráficos de marca/mascota no son capacidades funcionales del motor y no se dan por incluidos ni producidos en este backlog técnico; pueden tener una línea de trabajo propia cuando se prioricen.

## Trazabilidad de los criterios de aceptación de §16

| Criterio | Implementación | Verificación de salida |
|---|---|---|
| §16.1 Inspección semántica sin grep redundante | DC-017–022 | DC-025 |
| §16.1 Rename muestra referencias y cobertura | DC-023 | DC-025 |
| §16.1 Sin LSP se declara fallback y límites | DC-018–022 | DC-025 |
| §16.2 Compresión conserva fallos, estado y log | DC-012–013 | DC-016 |
| §16.2 Raw recuperable coincide byte a byte durante retención | DC-013 | DC-016 |
| §16.2 Aislamiento anunciado corresponde a sandbox probado | DC-003, DC-012 | DC-016, DC-047 |
| §16.3 Decisión compartida entre agentes sin duplicado exacto | DC-014–015 | DC-016 |
| §16.3 Worktrees comparten proyecto con sesiones separadas | DC-008, DC-028 | DC-016, DC-030 |
| §16.3 Topic key y revisión preservan evidencia | DC-014, DC-037 | DC-016, DC-038 |
| §16.3 Código cambiado marca memoria para revisión | DC-029 | DC-030 |
| §16.4 Lote idle respeta cuotas y locks | DC-031, DC-035, DC-037 | DC-038 |
| §16.4 Interacción pausa sin corrupción | DC-031, DC-037 | DC-038 |
| §16.4 JSON con evidencia validada | DC-033, DC-036 | DC-038 |
| §16.4 Sin API/red sigue mantenimiento determinístico | DC-032–035 | DC-038 |
| §16.4 Patrones de impacto generan propuestas | DC-036, DC-039 | DC-038, DC-041 |
| §16.4 Cada cambio autónomo se revierte por lote | DC-037 | DC-038 |
| §16.5 Doctor aísla componente roto | DC-011 y registro de checks por módulo | DC-016, DC-038, DC-047 |
| §16.5 Update fallido conserva binario/DB recuperable | DC-009, DC-049; DC-044 amplía | DC-050/016 en R1; DC-047 en distribución |
| §16.5 Suite de fuga no envía secretos | DC-034 | DC-038, DC-047 |
| §16.5 Ambigüedad de cwd no permite escritura cruzada | DC-008, DC-014 | DC-016, DC-047 |
| §16.4 Discover/Verify/Commit-Propose persistentes sin duplicados | DC-051, DC-031, DC-037 | DC-025, DC-038 |
| §16.4 Cuatro configuraciones IA y ausencia válida | DC-005, DC-007, DC-033, DC-042 opcional | DC-038, DC-047; reales vs dobles explícitos |
| §16.4 Conservación semántica y linaje a fuentes primarias | DC-052, DC-032, DC-033, DC-037 | DC-038, DC-041 |
| §16.5 Instalación/recuperación por agente desde R1 | DC-015, DC-049, DC-050 | DC-016 y repetición por entrega; DC-047 |
| §17.1–17.2 Bench nativo y regresiones por candidata | DC-002/005/010/013/016 | DC-016 y validaciones por hito; DC-043/044/047 con hash del candidato |
| §17.3 Horizonte operativo y sustitución por flujo | DC-002 fija protocolo/eventos; DC-048 ejecuta | DC-048: minutos manuales, periodo y ciclos representativos, dictamen Bench por flujo |

## Invariantes que ninguna fase puede aplazar

1. Identidad y scope inequívocos antes de escribir; permisos del cliente no se amplían por fallback.
2. Fuentes originales y revisiones recuperables; no consolidación destructiva de memoria esencial.
3. Toda respuesta declara procedencia, estrategia y límites de cobertura.
4. No se envía contenido al exterior sin consentimiento por proyecto y controles de datos/coste.
5. Inferencias, scores o preferencias aprendidas no autorizan cambios sensibles.
6. Una salida parcial, un proveedor caído o una prueba no ejecutada no se presentan como éxito completo.
7. JEV y LLM no son dependencias necesarias para arrancar, usar o promover el núcleo/KEE determinístico. Funciones exclusivas sin motor se desactivan, sin simulación engañosa.
8. Derivados no verifican otros derivados por sí solos; linaje, límites de profundidad y fuentes primarias impiden amplificar errores.

## Condiciones para empezar

R0 está autorizado por el usuario y sus tareas son trabajo de discovery. DC-001 inicia sin bloqueo; DC-002/003 usan sus escenarios; DC-004/005 fijan arquitectura/contrato; DC-052 fija clasificación/evaluación; DC-006 cierra el hito. Sus criterios figuran en ISSUES.md.

Antes de implementar R1 deben estar resueltos los ADR de runtime/IPC, permisos/aislamiento, identidad, persistencia, recuperación básica y contratos de capacidades; dependencias concretas se revisan por incremento. Un contrato opcional no viable se registra y se desactiva su función, sin bloquear funciones independientes. La resolución documental de auditoría no equivale a prueba técnica ni a aprobación de una decisión aún sin evidencia.

La instrucción actual del usuario es **aún no programar**. Esta revisión resuelve documentación y conserva R0 como siguiente alcance permitido; no ejecuta sus pruebas técnicas, instala herramientas ni inicia desarrollo. La segunda auditoría se traza en [AUDITORIA_SEGUNDA.md](AUDITORIA_SEGUNDA.md).
