# Especificación maestra — Motor unificado de inteligencia para agentes de programación

**Nombre de trabajo:** DrCooper / DevCore (pendiente de selección y verificación de disponibilidad; también se exploraron Orvexis, Nexlith, Coderva y Arkyra).  
**Versión del documento:** 0.3.0 · **Fecha:** 26 de octubre de 2026  
**Estado:** especificación de producto y arquitectura propuesta, no implementación existente.  
**Objetivo:** servir de base para issues, ADR, roadmap, implementación y criterios de aceptación.

> **Principio rector:** una instalación y un único punto de mantenimiento para los agentes; aprovechar únicamente las capacidades útiles de RTK, Serena, Context Mode, AgentMemory, Graphify, Context7 y enfoques de memoria como Engram, **sin exigir instalar ni ejecutar esos productos**. Se permite integrar librerías de código y servidores LSP estándar; «un solo binario» describe el producto principal, no garantiza la inexistencia de procesos externos para lenguajes o servicios remotos.

## 1. Resumen ejecutivo

Se desarrollará una herramienta local-first, agnóstica de agente, distribuida preferentemente como **un ejecutable Rust**, con interfaces CLI y MCP (y API local interna si está justificada). Será utilizable desde **Codex, Claude Code y OpenCode**, mediante un núcleo de inteligencia compartido y adaptadores ligeros por cliente. Agrupará:

1. **Code Intelligence:** símbolos, definiciones, implementaciones, referencias, diagnósticos y ediciones semánticas mediante AST/Tree-sitter y LSP.
2. **Smart Execution:** ejecución de comandos segura, captura íntegra, filtrado estructurado, compresión contextual y acceso recuperable a resultados originales (inspiración RTK).
3. **Context Engine:** procesamiento fuera de la ventana de contexto, indexación de salidas, búsqueda, sesiones y entrega progresiva (inspiración Context Mode).
4. **Persistent Memory:** conocimiento por proyecto/sesión/usuario, recuperación selectiva, deduplicación, decisiones y procedencia (inspiración AgentMemory y Engram).
5. **Code Graph:** dependencias, callers/callees, rutas, impacto y puntos de acoplamiento (inspiración Graphify).
6. **Documentation Engine:** fuentes locales, versiones instaladas, Context7 por API externa cuando sea viable, documentación oficial como alternativa.
7. **Knowledge Evolution Engine:** mantenimiento autónomo determinístico en inactividad, con validación, deduplicación y archivado reversible. Soportará **LLM y JEV opcionales e independientes**; solo se ofrecen síntesis generativa, clasificación externa u otras funciones dependientes cuando el proveedor correspondiente esté habilitado y operativo. No se exige clave ni proveedor externo para utilizar el motor.
8. **Learning Governance:** política por niveles de autonomía, propuestas al usuario, aprobaciones, rechazos, trazabilidad y aprendizaje de preferencias sin modificar las reglas críticas silenciosamente.
9. **Reliability Runtime:** diagnóstico, compatibilidad de clientes, aislamiento de fallos, migraciones, actualizaciones atómicas y rollback.

La herramienta debe proporcionar **menos configuración y menos fallos operativos** que el conjunto actual de MCP y CLI independientes; esta promesa debe validarse mediante benchmarks reproducibles y pilotos en proyectos reales.

**DrCooper Bench** será una capacidad nativa CLI para ejecutar suites, comparar versiones/herramientas y consultar resultados históricos. Calidad y fidelidad preceden a rendimiento; cada release requiere evidencia de regresión sobre sus capacidades comprometidas. El contrato se desarrolla en §17 y en [BENCHMARKS.md](docs/plan/BENCHMARKS.md).

## 2. Contexto y problema

### 2.1 Dolor actual

- Instalaciones y actualizaciones independientes de 5–6 herramientas y servidores MCP.
- Roturas de arranque por cambios de versiones, PATH, runtimes, protocolos o configuración.
- Trabajo duplicado: varios índices, memorias, buscadores y políticas parcialmente solapadas.
- Consumo adicional de RAM/CPU en WSL2 y fatiga de mantenimiento.
- Necesidad de recordar manualmente prioridades entre herramientas y de repetir políticas por cliente.

### 2.2 Entorno objetivo inicial

- Windows 11 + WSL2 Ubuntu; compatibilidad futura Linux nativo, Windows nativo y macOS.
- Agentes: Codex, Claude Code y OpenCode; otros MCP compatibles después.
- Lenguajes: PHP (incluidos proyectos legacy), TypeScript/JavaScript y Python.
- Servidores LSP instalados o gestionables: PHP LSP, TypeScript Language Server y BasedPyright; alternativas configurables.
- Git, monorepos y worktrees, IDE y Docker como parte del entorno de desarrollo.
- Convivencia opcional con Code Cycle Toolkit: orquestación externa, sin acoplamiento duro.

### 2.3 Objetivos medibles

- Un solo producto instalable y configurable globalmente; comando `doctor` útil sin necesidad de abrir varios repositorios.
- Lecturas y ediciones por símbolos priorizadas cuando sea apropiado.
- Menos tokens enviados a los agentes sin pérdida silenciosa de evidencias relevantes.
- Recuperación precisa de decisiones entre sesiones y clientes.
- Degradación parcial ante fallo de LSP, grafo, red o LLM.
- Mantenimiento autónomo de conocimiento con límites de coste, CPU y privacidad.
- Sin pérdida irrecuperable de memoria por consolidación/actualización.

## 3. Alcance y exclusiones

### 3.1 En alcance

- Motor Rust propio y adaptadores CLI/MCP, índices SQLite/FTS5, AST/grafo, cliente LSP y proveedores LLM.
- Políticas nativas, extensiones/hooks por agente cuando estén disponibles, gestión de sesiones y worktrees.
- Auto-mantenimiento local-first con inferencia externa autorizada y gobernanza.
- TUI de observabilidad y aprobaciones en una fase posterior.

### 3.2 Fuera del MVP

- Framework de agentes/autonomía generalista, reemplazo de Codex/Claude/OpenCode u orquestador de tareas.
- Reimplementación de compiladores o servidores LSP completos.
- Cloud propio, multitenancy empresarial, colaboración remota compleja, Obsidian, embeddings locales obligatorios.
- Duplicar de forma literal todas las herramientas de Serena/Engram/Graphify/RTK.
- Edición de código autónoma durante el mantenimiento del conocimiento.
- Migración automática irreversible de todas las memorias antiguas sin validación.

### 3.3 Límites honestos

- **Un único binario de aplicación** no elimina Git, los servidores LSP ni el acceso a APIs externas. Se documentarán y autodetectarán las dependencias opcionales.
- El motor no puede interceptar todos los comandos nativos de los agentes. Las políticas se aplicarán a sus propias operaciones y se complementarán con instrucciones/hooks soportados.
- JEV y LLM externos son **siempre opcionales** y se activan por separado. Su ausencia es una configuración válida, no un error ni impedimento para arrancar o usar capacidades independientes. La API, despliegue y disponibilidad real de JEV deben verificarse antes de integrarlo.
- Un LLM no puede certificar por sí solo que una afirmación sea verdadera; deberá marcar procedencia, inferencias e incertidumbre.

## 4. Principios de diseño

1. **Local-first, privado y offline-capable en el núcleo**: sin conectividad, funcionan código, comandos, índice y memoria local.
2. **Zero surprise**: no modificar repositorios ni políticas globales de manera silenciosa.
3. **Semantic first**: símbolos antes que lectura indiscriminada cuando la tarea sea semántica.
4. **Progressive disclosure**: resumen primero, evidencias detalladas bajo demanda.
5. **Source of truth**: código ejecutado, versión instalada y tests prevalecen sobre documentación y recuerdos.
6. **Evidence provenance**: cada conclusión trazable a sesiones, ficheros, commits, resultados o fuentes.
7. **Idempotencia y rollback** en mutaciones y migraciones.
8. **Fail open para disponibilidad de lectura**, **fail closed en escrituras sensibles y controles de seguridad**.
9. **Determinismo antes de inferencia**, LLM para tareas semánticas justificadas.
10. **Priorizar utilidad real, no el número de features**; medir antes de ampliar.
11. **Proveedores de IA opcionales:** detección de capacidades, exposición dinámica y ninguna sustitución engañosa. Una heurística no se anuncia como síntesis generativa.
12. **Coste operativo como criterio de producto:** ninguna capacidad se considera mejora si aumenta el mantenimiento total sin ganancia medible en calidad, contexto, fiabilidad o productividad.

## 5. Arquitectura lógica

```text
Codex ─────────┐
Claude Code ───┼──> Adaptadores MCP stdio / hooks / CLI
OpenCode ──────┘                      │
                                    ▼
                          Runtime + Policy Engine
                                    │
            ┌─────────────┬─────────┼──────────┬─────────────┐
            ▼             ▼         ▼          ▼             ▼
      Code / LSP     Execution    Context    Memory        Docs
            │             │         │          │             │
            └─────────────┴────┬────┴──────────┴─────────────┘
                               ▼
                     Índice + Grafo + Evidencias
                               │
                     Knowledge Evolution Engine
                               │
              Reglas + JEV opcional + LLM opcional
                               │
                 Learning Governance + Audit Log
                               │
                         SQLite / FTS5
```

### 5.1 Modelo de procesos

- Un **core local** opcional compartido para índices, datos y operaciones costosas; acceso IPC local protegido (socket Unix; alternativa nombrada en Windows).
- **Puentes MCP stdio pequeños** por agente si su transporte lo exige. Los puentes son instancias del mismo ejecutable en modo adaptador, no productos aparte.
- **Modo standalone** cuando el daemon no pueda arrancar: operaciones locales de baja complejidad deben seguir funcionando siempre que la seguridad lo permita.
- Propiedad estricta de locks, sesiones, worktrees y límites de concurrencia; no asumir que distintos agentes comparten el mismo directorio activo.
- Distinguir recuperación del servicio, resolución/reintento de operaciones y recuperación del transporte MCP. Un puente vivo no prueba que una operación interrumpida terminase; una caída del puente puede exigir reconexión del cliente. Matriz obligatoria por agente en R1 con reinicios de core/puente/cliente, concurrencia e idempotencia; ninguna escritura de resultado ambiguo se repite a ciegas.
- ADR-02 evaluará dos modos, standalone para operaciones autocontenidas y shared core para índices/grafo/sesiones/mantenimiento. No exigir daemon persistente para todo: `doctor`, diagnóstico/plan de reparación básica y lecturas viables deben poder funcionar si el core no arranca. Toda reparación que escriba conserva autorización, locks y verificación de DB; no se fuerza acceso inseguro para ofrecer standalone. Es criterio de evaluación R0, no arquitectura experimentalmente confirmada.

### 5.2 Tecnologías propuestas

- Rust estable; MCP SDK Rust (`rmcp`) sujeto a evaluación y pin de versión.
- SQLite embebido con FTS5, WAL, backups y migraciones versionadas.
- Tree-sitter para AST sintáctico incremental; gramáticas por lenguaje empaquetadas/licenciadas correctamente.
- Cliente JSON-RPC LSP propio sobre stdio para servidores instalados o descargados de forma gestionada.
- Git mediante CLI o librería evaluada por robustez; ninguna lectura de Git debe ejecutar hooks del repositorio por accidente.
- HTTP con TLS para API de documentación/LLM; credenciales externas a SQLite.
- TUI posterior.

## 6. Motor de políticas y enrutamiento

### 6.1 Política semántica

- Para localizar declaraciones, implementaciones, estructura de fichero, referencias, diagnósticos y renombrados: **LSP/AST primero**.
- No comenzar por `rg`, `grep`, `find`, `cat` o lectura del fichero completo cuando un símbolo resoluble satisfaga la petición.
- Si el resultado semántico es suficiente, no repetir la exploración textual.
- Texto plano, configuración, documentación, logs, consultas literales, SQL sin soporte semántico o símbolos irresolubles: herramientas textuales apropiadas.
- Antes de renombrar, borrar o transformar símbolos compartidos: consultar referencias y advertir sobre falta de cobertura.
- El reemplazo de Serena no necesita `initial_instructions`; DrCooper inicializa capacidades/proyecto automáticamente una sola vez por sesión.

### 6.2 Documentación y versiones

- Código propio: herramientas locales, no Context7.
- Bibliotecas, SDK, frameworks, APIs, CLI y protocolos externos: identificar versión exacta instalada y consultar documentación versionada.
- Priorizar documentación local fiable si corresponde a la versión; después Context7 por API autorizada; finalmente fuente oficial. Evitar llamadas externas por conocimiento estable.
- No inventar opciones ni parámetros dependientes de versión. Si la documentación contradice comportamiento reproducible del proyecto, señalarlo y priorizar ejecución/versión real.
- Tiempo de caché y procedencia de documentos; no presentar fuente obsoleta como actual.

### 6.3 Memoria por tarea

- Al iniciar una tarea real, recuperación relevante y acotada, sin bloquear si la memoria falla.
- Al finalizar, guardar solo conocimiento no deducible directamente del repo: decisiones, alternativas rechazadas, correcciones del usuario, trampas de entorno, incidencias ya resueltas.
- No copiar estructura versionada, commits y ADR como memoria independiente si pueden referenciarse.
- Información clínica real o ficticia excluida del almacenamiento automático; secretos y datos sensibles filtrados.
- Los recuerdos son evidencia contextual, no instrucciones con mayor prioridad que la orden actual del usuario.

### 6.4 Ejecución, contexto y reducción de ruido

- Capturar salida completa y estado de salida (`exit_code`, stdout/stderr, duración, comando, directorio, truncado).
- Filtros por familia: Git, tests, builds, diagnósticos y logs.
- Ofrecer recuperación de salida cruda y repetición equivalente (`raw`, `proxy`) antes de concluir basándose en una compresión sospechosa.
- Lotes de comandos para análisis, búsquedas en resultados indexados y sesiones temporales.
- Distinguir **sandbox real** de proceso separado: no anunciar aislamiento de escritura si se permite ejecutar comandos que escriben en disco.
- Para procesos no confiables, aislamiento real y permisos separados; para procesamiento puro, entorno explícitamente de solo lectura.

## 7. Superficie MCP y CLI (contrato inicial)

Evitar decenas de herramientas. Propuesta inicial de 10 herramientas MCP:

| Tool MCP | Comportamiento |
|---|---|
| `dev_code_search` | Resolución de símbolos, patrones y archivos con estrategia semántica primero |
| `dev_code_inspect` | Firma, implementación, definición y resumen progresivo |
| `dev_code_references` | Referencias, callers/callees y ubicaciones verificadas |
| `dev_code_edit` | Renombrado, inserciones/sustituciones simbólicas con preview y checks |
| `dev_diagnostics` | Diagnósticos LSP, gravedad, rango, procedencia |
| `dev_execute` | Comandos, filtrado y artefactos recuperables |
| `dev_context_search` | Búsqueda FTS en logs, resultados y documentos indexados |
| `dev_memory_search` | Búsqueda/retrieval escalonado de memorias |
| `dev_memory_save` | Memorias tipadas con scope, topic key y evidencia |
| `dev_session` | Estado, recuperación, finalizar y seguimiento |

El grafo, documentación y gobernanza pueden incorporarse como suboperaciones tipadas o herramientas adicionales solo tras medir ergonomía y compatibilidad. No sacrificar contratos claros por reducir artificialmente el número de herramientas.

### 7.1 Ejemplo de inspección

```json
{
  "tool": "dev_code_inspect",
  "arguments": {
    "symbol": "asErpSyncRepository",
    "include_references": true,
    "depth": 1,
    "project": "auto"
  }
}
```

### 7.2 Requisitos de cada respuesta

- `status`: `ok | partial | unavailable | error`.
- `strategy_used`: LSP, AST, texto, cache, Git, etc.
- `source_locations`: archivos, símbolos, líneas/rangos, commit, ID de artefacto.
- `completeness`: cobertura y límites conocidos.
- `next_steps`: IDs para expandir resultados sin repetir trabajo.
- `warnings`: incertidumbres reales; sin convertir ausencia de un proveedor opcional en bloqueo genérico.
- `correlation_id` y tiempos para depuración.

### 7.4 Capacidades y proveedores opcionales

| Configuración | Capacidades, una vez implementado su hito |
|---|---|
| Sin JEV ni LLM | CLI/MCP, código LSP/AST, grafo, ejecución, contexto, memoria y mantenimiento determinístico |
| Solo LLM | Base más síntesis generativa, contradicciones semánticas y patrones que el adaptador validado soporte |
| Solo JEV | Base más clasificación de opciones cerradas que su API verificada permita; no síntesis generativa |
| JEV y LLM | Unión de capacidades verificadas, con selección de motor autorizada y trazable |

- Registrar estado por proveedor y operación: `disabled`, `not_configured`, `ready` o `temporarily_unavailable`. Los dos primeros no generan error de salud del producto.
- MCP no anuncia operaciones exclusivas de proveedores ausentes como ejecutables. CLI/TUI permiten consultar disponibilidad y configuración sin anunciar esas funciones como disponibles; invocación explícita no disponible responde con estado y motivo, nunca éxito simulado.
- Proveedor configurado que falla degrada solo sus operaciones. Actualizar capacidades en sesión por mecanismos compatibles con cada cliente; si necesita reconectar, indicarlo. Reevaluar disponibilidad antes de cada operación sensible al proveedor.
- Funciones con varios motores usan únicamente implementaciones autorizadas y evaluadas para esa operación; no asumir equivalencia por compartir etiqueta. Sin motor válido, la función no se ofrece.
- Activación, claves, consentimiento, presupuesto y límites de datos son independientes por proveedor/proyecto. No existen llamadas ni costes implícitos.
- **Madurez de compatibilidad**, separada del estado de disponibilidad: `contract_tested` acredita dobles, `integration_verified` acredita API real y `production_ready` acredita validación operativa, seguridad y recuperación. Sin evidencia queda sin verificar, fuera de esos niveles. Registrar operación/proveedor/versiones y evidencias; solo `production_ready` permite anunciar soporte productivo pleno. Un proveedor listo/configurado puede seguir siendo experimental. La matriz simulada de R4 no prueba integración JEV, cuya adopción se decide en R5; revalidar al cambiar versión/configuración relevante.

### 7.3 CLI propuesto (no implementado)

```bash
drcooper setup codex
drcooper setup claude
drcooper setup opencode
drcooper doctor
drcooper status
drcooper index .
drcooper graph impact --symbol syncStock
drcooper memory search 'idempotencia'
drcooper knowledge status
drcooper knowledge review --dry-run
drcooper knowledge consolidate
drcooper knowledge history
drcooper knowledge rollback <batch-id>
drcooper knowledge stats
drcooper update --check
```

`drcooper` es nombre provisional; CLI y opciones son contratos propuestos.

## 8. Code Intelligence y grafo

### 8.1 Lenguajes y proveedores

- PHP 7.x legado: no confundir versión de runtime con capacidad de análisis; servidor LSP configurable y pruebas sobre sintaxis real.
- TS/JS: resolución de referencias y rename mediante TypeScript LSP.
- Python: BasedPyright o servidor compatible.
- AST fallback cuando servidor no disponible; texto fallback cuando AST es insuficiente.

### 8.2 Índice de símbolos

Clave lógica: `{repository_id, worktree_id, relative_path, content_hash, language, symbol_identity}`. Guardar firmas, rangos, identificadores, relaciones y procedencia de proveedor. Reindexación incremental por contenido; invalidación conservadora por cambios de configuración o dependencias.

### 8.3 Grafo

Nodos: proyecto, paquete, módulo, fichero, símbolo, commit, observación de memoria, decisión, prueba.  
Aristas: contains, imports, calls, references, implements, depends_on, changed_in, relates_to_memory, verified_by, supersedes.  
Cada arista incluirá tipo de evidencia, proveedor, versión de índice y grado de fiabilidad. Distinguir relaciones estáticas observadas de inferencias. El esquema anterior es extensible, no exige implementar todos los tipos al empezar: R3 comienza con fichero/símbolo/memoria y `contains`, `imports`, `references`, `relates_to_memory`; añadir `calls` solo con cobertura comprobada. Paquetes, commits, decisiones, pruebas y otras aristas se incorporan tras demostrar utilidad medida, sin bloquear el mantenimiento de memoria.

Operaciones: callers/callees, dependencia inversa, ruta entre símbolos, análisis de impacto, hotspots, memoria relacionada. Los resultados no deben afirmar causalidad sin evidencia.

## 9. Memoria persistente inspirada en Engram / AgentMemory

### 9.1 Capas

1. **Evidencia primaria inmutable:** evento/observación/archivo/commit de origen.
2. **Memoria de trabajo por sesión:** contexto y operaciones temporales.
3. **Conocimiento por proyecto:** decisiones, resoluciones, preferencias locales, patrones.
4. **Conocimiento personal/global autorizado:** prácticas reutilizables, nunca promocionadas globalmente por simple inferencia.
5. **Conocimiento derivado:** síntesis y relaciones con vínculo a fuentes y estado de validación.

### 9.2 Alcances

`worktree`, `project`, `personal`, `global`. Lectura cruzada intencional; escritura requiere propietario no ambiguo. Proyecto canónico basado en Git remoto/identidad persistida más alias y path, con detección de monorepos y worktrees.

### 9.3 Campos principales de memoria

- `id`, `project_id`, `scope`, `session_id`, `topic_key`, `type`, `title`, `content`.
- `status`: `active`, `derived`, `pending_review`, `superseded`, `archived`.
- `evidence_ids`, `source_commit`, `symbol_ids`, `created_at`, `updated_at`, `review_after`, `verified_at`.
- `confidence_type`: observado/verificado/inferido; evitar porcentajes espurios.
- `revision`, `supersedes_id`, `fingerprint`, `privacy_class`, `origin_actor`.

### 9.4 Higiene

- Deduplicación exacta por fingerprint de proyecto/scope/tipo/título/contenido normalizado.
- `topic_key` estable con revisiones y supersesión, sin sobreescribir pruebas originales.
- Retrieval escalonado: búsqueda compacta → contexto/timeline → evidencias completas.
- Conflictos mostrados con fuentes y motivaciones; nunca asumir que lo más reciente es automáticamente correcto.
- Memorias con fecha de revisión, especialmente al cambiar archivos/símbolos enlazados.
- Retención separada: caches/logs efímeros eliminables; memorias esenciales archivadas y recuperables.
- Importación/migración desde AgentMemory y otros sistemas solo con consentimiento, previews e idempotencia. Nunca exigir tener sus servicios activos.
- Mantenimiento básico desde R2, independiente de grafo: verificar existencia/hash de fuentes, dedupe exacto, agrupación por topic y consolidación estructural reversible. Consolidar localmente no inventa ni parafrasea contenido semántico; preserva excepciones, fechas y restricciones con enlaces a originales.
- Cuotas por clase (fuentes, derivados, propuestas, auditoría, artefactos/caches), proyecto y total. Medir crecimiento neto y amplificación por consolidación; alcanzar cuota frena nuevas derivaciones, compacta índices o archiva conforme a política, sin borrar silenciosamente memoria esencial.

## 10. Knowledge Evolution Engine (KEE)

### 10.1 Finalidad

Mientras la herramienta esté residente pero ociosa, ejecutar mantenimiento incremental del conocimiento. La actividad debe ser útil, observable, pausada por nueva interacción, acotada en consumo y reversible.

### 10.2 Detección de inactividad

- Umbral configurable (p. ej. 15 minutos), ventana mínima entre lotes (p. ej. 6 horas), cola de cambios pendientes y priorización incremental.
- No inferir inactividad únicamente de ausencia de llamadas MCP: comprobar trabajo activo, tareas concurrentes, CPU, presión RAM/IO y locks.
- En Windows/WSL: preferir detección de carga y presupuestos explícitos. Pausa cooperativa en checkpoints, no interrupción de transacciones a medias.
- Si el core no está activo, no prometer mantenimiento en background; al arrancar se recuperan trabajos pendientes si procede.

### 10.3 Pipeline persistente: Discover → Verify → Commit / Propose

Tres etapas con colas/estados persistentes independientes, fingerprints, revisión de entrada, reintentos acotados, leases y trazabilidad. Son etapas lógicas sobre SQLite, no tres servicios adicionales.

1. **Discover:** seleccionar cambios incrementales y candidatos a duplicado/relación/conflicto/patrón mediante FTS, topics y fuentes disponibles. No modificar conocimiento canónico. El grafo aporta señales cuando existe, no es requisito.
2. **Verify:** comprobar integridad, vigencia y procedencia; consultar código/grafo si están disponibles. Reglas primero; clasificación JEV o LLM solo si esa capacidad está habilitada, autorizada y presupuestada. Salida estructurada con evidencias, incertidumbres y naturaleza observada/verificada/inferida.
3. **Commit / Propose:** revalidar versión base, esquema, permisos y límites; aplicar solo cambios autorizados reversibles o crear propuesta L2/L3. Registrar lote, costes, versiones e inversa de rollback.

Cada transición conserva entrada, resultado, motor, versión y motivo; agotamiento de presupuesto o fallo externo deja candidato pendiente sin redescubrirlo ni repetir cambios. Una respuesta externa puede tener coste aunque no llegue: registrar intento y consumo incierto, sin prometer exactamente una llamada al proveedor.

### 10.4 Capacidades

Disponibilidad según §7.4: mantenimiento verificable local siempre que esté implementado; síntesis generativa y análisis semánticos externos solo con proveedor habilitado y validado para esa función.

- Deduplicar.
- Consolidar sin perder originales.
- Detectar contradicciones y señalar condiciones donde ambas pueden ser correctas.
- Revisar memoria vinculada a archivos/símbolos modificados.
- Proponer síntesis temáticas y relaciones verificables.
- Archivar conocimiento sin uso o superseded conforme a políticas explícitas.
- Aprender patrones de trabajo (errores recurrentes, operaciones que necesitan verificación, decisiones descartadas).
- Medir precisión de sugerencias y rechazos; ajustar ranking/notificaciones, no reglas críticas.

### 10.5 Ejemplo de inferencia permitida

Tres observaciones sobre reintentos e idempotencia permiten proponer un resumen «usar identificadores estables para evitar duplicados» con referencias a cada observación. El resultado queda `derived` hasta verificarlo con pruebas/código o decisión explícita. Nunca promocionar repetición de hipótesis a hecho confirmado.

**Límite de propagación:** una conclusión IA no puede ser la única evidencia de otra conclusión promovida a verificada. Conservar linaje hasta fuentes primarias, detectar ciclos y aplicar límite configurable de profundidad; al no poder resolver fuentes o superar el límite, detener derivación y solicitar revisión. Una aprobación de práctica no equivale a verificar empíricamente su verdad.

### 10.6 Modo de inferencia y LLM

- **Desde la primera versión funcional del KEE completo se soporta LLM remoto opcional**, desactivado por defecto. Configurarlo no es requisito de uso ni de salida del hito; las funciones generativas solo se habilitan con proveedor válido, clave segura y controles completos.
- Adaptadores OpenAI, Anthropic y endpoint compatible (validar contratos reales por proveedor antes de implementar).
- Configurables: modelo, timeout, reintentos exponenciales, tasa, presupuesto diario/mensual, límite de tokens, política de datos, redacción y nivel de acceso permitido.
- **Privacidad:** habilitación explícita de envío externo; previsualización/filtrado de qué datos salen; secretos, datos clínicos y información clasificada no se envían. Si no se puede redactar con garantías, omitir llamada.
- Sin API key/red: operaciones determinísticas locales disponibles; no marcar síntesis LLM como ejecutadas.
- No exponer claves en registros, MCP, TOML versionado, DB o informes.
- Control de costes por proveedor y trazabilidad de estimación vs coste real.
- Tres presupuestos independientes: dinero, recursos locales (CPU/RAM/IO/tiempo) y volumen de conocimiento exportable (bytes/tokens, memorias y fuentes por lote/periodo). Reservas persistentes por proveedor/proyecto antes del envío, también con agentes concurrentes; un límite no sustituye los otros.

### 10.7 JEV como clasificador opcional

- Evaluar su API y capacidades exactas con documentación vigente antes de concretar integración; tratarlo como proveedor de decisión, no como verdad ni autoridad.
- Opciones cerradas: nuevo/duplicado/relacionado, merece revisión, prioridad, ambigüedad, posible contradicción.
- Las reglas verificables se aplican primero; JEV solo cuando agregue valor medible frente a heurística/LLM.
- Desactivar sin bloquear resto del motor; registrar confianza y calibración; nunca autorizar acciones sensibles solo por un score alto.
- Contrato común desde R0 para reglas, JEV y LLM con opciones cerradas, abstención, IDs de evidencia, versión, latencia y coste. El benchmark incluye estrategias disponibles y marca las no disponibles; no exige credenciales ni adopción de JEV.
- Activación y consentimiento independientes del LLM. Si el despliegue JEV requiere red, se aplican los mismos controles de egress y tres presupuestos; sin su API viable no se anuncia soporte.

## 11. Learning Governance: qué aplica y qué consulta

### 11.1 Matriz de autonomía

| Nivel | Ejemplos | Política |
|---|---|---|
| L0 — mantenimiento mecánico | índices, caches, dedupe exacto | Automático con auditoría |
| L1 — conocimiento derivado reversible | relaciones respaldadas, síntesis no normativa | Automático como `derived`, conservar fuentes |
| L2 — interpretación y nuevas prácticas | contradicciones ambiguas, patrones, recomendaciones | Crear propuesta, no cambiar política |
| L3 — cambios normativos o sensibles | reglas globales, permisos, seguridad, borrado, escritura de código | Consentimiento explícito y, si aplica, revisión de diferencias |

**Regla invariable:** no aplicar política de seguridad nueva/rebajada ni cambios en permisos por inferencia autónoma; la confianza de JEV/LLM no eleva permisos.

### 11.2 Bandeja de propuestas

- No interrumpir la sesión normal por cada hallazgo; agrupar propuestas y mostrarlas en CLI/TUI, o resumen opcional al abrir una sesión.
- Cada propuesta: título, categoría, impacto, ámbito, evidencias, motivos, diff entre estado actual y propuesto, confianza cualitativa, fecha y estado.
- Acciones: `approve`, `reject`, `snooze`, `view-evidence`, `approve-for-project`, `approve-globally` (global con confirmación explícita adicional), `revert`.
- Rechazo documentado evita proponer la misma idea indefinidamente; reapertura solo ante evidencia nueva material.
- Aprendizaje de preferencias ajusta frecuencia y ranking de propuestas; no deshabilita checks obligatorios.
- Ante conflicto con una instrucción actual del usuario prevalece la instrucción actual dentro de límites de seguridad.
- Cuota de propuestas, agrupación por causa/topic, prioridad por utilidad, caducidad y digest opcional desde la bandeja mínima. Medir tiempo de revisión y acumulación neta; no convertir cada hallazgo en una interrupción.

### 11.3 Estados de propuestas

`candidate → proposed → approved/rejected/deferred → applied → verified/reverted`. Idempotencia por fingerprint, historial completo y expiración de candidaturas obsoletas.

## 12. Almacenamiento y migraciones

Tablas lógicas iniciales: `projects`, `project_aliases`, `worktrees`, `sessions`, `observations`, `memory_revisions`, `memory_sources`, `knowledge_links`, `symbols`, `edges`, `artifacts`, `artifact_chunks` (FTS5), `proposals`, `proposal_decisions`, `maintenance_jobs`, `maintenance_runs`, `audit_events`, `schema_migrations`.

- SQLite WAL donde sea apropiado, conexiones con busy timeout y transacciones pequeñas.
- IDs estables e índices por proyecto y `topic_key`; write operations idempotentes.
- Compatibilidad de versiones de esquema explícita; snapshot verificado antes de migrar.
- Exportación/importación portable, incluyendo provenance.
- Procedimiento de recuperación ante corrupción con `doctor --plan/--repair` y nunca reparación silenciosa destructiva.
- Control de crecimiento de logs/caches por cuotas y retención configurable.
- Estados/colas de Discover, Verify y Commit/Propose con revisión base, fingerprint, intentos, lease, siguiente reintento y relación con lote. Una sola DB puede alojar las tres etapas.

## 13. Seguridad y privacidad

- Modelo de amenazas: prompt injection en logs/docs/código, exfiltración por LLM, ejecución arbitraria, paths externos al workspace, symlinks, contaminación entre proyectos, agentes concurrentes, secreto en memorias.
- Separar **contenido no confiable** (código, docs, salida de comandos, páginas) de instrucciones del usuario y políticas.
- Shell commands: autorización según configuración del cliente, allowlist/denylist contextual, cwd fijado, timeout, límite de salida, subprocess tree cleanup y accesos a red/disco consistentes con sandbox real.
- Operaciones sensibles exigen preview/diff, verificación de estado base/hash, comprobación de referencias y consentimiento cuando proceda.
- Proveedores externos LLM/JEV: redacción, scopes por proyecto, opt-in independiente, preview del payload y límite de volumen; no enviar repos completos, permitir deny paths (`.env`, claves, credenciales, historiales sensibles). Si la clasificación/redacción no ofrece garantías, omitir llamada.
- API/IPC local: permisos de archivo/socket y tokens si se expone HTTP; loopback no implica acceso seguro por defecto.
- Logs estructurados sin secretos ni datos clínicos.
- Gestión de versiones y dependencias con lockfile/SBOM y auditoría de supply chain.

## 14. Fiabilidad y actualización

### 14.1 Doctor

Checks para protocolo MCP, negociación, proceso/bridge, CLI path, cliente, permisos IPC, SQLite, locking, proyecto activo, índices, memoria, grafo, disponibilidad de LSP, proveedores remotos configurados, budgets y migraciones. Salidas humanas y JSON.

### 14.2 Fallos y degradación

- LSP falla → AST y luego texto, marcando límites.
- Grafo falla → búsquedas semánticas y memoria siguen.
- LLM/JEV/red fallan → motor local mantiene operaciones determinísticas.
- DB bloqueada → reintento acotado e informe claro; no escrituras fuera de ámbito.
- Adaptador MCP falla → recuperación, diagnóstico y modo CLI; no prometer que un cliente siga operando tras perder el transporte.
- Hooks no bloquean trabajo nativo por indisponibilidad del core, **excepto** cuando la operación requiera un control de seguridad obligatorio.

### 14.3 Release y actualización

- Versión binaria y schema/API separadas; matriz de compatibilidad por cliente.
- Releases firmadas/verificadas, checksums, staging y pruebas de arranque/handshake.
- Actualización atómica con copia de binario anterior y base compatible; rollback probado.
- Ninguna actualización automática forzosa por defecto; `update --check` y `update --apply` separados.
- Tests E2E en WSL/Linux y clientes, incluyendo reconexión y sesiones existentes.
- Desde R1: actualización básica desde artefacto local verificado, cambio atómico, snapshot compatible y recuperación del binario/DB anterior. R6 amplía canales remotos y distribución multiplataforma; no aplaza recuperación básica.
- Prueba transversal **Zero-Maintenance Installation** desde R1: instalar, configurar tres agentes, desinstalar preservando datos/config ajena, reinstalar, actualizar, inyectar fallo y recuperar. Sin edición manual fuera de pasos declarados y consentimientos iniciales; medir intervenciones, no prometer mantenimiento literalmente nulo.
- Proveedores LSP gestionados desde R2: versiones fijadas, integridad, staging, rollback independiente y conservación de configuración del usuario. Fallo de instalación LSP no inutiliza el núcleo.
- Antes de cada release, ejecutar `bench` sobre capacidades comprometidas y archivar informe ligado al hash del candidato. Regresión de calidad por encima del umbral o evidencia obligatoria insuficiente bloquea promoción; mejora de velocidad no compensa pérdida de precisión. No hay actualización automática autorizada por un benchmark; se mantienen consentimiento y recuperación.

## 15. Configuración orientativa

```toml
# ~/.config/drcooper/config.toml — DISEÑO, NO CONFIG REAL
[code]
semantic_first = true
check_references_before_edit = true
text_fallback = true

[memory]
enabled = true
recall_on_task_start = true
save_policy = "selective"
exclude_sensitive = true

[execution]
optimize_output = true
preserve_full_output = true

[documentation]
providers = ["local", "context7", "official"]
version_aware = true
fallback_on_failure = true

[graph]
enabled = true
incremental = true

[knowledge.evolution]
enabled = true
deterministic_maintenance = true
idle_minutes = 15
interval_hours = 6
batch_size = 25
max_cpu_percent = 15
permanent_delete = false

[ai.llm]
enabled = false
provider = "openai"
model = "CONFIGURE_MODEL_ID"
api_key_env = "DRCOOPER_LLM_API_KEY"
daily_budget_usd = 0.50
monthly_budget_usd = 10.00
external_data_opt_in = false

[ai.jev]
enabled = false
provider = "jev"

[knowledge.governance]
auto_apply_l0 = true
auto_apply_l1_derived_only = true
require_review_l2 = true
require_approval_l3 = true

[reliability]
graceful_degradation = true
auto_update = false
```

**Importante:** ambos proveedores IA están desactivados por defecto y se activan por separado. Los presupuestos, tiempos y porcentajes son orientativos sujetos a benchmark; antes de enviar a cualquier proveedor externo se requieren consentimiento por proyecto y límites de dinero, recursos y volumen configurados. Las claves para esos límites se concretarán en el contrato, no se infieren de este ejemplo. Ninguna clave es todavía interfaz pública congelada.

## 16. Criterios de aceptación funcionales

### 16.1 Código

- Dado un símbolo resoluble, una inspección empieza por LSP/AST y evita grep redundante.
- Antes de renombrar un símbolo compartido, el plan muestra referencias y límites de cobertura.
- Si falta LSP, la respuesta indica la estrategia fallback y nunca inventa referencias semánticas.

### 16.2 Ejecución/contexto

- Salidas comprimidas mantienen exit status, fallos y referencias a logs íntegros.
- Una compresión errónea es reversible; el log original recuperable coincide byte a byte salvo política explícita de retención.
- Ejecución aislada no promete imposibilidad de mutar el workspace salvo sandbox probado.

### 16.3 Memoria

- Misma decisión desde distintos agentes aparece en el mismo scope/proyecto sin duplicado exacto.
- Worktrees comparten conocimiento canónico pero conservan estados de sesión separados.
- `topic_key` mantiene revisiones y vínculos a evidencia; las fuentes no desaparecen tras consolidación.
- Una memoria asociada a código modificado puede quedar `pending_review`.

### 16.4 Evolución

- Tras inactividad configurable, un lote se ejecuta respetando cuotas y locks.
- Nueva interacción pausa el lote sin corrupción ni transacciones interrumpidas.
- Cuando se habilita LLM, responde con JSON validable y fuentes; resultados sin evidencia se rechazan o marcan inferidos. Sin LLM no se ofrece síntesis generativa.
- Sin API key/Internet, dedupe, revisión de archivos y limpieza segura siguen funcionando.
- Patrón de alta repercusión genera propuesta, **no** política aplicada.
- Cada cambio autónomo reversible puede deshacerse por lote.
- Las etapas persistentes conservan candidatos al fallar Verify y no duplican commits al reintentar; no requieren grafo para mantenimiento básico.
- Las cuatro configuraciones sin IA, solo LLM, solo JEV y ambas tienen capacidades correctas; no configurado/desactivado no es error. Pruebas reales de un proveedor solo se exigen cuando está disponible y autorizado; dobles de prueba verifican el contrato restante sin fingir cobertura real.
- Síntesis conserva restricciones, excepciones, fechas y decisiones; medir omisiones, afirmaciones nuevas y contradicciones introducidas. Linaje reconstruible a fuentes primarias y ninguna inferencia se verifica por otra inferencia sola.

### 16.5 Seguridad/fiabilidad

- `doctor` identifica con precisión el componente roto sin inhabilitar los demás.
- Actualización fallida conserva binario anterior y DB recuperable.
- Ningún secreto llega al proveedor externo en suites de fuga simulada.
- Cliente A no puede escribir memorias de cliente B/proyecto B debido a detección ambigua de directorio.
- En R1 pasan Zero-Maintenance Installation y matriz de reinicio por cliente: servicio, operación y transporte se verifican por separado; resultado ambiguo no se repite sin resolución.

## 17. Métricas, evaluación y observabilidad

- Tokens y bytes por operación; **ahorro relativo** frente a baseline sin compresión.
- Latencia p50/p95 por tool, CPU máxima/tiempo de CPU, RSS, crecimiento de SQLite y volumen de índice.
- Precisión y cobertura de símbolos/referencias y análisis de impacto (golden fixtures).
- Utilidad de memoria: tasa de recuperación pertinente, duplicaciones, contradicciones, edad y stale rate.
- Knowledge Evolution: candidatos, revisados, sintetizados, descartados, aprobados, revertidos; feedback y tasa de falsas propuestas.
- Conservación semántica sobre corpus etiquetado: restricciones/excepciones/fechas/decisiones omitidas, afirmaciones sin evidencia, contradicciones introducidas y reconstrucción de fuentes. Comparar original y derivado; menor tamaño no implica mejor resultado.
- Clasificación comparable reglas/JEV/LLM: precisión por clase, abstención/calibración, latencia y coste; marcar proveedores no disponibles sin penalizar al producto.
- Crecimiento neto por clase/proyecto, amplificación de derivados y tiempo/backlog de revisión; tres presupuestos y profundidad de linaje.
- Coste efectivo de API por día/mes y por propuesta útil; logs redactados.
- Fiabilidad: startup success, MTTR, fallos MCP por versión, compatibilidad y frecuencia de rollback.
- Suite de regresión comparando antes/después en repositorios reales (PHP legado, TS y Python) con muestras congeladas y criterios predefinidos.

### 17.1 Bench como contrato público

Comandos propuestos, todavía no implementados: `drcooper bench run --suite <suite>`, `drcooper bench compare --baseline <run-id|version> --candidate <run-id|version>` y `drcooper bench report`. Diseño en DC-002/DC-005; primera implementación en DC-016 sobre CLI/artefactos de DC-010/DC-013, ampliada por cada módulo sin añadir issues padre.

Suites: ejecución, contexto, semántica, memoria, grafo, documentación, conocimiento, ciclo de vida y tareas completas. Comparar con RTK, Serena/LSP, Context Mode, AgentMemory, Graphify y Context7 en sus capacidades reales. Oráculos versionados independientes de esas herramientas; LSP directo con la misma versión/configuración permite separar calidad del proveedor y coste añadido por DrCooper.

### 17.2 Comparabilidad, calidad y resultados históricos

Cada run conserva ID, versión/esquema, hashes de corpus/oracle/configuración/binario, herramientas y proveedores, agente/modelo, entorno/carga, permisos, orden, caché fría/caliente, repeticiones, estado, métricas y evidencias recuperables redactadas. Registrar método de tokens, recursos del árbol de procesos completo, fallos y variabilidad; no atribuir mejoras del modelo a herramientas ni confundir bytes con tokens.

Veredictos: `pass`, `regression`, `inconclusive`, `incomparable`. Ausencia de medición no es cero ni aprobación. Solo comparar runs compatibles; alias de versión ambiguo requiere run IDs. Primero validar invariantes y umbrales de calidad por capacidad/lenguaje/agente; luego valorar ahorro, latencia y mantenimiento. Cambiar oráculo/umbral/baseline para ocultar regresión está prohibido; revisiones motivadas conservan historia y pueden exigir repetir ambos lados.

CI desde R1 ejecuta suites sintéticas/offline y comparación contra última release aceptada; primera release usa baseline/oráculos R0 explícitamente. Pruebas reales de integración solo cuando disponibles/autorizadas, diferenciadas de dobles. Informes/manifiestos locales exportables permiten conservar baseline antes de retirar herramientas sin exigirlas instaladas para usar el producto ni introducir otro servicio.

### 17.3 Evaluación operativa y sustitución por capacidades

Separar benchmark técnico repetible de evaluación operativa con horizonte y mínimo de ciclos/eventos acordados en R0: instalaciones, actualizaciones de producto/LSP/agente, reinicios WSL, reconexiones y recuperación de fallos provocados, además de uso cotidiano. Medir minutos activos de intervención manual y espera automatizada por separado; cifra mensual exige periodo observado o extrapolación etiquetada con supuestos. Una semana sin fallos naturales no prueba fiabilidad sostenida.

Informe de sustitución por herramienta/flujo/lenguaje/agente/plataforma: `ready`, `keep` o `not_evaluated`, con evidencia de calidad, recursos y mantenimiento, limitaciones y ruta de vuelta. Puede retirarse Serena en TS y conservarse en PHP dinámico. Si DrCooper usa un LSP o API Context7, retirar el MCP anterior no elimina esa dependencia. No desinstalar automáticamente por un dictamen Bench.

Detalle del protocolo, suites, privacidad y criterios de promoción en [BENCHMARKS.md](docs/plan/BENCHMARKS.md). Las cifras de ejemplo aportadas en la discusión son ilustrativas y no se almacenan como resultados medidos.

## 18. Roadmap incremental

| Hito | Entregable | Puerta de salida |
|---|---|---|
| R0 — Discovery | Baseline, contrato Bench, amenazas, clasificación común y evaluación operativa | Decisiones bloqueantes, oráculos, umbrales y horizonte/eventos explícitos |
| R1 — Núcleo | CLI/MCP, identidad, SQLite, ejecución, memoria, recuperación y Bench mínimo | Instalación/reconexión verificadas, informe run/compare/report y puerta CI de regresión |
| R2 — Inteligencia y memoria básica | LSP/AST gestionados, edición, docs y consolidación estructural sin grafo | Semántica validada en PHP/TS/Python; memoria mantenida localmente con reversión |
| R3 — Grafo y sesiones | Grafo esencial incremental, impacto, timeline y obsolescencia | Utilidad demostrada antes de ampliar tipos de relaciones |
| R4 — KEE completo | Discover → Verify → Commit/Propose, idle, reglas y adaptadores LLM/JEV opcionales | Motor determinístico completo sin proveedores; capacidades opcionales verificadas, tres cuotas y rollback |
| R5 — Aprendizaje y gobernanza | Patrones, bandeja, feedback, JEV experimental, revisión por cambios de código | Sin políticas autoaplicadas fuera de nivel |
| R6 — Distribución | Canales avanzados de actualización, TUI, paquetes multiplataforma, migración asistida | Piloto valida sustitución por flujo sin incrementar mantenimiento injustificado |

**Ajuste tras auditoría:** JEV y LLM son siempre opcionales e independientes. R2 adelanta mantenimiento básico de memoria sin grafo ni inferencia externa; R4 entrega el KEE completo con soporte opcional de proveedores desde su primera versión funcional. Ningún hito exige contratar/configurar IA. Se validan contratos y disponibilidad con dobles de prueba; llamadas reales solo con proveedor disponible, opt-in y controles completos. No declarar probada una integración real por ejecutar un doble.

## 19. Integración con Code Cycle Toolkit

- DrCooper ofrece herramientas e inteligencia; Code Cycle Toolkit/Orca orquesta fases, revisión y validación.
- Integración mediante MCP/CLI documentados; sin importar dependencias internas de Orca.
- Los flujos del toolkit pueden citar evidencias/correlation IDs de DrCooper.
- No introducir lógica de issue/PR en el núcleo de memoria salvo enlaces/procedencia.

## 20. ADR y decisiones pendientes

### Acordado conceptualmente

- Producto propio de cero; no empaquetar cinco MCP; Rust preferente; SQLite; Codex/Claude/OpenCode; LSP gestionados; grafo esencial ampliable y política semántica; docs versionadas; mantenimiento básico sin grafo desde R2; KEE completo con LLM/JEV siempre opcionales e independientes; gobernanza L0–L3; instalación/actualización recuperables desde R1; archivado reversible. El backlog mantiene IDs existentes y divide issues grandes antes de asignarlas.

### Pendiente de validar formalmente

1. **Nombre final y disponibilidad** en GitHub, crates.io, dominios y marcas.
2. Runtime único compartido vs stdio standalone según restricciones por cliente/OS.
3. SDK/crates concretos, soporte de compilación estática y empaquetado de Tree-sitter.
4. Contrato exacto con Context7 API y restricciones de proveedor.
5. API real y despliegue de JEV; coste/latencia/comparativa vs clasificador LLM.
6. Proveedor/modelo opcional soportado inicialmente, presupuesto y redacción cuando se habilite; no seleccionar ninguno para uso real es una configuración válida.
7. Compatibilidad específica de hooks, scopes y setup con versiones actuales de agentes.
8. Heurísticas fiables de similitud sin embeddings, y umbrales de automatización.
9. Política de retención cuantitativa y límite de tamaño por proyecto.
10. Grado de automatización de migración desde AgentMemory.
11. Escenarios de aislamiento real para ejecución de herramientas.
12. Priorización de UI TUI frente a CLI y bandeja por agente.

## 21. Referencias de inspiración (no dependencias)

- RTK: https://github.com/rtk-ai/rtk (confirmar identificador exacto antes de documentar formalmente)
- Serena: https://github.com/oraios/serena
- Context Mode: referencia a verificar según instalación real
- AgentMemory: referencia a verificar según instalación real
- Graphify: referencia a verificar según instalación real
- Context7: https://context7.com/ y documentación de API oficial
- Engram: https://github.com/Gentleman-Programming/engram
- Code Cycle Toolkit: https://github.com/datacas/code-cycle-toolkit
- Protocolo MCP: https://modelcontextprotocol.io/
- LSP: https://microsoft.github.io/language-server-protocol/
- Tree-sitter: https://tree-sitter.github.io/tree-sitter/

**Nota:** inspirarse en funcionalidades y patrones de arquitectura no equivale a reutilizar código. Si se reutiliza código de terceros, revisar licencias, atribuciones y seguridad de dependencias.

## 22. Definición de terminado del producto inicial

La herramienta estará lista para sustituir las instalaciones actuales cuando, durante un piloto diario razonable:

1. Codex, Claude y OpenCode se conecten con configuración estable.
2. La mayoría de tareas reales de inspección/edición/ejecución/memoria funcionen sin herramientas originales.
3. Fallos de LSP, LLM, red o grafo no comprometan las demás capacidades.
4. Haya recuperación de datos, compatibilidad y rollback probados.
5. Se observen mejoras objetivas en coste operativo, tiempo de mantenimiento o carga contextual, **sin regresiones críticas**.
6. El motor de conocimiento produzca propuestas trazables y reversibles sin modificar políticas importantes sin aprobación.

La evidencia incluye informes Bench por capacidad y evaluación operativa con periodo/eventos suficientes definidos en R0, especialmente minutos de intervención manual. No se exige ganar todas las métricas; ninguna pérdida crítica de calidad/fiabilidad puede ocultarse tras ahorro de tokens. La sustitución parcial empieza cuando un flujo alcanza equivalencia aceptada, sin esperar retirar todo el conjunto.

---

**Resumen del producto:** «Un único motor de inteligencia para agentes de código que une navegación semántica, ejecución optimizada, contexto, memoria persistente, documentación, grafos y evolución autónoma del conocimiento, con control explícito del usuario sobre lo que aprende y aplica».
