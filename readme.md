# Gamma Lab 2.0

Aplicación de escritorio para Windows que sirve para cargar, preprocesar y analizar señales electrofisiológicas. Trabaja con archivos `.abf`, `.edf` y `.mat`, y guarda el trabajo en proyectos `.glab`.

Está hecha en Python con PyQt5 y VTK, y se organiza en plugins: cada análisis es un módulo independiente que la aplicación carga al iniciar.

---

## Funcionalidades

| Categoría | Plugins |
|---|---|
| Entrada | Open Signal (`.abf`, `.edf`, `.mat`, incluido `.mat` v7.3) |
| Preprocesamiento | Filter, Remove Artifact, Trials |
| Análisis en el tiempo | Average, Event Related Potential |
| Análisis en frecuencia | FFT, FFT Average, PSD, PSD Average, Relative PSD |
| Tiempo y frecuencia | Wavelet, Wavelet Average, PAC, PPC, Modulation Index |
| Mediciones | Amplitude, Difference, Slope |
| Ayuda | Help (manual de usuario en PDF) |

Los resultados pueden exportarse a Excel e imagen desde la propia aplicación.

---

## 1. Instalar Gamma Lab (usuarios)

Es la forma recomendada y **no requiere Python**.

1. Descarga el instalador `GammaLab-Setup-2.0.0.exe` desde la [página de Gamma Lab](https://garzonlj.github.io/webGammaLab/).
2. Haz doble clic y acepta el aviso de administrador.
3. Sigue los pasos del asistente. Hay una casilla para crear un acceso directo en el escritorio.
4. Abre Gamma Lab desde el menú Inicio, o haz doble clic sobre cualquier archivo `.glab`.

**Requisitos:** Windows 10 u 11 de 64 bits, unos 700 MB libres y permisos de administrador solo para instalar.

En esa misma página, https://garzonlj.github.io/webGammaLab/, hay una guía paso a paso con capturas.

### Avisos de Windows
El instalador no está firmado digitalmente, por lo que Windows puede mostrar *"Windows protegió su PC"*. Elige *Más información* y luego *Ejecutar de todas formas*. Algunos antivirus también pueden retrasarlo o pedir confirmación.

### Actualizar y desinstalar
- **Actualizar:** ejecuta el instalador nuevo sin desinstalar el anterior. Se conservan los ajustes.
- **Desinstalar:** *Configuración, Aplicaciones, Gamma Lab, Desinstalar*.

### Archivos del usuario
Los ajustes y el registro de errores (`gamma_lab.log`) quedan en `%APPDATA%\GammaLab`. Si el programa no arranca, revisa ese registro.

---

## 2. Ejecutar desde el código fuente (desarrollo)

Requiere **Python 3.11 o superior** (el desarrollo y el instalador se hacen con Python 3.12), de 64 bits y agregado al `PATH`.

### Con el lanzador
Haz doble clic en [gamma_lab.bat](gamma_lab.bat). El script:

1. Comprueba que haya Python 3.11 o superior.
2. Instala o actualiza las dependencias de [requirements.txt](requirements.txt).
3. Abre la aplicación con `main.py`.

Para tener un acceso directo en el escritorio que apunte a este lanzador, ejecuta [create_shortcut.bat](create_shortcut.bat).

### Manualmente
Desde la raíz del proyecto:

```bash
python -m pip install -r requirements.txt
python main.py
```

También se puede abrir un proyecto directamente:

```bash
python main.py "ruta\al\proyecto.glab"
```

### Pruebas

```bash
python -m pytest test -q
```

Las pruebas usan las señales de [test/data](test/data). Algunas señales de doble canal pesan demasiado para GitHub y se comparten por fuera del repositorio (ver `.gitignore`).

---

## 3. Generar el instalador

Se necesita, además de las dependencias del proyecto, PyInstaller e Inno Setup 6:

```bash
python -m pip install pyinstaller
winget install -e --id JRSoftware.InnoSetup
```

Luego:

1. Sube el número de versión en [installer/gamma_lab.iss](installer/gamma_lab.iss) (`#define VersionApp`). No cambies el `AppId`.
2. Cierra Gamma Lab si está abierto.
3. Ejecuta [installer/construir.bat](installer/construir.bat).

El script congela la aplicación con PyInstaller, prueba el ejecutable resultante y lo empaqueta con Inno Setup. Tarda entre 6 y 8 minutos. El instalador queda en `installer\salida\GammaLab-Setup-X.Y.Z.exe`.

Las carpetas `installer\build`, `installer\dist` y `installer\salida` se regeneran y no se suben a git. El instalador (más de 200 MB) tampoco se sube al repositorio: se comparte por enlace o como adjunto de una *release*.

La guía completa, con solución de problemas y la lista de comprobación antes de entregar, está en [installer/INSTRUCTIVO.md](installer/INSTRUCTIVO.md).

---

## Estructura del proyecto

```
main.py                 Punto de entrada
app/view/               Ventana principal, explorador de proyectos y pantalla de inicio
core/
  kernel.py             Núcleo de la aplicación
  model/                Modelos de datos (señales y trials)
  services/             Proyectos, lectura de archivos, exportación, mediciones, tareas, ajustes
  plugins/              Carga y gestión de plugins
  filters/              Filtros y cálculos de señal
  utils/                Utilidades de interfaz, VTK, exportación y rutas
plugins/                Un plugin por carpeta, cada uno con su properties.yml
assets/                 Íconos, fuentes, logos y hoja de estilos
installer/              Todo lo necesario para generar el instalador
test/                   Pruebas automáticas y datos de prueba
docs/                   Documentación del proyecto (SRS, SAD, SDD, manual de usuario, pruebas)
web/instructivo/        Página con la guía de instalación (publicada en garzonlj.github.io/webGammaLab)
```

### Agregar un plugin
Crea una carpeta dentro de `plugins/` con su `properties.yml`, su lógica y su interfaz, siguiendo la estructura de los plugins existentes. La aplicación lo detecta al iniciar, y `installer/gamma_lab.spec` incluye automáticamente sus dependencias al generar el instalador.

---

## Documentación

- Manual de usuario: [docs/MU/main.pdf](docs/MU/main.pdf) (también accesible desde el plugin Help)
- Requerimientos (SRS): [docs/SRS/main.pdf](docs/SRS/main.pdf)
- Arquitectura (SAD): [docs/SAD/main.pdf](docs/SAD/main.pdf)
- Diseño (SDD): [docs/SDD/main.pdf](docs/SDD/main.pdf)
- Reportes de pruebas: [docs/tests documents](docs/tests%20documents)
