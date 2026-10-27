# Incorporación de auditoría técnica

Fecha: 2026-10-26. Base: auditoría aportada por el usuario, veredicto «GO WITH CHANGES» y corrección posterior: **JEV y LLM siempre opcionales e independientes**.

Estado: correcciones incorporadas a especificación v0.2.0 y planificación. Este estado describe documentos, no implementación ni controles ejecutados del producto. R0 queda autorizado como alcance; sus decisiones y experimentos siguen pendientes.

Registro histórico de la primera revisión. La especificación vigente del conjunto DC-DOCSET-0.3.0 es v0.3.0; cambios posteriores y validación canónica se trazan en [AUDITORIA_SEGUNDA.md](AUDITORIA_SEGUNDA.md). Los conteos de la validación inferior corresponden a aquella entrega, no al número de documentos de este paquete ampliado.

## Siete correcciones previas al desarrollo

- [x] Adelantar recuperación básica: DC-049 en R1, ampliación de canales y plataformas en DC-044/R6.
- [x] Convertir instalación/recuperación en prueba contractual: DC-050, obligatoria antes de DC-016/R1 y repetida por entrega.
- [x] Persistir Discover → Verify → Commit/Propose: especificación §10.3, DC-005/051 y ampliación DC-031/037, dentro de SQLite.
- [x] Adelantar mantenimiento sin grafo: DC-051/R2 tras memoria R1, independiente de LSP, grafo y proveedores IA.
- [x] Medir conservación semántica y errores de aprendizaje: DC-002/052, aceptación DC-033/038 y linaje hasta fuentes primarias.
- [x] Contrato común de clasificación reglas/JEV/LLM desde R0: DC-052; JEV sigue siendo integración opcional condicionada a evidencia en DC-042.
- [x] Dividir issues L: 23 contenedores y 69 subtareas concretas en [INCREMENTOS.md](INCREMENTOS.md), sin sumar doble esfuerzo ni asignar un contenedor como PR único.

## Resolución de hallazgos

| Hallazgo | Cambio documental | Evidencia futura que permite cerrarlo técnicamente |
|---|---|---|
| H-01 Fiabilidad demasiado tardía | DC-049/R1 para artefacto local verificado, binario/DB compatibles y rollback; DC-044 solo amplía | Fallos en staging/migración/sustitución y recuperación contrastada en DC-050/016 |
| H-02 Aprendizaje bloqueado por grafo | DC-051/R2 sin grafo; DC-031 depende de memoria estable, no DC-030; señales grafo opcionales | Dedupe/verificación/consolidación estructural offline con reversión antes de completar R3 |
| H-03 Instalación única no contractual | Zero-Maintenance Installation en DC-050, repetida en puertas posteriores | Ciclo limpio de los tres agentes, preservación de datos/config y medición de intervención manual |
| H-04 Core compartido y transporte | ADR-02/DC-004/010 y matriz obligatoria DC-050 | Reinicios de core/puente/cliente, operación ambigua y reconexión comprobados por separado |
| H-05 Descubrir/verificar/aplicar mezclados | Etapas persistentes lógicas con cola/estado/reintentos/lease y fingerprint en SQLite | Caída/proveedor/cuota agotada no pierde candidatos; Commit revalida base y no repite efectos |
| H-06 JEV aislado de evaluación | DC-052/R0 define entradas, clases, abstención, evidencia y métricas comunes | Comparación reproducible de motores disponibles; no requiere tener JEV o LLM contratados |
| H-07 Pérdida semántica no explícita | Corpus de restricciones/excepciones/fechas/decisiones; afirmaciones nuevas y contradicciones introducidas | Umbrales previos, reconstrucción de fuentes y evaluación antes/después; ahorro no basta |
| H-08 Mantenimiento de LSP | DC-017 incluye pin, integridad, staging y rollback de proveedor | Fallo de actualización conserva proveedor/config y núcleo operativo |
| H-09 Grafo excesivo | DC-026 empieza por fichero/símbolo/memoria y relaciones esenciales | Utilidad medida antes de añadir nodos/aristas; no se anuncia `calls` sin cobertura |
| H-10 Crecimiento de memoria | Cuotas por clase/proyecto/total; crecimiento neto y amplificación en DC-009/032/051 | Límite frena derivados o archiva bajo política, sin pérdida silenciosa de esenciales |
| H-11 Egress sensible | DC-034 cubre LLM y cualquier JEV externo; opt-in independiente, preview, exclusión conservadora y volumen | Suite de exfiltración/inyección, revocación de consentimiento y ausencia de envío ambiguo |
| H-12 Fatiga de propuestas | Agrupación/cuota/caducidad desde DC-036; utilidad y tiempo de revisión en DC-040/041 | Rechazos no reaparecen sin evidencia nueva; carga neta de revisión se mide |
| H-13 Issues grandes | 69 subtareas S/M con aceptación propia para 23 padres L | Asignaciones/PR por incremento; aceptación integrada completa antes de cerrar padre |

## Corrección obligatoria sobre JEV y LLM

La frase anterior «LLM remoto con API key desde primer KEE» se sustituye por soporte de adaptadores opcionales desde la primera versión funcional del KEE completo. Configurarlos, disponer de claves o contratar modelos no es requisito del producto, del mantenimiento determinístico ni de las puertas de salida.

| Estado | Conducta obligatoria |
|---|---|
| Sin JEV ni LLM | Local disponible según hito: MCP/CLI, LSP/AST, grafo, ejecución, contexto, memoria, dedupe y mantenimiento determinístico |
| Solo LLM habilitado y listo | Base más funciones generativas/semánticas verificadas; no clasificación JEV anunciada |
| Solo JEV habilitado y listo | Base más opciones cerradas de su API verificada; ninguna síntesis generativa simulada |
| Ambos habilitados y listos | Unión de capacidades verificadas; selección de motor autorizada, no equivalencia supuesta |
| Configurado pero temporalmente caído | Solo dependientes no disponibles; no bloqueo del núcleo, ni fallback engañoso |

La detección y exposición son dinámicas y compatibles con el cliente; indicar reconexión si no puede actualizar capacidades en sesión. Desactivado/no configurado no genera error de salud. CLI/TUI pueden mostrar cómo habilitar una función sin anunciarla ejecutable. Las llamadas externas requieren controles completos, no solo presencia de clave.

DC-033 y DC-042 son soporte de adaptadores, no requisitos de activación. DC-038 verifica la matriz mediante base local y dobles; si se ejecutan integraciones reales, registra proveedor/versión/consentimiento. Una simulación no acredita API real; capacidades sin verificación no se publicitan como integraciones validadas.

## Riesgos transversales adicionales

- **Tres presupuestos:** dinero, recursos locales y volumen de conocimiento exportable. Límites y reservas persistentes evitan elusión por concurrencia, cambio de proveedor o fragmentación.
- **Propagación de errores:** conservar linaje hasta fuentes primarias, detectar ciclos y fijar profundidad máxima antes de derivar. Un derivado no verifica por sí solo otro derivado.
- **Simplicidad operativa:** etapas del KEE son lógicas dentro de SQLite; no se añaden tres servicios. Cada ampliación debe demostrar ganancia frente al coste operativo.

## Siguiente trabajo autorizado

Ejecutar R0 en el orden DC-001 → DC-002/003 → DC-004 → DC-005 → DC-052 → DC-006. Este documento no inicia implementación Rust ni instala proveedores. DC-001 no tiene bloqueos previos; DC-006 exige decisiones y evidencias antes de abrir desarrollo R1. Detalle de bloqueo/criterio por tarea en [ISSUES.md](ISSUES.md) y registro ADR en [DECISIONES_Y_COBERTURA.md](DECISIONES_Y_COBERTURA.md).

## Validación documental ejecutada

Comprobaciones sobre archivos locales mediante context-mode, sin modificar configuración ni instalar paquetes:

- 52 IDs padre únicos y continuos; todas las dependencias existen y el grafo de padres no tiene ciclos.
- 23 padres L con tres subtareas cada uno: 69 IDs únicos. Al sustituir cada padre por sus subtareas y heredar dependencias externas, quedan 98 tareas/incrementos ejecutables sin ciclos ni referencias ausentes.
- Cada padre tiene alcance y aceptación; las 69 subtareas tienen resultado y aceptación propios. Enlaces relativos de los siete documentos revisados resuelven a archivos existentes.
- TOML de especificación parseado con `tomli`, disponible en Python 3.10 del entorno: `ai.llm.enabled = false`, `ai.jev.enabled = false`, evolución y mantenimiento determinístico activos. El primer intento con `tomllib` no fue aplicable a esa versión de Python; la comprobación se completó con `tomli`.
- Bloques de código Markdown balanceados; DC-031 depende de DC-016/DC-051 y no de la finalización del grafo DC-030.

Estas comprobaciones acreditan estructura documental, no viabilidad de APIs, aislamiento, calidad de síntesis, instalación ni recuperación real. Esas evidencias se obtendrán al ejecutar las issues correspondientes.
