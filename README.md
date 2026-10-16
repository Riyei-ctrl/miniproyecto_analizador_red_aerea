# Analizador de la Red Aérea Mundial
Miniproyecto - Estructuras de Datos
**TecNM / Instituto Tecnológico de Orizaba**

Sistema desarrollado en Python con estructuras de datos enlazadas implementadas a mano para analizar rutas aéreas, calcular itinerarios y realizar comparativas de rendimiento frente a arreglos contiguos.

---

## 🛠️ Requisitos Previos
* Tener instalado **Python 3.8 o superior**.
* Tener instalada la librería **Pandas** (únicamente requerida para la fase ETL de carga inicial):
  pip install pandas

# Instrucciones de Ejecución
1. Clonar el repositorio
Abre tu terminal y clona el proyecto en la computadora:
**git clone https://github.com/Riyei-ctrl/miniproyecto_analizador_red_aerea.git**

2. Ejecutar el Sistema Principal (Menú Interactivo)
Para probar la localización de rutas por aeropuerto y el cálculo recursivo de itinerarios, ejecuta:
**python main.py**

3. Ejecutar el Análisis de Rendimiento (Benchmarking)
Para generar los datos de la comparativa de complejidad entre la estructura enlazada y el arreglo contiguo, ejecuta:
**python benchmarking.py**