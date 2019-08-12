import os
import time
import datetime
from chatterbot import ChatBot
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from cliente import cliente

class wppbot:
    # caminho da aplicacao
    dir_path = os.getcwd()

    def __init__(self, nome_bot):
        self.bot = ChatBot(nome_bot)

        self.chrome = self.dir_path + '\chromedriver.exe'

        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r"user-data-dir=" + self.dir_path + "\profile\wpp")
        self.driver = webdriver.Chrome(self.chrome, chrome_options=self.options)

    # abre o whatsapp web
    def inicia(self):
        self.driver.get('https://web.whatsapp.com/')
        self.driver.implicitly_wait(15)
        time.sleep(3)

    # envia a primeira mensagem pra um contato
    def saudacao(self):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name("_3u328")
        hour = datetime.datetime.now().hour

        if (hour >= 6 and hour <= 12):
            mensagem = "Bom dia, aqui quem fala é o chatbot da Clínica Pulsar. Digite seu primeiro nome para que a gente possa salvar seu contato."
        elif (hour >= 12 and hour <= 18):
            mensagem = "Boa tarde, aqui quem fala é o chatbot da Clínica Pulsar. Digite seu primeiro nome para que a gente possa salvar seu contato."
        else:
            mensagem = "Boa noite, aqui quem fala é o chatbot da Clínica Pulsar. Digite seu primeiro nome para que a gente possa salvar seu contato."

        self.caixa_de_mensagem.send_keys(mensagem)
        time.sleep(2)
        self.botao_enviar = self.driver.find_element_by_class_name("_3M-N-")
        self.botao_enviar.click()
        time.sleep(2)

    def escuta(self, penultimo_texto):
        time.sleep(1)
        cronometro = 1
        mensagens = self.driver.find_elements_by_class_name("_1zGQT")
        mensagem = len(mensagens) - 1
        ultimo_texto = mensagens[mensagem].find_element_by_css_selector('span.selectable-text').text

        while (ultimo_texto == penultimo_texto):
            time.sleep(1)
            cronometro = cronometro + 1
            if (cronometro >= 3):
                break
            else:
                mensagens = self.driver.find_elements_by_class_name("_1zGQT")
                mensagem = len(mensagens) - 1
                penultimo_texto = ultimo_texto
                ultimo_texto = mensagens[mensagem].find_element_by_css_selector('span.selectable-text').text

        if (cronometro >= 3):
            return None
        else:
            return ultimo_texto

    # envia o menu para um contato
    def menu(self, nome_contato):
        img = self.dir_path + '\Pulsar-1.png'
        self.driver.find_element_by_css_selector('span[data-icon="clip"]').click()
        attach = self.driver.find_element_by_css_selector('input[type="file"]')
        attach.send_keys(img)
        time.sleep(2)

        self.caixa_de_mensagem = self.driver.find_element_by_class_name("_3u328")
        self.caixa_de_mensagem.send_keys(
            nome_contato + ", durante seu atendimento, escolha e digite uma das opções abaixo para dar continuidade ao seu atendimento: ")
        self.caixa_de_mensagem.send_keys(Keys.SHIFT, Keys.ENTER)
        self.caixa_de_mensagem.send_keys(Keys.SHIFT, Keys.ENTER)
        self.caixa_de_mensagem.send_keys("1 - Localização")
        self.caixa_de_mensagem.send_keys(Keys.SHIFT, Keys.ENTER)
        self.caixa_de_mensagem.send_keys("2 - Especialidades")
        self.caixa_de_mensagem.send_keys(Keys.SHIFT, Keys.ENTER)
        self.caixa_de_mensagem.send_keys("3 - Procedimentos realizados")
        self.caixa_de_mensagem.send_keys(Keys.SHIFT, Keys.ENTER)
        self.caixa_de_mensagem.send_keys("4 - Exames laboratoriais")
        self.caixa_de_mensagem.send_keys(Keys.SHIFT, Keys.ENTER)
        self.caixa_de_mensagem.send_keys("5 - Falar com atendente (agendamento)")
        self.caixa_de_mensagem.send_keys(Keys.SHIFT, Keys.ENTER)
        self.caixa_de_mensagem.send_keys("6 - Contato")

        time.sleep(2)
        self.botao_enviar = self.driver.find_element_by_class_name("_1g8sv")
        self.botao_enviar.click()
        time.sleep(2)

    def localizacao(self):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name("_3u328")
        localizacao = "https://goo.gl/maps/1EtJ8Hu5iiK2"
        self.caixa_de_mensagem.send_keys(localizacao)
        time.sleep(6)
        self.botao_enviar = self.driver.find_element_by_class_name("_3M-N-")
        self.botao_enviar.click()
        time.sleep(2)

    def especialidades(self):
        img = self.dir_path + '\Pulsar-2.png'
        self.driver.find_element_by_css_selector('span[data-icon="clip"]').click()
        attach = self.driver.find_element_by_css_selector('input[type="file"]')
        attach.send_keys(img)
        time.sleep(2)

        self.caixa_de_mensagem = self.driver.find_element_by_class_name("_3u328")
        self.caixa_de_mensagem.send_keys(
            "Aqui estão as especialidades médicas presentes aqui na Clínica Pulsar, que conta com profissionais altamente qualificados e humanizados para melhor atendê-lo.")

        time.sleep(2)
        self.botao_enviar = self.driver.find_element_by_class_name("_1g8sv")
        self.botao_enviar.click()
        time.sleep(2)

    def exames(self):
        img = self.dir_path + '\Pulsar-3.png'
        self.driver.find_element_by_css_selector('span[data-icon="clip"]').click()
        attach = self.driver.find_element_by_css_selector('input[type="file"]')
        attach.send_keys(img)
        time.sleep(2)

        self.caixa_de_mensagem = self.driver.find_element_by_class_name("_3u328")
        self.caixa_de_mensagem.send_keys(
            "Esses são os procedimentos realizados aqui na Clínica Pulsar. Entre em contato com um atendente e será um prazer recebê-lo.")
        time.sleep(2)
        self.botao_enviar = self.driver.find_element_by_class_name("_1g8sv")
        self.botao_enviar.click()
        time.sleep(2)

    def exames_laboratoriais(self):
        img = self.dir_path + '\Pulsar-4.png'
        self.driver.find_element_by_css_selector('span[data-icon="clip"]').click()
        attach = self.driver.find_element_by_css_selector('input[type="file"]')
        attach.send_keys(img)
        time.sleep(2)

        self.caixa_de_mensagem = self.driver.find_element_by_class_name("_3u328")
        self.caixa_de_mensagem.send_keys(
            "Nossos exames laboratoriais são realizados pelo nosso parceiro RB diagnósticos que utiliza a mais alta tecnologia do mercado e fornece aos nossos clientes atendimento humanizado e de qualidade.")
        self.caixa_de_mensagem.send_keys(Keys.SHIFT, Keys.ENTER)
        self.caixa_de_mensagem.send_keys("Entre em contato pelo número 991674868.")

        time.sleep(2)
        self.botao_enviar = self.driver.find_element_by_class_name("_1g8sv")
        self.botao_enviar.click()
        time.sleep(2)

    def atendimento(self):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name("_3u328")
        desmarcar = "Atendimento de segunda a sexta-feira das 7h às 18h e no sábado das 7h às 12h. Digite sua mensagem e " \
                    "aguarde alguns instantes para ser atendido."
        self.caixa_de_mensagem.send_keys(desmarcar)
        time.sleep(2)
        self.botao_enviar = self.driver.find_element_by_class_name("_3M-N-")
        self.botao_enviar.click()
        time.sleep(2)

    def mandar_contato(self):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name("_3u328")
        contato = "Atualmente você pode entrar em contato conosco pelos números: (92) 3347-0731, (92) 98146-0778, (92) 99223-9714."
        self.caixa_de_mensagem.send_keys(contato)
        time.sleep(2)
        self.botao_enviar = self.driver.find_element_by_class_name("_3M-N-")
        self.botao_enviar.click()
        time.sleep(2)

    def invalido(self):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name("_3u328")
        invalido = "Entrada inválida. Por favor, digite outra opção do nosso Menu."
        self.caixa_de_mensagem.send_keys(invalido)
        time.sleep(2)
        self.botao_enviar = self.driver.find_element_by_class_name("_3M-N-")
        self.botao_enviar.click()
        time.sleep(2)

    def nao_enviou_saudacao(self, client):
        encontrou = True
        hora_atual = datetime.datetime.now().hour

        time.sleep(6)
        mensagens = self.driver.find_elements_by_class_name("-N6Gq")

        tamanho = len(mensagens)
        controlador = 1

        while (controlador < tamanho):
            indice = tamanho - controlador

            div_texto = mensagens[indice].find_element_by_class_name("_12pGw")
            texto = div_texto.get_attribute('innerText')

            div_tempo = mensagens[indice].find_element_by_class_name("_1RNhZ")
            tempo_mensagem = div_tempo.get_attribute('innerText')
            hora_mensagem, minuto_mensagem = tempo_mensagem.split(':')

            if (texto == "Bom dia, aqui quem fala é o chatbot da Clínica Pulsar. Digite seu primeiro nome para que a gente possa salvar seu contato." or texto == "Boa tarde, aqui quem fala é o chatbot da Clínica Pulsar. Digite seu primeiro nome para que a gente possa salvar seu contato." or texto == "Boa noite, aqui quem fala é o chatbot da Clínica Pulsar. Digite seu primeiro nome para que a gente possa salvar seu contato."):
                if (hora_atual > int(hora_mensagem) + 6 or client.estado == 2):
                    # encontrou o cumprimento mas faz muito tempo ou o atendimento desse cliente ja foi finalizado, entao precisa cumprimentar de novo
                    encontrou = True
                    client.estado = 1
                else:
                    # encontrou o cumprimento mas faz pouco tempo ou o cliente ainda esta sendo atendido, entao ta escutando uma opcao do cliente
                    encontrou = False

            controlador += 1

        if (encontrou == True):
            return True
        else:
            return False