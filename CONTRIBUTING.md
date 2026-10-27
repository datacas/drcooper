# Contribuir

Gracias por el interés en DrCooper.

## Antes de abrir un PR

1. Localiza la issue padre o el incremento en la pestaña **Issues**. Las issues de tamaño `L` se trabajan por incrementos, nunca como un único PR.
2. Comprueba las decisiones bloqueantes y dependencias en [DECISIONES_Y_COBERTURA.md](docs/plan/DECISIONES_Y_COBERTURA.md) y [ROADMAP.md](docs/plan/ROADMAP.md).
3. Si la issue aún no está preparada, coméntalo en ella antes de escribir código.

## Flujo

- `main` está protegida: **solo se entra mediante pull request**. No hay push directo, force push ni borrado de la rama.
- Crea una rama corta y descriptiva, por ejemplo `dc-007-base-rust`.
- Un PR debe incluir: qué cambia, qué issue cierra o referencia (`Closes #N`), cómo se ha probado y qué límites quedan.
- La aceptación se demuestra con evidencia ejecutada: comando o escenario, versiones y entorno, resultado y artefacto. Una inspección de código no sustituye una prueba de comportamiento.
- No se anuncia como disponible ninguna capacidad que solo haya pasado dobles o pruebas simuladas; el plan distingue `contract_tested`, `integration_verified` y `production_ready`.

## Documentación canónica

Los documentos de `docs/plan/` forman el conjunto **DC-DOCSET-0.3.0** y están protegidos por hashes en [DOCUMENTOS_CANONICOS.json](docs/plan/DOCUMENTOS_CANONICOS.json). No los edites de forma incidental ni regeneres los hashes para validar una copia: un cambio intencional exige revisión del manifiesto y de la versión del conjunto.
