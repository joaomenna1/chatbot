import os
import time
from chatterbot import ChatBot
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class wppbot:
    # caminho da aplicacao
    dir_path = os.getcwd()

    def __init__(self, nome_bot):
        print(self.dir_path)
        self.bot = ChatBot(nome_bot)

        self.chrome = self.dir_path + '\chromedriver.exe'

        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r"user-data-dir=" + self.dir_path + "\profile\wpp")
        self.driver = webdriver.Chrome(self.chrome, chrome_options=self.options)

    # inicia uma conversa com um contato
    def inicia(self, nome_contato):
        # Entrar no whatsapp web
        self.driver.get('https://web.whatsapp.com/')
        self.driver.implicitly_wait(10)

        # Procurar pelo contato passado como parametro
        self.caixa_de_pesquisa = self.driver.find_element_by_class_name("_2zCfw")
        self.caixa_de_pesquisa.send_keys(nome_contato)
        time.sleep(2)

        # Clicar no contato passado como parametro
        self.contato = self.driver.find_element_by_xpath('//span[@title = "{}"]'.format(nome_contato))
        self.contato.click()
        time.sleep(2)

    def saudacao(self, frase_inicial):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name("_3u328")

        # Enviar as palavras contidas na frase passada como parametro
        if type(frase_inicial) == list:
            for frase in frase_inicial:
                self.caixa_de_mensagem.send_keys(frase)
                time.sleep(2)
                self.botao_enviar = self.driver.find_element_by_class_name("_3M-N-")
                self.botao_enviar.click()
                time.sleep(2)
        else:
            return False

    #def escuta(self, ultimo_texto):
     #   time.sleep(10)
      #  post = self.driver.find_elements_by_class_name("_1zGQT")
       # ultimo = len(post) - 1
        #texto = post[ultimo].find_element_by_css_selector('span.selectable-text').text
        #return texto

    def escuta(self, penultimo_texto):
        time.sleep(10)
        cronometro = 5
        post = self.driver.find_elements_by_class_name("_1zGQT")
        ultimo = len(post) - 1
        ultimo_texto = post[ultimo].find_element_by_css_selector('span.selectable-text').text

        while (ultimo_texto == penultimo_texto):
            time.sleep(5)
            cronometro = cronometro + 5
            if (cronometro >= 60):
                break
            else:
                post = self.driver.find_elements_by_class_name("_1zGQT")
                ultimo = len(post) - 1
                penultimo_texto = ultimo_texto
                ultimo_texto = post[ultimo].find_element_by_css_selector('span.selectable-text').text

        if (cronometro >= 60):
            return None
        else:
            return ultimo_texto

    def menu(self, nome_contato):
        img = self.dir_path + '\Pulsar-1.png'
        self.driver.find_element_by_css_selector('span[data-icon="clip"]').click()
        attach = self.driver.find_element_by_css_selector('input[type="file"]')
        attach.send_keys(img)
        time.sleep(2)

        self.caixa_de_mensagem = self.driver.find_element_by_class_name("_3u328")
        self.caixa_de_mensagem.send_keys(nome_contato + ", durante seu atendimento, escolha e digite uma das opções abaixo para dar continuidade ao seu atendimento: ")
        self.caixa_de_mensagem.send_keys(Keys.SHIFT, Keys.ENTER)
        self.caixa_de_mensagem.send_keys(Keys.SHIFT, Keys.ENTER)
        self.caixa_de_mensagem.send_keys("1 - Localização")
        self.caixa_de_mensagem.send_keys(Keys.SHIFT, Keys.ENTER)
        self.caixa_de_mensagem.send_keys("2 - Especialidades")
        self.caixa_de_mensagem.send_keys(Keys.SHIFT, Keys.ENTER)
        self.caixa_de_mensagem.send_keys("3 - Exames oferecidos")
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
        time.sleep(10)
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
        self.caixa_de_mensagem.send_keys("Aqui estão as especialidades médicas presentes aqui na Clínica Pulsar, que conta com profissionais altamente qualificados e humanizados para melhor atendê-lo.")

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
        self.caixa_de_mensagem.send_keys("Esses são os procedimentos realizados aqui na Clínica Pulsar. Entre em contato com um atendente e será um prazer atendê-lo.")
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
        self.caixa_de_mensagem.send_keys("Os exames laboratoriais são realizados pelo nosso parceiro RB diagnósticos que utiliza a mais alta tecnologia do mercado e fornece aos nossos clientes atendimento humanizado e de qualidade.")
        self.caixa_de_mensagem.send_keys(Keys.SHIFT, Keys.ENTER)
        self.caixa_de_mensagem.send_keys("Entre em contato pelo número 991674868.")
        time.sleep(2)

        self.botao_enviar = self.driver.find_element_by_class_name("_1g8sv")
        self.botao_enviar.click()
        time.sleep(2)

    def desmarcar(self):
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
