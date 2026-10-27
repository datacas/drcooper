# Segunda auditoría — resolución documental

Fecha: 2026-10-26. Veredicto aportado: **GO para R0**, desarrollo posterior condicionado a ADR bloqueantes. Instrucción actual: **aún no programar**. Esta entrega actualiza documentos y comprueba su integridad; no ejecuta prototipos, benchmarks de producto ni discovery técnico.

## Estado y alcance conservado

Se mantienen 52 issues padre y 69 incrementos en 23 contenedores L. No se añade fase de planificación ni issue padre para Bench. DC-049 conserva su función de recuperación básica. El contrato Bench se integra en DC-002/005 y su primera implementación se asigna a DC-010/013/016, con ampliación en las validaciones de módulos existentes.

## Resolución de N-01 a N-05

| Hallazgo | Corrección incorporada | Evidencia/criterio pendiente de producto |
|---|---|---|
| N-01 Paquete con especificación y enlaces ambiguos | Conjunto DC-DOCSET-0.3.0; especificación maestra v0.3.0 y documentos canónicos con rutas, versiones de conjunto, SHA-256 y tamaño en DOCUMENTOS_CANONICOS.json. README explica exportación. DC-007 incorpora validación documental CI | Ejecutar en CI futura comprobación de inventario, hashes, enlaces y revisiones. No se certifican los adjuntos anteriores del auditor por su nombre |
| N-02 Benchmarking sin contrato público | BENCHMARKS.md y especificación §17.1–17.3: run/compare/report, manifiestos, calidad previa, regresiones por release e historial; baseline portable antes de retirar comparadores | DC-016 entrega runner y gate CI; DC-025/030/038/041 amplían suites, DC-043/044/047 exigen evidencia por candidata y DC-048 decide sustitución por flujo |
| N-03 Simulado frente a real | Tres niveles explícitos por proveedor/versión/operación: contract_tested, integration_verified, production_ready; separados de disponibilidad | R4 con dobles no integra JEV real. DC-042 decide adopción; solo evidencia operativa/seguridad/recuperación acredita production_ready y soporte productivo pleno |
| N-04 Complejidad del residente | ADR-02/DC-004 comparan standalone/shared core; doctor/plan de reparación/lecturas viables sin daemon, conservando locks/permisos | Probar escenarios con core que no arranca en DC-011/016. El criterio no confirma arquitectura ni autoriza escrituras inseguras |
| N-05 Horizonte operativo insuficiente | DC-002 fija periodo, mínimo de ciclos/eventos, intervención manual y separación de benchmark técnico/piloto operativo | DC-048 verifica instalación/actualización, cambios de agentes/LSP, reinicio WSL y fallos provocados además de uso diario; sin cobertura no declarar mejora mensual sostenida |

## Bench sin ampliar el backlog

- DC-002 conserva baseline de RTK, Serena/LSP, Context Mode, AgentMemory, Graphify y Context7 disponibles, con versiones/corpus/condiciones y evidencias. Ausencia no se contabiliza como victoria.
- DC-005 define contratos; DC-010 reserva CLI; DC-013 usa almacén común para runs/historial; DC-016 entrega run/compare/report y CI mínima en R1. Se evita otro daemon o base paralela.
- Oráculos independientes, condiciones equivalentes, orden alternado, repeticiones, caché y variación del modelo impiden atribuciones sesgadas. Recursos incluyen árbol de procesos y tokens identifican método/tokenizer.
- Calidad y fidelidad preceden a rendimiento; cada release compara capacidades comprometidas con baseline aceptado y hash del candidato. Evidencia insuficiente no aprueba una celda obligatoria.
- `ready/keep/not_evaluated` por flujo permite sustitución parcial. Retirar un MCP no elimina un LSP o API aún utilizada por DrCooper. No se desinstala automáticamente.
- JEV/LLM siguen opcionales: contratos probados con dobles no acreditan API real ni soporte productivo. Las cifras ilustrativas no son resultados observados.

## Paquete canónico

El manifiesto se encuentra junto a este archivo y usa rutas relativas a la raíz del proyecto. El ID de conjunto versiona todos los documentos listados, aunque cada uno no tenga encabezado de versión individual. La especificación declara su propia versión 0.3.0; el registro de la primera auditoría conserva referencias históricas a 0.2.0, sin ser la especificación vigente.

Para validar una copia compartida, conservar la jerarquía y cotejar inventario, bytes y hashes antes de resolver enlaces. No aceptar automáticamente archivos con sufijos `(1)` ni reemplazos NEXUM como la misma revisión. El manifiesto no incluye su propio hash para evitar autorreferencia; debe conservarse desde la copia canónica de confianza, no regenerarse para certificar un paquete desconocido. SHA-256 detecta cambios respecto a ese inventario, no prueba autenticidad por sí solo.

Las reglas de CI se planifican en DC-007; no se ha escrito código ni workflow de CI en esta revisión. No se afirma haber validado el paquete anterior que recibió el auditor: su limitación N-01 se resuelve para este conjunto local y sus futuras copias exactas.

## Próximo paso y límite de autorización

R0 sigue siendo el siguiente trabajo: DC-001 → DC-002/DC-003 → DC-004 → DC-005 → DC-052 → DC-006. No se ejecuta en esta entrega. Antes de programar R1 deben existir baseline medido, ADR bloqueantes resueltos y arquitectura probada; los documentos no sustituyen esa evidencia. No se amplía alcance, ni se configura proveedor externo o memoria, ni se declara producto implementado.

## Comprobaciones documentales de esta revisión

Inventario canónico: diez documentos Markdown más el manifiesto, incluido el brief de identidad enlazado como referencia de apoyo. Se conservan 52 IDs padre únicos, 23 contenedores L y 69 subtareas únicas; grafo expandido de 98 asignaciones sin ciclos, referencias ausentes ni dependencias de hitos posteriores. Todas las issues tienen alcance/aceptación y cada contenedor conserva sus tres incrementos.

La validación de entrega contrasta hashes/tamaños del manifiesto con los archivos, versión 0.3.0 de la maestra, enlaces relativos dentro del conjunto y bloques Markdown balanceados. La CI del producto sigue pendiente en DC-007; estas comprobaciones locales no son ejecución de esa CI ni de benchmarks reales.
