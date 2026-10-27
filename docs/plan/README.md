# Plan de producto de DrCooper

Estado: planificación revisada tras auditoría «GO WITH CHANGES»; R0 autorizado como alcance, ejecución pendiente. Fecha: 2026-10-26.

Conjunto canónico: **DC-DOCSET-0.3.0**, inventario/rutas/versiones y hashes SHA-256 en [DOCUMENTOS_CANONICOS.json](DOCUMENTOS_CANONICOS.json). Esta revisión incorpora la segunda auditoría y Bench. No se inicia programación ni prototipos por instrucción del usuario.

Fuente de requisitos: [especificación maestra](../../drcooper_ESPECIFICACION_MAESTRA.md). El [brief de identidad](../../brief_identidad.md) guía la identidad visual, sin condicionar la arquitectura ni bloquear el núcleo.

## Objetivo

Construir un motor local de inteligencia compartido por Codex, Claude Code y OpenCode que permita comprender y editar código, ejecutar comandos, recuperar contexto y conservar conocimiento verificable entre sesiones. Debe reducir configuración, fallos operativos y consumo contextual frente al conjunto actual de herramientas, sin perder evidencias ni control del usuario.

DrCooper proporciona inteligencia y herramientas. Code Cycle Toolkit y Orca conservan la orquestación de trabajo, issues, revisiones y PR. El núcleo no incorpora un gestor de tareas ni un framework de autonomía general.

**JEV y LLM son siempre opcionales e independientes.** Sin ambos funcionan las capacidades locales implementadas y el mantenimiento determinístico. Las funciones exclusivas de un proveedor ausente no se anuncian disponibles; no configurado/desactivado es un estado válido. Configurar uno no activa el otro ni autoriza llamadas externas.

Regla de producto: ninguna capacidad cuenta como mejora si aumenta esfuerzo operativo sin ganancia medible en calidad, contexto, fiabilidad o productividad.

## Documentos de trabajo

| Documento | Uso |
|---|---|
| [Roadmap](ROADMAP.md) | Alcance por entrega, prioridades, puertas de salida y secuencia de trabajo |
| [Backlog de issues](ISSUES.md) | 52 issues padre con alcance, dependencias y aceptación verificable |
| [Incrementos de implementación](INCREMENTOS.md) | 69 subtareas que dividen las 23 issues L en entregas revisables |
| [Decisiones y cobertura](DECISIONES_Y_COBERTURA.md) | Incertidumbres, responsables por issue y trazabilidad con la especificación |
| [Correcciones de auditoría](AUDITORIA_CAMBIOS.md) | Resolución documental de H-01–H-13 y condiciones antes de desarrollar |
| [DrCooper Bench](BENCHMARKS.md) | Contrato nativo run/compare/report, calidad, regresiones y evaluación operativa |
| [Segunda auditoría](AUDITORIA_SEGUNDA.md) | Resolución de N-01–N-05 y control del paquete canónico |

Las issues se preparan aquí por decisión del usuario. Se conservan `DC-001` a `DC-048` y se añaden `DC-049` a `DC-052` sin renumerar. Son referencias locales, no tickets publicados. Las subtareas `DC-NNN-A/B/C` heredan el hito del padre. Al importarlas, conservar referencias y resolver dependencias a los números reales; no contar padres y subtareas como esfuerzo adicional duplicado.

## Qué significa terminar

R1 entrega el primer núcleo utilizable con actualización/rollback básicos y ciclo de instalación/recuperación en tres agentes. R2 añade inteligencia y mantenimiento básico de memoria sin grafo ni IA; R3 incorpora grafo esencial y obsolescencia. R4 completa KEE con etapas persistentes, gobernanza, tres presupuestos y adaptadores externos opcionales. R5 mejora aprendizaje y revisión. R6 amplía distribución y valida sustitución mediante piloto. Ninguna puerta exige contratar IA.

El producto inicial completo termina cuando los tres agentes funcionan de forma estable, los flujos reales cubiertos pueden ejecutarse sin las herramientas originales, los fallos parciales no inutilizan el resto y se demuestran recuperación, mejora medible y respeto de permisos. Ver las puertas de salida del roadmap; implementar todas las issues por sí solo no demuestra ese resultado.

Bench es una capacidad permanente desde R1: ejecutar suites, comparar y consultar historia. Calidad antes que rendimiento; cada release pasa su gate aplicable. El piloto mide además minutos manuales y ciclos/eventos operativos definidos en R0. Las herramientas se sustituyen por flujo validado, sin exigir ganar todas las métricas ni retirar todas a la vez.

## Convenciones

- `P0`: bloquea la seguridad, integridad o puerta de salida del hito. `P1`: capacidad comprometida del hito. `P2`: experimento opcional, condicionado a evidencia.
- Tamaño orientativo: `S` = un cambio acotado; `M` = varios cambios relacionados; `L` = contenedor ya dividido en INCREMENTOS.md, nunca una sola asignación/PR. No representa días ni un calendario.
- Estado inicial: `propuesta`, sin trabajo ejecutado. El usuario autoriza el alcance R0; las decisiones técnicas permanecen pendientes hasta obtener evidencia. Dependencias expresan orden de entrega, no obligación de configurar proveedores opcionales.
- Una issue pasa a preparada cuando sus decisiones bloqueantes están resueltas, sus entradas existen y puede verificarse su aceptación.
- Cerrar con evidencia ejecutada: comando o escenario, versiones y entorno, resultado y referencia al artefacto. Una inspección de código no sustituye una prueba de comportamiento.
- Compatibilidad de proveedor: `contract_tested` solo dobles; `integration_verified` API real; `production_ready` operación/seguridad/recuperación. Solo el último permite anunciar soporte productivo pleno; no confundir madurez con proveedor configurado o listo.

## Límites del plan

La carpeta contiene los dos documentos fuente; no se ha encontrado implementación ni repositorio Git. No hay estimación de velocidad, equipo o fecha de entrega. No se han verificado aún las APIs, versiones o licencias de proveedores: esa investigación es trabajo explícito de R0. Las cifras orientativas del TOML de la especificación no se convierten automáticamente en requisitos de rendimiento o gasto.

No se configura memoria externa ni se guarda esta planificación en agentmemory. El proyecto aún no declara un slug canónico; cualquier futura escritura de memoria requiere resolverlo explícitamente y utilizar REST con scope.

Para compartir, conservar las rutas del manifiesto y su jerarquía, incluyendo la especificación maestra v0.3.0. Copias como `README(1).md` o `NEXUM_ESPECIFICACION_MAESTRA.md` no forman parte de este conjunto. Un paquete anterior no se certifica por compartir nombres: hay que contrastar inventario, versiones, hashes y enlaces. Cambios intencionales requieren nueva revisión del manifiesto; no se recalculan hashes silenciosamente para validar una copia ajena.
