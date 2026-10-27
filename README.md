# DrCooper

**Tu segundo cerebro para el código.**

DrCooper es un motor local de inteligencia para agentes de programación —Codex, Claude Code y OpenCode— que unifica navegación semántica, ejecución y contexto, memoria persistente, grafo de código, documentación y evolución del conocimiento. LLM y JEV son opcionales e independientes: el núcleo funciona sin ellos.

> **Estado:** planificación. Este repositorio contiene la especificación y el plan de producto; todavía no hay implementación. La ejecución autorizada empieza por R0 (discovery), no por código.

## Documentación

El conjunto canónico es **DC-DOCSET-0.3.0**, fechado el 2026-10-26. Se publica byte a byte, con sus hashes SHA-256 originales.

| Documento | Contenido |
|---|---|
| [Plan de producto](docs/plan/README.md) | Punto de entrada, convenciones y límites |
| [Especificación maestra](drcooper_ESPECIFICACION_MAESTRA.md) | Producto, arquitectura, contratos y criterios |
| [Roadmap](docs/plan/ROADMAP.md) | Entregas R0–R6 y puertas de salida |
| [Backlog](docs/plan/ISSUES.md) | 52 issues padre con aceptación verificable |
| [Incrementos](docs/plan/INCREMENTOS.md) | 69 subtareas de las 23 issues L |
| [Decisiones y cobertura](docs/plan/DECISIONES_Y_COBERTURA.md) | ADR pendientes y trazabilidad |
| [DrCooper Bench](docs/plan/BENCHMARKS.md) | Contrato run / compare / report |
| [Auditorías](docs/plan/AUDITORIA_CAMBIOS.md) | Primera revisión y [segunda](docs/plan/AUDITORIA_SEGUNDA.md) |
| [Brief de identidad](brief_identidad.md) | Mascota y dirección visual |
| [Manifiesto](docs/plan/DOCUMENTOS_CANONICOS.json) | Inventario, versiones, tamaños y hashes |

## Backlog en GitHub

Las 52 issues padre y sus 69 incrementos están publicados en la pestaña **Issues**, agrupados por milestones `R0`–`R6` y etiquetados por área, prioridad y tamaño. Los incrementos son sub-issues del padre y cada uno puede tener su propio PR. Las dependencias del plan apuntan a los números reales de GitHub.

## Cómo se trabaja aquí

`main` está protegida: **todos los cambios entran mediante pull request**. No se permite push directo, force push ni borrado de la rama. Un PR debe describir el cambio, enlazar la issue correspondiente y aportar la evidencia de aceptación definida en el plan.

Antes de implementar una issue, comprueba sus decisiones bloqueantes y dependencias en [DECISIONES_Y_COBERTURA.md](docs/plan/DECISIONES_Y_COBERTURA.md) y [ROADMAP.md](docs/plan/ROADMAP.md). Las issues L no se abordan como un único PR: se asignan por incrementos.

## Nota de publicación

Los documentos conservan el estado y las afirmaciones de su revisión del 2026-10-26 (por ejemplo, «no hay repositorio remoto» o «ninguna issue está publicada»). El conjunto se mantiene intacto para que el manifiesto y sus hashes sigan siendo verificables. La publicación del repositorio y del backlog es posterior y no altera el contenido canónico.

## Licencia

[MIT](LICENSE). Puedes usar, modificar y distribuir el proyecto; se agradece la mención.
