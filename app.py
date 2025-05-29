import streamlit as st
import serial
import time

# Configuración del puerto serial
try:
    ser = serial.Serial('COM3', 9600, timeout=1)  # Cambia 'COM3' según tu sistema
    time.sleep(2)  # Espera a que el puerto serial se inicialice
except serial.SerialException:
    st.error("Error: No se pudo conectar con Arduino. Verifica el puerto.")
    ser = None

# Función para leer datos del Arduino
def read_arduino():
    if ser and ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        if line.startswith("SLOTS:"):
            try:
                slots = int(line.split(",")[0].split(":")[1])
                smoke = int(line.split(",")[1].split(":")[1])
                return slots, smoke
            except:
                return None, None
    return None, None

# Función para enviar comando al Arduino
def send_command(command):
    if ser:
        ser.write((command + '\n').encode('utf-8'))

# Interfaz de Streamlit
st.title("Sistema de Estacionamiento Arduino")

# Estado de los lugares disponibles
slots_placeholder = st.empty()
smoke_placeholder = st.empty()
control_button = st.button("Abrir Barrera")

# Bucle principal para actualización en tiempo real
while True:
    slots, smoke = read_arduino()
    if slots is not None:
        slots_placeholder.write(f"Lugares disponibles: **{slots}**")
    if smoke is not None:
        if smoke == 1:
            smoke_placeholder.error("🚨 ¡Humo detectado!")
        else:
            smoke_placeholder.success("✅ Sin humo detectado")

    if control_button:
        send_command("OPEN")
        st.success("Barrera abierta por 1 segundo")

    time.sleep(0.5)  # Actualizar cada 0.5 segundos
