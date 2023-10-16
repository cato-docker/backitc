from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from datetime import date
import mysql.connector
import requests
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Conexión a la base de datos MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'CmDmEmFm95',
    'database': 'registros_estudiantes_itc'
}

try:
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        print("Conexión exitosa")
except Exception as ex:
    print(ex)

# Formulario HTML
@app.get("/")
def index():
    return {"Mensaje": "Bienvenidos"}

@app.post("/prueba")
def app_prueba():
    return {"Mensaje":"Acceso concedido."}

# Validación de DNI
def validar_dni(dni):
    url = f"https://informes.nosis.com/{dni}"
    response = requests.get(url)
    return "DNI VALIDO" in response.text

@app.post("/validar_dni")
async def validar_dni_endpoint(dni: str = Form(...)):
    es_valido = validar_dni(dni)
    if es_valido:
        return {"mensaje": "El DNI es válido"}
    else:
        raise HTTPException(status_code=400, detail="El DNI no es válido")

@app.get("/registrar_estudiantes", response_class=HTMLResponse)
async def show_registration_form(request: Request, success: bool = None):
    if success:
        return templates.TemplateResponse("index.html", {"request": request})
    else:
        return templates.TemplateResponse("index.html", {"request": request, "success": False})

@app.post("/registrar_estudiantes")
def registrar_estudiantes(
    numero_recibo: int = Form(),
    numero_cuenta: int = Form(),
    nombre_apellido_estudiante: str = Form(),
    dni: int = Form(),
    fecha_nacimiento: datetime = Form(),
    edad: int = Form(),
    direccion: str = Form(),
    barrio: str = Form(),
    celular: str = Form(),
    telefono: str = Form(),
    mail: str = Form(),
    curso: str = Form(),
    dia: str = Form(),
    hora_de_curso: str = Form(),
    fecha_de_inicio: datetime = Form(),
    vendedor: str = Form(),
    ciudad: str = Form(),
    plan: str = Form(),
    forma_de_pago: str = Form(),
    valor_cuotas: str = Form(),
    cantidad_de_cuotas: int = Form(),
    valor_certificado: float = Form(),
    abona_matricula: float = Form(),
    abona_cuota_1: float = Form(),
    abona_cuota_2: float = Form(),
    abona_certificado: float = Form()
):
    try:
        cursor = connection.cursor()

        sql = """
        INSERT INTO registros_estudiantes (Numero_Recibo, Numero_cuenta, Nombre_y_Apellido_estudiante, dni, Fecha_nacimiento, Edad, Direccion, Barrio, Celular, Telefono, Mail, Curso, Dia, Hora_de_Curso, Fecha_de_inicio, Vendedor, Ciudad, Plan, Forma_de_pago, Valor_cuotas, Cantidad_de_cuotas, Valor_certificado, Abona_matricula, Abona_cuota_1, Abona_cuota_2, Abona_certificado)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        registros_estudiantes = (
            numero_recibo, numero_cuenta, nombre_apellido_estudiante, dni, fecha_nacimiento, edad, direccion,
            barrio, celular, telefono, mail, curso, dia, hora_de_curso, fecha_de_inicio, vendedor, ciudad, plan,
            forma_de_pago, valor_cuotas, cantidad_de_cuotas, valor_certificado, abona_matricula, abona_cuota_1,
            abona_cuota_2, abona_certificado
        )

        cursor.execute(sql, registros_estudiantes)
        connection.commit()

        return RedirectResponse("/registrar_estudiantes")

    except mysql.connector.Error as ex:
        return {"error": f"Error al querer insertar datos en registros de estudiantes: {ex}"}

#Muestra los estudiantes cargados
@app.get("/estudiantes")
def get_estudiantes():
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM registros_estudiantes")
        estudiantes = cursor.fetchall()
        return {"estudiantes": estudiantes}
    except mysql.connector.Error as ex:
        return {"error": f"Error al obtener datos de estudiantes: {ex}"}

@app.get("/users", response_class=HTMLResponse)
def get_users(request: Request):
    return templates.TemplateResponse("inicio_sesion.html", {"request": request})

#Validación de usuarios
@app.post("/users")
def validar_users(
    usuarios: str = Form(),
    passwords: str = Form()
):
    if not usuarios or not passwords:
        return templates.TemplateResponse("inicio_sesion.html", {"request": Request})
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT nombre_usuarios, passwords FROM usuarios WHERE nombre_usuarios = %s"
        cursor.execute(query, (usuarios,))
        user = cursor.fetchone()

        if user and user["passwords"] == passwords:
            return "acceso concedido"
        else:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    except mysql.connector.Error as ex:
        raise HTTPException(status_code=500, detail=f"Error al autenticar credenciales: {ex}")
