import time

class cliente:
    def __init__(self, nome, numero, estado, tempo):
        self.nome = nome
        self.numero = numero
        self.estado = estado
        self.tempo = tempo

    def calcula_tempo(self):
        return self.tempo