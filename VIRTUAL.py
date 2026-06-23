import json
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class AsistenteVirtualSalud:
    def __init__(self):
        self.usuarios = {}
        self.cargar_datos()
        self.vectorizer = TfidfVectorizer()
        
        # Base de conocimiento médica ampliada
        self.base_conocimiento = {
            "síntomas": {
                "fiebre": ["gripe", "resfriado", "covid-19", "infección", "dengue"],
                "dolor de cabeza": ["migraña", "tensión", "deshidratación", "sinusitis"],
                "tos": ["resfriado", "gripe", "covid-19", "alergias", "asma"],
                "dolor de garganta": ["faringitis", "amigdalitis", "resfriado", "covid-19"],
                "congestión nasal": ["resfriado", "sinusitis", "alergias"],
                "dolor muscular": ["gripe", "covid-19", "esfuerzo físico"],
                "fatiga": ["anemia", "covid-19", "depresión", "hipotiroidismo"],
                "náuseas": ["gastritis", "intoxicación", "migraña", "embarazo"],
                "dolor abdominal": ["gastritis", "apendicitis", "cólicos", "indigestión"],
                "mareos": ["presión baja", "deshidratación", "problemas de oído"],
                "erupción cutánea": ["alergia", "varicela", "dengue", "sarampión"],
                "sed excesiva": ["diabetes", "deshidratación"],
                "micción frecuente": ["diabetes", "infección urinaria"],
                "visión borrosa": ["diabetes", "hipertensión", "migraña"],
                "fatiga extrema": ["diabetes", "anemia", "hipotiroidismo"],
                "heridas que no cicatrizan": ["diabetes"],
                "dolor de cabeza persistente": ["hipertensión", "migraña", "tensión"],
                "mareos frecuentes": ["hipertensión", "problemas de oído", "anemia"],
                "dolor en el pecho": ["hipertensión", "problemas cardíacos", "ansiedad"],
                "latidos irregulares": ["hipertensión", "arritmia", "ansiedad"],
                "dificultad para respirar": ["hipertensión", "asma", "problemas cardíacos"]
            },
            "recomendaciones": {
                "gripe": [
                    "Descansar adecuadamente",
                    "Mantener una buena hidratación",
                    "Tomar antitérmicos si hay fiebre (paracetamol)",
                    "Usar ropa cómoda y mantener ambiente fresco"
                ],
                "resfriado": [
                    "Descanso adecuado",
                    "Tomar antihistamínicos si hay congestión",
                    "Hacer gárgaras con agua tibia y sal para dolor de garganta",
                    "Usar humidificador si hay congestión nasal"
                ],
                "covid-19": [
                    "Aislamiento preventivo",
                    "Realizar prueba PCR o de antígenos",
                    "Consulta médica urgente si hay dificultad para respirar",
                    "Monitorear saturación de oxígeno"
                ],
                "alergias": [
                    "Evitar alérgenos conocidos",
                    "Tomar antihistamínicos",
                    "Usar descongestionantes nasales si es necesario",
                    "Considerar visita al alergólogo"
                ],
                "gastritis": [
                    "Dieta blanda sin irritantes",
                    "Comer porciones pequeñas frecuentes",
                    "Evitar alcohol, café y tabaco",
                    "Considerar antiácidos bajo supervisión médica"
                ],
                "diabetes": [
       "Monitorear niveles de glucosa regularmente",
       "Mantener una dieta balanceada baja en azúcares",
       "Realizar actividad física regular",
       "Tomar medicamentos según prescripción médica",
       "Revisar pies diariamente para detectar heridas",
       "Programar chequeos oftalmológicos anuales"
   ],
   "hipertensión": [
       "Controlar la presión arterial regularmente",
       "Reducir el consumo de sal en las comidas",
       "Mantener un peso saludable",
       "Limitar el consumo de alcohol",
       "Evitar fumar",
       "Practicar técnicas de relajación para manejar el estrés",
       "Tomar medicamentos según prescripción médica"
   ]
            }
        }
        
        self.entrenar_modelo_recomendaciones()
    
    def cargar_datos(self):
        try:
            with open('datos_salud.json', 'r') as f:
                self.usuarios = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.usuarios = {}
    
    def guardar_datos(self):
        with open('datos_salud.json', 'w') as f:
            json.dump(self.usuarios, f, indent=4)
    
    def entrenar_modelo_recomendaciones(self):
        textos = []
        for enfermedad, recomendaciones in self.base_conocimiento["recomendaciones"].items():
            textos.append(f"{enfermedad} {' '.join(recomendaciones)}")
        self.vectorizer.fit(textos)
    
    def registrar_usuario_interactivo(self):
        print("\n" + "="*50)
        print(" REGISTRO DE NUEVO USUARIO ".center(50, '='))
        print("="*50 + "\n")
        
        id_usuario = input("Ingrese un ID de usuario: ")
        if id_usuario in self.usuarios:
            print("\n⚠️ Este ID de usuario ya existe. ¿Desea actualizar los datos? (s/n)")
            if input().lower() != 's':
                return
        
        nombre = input("Nombre completo: ")
        edad = input("Edad: ")
        genero = input("Género (M/F/O): ").upper()
        peso = input("Peso (kg): ")
        altura = input("Altura (cm): ")
        alergias = input("Alergias conocidas (separar por comas): ")
        medicamentos = input("Medicamentos actuales (separar por comas): ")
        condiciones = input("Condiciones médicas conocidas (separar por comas): ")
        
        self.usuarios[id_usuario] = {
            "nombre": nombre,
            "edad": edad,
            "genero": genero,
            "peso": peso,
            "altura": altura,
            "alergias": [a.strip() for a in alergias.split(',') if a.strip()],
            "medicamentos": [m.strip() for m in medicamentos.split(',') if m.strip()],
            "condiciones": [c.strip() for c in condiciones.split(',') if c.strip()],
            "historial": [],
            "ultima_consulta": None
        }
        
        self.guardar_datos()
        print(f"\n✅ Usuario {nombre} registrado exitosamente!")
    
    def registrar_sintomas_interactivo(self, id_usuario):
        if id_usuario not in self.usuarios:
            print("\n⚠️ Usuario no registrado. Por favor regístrese primero.")
            return
        
        usuario = self.usuarios[id_usuario]
        print(f"\n" + "="*50)
        print(f" REGISTRO DE SÍNTOMAS - {usuario['nombre'].upper()} ".center(50, '='))
        print("="*50 + "\n")
        
        print("Síntomas disponibles:")
        for i, sintoma in enumerate(self.base_conocimiento["síntomas"].keys(), 1):
            print(f"{i}. {sintoma.capitalize()}")
        
        print("\nIngrese los números de sus síntomas separados por comas (ej: 1,3,5)")
        seleccion = input("> ")
        
        try:
            indices = [int(i.strip())-1 for i in seleccion.split(',')]
            sintomas = list(self.base_conocimiento["síntomas"].keys())
            sintomas_seleccionados = [sintomas[i] for i in indices if 0 <= i < len(sintomas)]
        except:
            print("\n⚠️ Entrada inválida. Por favor intente nuevamente.")
            return
        
        if not sintomas_seleccionados:
            print("\n⚠️ No seleccionó ningún síntoma válido.")
            return
        
        intensidad = input("\nIntensidad general (1-10): ")
        duracion = input("Duración de los síntomas (ej: 2 días): ")
        notas = input("Notas adicionales: ")
        
        registro = {
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "síntomas": sintomas_seleccionados,
            "intensidad": intensidad,
            "duracion": duracion,
            "notas": notas,
            "recomendaciones": []
        }
        
        # Analizar síntomas
        posibles_condiciones = self.analizar_sintomas(sintomas_seleccionados)
        recomendaciones = self.generar_recomendaciones(posibles_condiciones)
        
        # Añadir advertencias por alergias
        for condicion in posibles_condiciones:
            if condicion in usuario['alergias']:
                recomendaciones.append(f"⚠️ ADVERTENCIA: Usted tiene alergia conocida a {condicion}")
        
        registro["posibles_condiciones"] = posibles_condiciones
        registro["recomendaciones"] = recomendaciones
        
        usuario["historial"].append(registro)
        usuario["ultima_consulta"] = registro["fecha"]
        self.guardar_datos()
        
        self.mostrar_recomendaciones(registro)
    
    def mostrar_recomendaciones(self, registro):
        print("\n" + "="*50)
        print(" RECOMENDACIONES DE SALUD ".center(50, '='))
        print("="*50 + "\n")
        
        print(f"Fecha: {registro['fecha']}")
        print(f"Síntomas: {', '.join(registro['síntomas'])}")
        
        print("\nPosibles condiciones:")
        for condicion in registro['posibles_condiciones']:
            print(f"- {condicion}")
        
        print("\nRecomendaciones:")
        for i, rec in enumerate(registro['recomendaciones'], 1):
            print(f"{i}. {rec}")
        
        print("\n" + "-"*50)
        print("Si los síntomas empeoran o persisten, consulte a un médico.")
        print("Estas recomendaciones no sustituyen una evaluación médica profesional.")
    
    def analizar_sintomas(self, sintomas):
        condiciones_posibles = set()
        for sintoma in sintomas:
            if sintoma.lower() in self.base_conocimiento["síntomas"]:
                for condicion in self.base_conocimiento["síntomas"][sintoma.lower()]:
                    condiciones_posibles.add(condicion)
        return list(condiciones_posibles)
    
    def generar_recomendaciones(self, condiciones):
        recomendaciones = []
        for condicion in condiciones:
            if condicion in self.base_conocimiento["recomendaciones"]:
                recomendaciones.extend(self.base_conocimiento["recomendaciones"][condicion])
        
        # Recomendaciones generales
        recomendaciones.append("Mantener una buena hidratación")
        recomendaciones.append("Descansar adecuadamente")
        recomendaciones.append("Evitar automedicarse sin supervisión médica")
        
        return list(set(recomendaciones))  # Eliminar duplicados
    
    def menu_principal(self):
        while True:
            print("\n" + "="*50)
            print(" ASISTENTE VIRTUAL DE SALUD ".center(50, '='))
            print("="*50 + "\n")
            print("1. Registrarse como nuevo usuario")
            print("2. Registrar síntomas (usuarios existentes)")
            print("3. Ver historial de salud")
            print("4. Salir")
            
            opcion = input("\nSeleccione una opción: ")
            
            if opcion == '1':
                self.registrar_usuario_interactivo()
            elif opcion == '2':
                id_usuario = input("Ingrese su ID de usuario: ")
                self.registrar_sintomas_interactivo(id_usuario)
            elif opcion == '3':
                id_usuario = input("Ingrese su ID de usuario: ")
                self.mostrar_historial(id_usuario)
            elif opcion == '4':
                print("\nGracias por usar el Asistente Virtual de Salud. ¡Cuídese!")
                break
            else:
                print("\n⚠️ Opción inválida. Por favor intente nuevamente.")
    
    def mostrar_historial(self, id_usuario):
        if id_usuario not in self.usuarios:
            print("\n⚠️ Usuario no encontrado.")
            return
        
        usuario = self.usuarios[id_usuario]
        print(f"\nHISTORIAL DE SALUD DE {usuario['nombre'].upper()}")
        print(f"Edad: {usuario['edad']} | Género: {usuario['genero']}")
        print(f"Alergias: {', '.join(usuario['alergias']) or 'Ninguna'}")
        print(f"Condiciones médicas: {', '.join(usuario['condiciones']) or 'Ninguna'}")
        print("\nConsultas anteriores:")
        
        for i, consulta in enumerate(usuario['historial'], 1):
            print(f"\nConsulta #{i} - {consulta['fecha']}")
            print(f"Síntomas: {', '.join(consulta['síntomas'])}")
            print(f"Diagnósticos posibles: {', '.join(consulta['posibles_condiciones'])}")
            print("Recomendaciones recibidas:")
            for rec in consulta['recomendaciones']:
                print(f"- {rec}")


# Ejecutar el asistente
if __name__ == "__main__":
    asistente = AsistenteVirtualSalud()
    asistente.menu_principal()