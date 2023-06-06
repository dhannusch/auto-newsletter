class LoadingBar:
    def __init__(self, total=100, length=50, char='█'):
        self.total = total  # Total number of iterations
        self.length = length  # Length of the loading bar in characters
        self.char = char  # Character used to represent the progress
        self.progress = 0  # Current progress

    def update(self):
        self.progress += 1
        self.draw()

    def draw(self):
        filled_length = int(self.length * self.progress / self.total)
        bar = self.char * filled_length + '-' * (self.length - filled_length)
        percent = self.progress * 100 / self.total
        print(f'\r[{bar}] {percent:.2f}%', end='', flush=True)