from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from datetime import date 
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from datetime import datetime
import mysql.connector
import requests
from fastapi import FastAPI


app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Conexión a la base de datos MySQL
configuracion_db = {
    'host': 'localhost',
    'user': 'root',
    'password': 'CmDmEmFm95',
    'database': 'registros_estudiantes_itc'  
}

try:
    connection = mysql.connector.connect(**configuracion_db)

    if connection.is_connected():
        print("Conexión exitosa")

except Exception as ex:
    print(ex)


    

#Formulario html
@app.get("/")
def index():
    return {"Mensaje": "Bienvenidos"}

#Validacion de DNI
def validar_dni(dni):
    url = f"https://informes.nosis.com/{dni}"
    response = requests.get(url)

    if "DNI VALIDO" in response.text:
        return True
    else:
        return False
@app.post("/validar_dni")
async def validar_dni_endpoint(dni: str = Form(...)):
    # Llama a la función de validación de DNI
    es_valido = validar_dni(dni)

    # Si el DNI es válido, devuelve un mensaje de éxito
    if es_valido:
        return {"mensaje": "El DNI es válido"}
    else:
        # Si el DNI no es válido, puedes levantar una excepción HTTP
        raise HTTPException(status_code=400, detail="El DNI no es válido")

@app.get("/registrar_estudiantes", response_class=HTMLResponse)
async def show_registration_form(request: Request, success: bool =None):

    if success:
        return templates.TemplateResponse("index.html",{"request": request})
    else:
        return templates.TemplateResponse("index.html", {"request": request, "success": False})


@app.post("/registrar_estudiantes")
def registrar_estudiantes(
    Número_recibo: int = Form(),
    Número_cuenta: int = Form(),
    Nombre_y_Apellido_estudiante: str = Form(),
    dni: int = Form(),
    Fecha_nacimiento: datetime = Form(),
    Edad: int = Form(),
    Dirección: str = Form(),
    Barrio: str = Form(),
    Celular: str = Form(),
    Teléfono: str = Form(),
    Mail: str = Form(),
    Curso: str = Form(),
    Día: str = Form(),
    Hora_de_Curso: str = Form(),
    Fecha_de_inicio: datetime = Form(),
    Vendedor: str = Form(),
    Ciudad: str = Form(),
    Plan: str = Form(),
    Forma_de_pago: str = Form(),
    Valor_cuotas: str = Form(),
    Cantidad_de_cuotas: int = Form(),
    Valor_certificado: float = Form(),
    Abona_matricula: float = Form(),
    Abona_cuota_1: float = Form(),
    Abona_cuota_2: float = Form(),
    Abona_certificado: float = Form()
):
    try:
        cursor = connection.cursor()

       

        sql = """
        INSERT INTO registros_estudiantes (Número_Recibo, Número_cuenta, Nombre_y_Apellido_estudiante, dni, Fecha_nacimiento, Edad, Dirección, Barrio, Celular, Teléfono, Mail, Curso, Día, Hora_de_Curso, Fecha_de_inicio, Vendedor, Ciudad, Plan, Forma_de_pago, Valor_cuotas, Cantidad_de_cuotas, Valor_certificado, Abona_matricula, Abona_cuota_1, Abona_cuota_2, Abona_certificado)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        registros_estudiantes = (Número_recibo, Número_cuenta, Nombre_y_Apellido_estudiante, dni, Fecha_nacimiento, Edad, Dirección, Barrio, Celular, Teléfono, Mail, Curso, Día, Hora_de_Curso, Fecha_de_inicio, Vendedor, Ciudad, Plan, Forma_de_pago, Valor_cuotas, Cantidad_de_cuotas, Valor_certificado, Abona_matricula, Abona_cuota_1, Abona_cuota_2, Abona_certificado)

        cursor.execute(sql, registros_estudiantes)
        connection.commit()

        #return {"Mensaje": "Datos de estudiantes ingresados correctamente"}
        return RedirectResponse("/registrar_estudiantes")
    
    except Exception as ex:
        return {"error": f"Error al querer insertar datos en registros de estudiantes: {ex}"}
    

@app.get("/estudiantes")
def get_estudiantes():
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM registros_estudiantes")
        estudiantes = cursor.fetchall()
        return {"estudiantes": estudiantes}
    except Exception as ex:
        return {"error": f"Error al obtener datos de estudiantes: {ex}"}



@app.get("/users", response_class=HTMLResponse)
def get_users(request: Request):
    return templates.TemplateResponse("inicio_sesion.html", {"request": request})

@app.post("/users")
def validar_users(
    Usuarios: str = Form(),
    Passwords: str = Form()
):
    if not Usuarios or not Passwords:
        return templates.TemplateResponse("inicio_sesion.html", {"request": Request})
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT nombre_usuarios, passwords FROM usuarios WHERE nombre_usuarios = %s"
        cursor.execute(query, (Usuarios,))  
        user = cursor.fetchone()

        if user and user["passwords"] == Passwords:
            return "acceso concedido"
        else:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error al autenticar credenciales: {ex}")
