from enum import Enum
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from datetime import datetime
import mysql.connector

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Conexión a la base de datos MySQL
configuracion_db = {
    'host': 'localhost',
    'user': 'root',
    'password': 'CmDmEmFm95',
    'database': 'registros_estudiantes_itc'  # Nombre de la base de datos corregido
}

try:
    connection = mysql.connector.connect(**configuracion_db)

    if connection.is_connected():
        print("Conexión exitosa")

except Exception as ex:
    print(ex)

# class DiasSemana(str,Enum):
#     Lunes = 'Lunes'
#     Martes = 'Martes'
#     Miercoles = 'Miércoles'
#     Jueves = 'Jueves'
#     Viernes = 'Viernes'

def convertir_fecha_formato(fecha_texto):
    try:
        # Intenta convertir la fecha en formato DD-MMMM-YYYY a YYYY-MM-DD
        fecha_obj = datetime.strptime(fecha_texto, "%d-%B-%Y")
        return fecha_obj.date()
    except ValueError:
        return None
    
def calcular_edad(fecha_nacimiento):
    today = datetime.today()
    age = today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return age
#Formulario html
@app.get("/registrar_estudiantes", response_class=HTMLResponse)
async def show_registration_form(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})

@app.get("/")
def index():
    return {"Mensaje": "Bienvenidos"}

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

        fecha_de_inicio = convertir_fecha_formato(fecha_de_inicio)
        if fecha_de_inicio is None:
            return {"error":"Formato de fecha incorrecto"}
        
        Edad = calcular_edad(Fecha_nacimiento)

        sql = """
        INSERT INTO registros_estudiantes (Número_Recibo, Número_cuenta, Nombre_y_Apellido_estudiante, dni, Fecha_nacimiento, Edad, Dirección, Barrio, Celular, Teléfono, Mail, Curso, Día, Hora_de_Curso, Fecha_de_inicio, Vendedor, Ciudad, Plan, Forma_de_pago, Valor_cuotas, Cantidad_de_cuotas, Valor_certificado, Abona_matricula, Abona_cuota_1, Abona_cuota_2, Abona_certificado)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        registros_estudiantes = (Número_recibo, Número_cuenta, Nombre_y_Apellido_estudiante, dni, Fecha_nacimiento, Edad, Dirección, Barrio, Celular, Teléfono, Mail, Curso, Día, Hora_de_Curso, Fecha_de_inicio, Vendedor, Ciudad, Plan, Forma_de_pago, Valor_cuotas, Cantidad_de_cuotas, Valor_certificado, Abona_matricula, Abona_cuota_1, Abona_cuota_2, Abona_certificado)

        cursor.execute(sql, registros_estudiantes)
        connection.commit()

        return {"Mensaje": "Datos de estudiantes ingresados correctamente"}
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
    

@app.get ("/users",response_class=HTMLResponse)
async def show_registration_form(request: Request):
    extensions = request.extensions
    return templates.TemplateResponse("inicio_sesion.html",{"request": request, "extensions": extensions})

#Validar usuarios
@app.post("/users")
def show_users(
    
    Usuario: str = Form(None),
    Passwords: str = Form(None)
):
    if not Usuario or not Passwords:
        return templates.TemplateResponse("inicio_sesion.html",{"request":Request})
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT nombre_usuarios, passwords FROM usuarios WHERE nombre_usuarios = %s"
        cursor.execute(query, (Usuario,))
        user = cursor.fetchone()

        if user and user["passwords"] == Passwords:
            return RedirectResponse("/registrar_estudiantes")
        else:
             raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Error al autenticar usuario: {ex}")


        
    
        
    


