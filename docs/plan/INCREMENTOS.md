# Incrementos revisables de las issues L

Los 23 contenedores L de [ISSUES.md](ISSUES.md) se dividen en 69 subtareas. No son 69 capacidades adicionales: concretan el mismo alcance. Ningún contenedor L se asigna como un único PR.

Cada fila es una subtarea propuesta de tamaño S/M, con resultado y aceptación propios. Hereda hito, prioridad, fuente, seguridad y dependencias externas del padre. Dentro de cada padre: A precede a B y B a C; el padre solo cierra al completar los tres incrementos y todos sus criterios de aceptación. Las condiciones del padre prevalecen si son más estrictas. Si una fila todavía excede un cambio revisable al conocer el código, se subdivide antes de asignarla; no se abandona su aceptación.

Los incrementos prueban un flujo pequeño de extremo a extremo o un escenario de recuperación completo; no se exige terminar la arquitectura de todas las capas antes de demostrar valor. Donde hay edición, ejecución sensible o envío externo, el incremento permanece en preview/dry-run o usa dobles hasta que todos sus controles estén integrados. Una dependencia de adaptador nunca exige contratarlo.

## R1

| Subtarea | Resultado acotado | Aceptación y evidencia propia |
|---|---|---|
| DC-008-A | Registrar proyecto persistido y consultar identidad resuelta | Registrar/reabrir y mover checkout conserva ID; contexto ambiguo rechaza escritura |
| DC-008-B | Abrir sesiones de dos worktrees sobre un proyecto | CLI consulta sesiones distintas con conocimiento canónico compartido, sin heredar cwd |
| DC-008-C | Probar ownership con dos agentes concurrentes | Alias conflictivo y symlink no permiten escribir en otro scope; registrar resultados de cada cliente |
| DC-009-A | Guardar y reabrir un registro scoped en SQLite | Reinicio conserva ID/contenido; cuota y segunda escritura idempotente comprobadas |
| DC-009-B | Migrar esquema con snapshot verificable | Fallo inducido restaura snapshot compatible y se contrasta contenido, no solo exit code |
| DC-009-C | Recuperar ante contención/corrupción con plan explícito | Busy timeout acotado y restauración ejecutada; sin reparación destructiva automática |
| DC-010-A | Ejecutar lectura por CLI/MCP y reservar interfaces Bench | Mismo resultado/correlación/esquema; stdout solo protocolo; Bench no se anuncia ejecutable hasta DC-016 |
| DC-010-B | Reconectar puente al core preservando identidad | Reiniciar core con dos sesiones no duplica procesos/IDs; documentar transporte que requiere reconectar |
| DC-010-C | Resolver operación interrumpida y exponer capacidades con madurez | Respuesta perdida se resuelve sin replay ciego; cancelación trazable; contrato simulado no se anuncia productivo |
| DC-012-A | Ejecutar comando autorizado con resultado íntegro | Comando/cwd/stdout/stderr/exit/duración recuperables; comando denegado nunca se ejecuta |
| DC-012-B | Cancelar/limitar comando con descendientes | Timeout termina árbol conforme a política; límites se declaran, sin éxito falso |
| DC-012-C | Validar niveles de aislamiento anunciados | Pruebas de disco/red/symlink acreditan restricciones; plataforma sin sandbox restringe capacidad |
| DC-013-A | Recuperar salida por ID y scope | Bytes raw coinciden durante retención; otro scope no puede recuperar el artefacto |
| DC-013-B | Entregar filtro y expansión de Git/tests | Fixtures mantienen fallos/exit code y expanden detalle sin recapturar salida |
| DC-013-C | Buscar chunks/lotes e indexar historial Bench en el almacén común | FTS/scope y resultados individuales correctos; runs/manifiestos exportables con hash, cuota/retención y validación sin ejecutar contenido |
| DC-014-A | Guardar y recuperar una decisión con fuentes | Scope obligatorio; datos prohibidos rechazados; recall compacto devuelve evidencia expandible |
| DC-014-B | Crear revisión por topic sin destruir original | Dos agentes guardan misma decisión sin duplicado exacto; nueva revisión conserva historial |
| DC-014-C | Verificar estados, privacidad y recuperación archivada | Buscar/expandir fuentes y archivados autorizados funciona; memoria no se interpreta como permiso o instrucción superior |
| DC-015-A | Configurar y revertir Codex | Setup repetido conserva configuración ajena; flujo ejecución/artefacto/memoria completado en versión registrada |
| DC-015-B | Configurar y revertir Claude Code | Mismo flujo y reversión; hook disponible falla sin bloquear trabajo nativo salvo control obligatorio |
| DC-015-C | Configurar y revertir OpenCode y contrastar clientes | Flujo por cliente, backup recuperable y límites de hooks documentados; entrada lista para DC-050 |

## R2

| Subtarea | Resultado acotado | Aceptación y evidencia propia |
|---|---|---|
| DC-017-A | Abrir documento con un LSP configurado y leer capacidades | JSON-RPC, sincronización y diagnóstico contrastados; versión/capacidades en doctor |
| DC-017-B | Instalar/actualizar un proveedor gestionado con rollback | Pin, licencia e integridad verificados; fallo de staging conserva proveedor y configuración anterior |
| DC-017-C | Recuperar crash LSP en dos worktrees | Cancelación/reinicio no mezclan estado ni muestran diagnósticos obsoletos; memoria/ejecución siguen |
| DC-018-A | Indexar símbolos AST de un archivo por lenguaje objetivo | Rangos, hash y procedencia contrastados en fixtures; sintaxis no soportada marca parcial |
| DC-018-B | Actualizar índice tras editar/mover/borrar | No quedan símbolos de revisión antigua; segunda indexación no duplica resultados |
| DC-018-C | Aislar worktrees e invalidar configuración/dependencias | Corpus mide incrementalidad y consumo; invalidate conservador sin atribuir semántica al AST |
| DC-023-A | Generar preview de rename con referencias | Diff/archivos/cobertura visibles; ningún archivo se modifica |
| DC-023-B | Aplicar rename autorizado con base vigente | Hash cambiado invalida plan y symlink externo se rechaza; checks de lenguaje comprueban caso permitido |
| DC-023-C | Añadir inserción/sustitución y recuperar fallo parcial | Fallo inducido recupera estado previo; cobertura insuficiente y errores previos quedan explícitos |
| DC-024-A | Resolver versión y buscar documentación local fiable | Lockfile/versión ambigua y fuente obsoleta se declaran; código propio no produce egress |
| DC-024-B | Consultar proveedor autorizado y fallback oficial | Contrato viable verificado; caída Context7 usa alternativa con versión/fuente/caché, sin inventar soporte |
| DC-024-C | Resolver consulta offline y discrepancia reproducible | Caché no se presenta como actual; discrepancia docs/ejecución conserva ambas evidencias y límites |

## R3

| Subtarea | Resultado acotado | Aceptación y evidencia propia |
|---|---|---|
| DC-026-A | Persistir grafo esencial fichero/símbolo/memoria | Relaciones `contains`, `imports`, `references`, `relates_to_memory` con evidencia; no se anuncia `calls` sin cobertura |
| DC-026-B | Reconciliar aristas tras cambio/borrado de archivo | Dos worktrees/revisiones no se mezclan; repetición no duplica; fallo grafo no bloquea memoria |
| DC-026-C | Demostrar utilidad antes de ampliar tipos | Consulta de impacto medida contra corpus y baseline; extensión solo con ganancia registrada y compatibilidad de esquema |

## R4

| Subtarea | Resultado acotado | Aceptación y evidencia propia |
|---|---|---|
| DC-031-A | Reanudar las tres etapas desde SQLite | Discover no muta canónico; reinicio conserva candidatos y resultados de Verify sin redescubrir |
| DC-031-B | Lanzar lote local solo bajo inactividad válida | Trabajo activo, presión CPU/RAM/IO y locks impiden arrancar; segundo scheduler no toma mismo lease |
| DC-031-C | Pausar/reanudar lote por interacción o caída | Checkpoints conservan transacciones; core ausente no anuncia trabajo activo; stats explica cola/pausa |
| DC-033-A | Probar adaptador generativo opcional contra contrato | Doble devuelve JSON con evidencias; esquema/IDs inválidos rechazados; sin proveedor síntesis no disponible |
| DC-033-B | Añadir clasificación cerrada y manejo de fallo | Opciones/abstención compatibles con DC-052; timeout/rate limit mantienen pendiente sin duplicar Commit |
| DC-033-C | Integrar controles y evaluar síntesis con linaje/madurez | Solo con DC-034/035 hay egress; corpus mide pérdida semántica; doble/API real/validación operativa acreditan niveles distintos |
| DC-034-A | Autorizar y revocar egress por proveedor/proyecto | Sin consentimiento no sale payload; habilitar LLM no habilita JEV ni otro proyecto |
| DC-034-B | Previsualizar/redactar payload y reservar volumen | Deny paths, datos clínicos/secretos sintéticos y cuota impiden envíos indebidos, incluso por fragmentación |
| DC-034-C | Ejecutar suite de exfiltración e inyección | Instrucciones en logs/memoria/docs no cambian política; contenido incierto omite llamada; claves ausentes en registros |
| DC-036-A | Evaluar niveles de autonomía con dry-run | L0/L1/L2/L3 reciben destino correcto; score IA nunca autoriza acción sensible |
| DC-036-B | Listar propuesta y registrar aprobación/rechazo | Diff/evidencias/scope visibles; aprobación global exige confirmación adicional; base obsoleta invalida decisión |
| DC-036-C | Integrar gate de aplicación y bandeja mínima | Antes de DC-037 no aplica; fingerprint, cuota, agrupación y caducidad limitan ruido sin saltar permisos |
| DC-037-A | Registrar plan de lote con inversa y fuentes | Dry-run no muta; versión/modelo/reglas/coste y base quedan trazados; originales preservados |
| DC-037-B | Aplicar lote validado con fallo/reintento inyectado | Gate L0–L3 y tres cuotas activos; Commit idempotente; cada checkpoint deja estado consistente |
| DC-037-C | Revertir lote y resolver conflicto posterior | Restauración contrastada con estado previo; cambios posteriores no se pisan; intento remoto incierto queda contabilizado |

## R6

| Subtarea | Resultado acotado | Aceptación y evidencia propia |
|---|---|---|
| DC-043-A | Producir release WSL/Linux verificable con gate Bench | Build/checksums/SBOM/licencias; hash del candidato ligado a informe sin regresiones bloqueantes; nombre validado antes de publicar |
| DC-043-B | Instalar/desinstalar release en entorno limpio | Sin herramientas sustituidas activas salvo proveedores declarados; datos/config ajena sobreviven; DC-050 repetido |
| DC-043-C | Publicar matriz de plataformas probadas | Windows nativo/macOS solo si pasan sus pruebas; incompatibilidades explícitas, no soporte inferido de compilación |
| DC-044-A | Consultar canal remoto autenticado/verificado | Check no instala; metadatos/artefacto manipulados se rechazan; clave de confianza preservada |
| DC-044-B | Aplicar actualización coordinada en plataforma inicial | Reutiliza DC-049; sesiones/locks y binario/schema/API compatibles; fallo restaura combinación funcional |
| DC-044-C | Extender actualización y recuperación a plataformas soportadas | Matriz de fallos por plataforma ejecutada, sin actualización forzosa ni apertura de DB incompatible |
| DC-045-A | Mostrar estado/capacidades y costes por proyecto en TUI | Scope visible; proveedor ausente no aparece como error; navegación por teclado comprobada |
| DC-045-B | Inspeccionar propuesta y aprobar mediante contrato CLI | Mismo diff/evidencias/permisos/confirmaciones; no hay atajo sensible ni secretos expuestos |
| DC-045-C | Usar historial/reversión en terminal limitado | Terminal estrecho/sin color y CLI equivalente probados; identidad no bloquea funciones esenciales |
| DC-046-A | Exportar y previsualizar importación sin escribir | IDs/fuentes/revisiones y pérdidas declaradas; scope faltante se aísla para resolución explícita |
| DC-046-B | Importar con consentimiento e idempotencia | Reimportar no duplica; sensibles excluidos; exportación basta sin servicio original activo |
| DC-046-C | Cancelar/revertir importación con datos preexistentes | Ningún conocimiento anterior se pierde; mapeo canónico y registro de importación auditables |
| DC-047-A | Ejecutar flujos/ciclo de vida por cliente en WSL2 | Tres agentes, setup/reconexión y DC-050 con versiones/artefactos; servicio/operación/transporte separados |
| DC-047-B | Validar capacidades opcionales, madurez y fallos parciales | Cuatro configuraciones con dobles no acreditan API real; solo production_ready se anuncia productivo; fallo proveedor no bloquea locales |
| DC-047-C | Completar plataformas y recuperación de release | Binario/DB y migración restaurados; matriz publicada y regresiones críticas bloqueantes |
| DC-048-A | Preparar piloto técnico/operativo y selección de flujos | Corpus/periodo/umbrales y mínimo de eventos/ciclos de DC-002 explícitos; baseline conservado y plan de vuelta; sin IA obligatoria |
| DC-048-B | Ejecutar piloto y medir utilidad/coste total | Bench histórico y eventos de actualización/WSL/agente/fallos cubiertos; minutos activos separados de espera; mensual observado o extrapolado explícito |
| DC-048-C | Decidir sustitución por flujo con usuario | Seis puntos de §22 contrastados; sin regresiones críticas ni mantenimiento injustificado; gaps generan tareas, no éxito declarado |

## Regla de asignación

Antes de iniciar cada fila, comprobar decisiones bloqueantes del padre y dependencias externas. No es necesario terminar todos los incrementos de todas las áreas antes de probar el primero permitido. La aceptación del padre exige integración final, aunque cada fila tenga su propio PR y evidencia. Todos los incrementos siguen pendientes: este documento no afirma pruebas ejecutadas del producto.
