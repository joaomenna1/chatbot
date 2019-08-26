# -*- coding: utf-8 -*-

import datetime
import time
from wppbot import wppbot
from cliente import cliente
from datetime import date
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

# instancia um objeto da classe wppbot
bot = wppbot('Chatbot')
# inicializa o whatsapp web
bot.inicia()

global Clientes, ClientesEsperando
Clientes = []
ClientesEsperando = []

# 1 - cliente sendo atendido pelo chatbot
# 0 - cliente esperando falar com atendente
# 2 - cliente com atendimento finalizado (ja falou com atendimento humano)

def atualiza_listas_clientes(lst1, lst2, cliente_buscado):
    hora = datetime.datetime.now().hour
    data_atual = date.today()
    data = "{}/{}".format(data_atual.day, data_atual.month)
    dia_atual, mes_atual = data.split('/')

    if (len(lst2) > 0 and cliente_buscado.estado == 0):
        if (hora > cliente_buscado.hora_inicio_atendimento + 6 and (cliente_buscado.dia_inicio_atendimento == int(dia_atual) and cliente_buscado.mes_inicio_atendimento == int(mes_atual))):
            cliente_buscado.estado = 2
            lst1.remove(cliente_buscado)
            lst2.remove(cliente_buscado)

def recupera_cliente_id(lst, id):
    cliente = None
    if (len(lst) > 0):
        for c in lst:
            if (c.id == id):
                cliente = c
    return cliente

while True:
    # seleciona a div de contatos
    div_contatos = bot.driver.find_element_by_class_name("_3La1s")
    # seleciona todos os contatos
    contatos = div_contatos.find_elements_by_class_name("_2UaNq")

    # tamanho da amostra
    tamanho = len(contatos)
    i = 0

    while i < tamanho:
        # seleciona um contato em especifico dessa lista
        contato = contatos[i]

        try:
            # tenta clicar no contato
            contato.click()
            clicou = True
        except (NoSuchElementException, StaleElementReferenceException) as error:
            clicou = False

        # se conseguiu clicar no contato, entao verifica se precisa fazer o atendimento
        if (clicou == True):
            print("Clicou")
            time.sleep(2)
            tem_nova_mensagem = False

            mensagens = bot.driver.find_elements_by_class_name("_1zGQT")
            ultimo = len(mensagens) - 1
            # seleciona a ultima mensagem
            ultima_mensagem = mensagens[ultimo]
            tipo_ultima_mensagem = ultima_mensagem.get_attribute('className')

            # recupera hora, minuto atual
            hora_atual = datetime.datetime.now().hour
            minuto_atual = datetime.datetime.now().minute
            segundo_atual = datetime.datetime.now().second

            if (len(mensagens) > 1):
                # nao eh a primeira mensagem desse cliente
                # texto_ultima_mensagem = ultima_mensagem.find_element_by_css_selector('span.selectable-text').text
                print("Entrou no if")
                # se a ultima mensagem eh do cliente
                if ('message-in' in tipo_ultima_mensagem):
                    print("Ultima mensagem da pessoa")
                    # recupera hora e minuto da mensagem
                    div_tempo = ultima_mensagem.find_element_by_class_name("_3MYI2")
                    tempo_mensagem = div_tempo.get_attribute('innerText')
                    hora_mensagem, minuto_mensagem = tempo_mensagem.split(':')
                    # print(hora_mensagem + ":" + minuto_mensagem)
                    if (hora_atual == int(hora_mensagem) and minuto_atual <= int(minuto_mensagem) + 10):
                        # mensagem enviada nos ultimos 10 minutos
                        tem_nova_mensagem = True
                        print("Tem mensagem nova")
            else:
                # tem so uma mensagem e eh do cliente
                if ('message-in' in tipo_ultima_mensagem):
                    tem_nova_mensagem = True
                    print("Tem mensagem nova")

            # recupera o numero (contato nao salvo) ou nome (contato salvo)
            id = contato.find_element_by_class_name("_3NWy8").get_attribute('innerText')
            # verifica se o id do cliente esta presente na lista de Clientes
            client = recupera_cliente_id(Clientes, id)

            # se tem uma nova mensagem
            if(tem_nova_mensagem == True):
                data_atual = date.today()
                data = "{}/{}".format(data_atual.day, data_atual.month)
                dia_atual, mes_atual = data.split('/')

                # se o id nao esta presente na lista, cria o obj cliente e adiciona na lista
                if (client == None):
                    client = cliente(id, hora_atual, minuto_atual, int(dia_atual), int(mes_atual))
                    Clientes.append(client)

                # verifica se o cliente esta esperando atendimento humano
                if (client.estado == 0):
                    cliente_esperando_atendimento_humano = True
                else:
                    cliente_esperando_atendimento_humano = False

                # faz uma atualizacao das listas se o cliente esta esperando por atendimento humano ha muito tempo
                atualiza_listas_clientes(Clientes, ClientesEsperando, client)

                # se o cliente nao esta esperando atendimento humano, entao ele vai conversar com o chatbot
                if (cliente_esperando_atendimento_humano == False):
                    # recupera a ultima mensagem da conversa
                    mensagens = bot.driver.find_elements_by_class_name("-N6Gq")
                    ultimo = len(mensagens) - 1
                    ultima_mensagem = mensagens[ultimo].find_element_by_class_name("_12pGw").get_attribute('innerText')
                    mensagem = ultima_mensagem

                    # se precisa enviar saudacao pro cliente entao manda a mensagem
                    if (bot.enviar_saudacao(client)):
                        bot.saudacao()

                        if (hora_atual >= 6 and hora_atual <= 12):
                            ultima_mensagem = bot.saudacao_manha
                        elif (hora_atual >= 12 and hora_atual <= 18):
                            ultima_mensagem = bot.saudacao_tarde
                        else:
                            ultima_mensagem = bot.saudacao_noite

                        mensagem = bot.escuta(ultima_mensagem)

                    # se a mensagem existir
                    if (mensagem != None):
                        # procura pela antepenultima mensagem
                        mensagens = bot.driver.find_elements_by_class_name("-N6Gq")
                        if (len(mensagens) > 3):
                            antepenultimo = len(mensagens) - 3
                            antepenultima_mensagem = mensagens[antepenultimo].find_element_by_class_name("_12pGw").get_attribute('innerText')
                            encontrou_antepenultima_mensagem = True
                        else:
                            encontrou_antepenultima_mensagem = False

                        if (encontrou_antepenultima_mensagem == True):
                            # se antepenultima mensagem foi saudacao, entao a mensagem recebida é o nome do cliente
                            if (antepenultima_mensagem == bot.saudacao_manha or antepenultima_mensagem == bot.saudacao_tarde or antepenultima_mensagem == bot.saudacao_noite):
                                nome = mensagem
                                bot.menu(nome) # envia o menu para o cliente
                            else:
                                # senao, a mensagem recebida é a opcao do menu selecionada
                                opcao = mensagem

                                # realiza tratamento da opcao selecionada pelo cliente
                                if opcao == "0" or opcao == "zero" or opcao == 'ZERO' or opcao == 'Zero':
                                    bot.menu()
                                elif opcao == "01" or opcao == "1" or opcao == "um" or opcao == 'UM' or opcao == 'Um' or opcao == "Localização" or opcao == "Localizacao" or opcao == "localização" or opcao == "localizacao":
                                    bot.localizacao()
                                elif opcao == "02" or opcao == "2" or opcao == "dois" or opcao == 'DOIS' or opcao == 'Dois' or opcao == "Especialidades" or opcao == "especialidades":
                                    bot.especialidades()
                                elif opcao == "03" or opcao == "3" or opcao == "tres" or opcao == 'TRES' or opcao == 'Tres' or opcao == "Procedimentos" or opcao == "Procedimentos realizados" or opcao == "procedimentos realizados" or opcao == "Procedcimentos Realizados":
                                    bot.procedimentos()
                                elif opcao == "04" or opcao == "4" or opcao == "quatro" or opcao == 'QUATRO' or opcao == 'Quatro' or opcao == "Exames laboratoriais" or opcao == "Exames Laboratoriais" or opcao == "exames Laboratoriais" or opcao == "exames laboratoriais":
                                    bot.exames_laboratoriais()
                                elif opcao == "05" or opcao == "5" or opcao == "cinco" or opcao == 'CINCO' or opcao == 'Cinco' or opcao == "agendamento" or opcao == "Agendamento" or opcao == "Falar com atendente" or opcao == "falar com atendente" or opcao == "Falar com atendente (agendamento)" or opcao == "falar com atendente (agendamento)" or opcao == "Falar com atendente(agendamento)" or opcao == "falar com atendente(agendamento)":
                                    bot.atendimento()
                                    # faz a atualizacao da hora, minuto e segundo atual
                                    client.hora_inicio_atendimento = hora_atual
                                    client.minuto_inicio_atendimento = minuto_atual
                                    # muda o estado do cliente
                                    client.estado = 0
                                    # adiciona o cliente na lista de clientes esperando pra falar com atendimento humano
                                    ClientesEsperando.append(client)
                # se o cliente esta esperando por atendimento humano, entao desmarca a conversa
            if (client != None):
                if (client.estado == 0):
                    ActionChains(bot.driver).context_click(contato).perform()
                    time.sleep(1)
                    contato.find_element_by_xpath("//*[text()='Marcar como não lida']").click()
        print("")
        i += 1