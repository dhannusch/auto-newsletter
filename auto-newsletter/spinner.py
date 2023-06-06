import threading
import time

class Spinner:
    def __init__(self):
        self.spinner_thread = None
        self.is_running = False

    def _spin(self):
        while self.is_running:
            for char in '|/-\\':
                if self.is_running:
                    print(char, end='\r')
                    time.sleep(0.1)

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.spinner_thread = threading.Thread(target=self._spin)
            self.spinner_thread.start()

    def stop(self):
        if self.is_running:
            self.is_running = False
            self.spinner_thread.join()
            print(' ' * len('|/-\\'), end='\r')