import re
from wppbot import wppbot

bot = wppbot('Chatbot')
#bot.treina('treino')
bot.inicia('Mamãe')
bot.saudacao(['Bot: Olá, sou Lucas, o chatbot da Pulsar!'])
# ultimo_texto = ''

bot.menu()

#while True:
#    texto = bot.escuta()
#    if texto != ultimo_texto and re.match(r'^::', texto):
#        ultimo_texto = texto
#        texto = texto.replace('::', '')
#        texto = texto.lower()
#       if (texto == 'aprender' or texto == ' aprender' or texto == 'ensinar' or texto == ' ensinar'):
#           bot.aprender(texto, 'bot: Escreva a pergunta e após o ? a resposta.','bot: Obrigado por ensinar! Agora já sei!','bot: Você escreveu algo errado! Comece novamente..')
#       else:
#           bot.responde(texto)
