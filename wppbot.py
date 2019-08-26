# -*- coding: utf-8 -*-
import os
import time
import datetime
from chatterbot import ChatBot
from selenium import webdriver
from cliente import cliente
from datetime import date
from selenium.webdriver.common.keys import Keys

class wppbot:
    # caminho da aplicacao
    dir_path = os.getcwd()

    # mensagens padronizadas
    saudacao_manha = "Bom dia, aqui quem fala é o chatbot da Clínica Pulsar. Digite seu nome completo para que a gente possa salvar seu contato."
    saudacao_tarde = "Boa tarde, aqui quem fala é o chatbot da Clínica Pulsar. Digite seu nome completo para que a gente possa salvar seu contato."
    saudacao_noite = "Boa noite, aqui quem fala é o chatbot da Clínica Pulsar. Digite seu nome completo para que a gente possa salvar seu contato."

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
            mensagem = self.saudacao_manha
        elif (hour >= 12 and hour <= 18):
            mensagem = self.saudacao_tarde
        else:
            mensagem = self.saudacao_noite

        self.caixa_de_mensagem.send_keys(mensagem)
        time.sleep(1)
        self.botao_enviar = self.driver.find_element_by_class_name("_3M-N-")
        self.botao_enviar.click()

        self.caixa_de_mensagem.send_keys("Para mais informações, entrar em contato pelos números: ")
        self.caixa_de_mensagem.send_keys(Keys.SHIFT, Keys.ENTER)
        self.caixa_de_mensagem.send_keys("Fixo: (92) 3347-0731 ")
        self.caixa_de_mensagem.send_keys(Keys.SHIFT, Keys.ENTER)
        self.caixa_de_mensagem.send_keys("Tim: (92) 98146-0778 ")
        self.caixa_de_mensagem.send_keys(Keys.SHIFT, Keys.ENTER)
        self.caixa_de_mensagem.send_keys("Vivo: (92) 99223-9714")
        time.sleep(1)
        self.botao_enviar = self.driver.find_element_by_class_name("_3M-N-")
        self.botao_enviar.click()

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

        time.sleep(2)
        self.botao_enviar = self.driver.find_element_by_class_name("_1g8sv")
        self.botao_enviar.click()

    def localizacao(self):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name("_3u328")
        localizacao = "https://goo.gl/maps/1EtJ8Hu5iiK2"
        self.caixa_de_mensagem.send_keys(localizacao)
        time.sleep(6)
        self.botao_enviar = self.driver.find_element_by_class_name("_3M-N-")
        self.botao_enviar.click()

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

    def procedimentos(self):
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

    def exames_laboratoriais(self):
        img = self.dir_path + '\Pulsar-4.png'
        self.driver.find_element_by_css_selector('span[data-icon="clip"]').click()
        attach = self.driver.find_element_by_css_selector('input[type="file"]')
        attach.send_keys(img)
        time.sleep(2)

        self.caixa_de_mensagem = self.driver.find_element_by_class_name("_3u328")
        self.caixa_de_mensagem.send_keys(
            "Nossos exames laboratoriais são realizados pelo nosso parceiro RB diagnósticos que utiliza a mais alta tecnologia do mercado e fornece aos nossos clientes atendimento humanizado e de qualidade.")
        time.sleep(2)
        self.botao_enviar = self.driver.find_element_by_class_name("_1g8sv")
        self.botao_enviar.click()

        # seleciona o clip pra enviar um anexo
        self.botao_clip = self.driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/div/span')
        self.botao_clip.click()
        time.sleep(1)
        # seleciona a opcao pra enviar contato
        self.botao_contato = self.driver.find_element_by_xpath('//*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[4]/button')
        self.botao_contato.click()
        time.sleep(1)
        # procura na caixa de pesquisa pelo nome do contato
        self.caixa_contato = self.driver.find_element_by_class_name("aymnx")
        self.caixa_pesquisa = self.caixa_contato.find_element_by_class_name("_2zCfw")
        self.caixa_pesquisa.send_keys("RB Diagnósticos")
        time.sleep(1)
        # clica no contato
        self.contato = self.driver.find_element_by_xpath('//span[@title = "{}"]'.format("RB Diagnósticos"))
        self.contato.click()
        # envia o contato
        self.botao_visualizar = self.driver.find_element_by_class_name("_1g8sv")
        self.botao_visualizar.click()
        time.sleep(1)
        self.botao_enviar_definitivo = self.driver.find_element_by_class_name("_1g8sv")
        self.botao_enviar_definitivo.click()

    def atendimento(self):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name("_3u328")
        desmarcar = "Atendimento de segunda a sexta-feira das 7h às 18h e no sábado das 7h às 12h. Digite sua mensagem e " \
                    "aguarde alguns instantes para ser atendido ou entre em contato pelos nossos telefones."
        self.caixa_de_mensagem.send_keys(desmarcar)
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

    def enviar_saudacao(self, client):
        hora_atual = datetime.datetime.now().hour
        data_atual = date.today()
        data = "{}/{}".format(data_atual.day, data_atual.month)
        dia_atual, mes_atual = data.split('/')

        time.sleep(7)
        mensagens = self.driver.find_elements_by_class_name("-N6Gq")
        tamanho = len(mensagens)

        if (tamanho == 1):
            # primeiro contato do cliente, entao envia saudacao
            return True
        elif (client.estado == 1):
            # nao eh primeiro contato do cliente, mas faz muito tempo que enviei a saudacao hoje
            if (hora_atual >= client.hora_inicio_atendimento + 8 and client.dia_inicio_atendimento == int(dia_atual) and client.mes_inicio_atendimento == int(mes_atual)):
                return True
            else:
                return False
        elif (client.estado == 2):
            # o cliente ja teve seu atendimento finalizado e enviou uma nova mensagem, entao troca o estado dele e envia a saudacao
            client.estado = 1
            return True
        else:
            # nao eh o primeiro contato do cliente e enviou a saudacao ha pouco tempo, entao nao envia saudacao (cliente enviou mensagem normal)
            return False

