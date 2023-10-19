import multiprocessing
import subprocess


if __name__ == '__main__':
    # Inicia a aplicação Flask em um processo separado
    flask_process = multiprocessing.Process(target=subprocess.run, args=(['python', 'rotas.py'],)) 

    # Inicia a interface Kivy em um processo separado
    kivy_process = multiprocessing.Process(target=subprocess.run, args=(['python', 'main.py'],))

    # Inicia os dois processos
    flask_process.start()
    kivy_process.start()

    # Espera até que os processos terminem
    flask_process.join()
    kivy_process.join()
