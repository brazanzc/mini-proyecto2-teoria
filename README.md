
# 🧪 Generador de Casos de Prueba a partir de Gramáticas

### *Proyecto – Grupo 3*

Este proyecto es una herramienta gráfica desarrollada en **Python + Tkinter** que permite generar automáticamente **casos de prueba válidos, inválidos y extremos** basados en una gramática libre de contexto definida en un archivo `.txt`.

Su objetivo principal es apoyar procesos de **testing**, **validación sintáctica** y **verificación de parsers**.

---

## 🚀 Características principales

✔ **Carga de gramáticas** desde archivos de texto
✔ **Generación automática de cadenas**:

* 🟢 *Válidas* (derivaciones correctas)
* 🔴 *Inválidas* (mutaciones sintácticas)
* 🔵 *Extremas* (máxima profundidad, casos largos o recursivos)
  ✔ **Interfaz gráfica intuitiva (Tkinter)**
  ✔ **Exportación de resultados a JSON**
  ✔ **Vista previa de ejemplos generados**
  ✔ **Configuración de número total de casos**

---

## 📂 Formato del archivo de gramática

El archivo `.txt` debe contener reglas en el formato:

```
E -> E + T | T
T -> T * F | F
F -> ( E ) | num
```

Cada producción usa `->` y las alternativas se separan con `|`.
La primera regla del archivo se toma como **símbolo inicial**.

---

## 🖥️ Interfaz de usuario

La aplicación incluye:

* **Botón para cargar gramática `.txt`**
* **Campo para elegir la cantidad total de casos**
* **Generación automática con porcentajes predeterminados:**

  * 60% válidos
  * 25% inválidos
  * 15% extremos
* **Visualización de los primeros casos generados**
* **Exportación del conjunto completo a JSON**

---

## 🔧 Instalación y ejecución

### 1️⃣ Requisitos

Asegúrate de tener Python 3 instalado.

### 2️⃣ Instalar dependencias (opcional)

La app usa solo librerías estándar de Python:

* `tkinter`
* `json`
* `random`

No necesitas instalar nada adicional.

### 3️⃣ Ejecutar el programa


python app.py


## 📘 Estructura del proyecto

```
├─ app.py               # Código principal con interfaz y generador
├─ gramaticas/          # Carpeta opcional para guardar tus gramáticas
└─ README.md            # Este documento
```

---

## 🧠 Funcionamiento interno

### Generación de casos válidos

Se realiza una derivación aleatoria desde el símbolo inicial, limitando la profundidad para evitar recursiones infinitas.

### Generación de casos inválidos

A partir de un caso válido se aplican mutaciones como:

* Duplicar operadores (`+ +`)
* Quitar paréntesis
* Insertar tokens basura (`@`)

### Generación de casos extremos

Se fuerzan reglas largas o recursivas para lograr cadenas profundas y más complejas.

---

## 📤 Exportación a JSON

Los casos se exportan con metadatos como:

```json
{
    "tipo": "valido",
    "cadena": "num + num * num",
    "longitud": 5
}
```

---




---

Si quieres, también puedo generarte una versión en **Markdown con emojis**, o un **README estilo profesional para GitHub con badges, screenshots e instalación extendida**.
