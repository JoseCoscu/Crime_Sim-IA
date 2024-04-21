import threading
import time
import random as r


class TimeMeter:
    def __init__(self):
        self._lock = threading.Lock()
        self._global_time = 0

    def get_global_time(self):
        with self._lock:
            return self._global_time

    def increment_global_time(self, increment):
        with self._lock:
            self._global_time += increment


def time_updater(time_meter):
    while True:
        time.sleep(0.2)  # Espera 1 segundo
        time_meter.increment_global_time(1)  # Incrementa el tiempo global en 1 segundo


class MiClase:
    def __init__(self, name, time_meter):
        self.name = name
        self.time_meter = time_meter

    def do_something(self):
        while True:
            current_time = self.time_meter.get_global_time()
            print(f"{self.name} - Global Time: {current_time}")
            i = r.randint(1, 5)
            time.sleep(i)


# Creamos un objeto para el medidor de tiempo
# time_meter = TimeMeter()
#
# # Creamos un hilo para actualizar el tiempo
# time_updater_thread = threading.Thread(target=time_updater, args=(time_meter,))
# time_updater_thread.daemon = True  # El hilo se detendrá cuando el programa principal termine
# time_updater_thread.start()

# # Creamos instancias de las clases y las ejecutamos en hilos diferentes
# clase1 = MiClase("Clase1", time_meter)
# clase2 = MiClase("Clase2", time_meter)
#
# thread1 = threading.Thread(target=clase1.do_something)
# thread2 = threading.Thread(target=clase2.do_something)
#
# thread1.start()
# thread2.start()
#
# # Esperamos a que los hilos terminen
# thread1.join()
# thread2.join()
