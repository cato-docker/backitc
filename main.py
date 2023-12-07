from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from datetime import date
import mysql.connector
import requests
import pdb
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/templates",StaticFiles(directory="templates"),name="style")

def calcular_edad(fecha_nacimiento):
    fecha_actual = datetime.now()
    edad = fecha_actual.year - fecha_nacimiento.year -((fecha_actual.month, fecha_actual.day)<(fecha_nacimiento.moth, fecha_nacimiento.day))
    return edad

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
        return templates.TemplateResponse("index.html", {"request": request, "success": True})
        #mensaje = "datos cargados exitosamente"
    else:
        return templates.TemplateResponse("index.html", {"request": request, "success": False})
        #None
    #return templates.TemplateResponse("index.html", {"request": request, "success_message": mensaje})

# class EstudiantesCreate(BaseModel):
#     numero_recibo: int
#     numero_cuenta: int
#     nombre_apellido_estudiante: str
#     dni: str
#     fecha_nacimiento: datetime
#     edad: int
#     direccion: str
#     barrio: str
#     celular: str
#     telefono: str
#     mail: str
#     curso: str
#     dia: str
#     hora_de_curso: str
#     fecha_de_inicio: datetime
#     vendedor: str
#     ciudad: str
#     plan: str
#     forma_de_pago: str
#     valor_cuotas: str
#     cantidad_de_cuotas: int
#     valor_certificado: int
#     abona_matricula: int
#     abona_cuota_1: int
#     abona_cuota_2: int
#     abona_certificado: int


@app.post("/registrar_estudiantes")
def registrar_estudiantes(
    
    # numero_recibo = estudiantes.numero_recibo
    # numero_cuenta = estudiantes.numero_cuenta
    # nombre_apellido_estudiante = estudiantes.nombre_apellido_estudiante
    # dni = estudiantes.dni
    # fecha_nacimiento = estudiantes.fecha_nacimiento
    # edad = estudiantes.edad
    # direccion = estudiantes.direccion
    # barrio = estudiantes.barrio
    # celular = estudiantes.celular
    # telefono = estudiantes.telefono
    # mail = estudiantes.mail
    # curso = estudiantes.curso
    # dia = estudiantes.dia
    # hora_de_curso = estudiantes.hora_de_curso
    # fecha_de_inicio = estudiantes.fecha_de_inicio
    # vendedor = estudiantes.vendedor
    # ciudad = estudiantes.ciudad
    # plan = estudiantes.plan
    # forma_de_pago = estudiantes.forma_de_pago
    # valor_cuotas = estudiantes.valor_cuotas
    # cantidad_de_cuotas = estudiantes.cantidad_de_cuotas
    # valor_certificado = estudiantes.valor_certificado
    # abona_matricula = estudiantes.abona_matricula
    # abona_cuota_1 = estudiantes.abona_cuota_1
    # abona_cuota_2 = estudiantes.abona_cuota_2
    # abona_certificado = estudiantes.abona_certificado
    # @app.post("/registrar_estudiantes")

    Número_recibo: int = Form(...),
    Número_cuenta: int = Form(...),
    nombre_y_apellido_estudiante: str = Form(...),
    dni: str = Form(...),
    fecha_nacimiento: datetime = Form(...),
    edad: int = Form(...),
    dirección: str = Form(...),
    barrio: str = Form(...),
    celular: str = Form(...),
    teléfono: str = Form(...),
    mail: str = Form(...),
    curso: str = Form(...),
    día: str = Form(...),
    hora_de_curso: str = Form(...),
    fecha_de_inicio: datetime = Form(...),
    vendedor: str = Form(...),
    ciudad: str = Form(...),
    plan: str = Form(...),
    forma_de_pago: str = Form(...),
    valor_cuotas: int = Form(...),
    cantidad_de_cuotas: int = Form(...),
    valor_certificado: int = Form(...),
    abona_matricula: int = Form(...),
    abona_cuota_1: int = Form(...),
    abona_cuota_2: int = Form(...),
    abona_certificado: int = Form(...)
):

    try:
        cursor = connection.cursor()

        sql = """
        INSERT INTO registros_estudiantes (Número_recibo, Número_cuenta, Nombre_y_Apellido_estudiante, dni, Fecha_nacimiento, Edad, Dirección, Barrio, Celular, Teléfono, Mail, Curso, Día, Hora_de_Curso, Fecha_de_inicio, Vendedor, Ciudad, Plan, Forma_de_pago, Valor_cuotas, Cantidad_de_cuotas, Valor_certificado, Abona_matricula, Abona_cuota_1, Abona_cuota_2, Abona_certificado)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        registros_estudiantes = (
            Número_recibo, Número_cuenta, nombre_y_apellido_estudiante, dni, fecha_nacimiento, edad, dirección,
            barrio, celular, teléfono, mail, curso, día, hora_de_curso, fecha_de_inicio, vendedor, ciudad, plan,
            forma_de_pago, valor_cuotas, cantidad_de_cuotas, valor_certificado, abona_matricula, abona_cuota_1,
            abona_cuota_2, abona_certificado
        )

        cursor.execute(sql, registros_estudiantes)
        connection.commit()

        #return {"mensaje": "Estudiante registrado exitosamente"}
        return RedirectResponse("/registrar_estudiantes")

    except mysql.connector.Error as ex:
        return {"error": f"Error al querer insertar datos en registros de estudiantes: {ex}"}


    

#Muestra los estudiantes cargados
@app.get("/estudiantes")
def get_estudiantes():
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT Número_cuenta, Nombre_y_Apellido_estudiante, Plan, Valor_cuotas  FROM registros_estudiantes WHERE Plan = 'Financiado'"
        "GROUP BY Número_cuenta,Nombre_y_Apellido_estudiante,Plan, Valor_cuotas;")
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
    usuarios: str = Form(),  passwords: str = Form()):
    #pdb.set_trace()
    
   

    if usuarios == ""  or passwords == "":
        return {"Mensaje":"Usuario y/o contraseña estan vacios"}
    # if usuarios == 'cato' and passwords == 'cat2015':
    #     return RedirectResponse("/registrar_estudiantes?success=True")
    
    
    
    
    if not usuarios or not passwords:
        raise HTTPException(status_code=400, detail="Usuario y contraseña son requeridos")
        #return {"mensaje":"Usuario y contraseña son requeridos"}

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT nombre_usuarios, passwords FROM usuarios WHERE nombre_usuarios = %s"
        cursor.execute(query, (usuarios,))
        user = cursor.fetchone()

        if user and user["passwords"] == passwords:
            #print("Redirigiendo a: /registrar_estudiantes")
            return RedirectResponse ("/registrar_estudiantes") # liena problematica
            #return JSONResponse({"mensaje": "Acceso concedido", "redirect": "/registrar_estudiantes"})

        else:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    except mysql.connector.Error as ex:
        raise HTTPException(status_code=500, detail=f"Error al autenticar credenciales: {ex}")
    
   
    