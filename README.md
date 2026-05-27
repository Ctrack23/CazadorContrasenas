# 🔐 Cazador de Contraseñas

Juego interactivo de consola desarrollado en Python con **Programación Orientada a Objetos**. El jugador genera contraseñas aleatorias para abrir cofres y acumular puntos, enfrentando penalizaciones cuando las contraseñas no cumplen los requisitos.

---

## 🎮 ¿Cómo funciona el juego?

1. El jugador elige la longitud de la contraseña (mínimo 8 caracteres).
2. El sistema genera una contraseña completamente aleatoria.
3. Si la contraseña es **válida** → se abre un cofre aleatorio y se suman puntos.
4. Si la contraseña es **inválida** → se abre un cofre maldito y se restan puntos.
5. El jugador decide si continuar o salir.

---

## 🧩 Estructura del proyecto

```
cazador-contrasenas/
│
├── cazador_contrasenas.py   # Código fuente principal
└── README.md                # Este archivo
```

---

## 🏗️ Arquitectura — Programación Orientada a Objetos

El proyecto aplica los cuatro pilares de la POO:

### Clases principales

| Clase | Responsabilidad |
|---|---|
| `Contrasena` | Genera y valida contraseñas aleatorias |
| `Cofre` | Clase base que representa un cofre |
| `CofreComun` | Hereda de `Cofre` — otorga **+10 puntos** |
| `CofreRaro` | Hereda de `Cofre` — otorga **+25 puntos** |
| `CofreLegendario` | Hereda de `Cofre` — otorga **+50 puntos** |
| `CofreMaldito` | Hereda de `Cofre` — penaliza **-20 puntos** |
| `JuegoCazador` | Administra el flujo del juego y el puntaje |

### Excepciones personalizadas

| Excepción | Cuándo se lanza |
|---|---|
| `LongitudInvalidaError` | Longitud menor a 8 caracteres |
| `EntradaNoNumericaError` | El usuario ingresa texto en vez de número |
| `ContrasenaInvalidaError` | La contraseña generada no cumple los requisitos |

### Pilares POO aplicados

- **Encapsulamiento** — métodos internos con prefijo `_` (`_generar`, `_eliminar_repetidos`)
- **Herencia** — `CofreComun`, `CofreRaro`, `CofreLegendario` y `CofreMaldito` heredan de `Cofre`
- **Polimorfismo** — cada subclase sobreescribe el método `abrir()` con su propio comportamiento
- **Abstracción** — `Cofre` define la estructura general; los detalles están en las subclases

---

## ✅ Requisitos de una contraseña válida

- Longitud mínima de **8 caracteres** (definida por el usuario)
- Al menos **una letra mayúscula**
- Al menos **una letra minúscula**
- Al menos **un número**
- Al menos **un carácter especial** de: `¿¡?=)(/¨*+-%&$#!`
- **Sin caracteres repetidos**

---

## 🎲 Tipos de cofre

| Cofre | Puntos | Probabilidad |
|---|---|---|
| 🪵 Común | +10 | 50% |
| 💎 Raro | +25 | 30% |
| 🏆 Legendario | +50 | 20% |
| 💀 Maldito | -20 | Al fallar la contraseña |

---

## 🚀 Instalación y uso

### Requisitos

- Python 3.10 o superior
- No requiere librerías externas (solo módulos estándar: `random`, `string`)

### Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/cazador-contrasenas.git
cd cazador-contrasenas
```

### Ejecutar el juego

```bash
python cazador_contrasenas.py
```

### Ejemplo de una partida

```
════════════════════════════════════════════════════════════
   ⚔️   CAZADOR DE CONTRASEÑAS   ⚔️
════════════════════════════════════════════════════════════

  ¿Cómo te llamas, Cazador? Ana
  ¡Bienvenido, Ana! Que los cofres te favorezcan.

  🎲 RONDA 1
  Ingresa la longitud de la contraseña (mín. 8): 12

  🔑 Contraseña generada: R7¿kWpZ#mQeN

  ✅ ¡Contraseña VÁLIDA!

  🔓 ¡Cofre Legendario abierto!
  ¡Un cofre de oro puro! La leyenda es tuya.
  Puntos: +50
  🏆 ¡El brillo del oro ilumina toda la sala!

  ⭐ Puntaje actualizado: 50 pts
```

---

## 📚 Conceptos académicos demostrados

Este proyecto fue desarrollado como actividad académica para demostrar el dominio de:

- Definición e instanciación de clases y objetos
- Herencia simple y uso de `super()`
- Polimorfismo mediante sobreescritura de métodos
- Encapsulamiento con atributos y métodos privados
- Manejo de excepciones con clases personalizadas (`raise`, `try/except`)
- Principio de aleatoriedad controlada con el módulo `random`

---

## 👤 Autor

Desarrollado por Camilo Nuñez Garzon
Materia: Programación Orientada a Objetos 
Institución: UNAD
