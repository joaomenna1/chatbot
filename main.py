import re
from wppbot import wppbot

bot = wppbot('Chatbot')
bot.inicia('Mamãe')
bot.saudacao(['Olá, digite seu nome para que a gente possa salvar seu contato!'])
nome = bot.escuta()
bot.menu(nome)

controla = True

while controla:
    opcao = bot.escuta()
    if opcao == "0" or opcao == "zero" or opcao == 'ZERO' or opcao == 'Zero':
        bot.menu()
    elif opcao == "01" or opcao == "1" or opcao == "um" or opcao == 'UM' or opcao == 'Um':
        bot.historico(nome)
    elif opcao == "02" or opcao == "2" or opcao == "dois" or opcao == 'DOIS' or opcao == 'Dois':
        bot.localizacao()
    elif opcao == "03" or opcao == "3" or opcao == "tres" or opcao == 'TRES' or opcao == 'Tres':
        bot.servicos()
    elif opcao == "04" or opcao == "4" or opcao == "quatro" or opcao == 'QUATRO' or opcao == 'Quatro':
        bot.desmarcar()
        controla = False
    elif opcao == "05" or opcao == "5" or opcao == "cinco" or opcao == 'CINCO' or opcao == 'Cinco':
        bot.desmarcar()
        controla = False
    elif opcao == "06" or opcao == "6" or opcao == "seis" or opcao == 'SEIS' or opcao == 'Seis':
        bot.contato()
    else:
        bot.invalido()