from pytube import YouTube
import telebot
import random, datetime
#Aqui é necessário colocar o token do bot
bot = telebot.TeleBot(TOKEN)
#Se inicia a função de start do bot
@bot.message_handler(commands=['start','help'])
def send_start_message(message):
        bot.reply_to(message, "Me jogue um link do Youtube que te taco o vídeo :p")
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAPoX9vLhXFwPvAsBBw028RvqWs0oyMAAqsBAAIQGm0ieL6-kcxUbMceBA')
#Demais funções do bot
@bot.message_handler(func=lambda m: True)
def pegar(message):
    if message.text.count('http'):
            #Será feito scraping do Youtube e enviado o resumo para o usuário que requisitou pelo token
        try:
            link = message.text
            yt = YouTube(link)
            qualidade = telebot.types.InlineKeyboardMarkup()
            qualidade.row(telebot.types.InlineKeyboardButton('Baixa',callback_data=f'baixa:{link}'),
                          telebot.types.InlineKeyboardButton('Alta',callback_data=f'alta:{link}'))
            imagem = ['captado.png','captado2.png','captado3.jpeg']
            bot.send_photo(message.chat.id, open(imagem[random.randint(0,2)], 'rb'))
            bot.send_message(message.chat.id, f"🎬 Título: {yt.title}\n"
                                              f"📈 Views: {'{:,}'.format(int(yt.views)).replace(',','.')}\n"
                                              f"🕐 Duração: {str(datetime.timedelta(seconds=yt.length))}\n"
                                              f"👍 Avaliação: {round(float(yt.rating), 1)} ⭐️\n",reply_markup=qualidade)
        except:
            print('erro')
    else:
        bot.send_message(message.chat.id, 'Envie uma URL que preste!')
        bot.send_sticker(message.chat.id, 'CAACAgEAAxkBAAOxX9vGuWMlPoI0xwSkdtce4SPO2JwAAkMAA54znB-tZhelgxk-4R4E')
        print(f"Usuário {message.chat.first_name} {message.chat.last_name} está falando asneiras.")
#Funções acionadas por botões
@bot.callback_query_handler(func=lambda call: True)
def qualidade(query):
    #Download dos vídeos em baixa resolução    
    if query.data.count('baixa'):
        link = query.data.replace('baixa:', '')
        yt = YouTube(link)
        ys = yt.streams.get_lowest_resolution()
    #Download dos vídeos em alta resolução
    elif query.data.count('alta'):
        link = query.data.replace('alta:', '')
        yt = YouTube(link)
        ys = yt.streams.get_highest_resolution()
    try:
    #Envio de vídeos para o usuário pelo token
        if int(yt.length) < 600:
            ys.download(filename='video')
            print('Usuário baixando vídeo')
            arquivo = open('video.mp4','rb')
            try:
                print('Upando vídeo para usuário')
                bot.send_message(query.message.chat.id, '[Enviando...]')
                bot.send_sticker(query.message.chat.id, 'CAACAgIAAxkBAAIB2l_f-7aq-2V4TvoWI7DzeGl1_LiTAALIAQACEBptIg5zcps1Oc8WHgQ')
                bot.send_video(query.message.chat.id, arquivo)
                print(f"Usuário {query.message.chat.first_name} {query.message.chat.last_name} pediu um vídeo e enviado com sucesso.")
            except:
                bot.send_message(query.message.chat.id, 'Vídeo muito grande, excedeu 50MB. Sinto muito!')
                bot.send_sticker(query.message.chat.id, 'CAACAgIAAxkBAAO4X9vHcFHIzdZ1yEXCEIG9qcMsCBUAApIBAAIw1J0RWCZHoYykemAeBA')
                print(f"Usuário {query.message.chat.first_name} {query.message.chat.last_name} pediu um vídeo muito grande.")
        else:
            bot.send_message(query.message.chat.id, 'Vídeo muito longo!')
            bot.send_sticker(query.message.chat.id, 'CAACAgIAAxkBAAO4X9vHcFHIzdZ1yEXCEIG9qcMsCBUAApIBAAIw1J0RWCZHoYykemAeBA')
            print(f"Usuário {query.message.chat.first_name} {query.message.chat.last_name} pediu um vídeo muito longo.")
    except:
        bot.send_message(query.message.chat.id, 'Sua requisição não foi compreendida ou violou os direitos autorais de Sony Music. Sinto muito!')
        bot.send_sticker(query.message.chat.id, 'CAACAgIAAxkBAAO2X9vHYeMv2hdFz_EdsiVgxyXME_EAApQBAAIw1J0RtqQbQKs2VWceBA')
        print(f"Usuário {query.message.chat.first_name} {query.message.chat.last_name} violou ou enviou uma URL errada.")
#Função que não autoriza o programa se fechar após o final do código, retornando a ouvir os chamados do usuário pelo token
bot.polling(none_stop=True)
