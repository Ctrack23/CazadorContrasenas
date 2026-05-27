"""
-------------------------------------------------------------------
         CAZADOR DE CONTRASEÑAS                                 
 Programación Orientada a Objetos | Herencia | Polimorfismo   
 -----------------------------------------------------------------
Autor: Camilo Nuñez Garzon          
Descripción: Juego interactivo donde el usuario genera contraseñas
             aleatorias para abrir cofres y acumular puntos.
"""

import random
import string


# ─────────────────────────────────────────────────────────────────
# EXCEPCIONES
# ─────────────────────────────────────────────────────────────────

class LongitudInvalidaError(Exception):
    """Se lanza cuando la longitud ingresada es menor a 8 o no es un número."""
    pass


class EntradaNoNumericaError(Exception):
    """Se lanza cuando el usuario ingresa un valor que no es numérico."""
    pass


class ContrasenaInvalidaError(Exception):
    """Se lanza cuando la contraseña generada no cumple los requisitos."""
    def __init__(self, mensaje, razones=None):
        super().__init__(mensaje)
        self.razones = razones or []  # lista de razones específicas del fallo


# ─────────────────────────────────────────────────────────────────
# CLASE CONTRASEÑA
# ─────────────────────────────────────────────────────────────────

class Contrasena:
    """
    Clase responsable de generar y validar contraseñas.

    Atributos:
        CARACTERES_ESPECIALES (str): Conjunto de caracteres especiales permitidos.
        longitud (int): Longitud deseada de la contraseña.
        valor (str): La contraseña generada.
    """

    CARACTERES_ESPECIALES = "¿¡?=)(/¨*+-%&$#!"

    def __init__(self, longitud: int):
        """
        Constructor: valida la longitud y genera la contraseña.

        Args:
            longitud (int): Número de caracteres de la contraseña (mínimo 8).

        Raises:
            LongitudInvalidaError: Si la longitud es menor a 8.
        """
        if longitud < 8:
            raise LongitudInvalidaError(
                f"La longitud {longitud} no es válida. Debe ser al menos 8 caracteres."
            )
        self.longitud = longitud
        self.valor = self._generar()

    def _generar(self) -> str:
        """
        Genera una contraseña aleatoria que intenta cumplir los requisitos.

        La estrategia es:
          1. Garantizar al menos 1 carácter de cada tipo obligatorio.
          2. Completar con caracteres aleatorios del pool total.
          3. Mezclar todo de forma aleatoria.
          4. Eliminar duplicados si los hubiera (reemplazando con nuevos).

        Returns:
            str: Contraseña generada aleatoriamente.
        """
        mayusculas   = list(string.ascii_uppercase)
        minusculas   = list(string.ascii_lowercase)
        digitos      = list(string.digits)
        especiales   = list(self.CARACTERES_ESPECIALES)

        # Pool completo de caracteres disponibles
        pool_total = mayusculas + minusculas + digitos + especiales

        # Garantizamos al menos 1 de cada tipo obligatorio
        obligatorios = [
            random.choice(mayusculas),
            random.choice(minusculas),
            random.choice(digitos),
            random.choice(especiales),
        ]

        # Completamos los caracteres restantes del pool total
        restantes = random.choices(pool_total, k=self.longitud - 4)
        candidatos = obligatorios + restantes

        # Mezclamos de forma aleatoria para no revelar el orden
        random.shuffle(candidatos)

        # Eliminamos caracteres repetidos sustituyéndolos
        contrasena = self._eliminar_repetidos(candidatos, pool_total)
        return "".join(contrasena)

    def _eliminar_repetidos(self, candidatos: list, pool: list) -> list:
        """
        Reemplaza caracteres duplicados por caracteres únicos del pool.

        Args:
            candidatos (list): Lista de caracteres candidatos.
            pool (list): Pool de caracteres disponibles.

        Returns:
            list: Lista de caracteres sin duplicados (hasta donde sea posible).
        """
        vistos = set()
        resultado = []

        # Construimos el pool de caracteres que aún no han aparecido
        disponibles = [c for c in pool if c not in vistos]

        for char in candidatos:
            if char not in vistos:
                resultado.append(char)
                vistos.add(char)
            else:
                # Buscamos un reemplazo que no esté en vistos
                disponibles = [c for c in pool if c not in vistos]
                if disponibles:
                    nuevo = random.choice(disponibles)
                    resultado.append(nuevo)
                    vistos.add(nuevo)
                # Si no hay disponibles (pool agotado) simplemente omitimos
                # esto solo ocurriría si longitud > tamaño del pool total

        return resultado

    def validar(self) -> tuple[bool, list]:
        """
        Verifica que la contraseña cumpla todos los requisitos.

        Requisitos:
          - Longitud mínima 8 (ya garantizada en __init__)
          - Al menos 1 mayúscula
          - Al menos 1 minúscula
          - Al menos 1 dígito
          - Al menos 1 carácter especial del listado
          - Sin caracteres repetidos

        Returns:
            tuple[bool, list]: (es_valida, lista_de_razones_de_fallo)
        """
        razones = []

        if not any(c.isupper() for c in self.valor):
            razones.append("Falta al menos una letra MAYÚSCULA.")

        if not any(c.islower() for c in self.valor):
            razones.append("Falta al menos una letra minúscula.")

        if not any(c.isdigit() for c in self.valor):
            razones.append("Falta al menos un número.")

        if not any(c in self.CARACTERES_ESPECIALES for c in self.valor):
            razones.append("Falta al menos un carácter especial.")

        if len(self.valor) != len(set(self.valor)):
            razones.append("Contiene caracteres repetidos.")

        es_valida = len(razones) == 0
        return es_valida, razones

    def __str__(self) -> str:
        return self.valor


# ─────────────────────────────────────────────────────────────────
# CLASE BASE COFRE (abstracción)
# ─────────────────────────────────────────────────────────────────

class Cofre:
    """
    Clase base que representa un cofre del juego.

    Atributos:
        nombre (str): Nombre del tipo de cofre.
        puntos (int): Puntos que otorga (positivo o negativo).
        descripcion (str): Mensaje descriptivo al abrir.
    """

    def __init__(self, nombre: str, puntos: int, descripcion: str):
        self.nombre      = nombre
        self.puntos      = puntos
        self.descripcion = descripcion

    def abrir(self) -> str:
        """
        Simula la apertura del cofre y retorna un mensaje.

        Returns:
            str: Mensaje al abrir el cofre.
        """
        signo = "+" if self.puntos >= 0 else ""
        return (
            f"\n  🔓 ¡Cofre {self.nombre} abierto!\n"
            f"  {self.descripcion}\n"
            f"  Puntos: {signo}{self.puntos}"
        )

    def __str__(self) -> str:
        return f"Cofre {self.nombre} ({self.puntos:+d} pts)"


# ─────────────────────────────────────────────────────────────────
# SUBCLASES DE COFRE (herencia + polimorfismo)
# ─────────────────────────────────────────────────────────────────

class CofreComun(Cofre):
    """Cofre común: recompensa básica. Hereda de Cofre."""

    def __init__(self):
        super().__init__(
            nombre="Común",
            puntos=10,
            descripcion="Un cofre de madera vieja... pero algo es algo."
        )

    def abrir(self) -> str:
        """Polimorfismo: mensaje especializado para cofre común."""
        return super().abrir() + "\n  🪙 Monedas de cobre tintinean en tu bolsa."


class CofreRaro(Cofre):
    """Cofre raro: recompensa intermedia. Hereda de Cofre."""

    def __init__(self):
        super().__init__(
            nombre="Raro",
            puntos=25,
            descripcion="Un cofre tallado con runas... algo valioso reposa aquí."
        )

    def abrir(self) -> str:
        """Polimorfismo: mensaje especializado para cofre raro."""
        return super().abrir() + "\n  💎 Una gema azul destella ante tus ojos."


class CofreLegendario(Cofre):
    """Cofre legendario: mayor recompensa. Hereda de Cofre."""

    def __init__(self):
        super().__init__(
            nombre="Legendario",
            puntos=50,
            descripcion="¡Un cofre de oro puro! La leyenda es tuya."
        )

    def abrir(self) -> str:
        """Polimorfismo: mensaje especializado para cofre legendario."""
        return super().abrir() + "\n  🏆 ¡El brillo del oro ilumina toda la sala!"


class CofreMaldito(Cofre):
    """Cofre maldito: penalización por contraseña inválida. Hereda de Cofre."""

    def __init__(self):
        super().__init__(
            nombre="Maldito",
            puntos=-20,
            descripcion="Una maldición antigua se activa... pierdes puntos."
        )

    def abrir(self) -> str:
        """Polimorfismo: mensaje especializado para cofre maldito."""
        return super().abrir() + "\n  💀 Una sombra oscura te envuelve. ¡Contraseña inválida!"


# ─────────────────────────────────────────────────────────────────
# CLASE JUEGO CAZADOR
# ─────────────────────────────────────────────────────────────────

class JuegoCazador:
    """
    Clase principal que administra el flujo del juego.

    Atributos:
        puntaje (int): Puntaje acumulado del jugador.
        ronda (int): Número de ronda actual.
        nombre_jugador (str): Nombre del cazador.
    """

    # Probabilidades de cada cofre (suma = 100)
    PROBABILIDADES_COFRE = {
        "Común":      50,   # 50%
        "Raro":       30,   # 30%
        "Legendario": 20,   # 20%
    }

    def __init__(self):
        self.puntaje        = 0
        self.ronda          = 0
        self.nombre_jugador = ""

    # ── Métodos de presentación ──────────────────────────────────

    def _mostrar_bienvenida(self):
        """Muestra la pantalla de bienvenida del juego."""
        print("\n" + "═" * 60)
        print("   ⚔️   CAZADOR DE CONTRASEÑAS   ⚔️")
        print("═" * 60)
        print("  Genera contraseñas válidas para abrir cofres y")
        print("  acumular puntos. ¡Que comience la cacería!")
        print("═" * 60)

    def _mostrar_estado(self):
        """Muestra el estado actual del jugador."""
        print(f"\n  👤 Cazador : {self.nombre_jugador}")
        print(f"  🎯 Ronda   : {self.ronda}")
        print(f"  ⭐ Puntaje : {self.puntaje} pts")
        print("  " + "─" * 40)

    def _mostrar_despedida(self):
        """Muestra el resumen final al salir del juego."""
        print("\n" + "═" * 60)
        print("   🏁  FIN DEL JUEGO")
        print("═" * 60)
        print(f"  Cazador  : {self.nombre_jugador}")
        print(f"  Rondas   : {self.ronda}")
        print(f"  Puntaje  : {self.puntaje} pts")
        if self.puntaje >= 100:
            print("  🥇 ¡Maestro Cazador! Eres una leyenda.")
        elif self.puntaje >= 50:
            print("  🥈 ¡Buen trabajo! Sigue entrenando.")
        elif self.puntaje > 0:
            print("  🥉 Apenas positivo. ¡La próxima será mejor!")
        else:
            print("  💀 Las maldiciones te dominaron. ¡Inténtalo de nuevo!")
        print("═" * 60 + "\n")

    # ── Métodos de lógica ────────────────────────────────────────

    def _pedir_longitud(self) -> int:
        """
        Solicita al usuario la longitud de la contraseña con validación.

        Returns:
            int: Longitud válida ingresada por el usuario.

        Raises:
            EntradaNoNumericaError: Si la entrada no es numérica.
            LongitudInvalidaError: Si la longitud es menor a 8.
        """
        entrada = input("\n  Ingresa la longitud de la contraseña (mín. 8): ").strip()

        # Validamos que sea numérico antes de convertir
        if not entrada.isdigit():
            raise EntradaNoNumericaError(
                f"'{entrada}' no es un número válido. Ingresa un entero positivo."
            )

        longitud = int(entrada)

        if longitud < 8:
            raise LongitudInvalidaError(
                f"Longitud {longitud} inválida. El mínimo permitido es 8."
            )

        return longitud

    def _seleccionar_cofre_valido(self) -> Cofre:
        """
        Selecciona aleatoriamente un cofre positivo según probabilidades.

        Returns:
            Cofre: Instancia del cofre seleccionado.
        """
        tipos   = list(self.PROBABILIDADES_COFRE.keys())
        pesos   = list(self.PROBABILIDADES_COFRE.values())
        elegido = random.choices(tipos, weights=pesos, k=1)[0]

        # Usamos un diccionario para instanciar el cofre correcto
        fabricas = {
            "Común":      CofreComun,
            "Raro":       CofreRaro,
            "Legendario": CofreLegendario,
        }
        return fabricas[elegido]()

    def _jugar_ronda(self):
        """
        Ejecuta una ronda completa del juego:
          1. Pide longitud con manejo de excepciones.
          2. Genera la contraseña.
          3. La valida.
          4. Abre el cofre correspondiente.
          5. Actualiza el puntaje.
        """
        self.ronda += 1
        self._mostrar_estado()
        print(f"  🎲 RONDA {self.ronda}")
        print("  " + "─" * 40)

        # ── Paso 1: Obtener longitud válida ──────────────────────
        longitud = None
        while longitud is None:
            try:
                longitud = self._pedir_longitud()
            except EntradaNoNumericaError as e:
                print(f"\n  ⚠️  ERROR: {e}")
            except LongitudInvalidaError as e:
                print(f"\n  ⚠️  ERROR: {e}")

        # ── Paso 2: Generar contraseña ───────────────────────────
        try:
            contrasena = Contrasena(longitud)
        except LongitudInvalidaError as e:
            # Aunque ya validamos, capturamos por robustez
            print(f"\n  ❌ Error al crear contraseña: {e}")
            return

        print(f"\n  🔑 Contraseña generada: {contrasena}")

        # ── Paso 3: Validar contraseña ───────────────────────────
        es_valida, razones = contrasena.validar()

        if not es_valida:
            # Lanzamos excepción personalizada y la capturamos
            try:
                raise ContrasenaInvalidaError(
                    "La contraseña no cumple los requisitos.", razones
                )
            except ContrasenaInvalidaError as e:
                print(f"\n  ❌ Contraseña INVÁLIDA: {e}")
                for r in e.razones:
                    print(f"     • {r}")
                cofre = CofreMaldito()
        else:
            print("\n  ✅ ¡Contraseña VÁLIDA!")
            cofre = self._seleccionar_cofre_valido()

        # ── Paso 4: Abrir cofre y actualizar puntaje ─────────────
        print(cofre.abrir())
        self.puntaje += cofre.puntos
        print(f"\n  ⭐ Puntaje actualizado: {self.puntaje} pts")

    def _preguntar_continuar(self) -> bool:
        """
        Pregunta al jugador si desea continuar.

        Returns:
            bool: True si desea continuar, False si desea salir.
        """
        while True:
            respuesta = input("\n  ¿Deseas continuar jugando? (s/n): ").strip().lower()
            if respuesta in ("s", "si", "sí", "y", "yes"):
                return True
            elif respuesta in ("n", "no"):
                return False
            else:
                print("  Por favor ingresa 's' para sí o 'n' para no.")

    # ── Método principal ─────────────────────────────────────────

    def iniciar(self):
        """
        Punto de entrada del juego. Controla el flujo principal.
        """
        self._mostrar_bienvenida()

        # Pedimos el nombre del jugador
        self.nombre_jugador = input("\n  ¿Cómo te llamas, Cazador? ").strip()
        if not self.nombre_jugador:
            self.nombre_jugador = "Desconocido"

        print(f"\n  ¡Bienvenido, {self.nombre_jugador}! Que los cofres te favorezcan.")

        # Bucle principal del juego
        seguir = True
        while seguir:
            try:
                self._jugar_ronda()
            except KeyboardInterrupt:
                # Permite salir con Ctrl+C de forma limpia
                print("\n\n  Juego interrumpido por el usuario.")
                break
            except Exception as e:
                # Captura cualquier excepción no prevista
                print(f"\n  ⚠️  Error inesperado: {e}")

            seguir = self._preguntar_continuar()

        self._mostrar_despedida()


# ─────────────────────────────────────────────────────────────────
# ENTRADA
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    juego = JuegoCazador()
    juego.iniciar()
