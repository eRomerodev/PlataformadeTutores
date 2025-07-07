# Plataforma de Tutoría Universitaria - Comentada
# Conecta tutorados con tutores, permite agendar y gestionar sesiones
import json
import re
from datetime import datetime

# --- Pensum completo (compacto y ordenado) ---

PENSUM = {
    "Ingeniería y Ciencias de la Computación Integradas": {
        1: [
            "Introducción a la ingeniería (IN10001)",
            "Física aplicada I (F10012)",
            "Cálculo diferencial de una variable (MA10013)",
            "Fundamentos de la programación (TC10014)",
            "Desarrollo personal (H10015)",
        ],
        2: [
            "Química para ingeniería (Q10016)",
            "Física aplicada II (F10027)",
            "Cálculo integral de una variable (MA10028)",
            "Programación orientada a objetos (H10029)",
            "Comunicación y colaboración efectiva (H100210)",
        ],
        3: [
            "Probabilidad y estadística (MA100311)",
            "Física aplicada III (F100312)",
            "Matemáticas multivariable (TC100313)",
            "Estructura de datos y algoritmos computacionales (MA100514)",
            "Álgebra lineal y matemáticas discretas (TE200115)",
        ],
        4: [
            "Ecuaciones diferenciales (MA200116)",
            "Organización y arquitectura de computadoras (TC200117)",
            "Pensamiento crítico y toma de decisiones (H200118)",
            "Circuitos eléctricos (TE200119)",
            "Fundamentos de economía (EC200120)",
        ],
        5: [
            "Bases de datos (TC200421)",
            "Sistemas operativos (TC200322)",
            "Evaluación y administración de proyectos (IN200423)",
            "Electrónica de estado sólido (TE200324)",
            "Evolución y metodología de la innovación tecnológica (IN200325)",
        ],
        6: [
            "Ciencia de datos e inteligencia artificial (TC200626)",
            "Ingeniería de software (TC200527)",
            "Liderazgo global (H200228)",
            "Tópicos selectos de la ingeniería I (OP200129)",
            "Gestión del talento, cultura y empresas conscientes (IN200730)",
        ],
        7: [
            "Desarrollo web (TC300231)",
            "Diseño lógico (TC300332)",
            "Sistemas distribuidos (TC300133)",
            "Tópicos selectos de la ingeniería II (OP200234)",
            "Fundamentos de finanzas para ingenieros (FZ300135)",
        ],
        8: [
            "Desarrollo para dispositivos móviles (TC300436)",
            "Redes y ciberseguridad (TC300537)",
            "Arquitectura de software (TC300638)",
            "Tópicos selectos de la ingeniería III (OP200339)",
            "Sistemas embedidos (TC300740)",
        ],
        9: [
            "Unidad de formación KEY I (OP300141)",
            "Unidad de formación KEY II (OP300242)",
            "Unidad de formación KEY III (OP300343)",
            "Unidad de formación KEY IV (OP300444)",
            "Unidad de formación KEY V (OP300545)",
        ],
        10: [
            "Tópicos selectos de la ingeniería IV (OP200646)",
            "Ventas técnicas y marketing (MT300147)",
            "Proyecto Integral de Ingeniería y Ciencias de la Computación Integradas (TC300848)",
        ],
    },
    "Ingeniería Industrial y Manufactura Avanzada": {
        1: [
            "Introducción a la ingeniería (IN10001)",
            "Física aplicada I (F10012)",
            "Cálculo diferencial de una variable (MA10013)",
            "Fundamentos de la programación (TC10014)",
            "Desarrollo personal (H10015)",
        ],
        2: [
            "Química para ingeniería (Q10016)",
            "Física aplicada II (F10027)",
            "Cálculo integral de una variable (MA10028)",
            "Programación orientada a objetos (TC10029)",
            "Comunicación y colaboración efectiva (H100210)",
        ],
        3: [
            "Probabilidad y estadística (MA100311)",
            "Física aplicada III (F100312)",
            "Matemáticas multivariable (MA100413)",
            "Estructura de datos y algoritmos computacionales (TC100314)",
            "Procesos de manufactura (IN100215)",
        ],
        4: [
            "Sistemas ciberfísicos (IN200016)",
            "Tecnologías exponenciales en manufactura avanzada (IN200217)",
            "Pensamiento crítico y toma de decisiones (H200118)",
            "Investigación de operaciones (IN200119)",
            "Fundamentos de economía (EC200120)",
        ],
        5: [
            "Control estadístico y diseño de experimentos (IN200521)",
            "Manufactura integrada por computadora (IN200622)",
            "Evaluación y administración de proyectos (IN200423)",
            "Gestión de inventarios y planificación de la demanda (IN200724)",
            "Evolución y metodologías de la innovación (IN200325)",
        ],
        6: [
            "Gestión de la producción (IN200826)",
            "Resolución de problemas con AI (IN200927)",
            "Liderazgo global (H200228)",
            "Tópicos selectos de la ingeniería I (OP200129)",
            "Gestión del talento, cultura y empresas conscientes (IN201030)",
        ],
        7: [
            "Sistemas esbeltos (IN300131)",
            "Viabilidad e innovación de procesos (IN300232)",
            "Simulación de procesos (IN300333)",
            "Tópicos selectos de la ingeniería II (OP200234)",
            "Fundamentos de finanzas para ingenieros (FZ300135)",
        ],
        8: [
            "Proyectos de automatización industrial (MR300936)",
            "Administración de la cadena de suministros (IN300537)",
            "Analítica de datos e inteligencia de negocios (IN300638)",
            "Tópicos selectos de la ingeniería III (OP200339)",
            "Planeación estratégica y tecnológica (IN300740)",
        ],
        9: [
            "Unidad de formación KEY I (OP300141)",
            "Unidad de formación KEY II (OP300242)",
            "Unidad de formación KEY III (OP300343)",
            "Unidad de formación KEY IV (OP300444)",
            "Unidad de formación KEY V (OP300545)",
        ],
        10: [
            "Tópicos selectos de la ingeniería IV (OP200446)",
            "Ventas técnicas y marketing (MT300147)",
            "Proyecto integrador de Ingeniería Industrial y Manufactura Avanzada (IN300848)",
        ],
    },
    "Ingeniería Mecatrónica y Robótica": {
        1: [
            "Introducción a la ingeniería (IN10001)",
            "Física aplicada I (F10012)",
            "Cálculo diferencial de una variable (MA10013)",
            "Fundamentos de programación (TC10014)",
            "Desarrollo personal (H10015)",
        ],
        2: [
            "Química para ingeniería (Q10016)",
            "Física aplicada II (F10027)",
            "Cálculo integral de una variable (MA10028)",
            "Programación orientada a objetos (H10029)",
            "Comunicación y colaboración efectiva (H100210)",
        ],
        3: [
            "Probabilidad y estadística (MA100311)",
            "Física aplicada III (F100312)",
            "Matemáticas multivariable (MA100413)",
            "Estructura de datos y algoritmos computacionales (TC100314)",
            "Álgebra lineal y matemática discretas (MA100515)",
        ],
        4: [
            "Ecuaciones diferenciales (MA200116)",
            "Circuitos eléctricos (TE200117)",
            "Pensamiento crítico y toma de decisiones (H200118)",
            "Dibujo industrial y P&ID (MR100119)",
            "Fundamentos de economía (EC200120)",
        ],
        5: [
            "Microcontroladores y circuitos integrados (MR200221)",
            "Materiales y procesos de fabricación (MR200322)",
            "Evaluación y administración de proyectos (IN200423)",
            "Electrónica de estado sólido (TE200324)",
            "Evolución y metodología de la innovación tecnológica (IN200325)",
        ],
        6: [
            "Resolución de problemas con inteligencia artificial (TC200626)",
            "Mecanismos y elementos de máquinas (MR200427)",
            "Liderazgo global (H200228)",
            "Tópicos selectos de la ingeniería I (OP200129)",
            "Gestión del talento, cultura y empresas conscientes (IN200730)",
        ],
        7: [
            "Automatización y buses de comunicación (MR200531)",
            "Gestión de energía y suministros industriales (MR300932)",
            "Diseño de sistemas de control (MR300133)",
            "Tópicos selectos de la ingeniería II (OP200234)",
            "Fundamentos de finanzas para ingenieros (FZ300135)",
        ],
        8: [
            "Diseño mecatrónico (MR300436)",
            "Fundamentos de robótica (MR300237)",
            "Automatización de sistemas de manufactura (MR300338)",
            "Tópicos selectos de la ingeniería III (OP200339)",
            "Mantenimiento predictivo y confiabilidad (MR300740)",
        ],
        9: [
            "Unidad de formación KEY I (OP300141)",
            "Unidad de formación KEY II (OP300242)",
            "Unidad de formación KEY III (OP300343)",
            "Unidad de formación KEY IV (OP300444)",
            "Unidad de formación KEY V (OP300545)",
        ],
        10: [
            "Tópicos selectos de la ingeniería IV (OP200446)",
            "Ventas técnicas y marketing (MT300147)",
            "Proyecto integral de mecatrónica y robótica (TC300848)",
        ],
    },
}

# --- Funciones auxiliares ---

def salir_si_necesario(texto):
    if texto.strip().lower() == "salir":
        print("👋 Programa finalizado por el usuario.")
        exit()

# Valida que la hora esté en formato HH:MM y sea múltiplo de 30 minutos.
def validar_hora(hora_str):
    try:
        dt = datetime.strptime(hora_str, "%H:%M")
        if dt.minute % 30 != 0:
            print("Debe ser en intervalos de 30 minutos.")
            return False
        return True
    except ValueError:
        return False

# Pide al usuario un número dentro de un rango permitido.
def input_numerico(minimo, maximo, prompt):
    while True:
        val = input(prompt).strip()
        salir_si_necesario(val)
        if val.isdigit() and minimo <= int(val) <= maximo:
            return int(val)
        print(f"Entrada inválida. Por favor, ingresa un número entre {minimo} y {maximo}.")

# Muestra opciones enumeradas al usuario y devuelve la seleccionada.
def seleccionar_opcion_lista(lista, mensaje):
    print(mensaje)
    for i, opcion in enumerate(lista, 1):
        print(f"{i}. {opcion}")
    return lista[input_numerico(1, len(lista), "Selecciona el número de la opción: ") - 1]

def correo_valido(correo):
    patron = r"^[a-zA-Z]+\.{1}[a-zA-Z]+@keyinstitute\.edu\.sv$" # Extracto de ChatGPT
    return re.match(patron, correo) is not None

# Valida que el nombre completo tenga formato correcto (mayúsculas, mínimo 2 nombres y 2 apellidos).
def validar_nombre(nombre):
    nombre = nombre.strip()
    if not re.match(r"^[a-zA-ZÁÉÍÓÚÑáéíóúñ\s]+$", nombre): # Extracto de ChatGPT
        return None
    return " ".join(word.capitalize() for word in nombre.split())

# Carga el registro desde el archivo JSON, si existe.
def cargar_registro():
    try:
        with open("Registro.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Guarda el registro actualizado en el archivo JSON.
def guardar_registro(registro):
    with open("Registro.json", "w", encoding="utf-8") as f:
        json.dump(registro, f, indent=4, ensure_ascii=False)

# --- Horarios: selección múltiple de días y bloques ---

# Permite al tutor ingresar varios bloques horarios con día, inicio y fin.
def ingresar_horarios():
    horarios = []
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    print("\nIngresa tus horarios disponibles en bloques.")
    print("Puedes seleccionar varios días separados por coma. Ejemplo: 1,3,5 para Lunes, Miércoles y Viernes.")
    print("Luego ingresa hora inicio y hora fin en formato 24h (HH:MM).")
    print("Cuando termines, escribe 'salir' en los días.\n")

    while True:
        for i, dia in enumerate(dias_semana, 1):
            print(f"{i}. {dia}")
        entrada_dias = input("Selecciona número(s) de día(s), separados por coma (o 'salir'): ").strip()
        if entrada_dias.lower() == "salir":
            break
        nums = [n.strip() for n in entrada_dias.split(",")]
        if not all(n.isdigit() and 1 <= int(n) <= len(dias_semana) for n in nums):
            print("Entrada inválida. Usa números válidos separados por coma.")
            continue
        dias_seleccionados = [dias_semana[int(n) - 1] for n in nums]

        while True:
            hora_inicio = input("Hora inicio (HH:MM, 24h): ").strip()
            salir_si_necesario(hora_inicio)
            if validar_hora(hora_inicio):
                break
            print("Formato inválido. Usa HH:MM (24h).")

        while True:
            hora_fin = input("Hora fin (HH:MM, 24h): ").strip()
            salir_si_necesario(hora_fin)
            if validar_hora(hora_fin):
                if hora_fin > hora_inicio:
                    break
                else:
                    print("Hora fin debe ser mayor que hora inicio.")
            else:
                print("Formato inválido. Usa HH:MM (24h).")

        for dia in dias_seleccionados:
            horarios.append({"dia": dia, "inicio": hora_inicio, "fin": hora_fin})

        print(f"Bloque horario guardado para: {', '.join(dias_seleccionados)} de {hora_inicio} a {hora_fin}.\n")

    return horarios

# --- Registro y login ---

# Verifica si el correo ya existe en el registro.
def correo_existe(correo, registro):
    return any(u["correo"] == correo for u in registro)

# Verifica si el carnet ya existe en el registro.
def carnet_existe(carnet, registro):
    return any(u["carnet"] == carnet for u in registro)

# Flujo completo de registro: nombre, correo, carnet, ciclo, materias, etc.
def registrar_usuario():
    registro = cargar_registro()
    registro = cargar_registro()
    print("\n¡Perfecto! Creemos tu cuenta =)\n")

    # Nombre completo
    while True:
        nombre = input("Ingrese su nombre completo (o 'salir'): ").strip()
        salir_si_necesario(nombre)
        nombre_valido = validar_nombre(nombre)
        if len(nombre_valido.split()) < 2:
            print("Debe ingresar al menos un nombre y un apellido.")
            continue
        if not all(p[0].isupper() and p[1:].islower() for p in nombre_valido.split()):
            print("Cada palabra debe iniciar con mayúscula seguida de minúsculas.")
            continue
        if len(nombre_valido.split()) < 4:
            print("Debes ingresar al menos dos nombres y dos apellidos.")
            continue
        if nombre_valido:
            break
        print("Formato de nombre inválido. Solo letras y espacios.")

    # Correo institucional
    while True:
        correo = input("Ingrese su correo institucional (nombre.apellido@keyinstitute.edu.sv): ").strip().lower()
        salir_si_necesario(correo)
        if not correo_valido(correo):
            print("Correo inválido. Use formato nombre.apellido@keyinstitute.edu.sv")
        elif correo_existe(correo, registro):
            print("Correo ya registrado.")
        else:
            break

    # Carnet
    while True:
        carnet = input("Ingrese su carnet (ejemplo KEY_99999): ").strip()
        if carnet_existe(carnet, registro):
            print("Carnet ya registrado.")
        else:
            break

        # Contraseña
    while True:
        password = input("Crea una contraseña (mínimo 4 caracteres): ").strip()
        if len(password) >= 4:
            break
        print("La contraseña es demasiado corta.")

    # Descripción personal
    while True:
        descripcion = input("Escribe una breve descripción (máx 150 caracteres): ").strip()
        salir_si_necesario(descripcion)
        if len(descripcion) <= 150:
            break
        print("La descripción es demasiado larga.")


    carreras = list(PENSUM.keys())
    carrera = seleccionar_opcion_lista(carreras, "\nSelecciona tu carrera:")    

    # Seleccionar ciclo
    ciclos = list(PENSUM[carrera].keys())
    print("Selecciona el ciclo que cursas (1,2,3,...,10):")
    ciclo = input_numerico(1, 10, "Selecciona el número de tu ciclo: ")

    # Seleccionar rol
    print("\nSelecciona tu rol:")
    print("1. Tutorado")
    print("2. Tutor")
    print("3. Ambos")
    rol_num = input_numerico(1,3,"Selecciona el número de tu rol: ")
    roles_map = {1: "Tutorado", 2: "Tutor"}
    rol = roles_map[rol_num]

    # Seleccionar materias que conoce/puede enseñar (solo hasta ciclo)
    materias_disponibles = []
    for c in range(1, ciclo+1):
        materias_disponibles.extend(PENSUM[carrera][c])

    materias = []
    print("\nSelecciona las materias que conoces (solo hasta tu ciclo). Ingresa números separados por coma:")
    for i, m in enumerate(materias_disponibles,1):
        print(f"{i}. {m}")
    while True:
        entrada = input("Tus materias (ejemplo: 1,3,5): ").strip()
        if "," not in entrada:
            print("Debes usar comas como separadores.")
            continue
        salir_si_necesario(entrada)
        indices = [x.strip() for x in entrada.split(",") if x.strip().isdigit()]
        if not indices:
            print("Entrada inválida, intenta de nuevo.")
            continue
        indices_int = [int(x) for x in indices]
        if any(i<1 or i>len(materias_disponibles) for i in indices_int):
            print("Número(s) fuera de rango.")
            continue
        materias = [materias_disponibles[i-1] for i in indices_int]
        break

    # Ingresar horarios
    horarios = ingresar_horarios() if rol in ["Tutor"] else []

    usuario = {
        "password": password,
        "descripcion": descripcion,
        "nombre_completo": nombre_valido,
        "correo": correo,
        "carnet": carnet,
        "carrera": carrera,
        "ciclo": ciclo,
        "rol": rol,
        "materias": materias,
        "horarios": horarios,
        "sesiones": [],  # sesiones agendadas y realizadas del usuario
    }
    registro.append(usuario)
    guardar_registro(registro)
    print("\nRegistro exitoso. Ya puedes iniciar sesión.\n")

# Solicita correo y contraseña, y devuelve el usuario autenticado si existe.
def login():
    registro = cargar_registro()
    print("\nPor favor ingresa tus datos para iniciar sesión. Escribe 'salir' para cancelar.\n")

    correo = input("Correo institucional: ").strip()
    password = input("Contraseña: ").strip()

    for usuario in registro:
        if usuario["correo"] == correo and usuario["password"] == password:
            print(f"\nBienvenido, {usuario['nombre_completo']}!\n")
            return usuario
    return None

# --- Gestión de sesiones dentro del registro ---

# Guarda el registro actualizado en el archivo JSON.
def guardar_registro_completo(registro):
    guardar_registro(registro)

# Muestra las sesiones agendadas que aún no tienen asistencia registrada.
def ver_calendario_sesiones(usuario, registro):
    sesiones = usuario.get("sesiones", [])
    pendientes = [s for s in sesiones if "asistencia" not in s]
    if not pendientes:
        print("No tienes sesiones agendadas.")
        return
    print("\n--- Sesiones agendadas ---")
    for s in pendientes:
        print(f"{s['fecha']} | {s['dia']} {s['inicio']} - {s['fin']} | Tutor: {s['tutor']} | Materia: {s['materia']} | Tutorado: {s['tutorado']}")

# Muestra sesiones pasadas con asistencia registrada.
def ver_historial_sesiones(usuario):
    sesiones = usuario.get("sesiones", [])
    realizadas = [s for s in sesiones if "asistencia" in s]
    if not realizadas:
        print("Aún no tienes sesiones realizadas.")
        return
    print("\n--- Historial de tutorías realizadas ---")
    for s in realizadas:
        print(f"{s['fecha']} | {s['dia']} {s['inicio']} - {s['fin']} | Tutor: {s['tutor']} | Asistencia: {s['asistencia']} | Duración: {s.get('duracion', 'N/A')} min | Calificación: {s.get('calificacion', 'No calificada')} | Tutorado: {s['tutorado']}")

# Permite registrar si una sesión se realizó y su duración.
def registrar_asistencia_y_duracion(usuario, registro):
    sesiones = usuario.get("sesiones", [])
    if not sesiones:
        print("No tienes sesiones registradas.")
        return
    print("Ingresa fecha y día de la sesión para registrar asistencia y duración.")
    fecha = input("Fecha (dd/mm/aaaa): ").strip()
    salir_si_necesario(fecha)
    dia = input("Día (Lunes, Martes, ...): ").strip()
    salir_si_necesario(dia)
    for s in sesiones:
        if s["fecha"] == fecha and s["dia"].lower() == dia.lower():
            respuesta = input("¿Se realizó la sesión? (si/no): ").strip().lower()
            salir_si_necesario(respuesta)
            if respuesta == "si":
                s["asistencia"] = True
                duracion = input("Duración en minutos: ").strip()
                salir_si_necesario(duracion)
                if duracion.isdigit():
                    s["duracion"] = int(duracion)
                else:
                    print("Duración inválida, se dejará como 'N/A'.")
                    s["duracion"] = "N/A"
                print("Asistencia y duración registradas.")
            else:
                s["asistencia"] = False
                print("Se registró que la sesión NO se realizó.")
            guardar_registro_completo(registro)
            return
    print("No se encontró la sesión con esa fecha y día.")

# Permite al usuario calificar una sesión ya realizada.
def calificar_sesion(usuario, registro):
    sesiones = usuario.get("sesiones", [])
    if not sesiones:
        print("No tienes sesiones registradas.")
        return
    fecha = input("Fecha de la sesión (dd/mm/aaaa): ").strip()
    salir_si_necesario(fecha)
    dia = input("Día de la sesión (Lunes, Martes, ...): ").strip()
    salir_si_necesario(dia)
    for s in sesiones:
        if s["fecha"] == fecha and s["dia"].lower() == dia.lower():
            while True:
                calif = input("Calificación (1-5): ").strip()
                salir_si_necesario(calif)
                if calif.isdigit() and 1 <= int(calif) <= 5:
                    s["calificacion"] = int(calif)
                    break
                else:
                    print("Calificación inválida.")
            comentario = input("Comentario (opcional): ").strip()
            salir_si_necesario(comentario)
            s["comentario"] = comentario
            guardar_registro_completo(registro)
            print("Calificación y comentario guardados.")
            return
    print("No se encontró la sesión.")

# Solo tutores: permite agendar una sesión con un tutorado.
def agendar_sesion(usuario, registro):
    print("\n--- Agendar nueva sesión ---")
    # El tutor debe ser usuario con rol Tutor o Ambos
    if usuario["rol"] not in ["Tutor"]:
        print("No tienes permisos para agendar sesiones como tutor.")
        return

    # Mostrar lista de tutorados para elegir a quién dar tutoría
    tutorados = [u for u in registro if u["rol"] in ["Tutorado"] and u["carrera"] == usuario["carrera"]]
    if not tutorados:
        print("No hay tutorados registrados para tu carrera.")
        return

    print("\nSelecciona el tutorado:")
    for i, t in enumerate(tutorados, 1):
        print(f"{i}. {t['nombre_completo']} (Ciclo {t['ciclo']})")
    idx = input_numerico(1, len(tutorados), "Selecciona el número del tutorado: ")
    tutorado = tutorados[idx-1]

    # Materias que tutor puede enseñar
    materias_tutor = usuario["materias"]
    # Materias que tutorado necesita (hasta su ciclo)
    materias_tutorado = []
    for c in range(1, tutorado["ciclo"]+1):
        materias_tutorado.extend(PENSUM[tutorado["carrera"]][c])
    # Filtrar materias en común que tutor puede enseñar y tutorado necesita
    materias_comunes = [m for m in materias_tutor if m in materias_tutorado]
    if not materias_comunes:
        print("No hay materias compatibles entre tú y el tutorado.")
        return
    print("\nSelecciona la materia para la sesión:")
    for i, m in enumerate(materias_comunes, 1):
        print(f"{i}. {m}")
    idx_m = input_numerico(1, len(materias_comunes), "Selecciona el número de la materia: ")
    materia = materias_comunes[idx_m-1]

    # Fecha
    while True:
        fecha = input("Fecha (dd/mm/aaaa): ").strip()
        salir_si_necesario(fecha)
        try:
            datetime.strptime(fecha, "%d/%m/%Y") # Extracto de ChatGPT
            break
        except ValueError:
            print("Fecha inválida.")

    # Día (obligatorio, para mostrar)
    dias_validos = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    while True:
        dia = input("Día (Lunes, Martes, Miércoles, Jueves, Viernes): ").strip().capitalize()
        salir_si_necesario(dia)
        if dia in dias_validos:
            break
        else:
            print("Día inválido.")

    # Hora inicio y fin
    while True:
        hora_inicio = input("Hora inicio (HH:MM, 24h): ").strip()
        salir_si_necesario(hora_inicio)
        if validar_hora(hora_inicio):
            break
        print("Hora inválida.")
    while True:
        hora_fin = input("Hora fin (HH:MM, 24h): ").strip()
        salir_si_necesario(hora_fin)
        if validar_hora(hora_fin) and hora_fin > hora_inicio:
            break
        print("Hora fin debe ser mayor que hora inicio y en formato válido.")

    # Modalidad
    modalidades = ["virtual", "presencial"]
    modalidad = seleccionar_opcion_lista(modalidades, "Selecciona modalidad:")

    # Crear sesión
    sesion = {
        "tutor": usuario["nombre_completo"],
        "tutorado": tutorado["nombre_completo"],
        "materia": materia,
        "fecha": fecha,
        "dia": dia,
        "inicio": hora_inicio,
        "fin": hora_fin,
        "modalidad": modalidad,
    }

    # Añadir a sesiones de ambos usuarios y al registro
    usuario.setdefault("sesiones", []).append(sesion)
    tutorado.setdefault("sesiones", []).append(sesion)

    guardar_registro_completo(registro)
    print("Sesión agendada correctamente.")

# --- Menú de gestión de sesiones ---

# Muestra menú de opciones para gestionar sesiones (ver, registrar, calificar).
def gestion_sesiones(usuario, registro):
    while True:
        print("\n--- GESTIÓN DE SESIONES DE TUTORÍA ---")
        print("1. Ver calendario de sesiones agendadas")
        print("2. Ver historial de tutorías realizadas")
        print("4. Calificar sesión y dejar comentarios")
        print("5. Agendar nueva sesión")
        print("0. Volver al menú principal")
        opcion = input("Seleccione una opción: ").strip()
        salir_si_necesario(opcion)

        if opcion == "1":
            ver_calendario_sesiones(usuario, registro)
        elif opcion == "2":
            ver_historial_sesiones(usuario)
        elif opcion == "4":
            calificar_sesion(usuario, registro)
        elif opcion == "5":
            agendar_sesion(usuario, registro)
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")

# --- Menú principal ---

        if opcion == "1":
            usuario = login()
            if usuario:
                while True:
                    print("\n--- Menú Principal ---")
                    print("1. Gestión de sesiones")
                    print("2. Cerrar sesión")
                    opcion2 = input("Elige una opción: ").strip()
                    salir_si_necesario(opcion2)
                    if opcion2 == "1":
                        registro = cargar_registro()
                        # refrescar usuario actualizado (por si hay cambios)
                        for u in registro:
                            if u["correo"] == usuario["correo"]:
                                usuario = u
                                break
                        gestion_sesiones(usuario, registro)
                    elif opcion2 == "2":
                        print("Sesión cerrada.")
                    elif opcion2 == "3":
                        busqueda_manual_tutores(usuario, registro)
                        break
                    else:
                        print("Opción inválida.")
            else:
                print("No se pudo iniciar sesión. Intenta de nuevo.")
        elif opcion == "2":
            registrar_usuario()
        elif opcion == "3":
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida.")

# --- Nueva funcionalidad: Emparejar tutorados con tutores automáticamente ---
        print("\n")




# Permite a tutorados buscar manualmente tutores por materia y horarios.
def busqueda_manual_tutores(usuario, registro):
    if usuario["rol"] != "Tutorado":
        print("Esta función es solo para usuarios tutorados.")
        return

    necesidades = usuario.get("materias", [])
    if not necesidades:
        print("No tienes materias marcadas como necesidades de refuerzo.")
        return

    print("\nMaterias que necesitas reforzar:")
    for i, m in enumerate(necesidades, 1):
        print(f"{i}. {m}")
    idx = input_numerico(1, len(necesidades), "Selecciona una materia: ")
    materia = necesidades[idx - 1].lower()

    tutores_disponibles = []
    for u in registro:
        if u["rol"] != "Tutor":
            continue
        if materia not in [m.lower() for m in u.get("materias", [])]:
            continue
        tutores_disponibles.append(u)

    if not tutores_disponibles:
        print("No hay tutores disponibles para esa materia.")
        return

    while True:
        print("\n=== Tutores disponibles para esa materia ===")
        for i, t in enumerate(tutores_disponibles, 1):
            print(f"{i}. {t['nombre_completo']} | Materias: {', '.join(t['materias'])}")
        idx = input_numerico(1, len(tutores_disponibles), "Selecciona un tutor: ")
        tutor = tutores_disponibles[idx - 1]

        dias = list({h["dia"] for h in tutor.get("horarios", [])})
        if not dias:
            print("Este tutor no tiene horarios disponibles.")
            return

        print("\nDías disponibles:")
        for i, d in enumerate(dias, 1):
            print(f"{i}. {d}")
        dia_idx = input_numerico(1, len(dias), "Selecciona un día: ")
        dia = dias[dia_idx - 1]

        horarios = [h for h in tutor["horarios"] if h["dia"] == dia]
        if not horarios:
            print("No hay horarios disponibles en ese día.")
            continue

        horario = horarios[0]
        print(f"El tutor {tutor['nombre_completo']} tiene un espacio de sesión el {dia} de {horario['inicio']} a {horario['fin']}.")
        confirmar = input("¿Deseas reservar esta sesión? (Sí/No): ").strip().lower()
        if confirmar == "sí":
            fecha = input("Fecha de la tutoría (dd/mm/aaaa): ").strip()
            while True:
                try:
                    datetime.strptime(fecha, "%d/%m/%Y")
                    break
                except ValueError:
                    print("Fecha inválida.")
            modalidad = seleccionar_opcion_lista(["virtual", "presencial"], "Selecciona modalidad:")

            sesion = {
                "tutor": tutor["nombre_completo"],
                "tutorado": usuario["nombre_completo"],
                "materia": materia,
                "fecha": fecha,
                "dia": dia,
                "inicio": horario["inicio"],
                "fin": horario["fin"],
                "modalidad": modalidad,
            }

            usuario.setdefault("sesiones", []).append(sesion)
            tutor.setdefault("sesiones", []).append(sesion)
            guardar_registro_completo(registro)
            print("✅ ¡Sesión agendada exitosamente!")
            return
        else:
            print("Regresando a la lista de tutores...")


# Permite a tutorados buscar manualmente tutores por materia y horarios.
def busqueda_manual_tutores(usuario, registro):
    if usuario["rol"] != "Tutorado":
        print("Esta función es solo para usuarios tutorados.")
        return

    necesidades = usuario.get("materias", [])
    if not necesidades:
        print("No tienes materias marcadas como necesidades de refuerzo.")
        return

    print("\nMaterias que necesitas reforzar:")
    for i, m in enumerate(necesidades, 1):
        print(f"{i}. {m}")
    idx = input_numerico(1, len(necesidades), "Selecciona una materia: ")
    materia = necesidades[idx - 1].lower()

    tutores_disponibles = []
    for u in registro:
        if u["rol"] != "Tutor":
            continue
        if materia not in [m.lower() for m in u.get("materias", [])]:
            continue
        tutores_disponibles.append(u)

    if not tutores_disponibles:
        print("No hay tutores disponibles para esa materia.")
        return

    while True:
        print("\n=== Tutores disponibles para esa materia ===")
        for i, t in enumerate(tutores_disponibles, 1):
            print(f"{i}. {t['nombre_completo']} | Materias: {', '.join(t['materias'])}")
        idx = input_numerico(1, len(tutores_disponibles), "Selecciona un tutor: ")
        tutor = tutores_disponibles[idx - 1]

        dias = list({h["dia"] for h in tutor.get("horarios", [])})
        if not dias:
            print("Este tutor no tiene horarios disponibles.")
            return

        print("\nDías disponibles:")
        for i, d in enumerate(dias, 1):
            print(f"{i}. {d}")
        dia_idx = input_numerico(1, len(dias), "Selecciona un día: ")
        dia = dias[dia_idx - 1]

        horarios = [h for h in tutor["horarios"] if h["dia"] == dia]
        if not horarios:
            print("No hay horarios disponibles en ese día.")
            continue

        horario = horarios[0]
        print(f"El tutor {tutor['nombre_completo']} tiene un espacio de sesión el {dia} de {horario['inicio']} a {horario['fin']}.")
        confirmar = input("¿Deseas reservar esta sesión? (Sí/No): ").strip().lower()
        if confirmar == "sí":
            fecha = input("Fecha de la tutoría (dd/mm/aaaa): ").strip()
            while True:
                try:
                    datetime.strptime(fecha, "%d/%m/%Y")
                    break
                except ValueError:
                    print("Fecha inválida.")
            modalidad = seleccionar_opcion_lista(["virtual", "presencial"], "Selecciona modalidad:")

            sesion = {
                "tutor": tutor["nombre_completo"],
                "tutorado": usuario["nombre_completo"],
                "materia": materia,
                "fecha": fecha,
                "dia": dia,
                "inicio": horario["inicio"],
                "fin": horario["fin"],
                "modalidad": modalidad,
            }

            usuario.setdefault("sesiones", []).append(sesion)
            tutor.setdefault("sesiones", []).append(sesion)
            guardar_registro_completo(registro)
            print("✅ ¡Sesión agendada exitosamente!")
            return
        else:
            print("Regresando a la lista de tutores...")

# Emparejamiento automático: busca tutor según materia y día disponible.
def buscar_tutores_para_tutorado(usuario, registro):
    if usuario["rol"] not in ["Tutorado"]:
        print("Esta función está disponible solo para usuarios tutorados.")
        return

    necesidades = usuario.get("materias", [])
    if not necesidades:
        print("No tienes materias marcadas como necesidades de refuerzo.")
        return

    print("\nMaterias que necesitas reforzar:")
    for i, m in enumerate(necesidades, 1):
        print(f"{i}. {m}")
    idx = input_numerico(1, len(necesidades), "Selecciona una materia: ")
    materia = necesidades[idx - 1].lower()

    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    print("Selecciona el día que deseas recibir tutoría:")
    for i, d in enumerate(dias_semana, 1):
        print(f"{i}. {d}")
    idx_dia = input_numerico(1, 5, "Día disponible: ")
    dia_usuario = dias_semana[idx_dia - 1]

    coincidencias = []
    for tutor in registro:
        if tutor["correo"] == usuario["correo"]:
            continue
        if tutor["rol"] not in ["Tutor"]:
            continue
        if materia not in [m.lower() for m in tutor.get("materias", [])]:
            continue
        if not any(h["dia"] == dia_usuario for h in tutor.get("horarios", [])):
            continue
        experiencia = len([s for s in tutor.get("sesiones", []) if s.get("asistencia")])
        coincidencias.append((tutor, experiencia))

    if not coincidencias:
        print("No se encontraron tutores compatibles con tu necesidad.")
        return

    coincidencias.sort(key=lambda x: x[1], reverse=True)
    tutor = coincidencias[0][0]
    horario = next(h for h in tutor["horarios"] if h["dia"] == dia_usuario)

    print(f"Tutor asignado automáticamente: {tutor['nombre_completo']}")
    print(f"Materia: {materia.capitalize()} | Día: {horario['dia']} {horario['inicio']} - {horario['fin']}")

    fecha = input("Fecha de la tutoría (dd/mm/aaaa): ").strip()
    while True:
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
            break
        except ValueError:
            print("Fecha inválida.")

    modalidad = seleccionar_opcion_lista(["virtual", "presencial"], "Selecciona modalidad:")

    sesion = {
        "tutor": tutor["nombre_completo"],
        "tutorado": usuario["nombre_completo"],
        "materia": materia,
        "fecha": fecha,
        "dia": horario["dia"],
        "inicio": horario["inicio"],
        "fin": horario["fin"],
        "modalidad": modalidad,
    }

    usuario.setdefault("sesiones", []).append(sesion)
    tutor.setdefault("sesiones", []).append(sesion)
    guardar_registro_completo(registro)
    print("✅ ¡Sesión agendada exitosamente!")

# Permite a tutorados buscar manualmente tutores por materia y horarios.
def busqueda_manual_tutores(usuario, registro):
    if usuario["rol"] not in ["Tutorado"]:
        print("Esta función es solo para usuarios tutorados.")
        return

    print("\n=== Búsqueda Manual de Tutores ===")
    tutores = [u for u in registro if u["rol"] in ["Tutor"]]
    if not tutores:
        print("No hay tutores registrados.")
        return

    for i, tutor in enumerate(tutores, 1):
        print(f"{i}. {tutor['nombre_completo']} | Materias: {', '.join(tutor['materias'])}")
        for h in tutor.get("horarios", []):
            print(f"   - {h['dia']} {h['inicio']} - {h['fin']}")

    seleccion = input_numerico(1, len(tutores), "Selecciona un tutor por número: ")
    tutor = tutores[seleccion - 1]

    materia = seleccionar_opcion_lista(tutor["materias"], "Selecciona la materia que deseas recibir:")
    dias = [h["dia"] for h in tutor["horarios"]]
    dia = seleccionar_opcion_lista(dias, "Selecciona el día disponible:")
    bloques = [h for h in tutor["horarios"] if h["dia"] == dia]
    horas = [f"{b['inicio']} - {b['fin']}" for b in bloques]
    seleccion_hora = seleccionar_opcion_lista(horas, "Selecciona el bloque horario:")
    bloque = bloques[horas.index(seleccion_hora)]

    # Revisar cupo
    sesiones = [s for s in tutor.get("sesiones", []) if s["dia"] == bloque["dia"] and s["inicio"] == bloque["inicio"] and s["fin"] == bloque["fin"]]
    if len(sesiones) >= 3:
        print("Ese horario ya está lleno. Intenta otro.")
        return

    fecha = input("Fecha de la tutoría (dd/mm/aaaa): ").strip()
    while True:
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
            break
        except ValueError:
            print("Fecha inválida.")

    modalidad = seleccionar_opcion_lista(["virtual", "presencial"], "Selecciona la modalidad:")

    sesion = {
        "tutor": tutor["nombre_completo"],
        "tutorado": usuario["nombre_completo"],
        "materia": materia,
        "fecha": fecha,
        "dia": bloque["dia"],
        "inicio": bloque["inicio"],
        "fin": bloque["fin"],
        "modalidad": modalidad,
    }

    usuario.setdefault("sesiones", []).append(sesion)
    tutor.setdefault("sesiones", []).append(sesion)
    guardar_registro_completo(registro)
    print("\n✅ ¡Sesión agendada exitosamente!")

# Punto de entrada del programa, con menú de navegación principal.
def main():
    print("=== Plataforma de Tutorías Key Institute ===")
    while True:
        print("\n1. Iniciar sesión")
        print("2. Registrarme")
        print("3. Salir")
        opcion = input("Escribe el número de la opción que deseas: ").strip()
        salir_si_necesario(opcion)

        if opcion == "1":
            usuario = login()
            registro = cargar_registro()
            if usuario:
                while True:
                    print("\n--- Menú Principal ---")
                    print("1. Gestión de sesiones")
                    print("2. Buscar tutor automáticamente")
                    print("3. Buscar tutor manualmente")
                    opcion2 = input("Elige una opción: ").strip()
                    salir_si_necesario(opcion2)
                    if opcion2 == "1":
                        for u in registro:
                            if u["correo"] == usuario["correo"]:
                                usuario = u
                                break
                        gestion_sesiones(usuario, registro)
                    elif opcion2 == "2":
                        for u in registro:
                            if u["correo"] == usuario["correo"]:
                                usuario = u
                                break
                        buscar_tutores_para_tutorado(usuario, registro)
                    
                    elif opcion2 == "3":
                        busqueda_manual_tutores(usuario, registro)
                        for u in registro:
                            if u["correo"] == usuario["correo"]:
                                usuario = u
                                break

                    elif opcion2 == "3":
                        busqueda_manual_tutores(usuario, registro)
                        for u in registro:
                            if u["correo"] == usuario["correo"]:
                                usuario = u
                                break
                        busqueda_manual_tutores(usuario, registro)
                    elif opcion2 == "4":

                        print("Sesión cerrada.")
                        break
                    else:
                        print("Opción inválida.")
            else:
                print("No se pudo iniciar sesión. Intenta de nuevo.")
        elif opcion == "2":
            registrar_usuario()
        elif opcion == "3":
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()
