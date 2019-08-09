import datetime
from wppbot import wppbot
import time
from cliente import cliente
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

# instancia um objeto da classe wppbot
bot = wppbot('Chatbot')
# inicializa o whatsapp web
bot.inicia()

global Clientes
Clientes = []

while True:
    # seleciona a div de contatos
    div_contatos = bot.driver.find_element_by_class_name("_3La1s")
    # seleciona todos os contatos
    contatos = div_contatos.find_elements_by_class_name("X7YrQ")

    for contato in contatos:
        print("Entrou num contato")

        # verifica se tem uma nova mensagem desse contato
        try:
            elemento = contato.find_element_by_class_name("P6z4j")
            tem_mensagem_nova = True
        except (NoSuchElementException, StaleElementReferenceException) as error:
            tem_mensagem_nova = False

        # se tem uma nova mensagem desse contato entao verifica se o cliente esta esperando pra falar com atendente
        if (tem_mensagem_nova == True):

            # recupera o numero (contato nao salvo) ou nome (contato salvo)
            id = contato.find_element_by_class_name("_3NWy8").get_attribute('innerText')

            # recupera hora, minuto e segundo atual
            hora = datetime.datetime.now().hour
            minuto = datetime.datetime.now().minute
            segundo = datetime.datetime.now().second

            # verifica se o id do cliente esta presente na lista de Clientes
            client = cliente.recupera_cliente_id(Clientes, id)

            # se o id nao esta presente na lista, cria o obj cliente e adiciona na lista
            if (client == None):
                client = cliente(id, hora, minuto, segundo)
                Clientes.append(client)

            # verifica se o cliente esta esperando atendimento humano
            if (client.estado == 0):
                cliente_esperando_atendimento_humano = True
            else:
                cliente_esperando_atendimento_humano = False

            if (cliente_esperando_atendimento_humano == False):
                # entra no contato
                contato.click()

                # recupera a ultima mensagem da conversa
                mensagens = bot.driver.find_elements_by_class_name("_1zGQT")
                ultimo = len(mensagens) - 1
                ultima_mensagem = mensagens[ultimo].find_element_by_css_selector('span.selectable-text').text
                mensagem = ultima_mensagem

                # se precisa enviar saudacao pro cliente entao manda a mensagem
                if (bot.nao_enviou_saudacao()):
                    # envia saudacao
                    bot.saudacao()
                    if (hora >= 6 and hora <= 12):
                        ultima_mensagem = "Bom dia, aqui quem fala é o chatbot da Clínica Pulsar. Digite seu primeiro nome para que a gente possa salvar seu contato."
                    elif (hora >= 12 and hora <= 18):
                        ultima_mensagem = "Boa tarde, aqui quem fala é o chatbot da Clínica Pulsar. Digite seu primeiro nome para que a gente possa salvar seu contato."
                    else:
                        ultima_mensagem = "Boa noite, aqui quem fala é o chatbot da Clínica Pulsar. Digite seu primeiro nome para que a gente possa salvar seu contato."
                    mensagem = bot.escuta(ultima_mensagem)

                if (mensagem != None):
                    print("Mensagem diferente de None")

                    # procura pela penultima mensagem
                    mensagens = bot.driver.find_elements_by_class_name("_1zGQT")
                    if (len(mensagens) > 2):
                        print("Entrou no if")
                        penultimo = len(mensagens) - 2
                        penultima_mensagem = mensagens[penultimo].find_element_by_css_selector(
                            'span.selectable-text').text
                        encontrou_penultima_mensagem = True
                    else:
                        print("Entrou no else")
                        encontrou_penultima_mensagem = False

                    if (encontrou_penultima_mensagem == True):
                        # se penultima mensagem foi saudacao, entao a mensagem recebida é o nome do cliente
                        if (penultima_mensagem == "Bom dia, aqui quem fala é o chatbot da Clínica Pulsar. Digite seu primeiro nome para que a gente possa salvar seu contato." or penultima_mensagem == "Boa tarde, aqui quem fala é o chatbot da Clínica Pulsar. Digite seu primeiro nome para que a gente possa salvar seu contato." or penultima_mensagem == "Boa noite, aqui quem fala é o chatbot da Clínica Pulsar. Digite seu primeiro nome para que a gente possa salvar seu contato."):
                            nome = mensagem
                            # envia o menu para o cliente
                            bot.menu(nome)
                        else:
                            # senao, a mensagem recebida é a opção do menu selecionada
                            opcao = mensagem

                            # realiza tratamento da opcao selecionada pelo cliente
                            if opcao == "0" or opcao == "zero" or opcao == 'ZERO' or opcao == 'Zero':
                                bot.menu()
                            elif opcao == "01" or opcao == "1" or opcao == "um" or opcao == 'UM' or opcao == 'Um' or opcao == "Localização" or opcao == "Localizacao" or opcao == "localização" or opcao == "localizacao":
                                bot.localizacao()
                            elif opcao == "02" or opcao == "2" or opcao == "dois" or opcao == 'DOIS' or opcao == 'Dois' or opcao == "Especialidades" or opcao == "especialidades":
                                bot.especialidades()
                            elif opcao == "03" or opcao == "3" or opcao == "tres" or opcao == 'TRES' or opcao == 'Tres' or opcao == "Procedimentos" or opcao == "Procedimentos realizados" or opcao == "procedimentos realizados" or opcao == "Procedcimentos Realizados":
                                bot.exames()
                            elif opcao == "04" or opcao == "4" or opcao == "quatro" or opcao == 'QUATRO' or opcao == 'Quatro' or opcao == "Exames laboratoriais" or opcao == "Exames Laboratoriais" or opcao == "exames Laboratoriais" or opcao == "exames laboratoriais":
                                bot.exames_laboratoriais()
                            elif opcao == "05" or opcao == "5" or opcao == "cinco" or opcao == 'CINCO' or opcao == 'Cinco' or opcao == "agendamento" or opcao == "Agendamento" or opcao == "Falar com atendente" or opcao == "falar com atendente" or opcao == "Falar com atendente (agendamento)" or opcao == "falar com atendente (agendamento)" or opcao == "Falar com atendente(agendamento)" or opcao == "falar com atendente(agendamento)":
                                bot.atendimento()
                                client.estado = 0
                            elif opcao == "06" or opcao == "6" or opcao == "seis" or opcao == 'SEIS' or opcao == 'Seis' or opcao == "Contato" or opcao == "contato":
                                bot.mandar_contato()
                            else:
                                bot.invalido()