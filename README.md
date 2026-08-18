# TermuxSchool

Colección histórica de **aprendizaje, utilidades y experimentos para Termux/Android** creada durante una etapa temprana de DesarrollAMO.

## Estado

**Histórico / educativo.** El repositorio mezcla ejercicios, proyectos terminados, pruebas actuales de aquella etapa y herramientas de diagnóstico. No debe asumirse que todos los scripts siguen siendo compatibles con las versiones actuales de Android/Termux.

## Estructura encontrada

- `scripts/` — utilidades shell/Python;
- `MiPagina/` — experimentos web;
- `NOW/` — trabajo que estaba en curso;
- `PTerminados/` — proyectos terminados de aquella etapa;
- `TermuxHell/` — experimentación adicional;
- `main.sh` — launcher histórico;
- `install-deps.sh` — instalación de dependencias;
- `requirements.txt` — dependencias Python.

## Herramientas de diagnóstico

El repo contiene scripts relacionados con información del sistema, conexiones, archivos, red y análisis local. Deben usarse **únicamente sobre el propio dispositivo, redes propias o entornos donde exista autorización**.

No se considera un toolkit de pentesting auditado ni una garantía de seguridad.

## Uso

Antes de ejecutar scripts antiguos:

```bash
pkg update
```

Revisá el contenido del script y sus dependencias. No ejecutes automáticamente instaladores antiguos como root ni copies comandos privilegiados sin entender qué modifican.

## Relación con DesarrollAMO

TermuxSchool documenta una parte importante del origen del proyecto: construir desde Android, shell y herramientas ligeras. Hoy esa idea continúa en apps y flujos AMO, pero este repositorio se conserva principalmente como **archivo de aprendizaje y experimentación**.

## Seguridad

- no guardar tokens ni claves en scripts;
- no versionar `.env`;
- no ejecutar herramientas sobre sistemas de terceros sin autorización;
- validar cualquier script que solicite root antes de usarlo.

---

**DesarrollAMO** · aprender haciendo, pero dejando claro qué es histórico, experimental y productivo.
