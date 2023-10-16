import unittest
from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)

class TestValidarDniEndpoint(unittest.TestCase): 
    def test_validar_dni_endpoint(self):  
        response = client.post("/validar_dni", data={"dni": "36852147"})
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["mensaje"], "El DNI es válido")
    
    def test_registrar_estudiantes_endpoint(self):
        data = {
            "numero_recibo": 1,
            "numero_cuenta": 2,
            "nombre_apellido_estudiantes": 'juan perez',
            "dni": 36258741,
            "fecha_nacimiento": '17/03/1995',
            "edad": 28,
            "direccion": 'av siempre viva',
            "barrio": 'el chucaro',
            "celular": 11587496,
            "telefono": 4805236,
            "mail": 'prueba@gmail.com',
            "curso": 'Robotica',
            "dia": 'Lunes',
            "hora_de_curso": '21:00hs a 22:30hs',
            "fecha_de_inicio": '10/10/2023',
            "vendedor": 'camila lopez',
            "ciudad": 'charata',
            "plan": 'financiado',
            "forma_de_pago": 'efectivo',
            "valor_cuotas": 22500,
            "cantidad_de_cuotas": 7,
            "valor_certificado": 15500,
            "abona_matricula": 0,
            "abona_cuota_1": 0,
            "abona_cuota_2": 0,
            "abona_certificado": 15500
        }

        response = client.post("/registrar_estudiantes", data=data)
        self.assertEqual(response.status_code, 307)


if __name__ == '__main__':
    unittest.main()
