
class cliente:
    def __init__(self, id, hora, minuto, segundo):
        self.id = id
        self.hora_inicio_atendimento = hora
        self.minuto_inicio_atendimento = minuto
        self.segundo_inicio_atendimento = segundo
        self.estado = 1
    # 1 - sendo atendido pelo chatbot
    # 0 - esperando falar com atendente
    # -1 - atendimento foi finalizado


    def esta_na_lista(Clientes, cliente_buscado):
        esta_na_lista = False
        for c in Clientes:
            if(c.id == cliente_buscado.id):
                esta_na_lista = True
        return esta_na_lista

    def recupera_cliente_id(Clientes, id):
        cliente = None
        if (len(Clientes) > 0):
            for c in Clientes:
                if (c.id == id):
                    cliente = c
        return cliente

