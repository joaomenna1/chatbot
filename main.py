import re
from wppbot import wppbot

bot = wppbot('Chatbot')
bot.inicia('Mamãe')
bot.saudacao(['Olá, aqui quem fala é o chatbot da Clínica Pulsar. Digite seu primeiro nome para que a gente possa salvar seu contato!'])

nome = bot.escuta("Olá, aqui quem fala é o chatbot da Clínica Pulsar. Digite seu primeiro nome para que a gente possa salvar seu contato!")
bot.menu(nome)

controla = True
ultima_mensagem = nome

while controla:
    opcao = bot.escuta(ultima_mensagem)
    if opcao != None:
        if opcao == "0" or opcao == "zero" or opcao == 'ZERO' or opcao == 'Zero':
            bot.menu()
        elif opcao == "01" or opcao == "1" or opcao == "um" or opcao == 'UM' or opcao == 'Um' or "Localização" or "Localizacao" or "localização" or "localizacao":
            bot.localizacao()
        elif opcao == "02" or opcao == "2" or opcao == "dois" or opcao == 'DOIS' or opcao == 'Dois' or "Especialidades" or "especialidades":
            bot.especialidades()
        elif opcao == "03" or opcao == "3" or opcao == "tres" or opcao == 'TRES' or opcao == 'Tres':
            bot.exames()
        elif opcao == "04" or opcao == "4" or opcao == "quatro" or opcao == 'QUATRO' or opcao == 'Quatro':
            bot.exames_laboratoriais()
        elif opcao == "05" or opcao == "5" or opcao == "cinco" or opcao == 'CINCO' or opcao == 'Cinco':
            bot.desmarcar()
            controla = False
        elif opcao == "06" or opcao == "6" or opcao == "seis" or opcao == 'SEIS' or opcao == 'Seis' or "Contato" or "contato":
            bot.mandar_contato()
    ultima_mensagem = opcao
