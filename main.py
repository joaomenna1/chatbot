# -*- coding: utf-8 -*-

import datetime
import time
from wppbot import wppbot
from cliente import cliente
from datetime import date
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchAttributeException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotSelectableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementNotVisibleException
from urllib3.exceptions import ConnectionError

try:
    # instancia um objeto da classe wppbot
    bot = wppbot()
    # inicializa o whatsapp web
    bot.inicia()
except (WebDriverException, ConnectionError, ConnectionRefusedError, ConnectionResetError, ConnectionAbortedError, TimeoutException):
    print("Error!")

global Clientes, ClientesEsperando
Clientes = []
ClientesEsperando = []

# 1 - cliente sendo atendido pelo chatbot
# 0 - cliente esperando falar com atendente

def atualiza_listas_clientes(lst1, lst2, cliente_buscado):
    hora_atual = datetime.datetime.now().hour
    data_atual = date.today()
    data = "{}/{}".format(data_atual.day, data_atual.month)
    dia_atual, mes_atual = data.split('/')

    if (len(lst2) > 0 and cliente_buscado != None):
        if (cliente_buscado.estado == 0):
            if (hora_atual >= cliente_buscado.hora_inicio_atendimento + 1 and cliente_buscado.dia_inicio_atendimento == int(dia_atual) and cliente_buscado.mes_inicio_atendimento == int(mes_atual)):
                lst1.remove(cliente_buscado)
                lst2.remove(cliente_buscado)

def recupera_cliente_id(lst, id):
    cliente = None
    if (len(lst) > 0):
        for c in lst:
            if (c.id == id):
                cliente = c
    return cliente

try:
    while True:
        bot.driver.implicitly_wait(600)
        # seleciona a div de contatos
        div_contatos = bot.driver.find_element_by_class_name("_1H6CJ")
        # seleciona todos os contatos
        contatos = div_contatos.find_elements_by_class_name("X7YrQ")

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
            except (NoSuchElementException, StaleElementReferenceException, TimeoutException, WebDriverException) as error:
                clicou = False

            # se conseguiu clicar no contato, entao verifica se precisa fazer o atendimento
            if (clicou == True):
                print("Clicou")
                # recupera id do cliente
                id = bot.driver.find_element_by_class_name("_19vo_").get_attribute('innerText')
                time.sleep(2)

                j = 0

                tem_nova_mensagem = False
                encontrou_data = False
                enviar_saudacao = True

                mensagens = bot.driver.find_elements_by_class_name("FTBzM")
                ultimo = len(mensagens) - 1
                # seleciona a ultima mensagem
                ultima_mensagem = mensagens[ultimo]
                tipo_ultima_mensagem = ultima_mensagem.get_attribute('className')
                tipo_ultima_mensagem_2 = ultima_mensagem.find_element_by_class_name("_1zGQT").get_attribute('className')

                mensagens_pulsar = []
                #mensagens_pulsar = bot.driver.find_elements_by_class_name("_1zGQT _2ugFP message-out tail")
                while (j < len(mensagens)):
                    mensagem = mensagens[j]
                    tipo_ultima_mensagem = mensagem.get_attribute('className')
                    tipo_ultima_mensagem_2 = mensagem.find_element_by_class_name("_1zGQT").get_attribute('className')
                    if ('_2ugFP' in tipo_ultima_mensagem_2 and 'message-out' in tipo_ultima_mensagem):
                        mensagens_pulsar.append(mensagem)
                    j += 1

                # recupera hora, minuto atual (int)
                hora_atual = datetime.datetime.now().hour
                minuto_atual = datetime.datetime.now().minute

                # recupera dia, mes atual (string)
                data_atual = date.today()
                data = "{}/{}".format(data_atual.day, data_atual.month)
                dia_atual, mes_atual = data.split('/')

                if (len(mensagens) == 1):
                    # tem so uma mensagem e eh do cliente
                    if ('message-in' in tipo_ultima_mensagem):
                        tem_nova_mensagem = True
                elif (len(mensagens) > 1):
                    # nao eh a primeira mensagem desse cliente
                    # se a ultima mensagem eh do cliente
                    if ('message-in' in tipo_ultima_mensagem):
                        # recupera hora e minuto da mensagem (string)
                        div_tempo = ultima_mensagem.find_element_by_class_name("_3MYI2")
                        tempo_mensagem = str(div_tempo.get_attribute('innerText'))
                        hora_mensagem, minuto_mensagem = tempo_mensagem.split(':')

                        if ('_2ugFP' in tipo_ultima_mensagem_2):
                            # se a mensagem recebida for um texto, tenta recuperar a data
                            try:
                                div_dia = ultima_mensagem.find_element_by_class_name("copyable-text")
                                data_mensagem = str(div_dia.get_attribute('data-pre-plain-text'))
                                encontrou_data = True
                            except (NoSuchElementException, NoSuchAttributeException, AttributeError) as error:
                                print(str(error))

                        if (encontrou_data == True):
                            # recupera data mensagem (string)
                            data_mensagem = data_mensagem[8:18]
                            dia_mensagem, mes_mensagem, ano_mensagem = data_mensagem.split('/')

                            if (int(dia_atual) == int(dia_mensagem) and int(mes_atual) == int(mes_mensagem) and hora_atual == int(hora_mensagem) and minuto_atual <= int(minuto_mensagem) + 20):
                                # mensagem nova eh mensagem enviada nos ultimos 20 minutos
                                tem_nova_mensagem = True
                            elif (int(dia_atual) == int(dia_mensagem) and int(mes_atual) == int(mes_mensagem) and hora_atual == int(hora_mensagem) + 1):
                                diferenca = 60 - int(minuto_mensagem)
                                if (diferenca + minuto_atual < 20):
                                    tem_nova_mensagem = True

                            # verifica se enviou mensagens pra esse contato nesse dia
                            if (len(mensagens_pulsar) > 0):
                                ultimo_pulsar = len(mensagens_pulsar) - 1
                                ultima_mensagem_pulsar = mensagens_pulsar[ultimo_pulsar]

                                try:
                                    div_dia = ultima_mensagem_pulsar.find_element_by_class_name("copyable-text")
                                    data_mensagem = str(div_dia.get_attribute('data-pre-plain-text'))
                                    encontrou_data = True
                                except (NoSuchElementException, NoSuchAttributeException, AttributeError) as error:
                                    print(str(error))

                                if (encontrou_data == True):
                                    data_mensagem = data_mensagem[8:18]
                                    dia_mensagem, mes_mensagem, ano_mensagem = data_mensagem.split('/')

                                    if(int(dia_atual) == int(dia_mensagem) and int(mes_atual) == int(mes_mensagem)):
                                        enviar_saudacao = False

                # verifica se o id do cliente esta presente na lista de Clientes
                client = recupera_cliente_id(Clientes, id)

                # faz uma atualizacao das listas se o cliente esta esperando por atendimento humano ha muito tempo
                atualiza_listas_clientes(Clientes, ClientesEsperando, client)

                # se tem uma nova mensagem
                if(tem_nova_mensagem == True):
                    time.sleep(3)
                    hora_atual = datetime.datetime.now().hour
                    minuto_atual = datetime.datetime.now().minute

                    data_atual = date.today()
                    data = "{}/{}".format(data_atual.day, data_atual.month)
                    dia_atual, mes_atual = data.split('/')

                    # verifica se o id do cliente esta presente na lista de Clientes
                    client = recupera_cliente_id(Clientes, id)

                    # se o id nao esta presente na lista, cria o obj cliente e adiciona na lista
                    if (client == None):
                        client = cliente(id, hora_atual, minuto_atual, int(dia_atual), int(mes_atual))
                        Clientes.append(client)

                    # verifica se o cliente esta esperando atendimento humano
                    if (client.estado == 0):
                        cliente_esperando_atendimento_humano = True
                    elif (client.estado == 1):
                        cliente_esperando_atendimento_humano = False

                    # se o cliente nao esta esperando atendimento humano, entao ele vai conversar com o chatbot
                    if (cliente_esperando_atendimento_humano  == False):
                        # recupera a ultima mensagem da conversa
                        mensagens = bot.driver.find_elements_by_class_name("-N6Gq")
                        ultimo = len(mensagens) - 1
                        ultima_mensagem = mensagens[ultimo].find_element_by_class_name("_12pGw").get_attribute('innerText')
                        mensagem = ultima_mensagem

                        # se nao foi enviada nenhuma mensagem pro cliente hoje, significa que é preciso enviar saudacao
                        # se foi enviada alguma mensagem pro cliente hoje, significa que não é preciso enviar saudacao
                        if (enviar_saudacao == True):
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
                            if (len(mensagens) > 2):
                                antepenultimo = len(mensagens) - 3
                                antepenultima_mensagem = mensagens[antepenultimo].find_element_by_class_name("_12pGw").get_attribute('innerText')
                                encontrou_antepenultima_mensagem = True
                                print(encontrou_antepenultima_mensagem)
                            else:
                                encontrou_antepenultima_mensagem = False
                                print(encontrou_antepenultima_mensagem)

                            if (encontrou_antepenultima_mensagem == True):
                                # se antepenultima mensagem foi saudacao, entao a mensagem recebida é o nome do cliente
                                if (antepenultima_mensagem == bot.saudacao_manha or antepenultima_mensagem == bot.saudacao_tarde or antepenultima_mensagem == bot.saudacao_noite):
                                    nome = mensagem
                                    bot.menu(nome) # envia o menu para o cliente
                                else:
                                    # senao, a mensagem recebida é a opcao do menu selecionada
                                    opcao = mensagem

                                    # realiza tratamento da opcao selecionada pelo cliente
                                    if opcao == "0" or "zero" in opcao or 'ZERO' in opcao or 'Zero' in opcao:
                                        bot.menu()
                                    elif opcao == "01" or opcao == "1" or "um" in opcao or 'UM' in opcao or 'Um' in opcao or "Localização" in opcao or "Localizacao" in opcao or "localização" in opcao or "localizacao" in opcao:
                                        bot.localizacao()
                                    elif opcao == "02" or opcao == "2" or "dois" in opcao or 'DOIS' in opcao or 'Dois' in opcao or "Especialidades" in opcao or "especialidades" in opcao:
                                        bot.especialidades()
                                    elif opcao == "03" or opcao == "3" or "tres" in opcao or 'TRES' in opcao or 'Tres' in opcao or "Procedimentos" in opcao or "Procedimentos realizados" in opcao or "procedimentos realizados" in opcao or "Procedimentos Realizados" in opcao or "procedimentos" in opcao or "Procedimentos" in opcao:
                                        bot.procedimentos()
                                    elif opcao == "04" or opcao == "4" or "quatro" in opcao or 'QUATRO' in opcao or 'Quatro' in opcao or "Exames laboratoriais" in opcao or "Exames Laboratoriais" in opcao or "exames Laboratoriais" in opcao or "exames laboratoriais" in opcao or "exames" in opcao or "Exames" in opcao:
                                        bot.exames_laboratoriais()
                                    elif opcao == "05" or opcao == "5" or "cinco" in opcao or 'CINCO' in opcao or 'Cinco' in opcao or "agendamento" in opcao or "Agendamento" in opcao or "Falar com atendente" in opcao or "falar com atendente" in opcao or "Falar com atendente (agendamento)" in opcao or "falar com atendente (agendamento)" in opcao or "Falar com atendente(agendamento)" in opcao or "falar com atendente(agendamento)" in opcao or "atendente" in opcao:
                                        bot.atendimento()
                                        # muda o estado do cliente
                                        client.estado = 0
                                        # adiciona o cliente na lista de clientes esperando pra falar com atendimento humano
                                        ClientesEsperando.append(client)

                if (client != None):
                    if (client.estado == 0):
                        # se o cliente esta esperando por atendimento humano, entao desmarca a conversa
                        try:
                            ActionChains(bot.driver).context_click(contato).perform()
                            time.sleep(1)
                            contato.find_element_by_xpath("//*[text()='Marcar como não lida']").click()
                        except (WebDriverException, AttributeError, NoSuchAttributeException, ConnectionError, ElementNotVisibleException, ElementNotInteractableException, ElementNotSelectableException, ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException) as error:
                            print(str(error))
            time.sleep(1.5)
            i += 1
except (WebDriverException, ConnectionError, ConnectionRefusedError, ConnectionResetError, ConnectionAbortedError, TimeoutException, AttributeError, NoSuchAttributeException) as error:
    bot.encerra()