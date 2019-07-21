import os
import time
from chatterbot import ChatBot
from selenium import webdriver


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

    def escuta(self):
        time.sleep(10)
        post = self.driver.find_elements_by_class_name("_1zGQT")
        ultimo = len(post) - 1
        texto = post[ultimo].find_element_by_css_selector('span.selectable-text').text
        return texto

    def menu(self, nome_contato):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name("_3u328")
        menu = nome_contato + ", durante seu atendimento, escolha e digite uma das opções abaixo para dar continuidade ao seu atendimento:\n" \
               "1 - Histórico\n" \
               "2 - Localização\n" \
               "3 - Serviços\n" \
               "4 - Agendar exames\n" \
               "5 - Falar com atendente\n" \
               "6 - Contato\n" \
               "0 - Voltar ao menu inicial"
        self.caixa_de_mensagem.send_keys(menu)
        time.sleep(2)
        self.botao_enviar = self.driver.find_element_by_class_name("_3M-N-")
        self.botao_enviar.click()
        time.sleep(2)

    def historico(self, nome_contato):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name("_3u328")
        historico = nome_contato + ", nós éramos um grupo de médicos, um grupo de amigos, porém com um sonho em comum: queríamos continuar " \
                    "a praticar a boa medicina, com qualidade técnica, com comprometimento, com olhar humano aos nossos pacientes, " \
                    "mas queríamos também tornar esse serviço acessível a um maior número de pessoas. Esse sonho ganhou força, " \
                    "e hoje já é realidade, é a PULSAR."
        self.caixa_de_mensagem.send_keys(historico)
        time.sleep(2)
        self.botao_enviar = self.driver.find_element_by_class_name("_3M-N-")
        self.botao_enviar.click()
        time.sleep(2)

    def localizacao(self):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name("_3u328")
        localizacao = "Estamos localizadados na Rua Miguel Faraday (Antiga rua Urariá) 29b, " \
                    "São José Operário, ao lado do 9DP. Manaus/AM. Brasil. " \
                    "Faça-nos uma visita!"
        self.caixa_de_mensagem.send_keys(localizacao)
        time.sleep(2)
        self.botao_enviar = self.driver.find_element_by_class_name("_3M-N-")
        self.botao_enviar.click()
        time.sleep(2)

    def servicos(self):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name("_3u328")
        servicos = "Oferecemos uma gama de exames para melhor atendê-lo." \
                   " Atualmente trabalhamos com diversos exames nas areas:" \
                   " cardiológica," \
                   " ultrassonografias," \
                   " exames laboratoriais." \
                   " Entre em contato com um de nossos atendentes para verificar no que podemos ajudá-lo" \
                   " ou visite nosso site para conhecer mais sobre os exames:" \
                   " https://clinicapulsarsaude.com.br/."
        self.caixa_de_mensagem.send_keys(servicos)
        time.sleep(2)
        self.botao_enviar = self.driver.find_element_by_class_name("_3M-N-")
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
