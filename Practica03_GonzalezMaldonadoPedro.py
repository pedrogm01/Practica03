import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QComboBox
)

# Clase del Simulador de Procesos
class SimuladorDeProcesos(QWidget):
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.setWindowTitle("Simulador de Algoritmos de Planificación")
        self.setGeometry(100, 100, 800, 400)
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Combobox para seleccionar el algoritmo
        self.comboBox = QComboBox()
        self.comboBox.addItem("FIFO")
        self.comboBox.addItem("SJF")
        layout.addWidget(QLabel("Selecciona el algoritmo de simulación:"))
        layout.addWidget(self.comboBox)
        
        # Botón para ejecutar la simulación
        self.botonEjecutar = QPushButton("Ejecutar simulación")
        self.botonEjecutar.clicked.connect(self.ejecutar_simulacion)
        layout.addWidget(self.botonEjecutar)
        
        # Tabla para mostrar los resultados
        self.tabla = QTableWidget()
        layout.addWidget(self.tabla)
        
        # Mostrar layout
        self.setLayout(layout)
        self.procesos = []
    
    # Método para cargar los procesos desde un archivo .txt
    def cargar_procesos(self, algoritmo):
        nombre_archivo = f"{algoritmo}.txt"
        if not os.path.exists(nombre_archivo):
            print(f"Error: El archivo {nombre_archivo} no existe.")
            return
        
        self.procesos = []
        with open(nombre_archivo, 'r') as archivo:
            for linea in archivo:
                partes = linea.strip().split(',')
                if len(partes) != 3:
                    print(f"Error: La línea '{linea.strip()}' no tiene el formato correcto.")
                    continue
                nombre_proceso, duracion, orden_llegada = partes
                self.procesos.append((nombre_proceso, int(duracion), int(orden_llegada)))
    
    # Método para ejecutar la simulación de los algoritmos de planificación
    def ejecutar_simulacion(self):
        algoritmo = self.comboBox.currentText()
        
        # Cargar el archivo de acuerdo al algoritmo seleccionado
        self.cargar_procesos(algoritmo)
        if not self.procesos:
            return  # No se cargaron procesos
        
        if algoritmo == "FIFO":
            resultado = self.fifo()
        elif algoritmo == "SJF":
            resultado = self.sjf()
        
        self.mostrar_resultados_simulacion(resultado)
    
    # Algoritmo FIFO (First In, First Out)
    def fifo(self):
        procesos_ordenados = sorted(self.procesos, key=lambda x: x[2])  # Ordenar por tiempo de llegada
        return self.simular(procesos_ordenados)
    
    # Algoritmo SJF (Shortest Job First)
    def sjf(self):
        tiempo_actual = 0
        resultados = []
        procesos_restantes = sorted(self.procesos, key=lambda x: x[2])  # Ordenar inicialmente por tiempo de llegada
        
        while procesos_restantes:
            # Filtrar procesos que han llegado
            procesos_disponibles = [p for p in procesos_restantes if p[2] <= tiempo_actual]
            
            if procesos_disponibles:
                # Procesar el proceso con la duración más corta
                proceso_a_procesar = min(procesos_disponibles, key=lambda x: x[1])
                procesos_restantes.remove(proceso_a_procesar)
                
                nombre_proceso, duracion, orden_llegada = proceso_a_procesar
                inicio = tiempo_actual
                tiempo_actual += duracion
                fin = tiempo_actual
                
                resultados.append((nombre_proceso, duracion, orden_llegada, inicio, fin))
            else:
                # Si no hay procesos disponibles, avanzar el tiempo al próximo proceso
                tiempo_actual = min(procesos_restantes, key=lambda x: x[2])[2]
        
        return resultados
    
    # Método para simular la ejecución de los procesos
    def simular(self, procesos_ordenados):
        tiempo = 0
        registro_ejecucion = []
        
        for (nombre_proceso, duracion, orden_llegada) in procesos_ordenados:
            if tiempo < orden_llegada:
                tiempo = orden_llegada  # Esperar hasta que el proceso llegue
            inicio = tiempo
            tiempo += duracion
            fin = tiempo
            registro_ejecucion.append((nombre_proceso, duracion, orden_llegada, inicio, fin))  # Incluye el orden de llegada
            
        return registro_ejecucion
    
    # Mostrar los resultados de la simulación en la tabla
    def mostrar_resultados_simulacion(self, resultados):
        self.tabla.setRowCount(len(resultados))
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(["Proceso", "Duración", "Llegada", "Inicio", "Fin"])
        
        for i, (nombre_proceso, duracion, orden_llegada, inicio, fin) in enumerate(resultados):
            self.tabla.setItem(i, 0, QTableWidgetItem(nombre_proceso))
            self.tabla.setItem(i, 1, QTableWidgetItem(str(duracion)))
            self.tabla.setItem(i, 2, QTableWidgetItem(str(orden_llegada)))
            self.tabla.setItem(i, 3, QTableWidgetItem(str(inicio)))
            self.tabla.setItem(i, 4, QTableWidgetItem(str(fin)))

# Función principal
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = SimuladorDeProcesos()
    ventana.show()
    sys.exit(app.exec_())
