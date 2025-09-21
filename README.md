# Medicontrol

Sistema de gestión farmacéutica desarrollado en Python con PyQt5 para la administración integral de inventarios de medicamentos, fármacos y laboratorios.

## Características

- **Gestión de Fármacos**: Administra catálogo de principios activos
- **Control de Laboratorios**: Mantén información de proveedores
- **Inventario de Medicamentos**: Control completo de stock, precios y vencimientos
- **Interfaz Intuitiva**: Navegación simple con operaciones CRUD
- **Base de Datos Local**: SQLite integrado para portabilidad

## Tecnologías

- **Python 3.x**
- **PyQt5** - Interfaz gráfica
- **SQLite** - Base de datos
- **Patrón MVC** - Arquitectura

## Instalación

Guía de Instalación

1. Clona el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd medicontrol
```

2. Crea y activa un entorno virtual (recomendado)

**En Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**En Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instala las dependencias

```bash
pip install -r requirements.txt
```

4. Ejecuta la aplicación

```bash
python -m main
```

---

**Notas:**
- Si usas Visual Studio Code, selecciona el intérprete de Python del entorno virtual (`venv`).
- Si tienes problemas con permisos, ejecuta la terminal como administrador.
