import datetime

class cliente:
    def __init__(self, id, hora, minuto, segundo):
        self.id = id
        self.hora_inicio_atendimento = hora
        self.minuto_inicio_atendimento = minuto
        self.segundo_inicio_atendimento = segundo
        self.estado = 1


