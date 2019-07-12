import telebot
import pypyodbc
from telebot import types
import config
from vedis import Vedis
from collections import defaultdict
#import botan
bot = telebot.TeleBot(config.token)

"""
bot ishlashi uchun protokollar e'lon qilinishni boshlaydi

"""
con=pypyodbc.connect(config.dbname)
cur=con.cursor()
res=cur.execute('SELECT  * FROM dbo.rayon order by ray').fetchall()
l=len(res)

tipp=cur.execute('SELECT TOP 100 * FROM dbo.prep_tipov').fetchall()
ll=len(tipp)

resor = cur.execute("SELECT ray, [or] from svr ;" ).fetchall()
lo = len(resor)
con.close()
resdi = defaultdict( list)
for row in resor:
  resdi[row[0]].append(row[1])
del(resor)
dba=Vedis(config.db_file)
db={}

def handle_messages(messages):
    for message in messages:
      log(message)
     #botan.track(config.botan_key, message.chat.id, message, 'Выбор лекарства')
def get_state(user_id):
    with Vedis(config.db_file) as dba:
        try:
            s=dba[user_id]
            return s.decode()
        except KeyError:  # Agar biron sababga ko'ra bunday kalit bo'lmasa
            return config.States.S_Start.value  # sukut dialog oynasining boshlanishi


# Bizning ma'lumotlar bazasida foydalanuvchining joriy "holatlarini" saqlab qolamiz
def set_state(user_id, value):
    with Vedis(config.db_file) as dba:
        dba[user_id] = value

"""
Console yoki dastur ishlayotgan payti loglarni yozib boradi, ya'ni qaysi foydalanuvchi qanday xabar yuborgan
"""
def log (message):
    from datetime import datetime
    print("\n ---------")
    print(datetime.now())
    print("Сообшение от {0} {1} .id={2} \n Текст: {3} ".format(message.from_user.first_name,
        message.from_user.last_name, str(message.from_user.id), message.text))

def get_sqlapt(message):
    if get_state(str(message.chat.id)+'msg_t') == config.btntxt['myadr'] :
       strsql = "SELECT  * from  aptbot('" + get_state(str(message.chat.id) + 'lek_sh') + \
                 "', '" + message.text[:-1] + "'," + get_state(str(message.chat.id) + 'lat') + \
                 "," + get_state(str(message.chat.id) + 'lon') + ") order by цена, r"
    else:
       strsql = "Select  * from aptbotg ('" + get_state(str(message.chat.id) + 'lek_sh') + \
                 "', '" + message.text[:-1] + "') as apt "
       if get_state(str(message.chat.id) + 'msg_t') == config.btntxt['rayon']:
            if get_state(str(message.chat.id) + 'msg_r') != config.btntxt['alray'][:-1]:
                strsql = strsql + " where apt.ray='" + get_state(str(message.chat.id) + 'msg_r') + "'"
                if get_state(str(message.chat.id) + 'msg_o') != config.btntxt['alori'][:-1]:
                   strsql = strsql + " and apt.ori='" + get_state(str(message.chat.id) + 'msg_o') + "'"
    return strsql


"""
Scrolling выводимого текста 

def geo_ori(message):
    sray=message.text[:-1]
    if sray != "Весь район" :
       set_state(str(message.chat.id)+'ori',sray)
       set_state(str(message.chat.id)+'lon',str(row[3]))
                break
    else :
        set_state(str(message.chat.id)+'lat','41.311169')
        set_state(str(message.chat.id)+'lon','69.279704')
"""
def pages_keyboard(start, stop):
    """
    Sahifalarda yurish uchun Inline tugmalarini yaratamiz.
    """
    keyboard = types.InlineKeyboardMarkup()
    btns = []
    if start > 0 :
        btns.append(types.InlineKeyboardButton(
        text='Orqaga ⬅', callback_data='to_{}'.format(start - h)))
    if stop < lresa :
        btns.append(types.InlineKeyboardButton(
        text='Oldinga ➡', callback_data='to_{}'.format(stop)))
    keyboard.add(*btns)

    return keyboard
def update_status_message(message, text):
    bot.edit_message_text(chat_id = message.chat.id,
                          message_id = message.message_id,
                          text = text, parse_mode='HTML')
def pages_markup(start, stop,lresa):
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=False, resize_keyboard=True)
        btns = []
        if start > 0:
            btns.append(config.btntxt['backl'])
        if stop < lresa:
            btns.append(config.btntxt['forwd'])
        markup.add(*btns)
        markup.row(config.btntxt['back'])
        return markup

def gen_lekar(message):
    con= pypyodbc.connect(config.dbname)
    cur=con.cursor()
    resl=cur.execute("SELECT top 100 lekar, фарм_группа  from leka_last('" +
                     get_state(str(message.chat.id)+'lek_sh')+"') as lek Order by lekar").fetchall()
    con.close()
    if len(resl) != 0 :
       markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=False, resize_keyboard=True)
       if get_state(str(message.chat.id)+'msg_t') == config.btntxt['gorod'] or \
               get_state(str(message.chat.id)+'msg_t') == config.btntxt['myadr']:
           markup.row(config.btntxt['back'])
       if get_state(str(message.chat.id) + 'msg_t') == config.btntxt['rayon']:
            if get_state(str(message.chat.id) + 'msg_r') == config.btntxt['alray'][:-1]:
                markup.row(config.btntxt['back'])
            elif  get_state(str(message.chat.id) + 'msg_o') == config.btntxt['alori'][:-1]:
                     markup.row(config.btntxt['drray'])
            else:
                    markup.row( config.btntxt['drori'])

       for row in resl:
            markup.add(row[0]+config.lek)
       markup.row(config.btntxt['back'], config.btntxt['main'])
       bot.send_message(message.chat.id, config.msgtxt['lekar'],
                     reply_markup=markup, parse_mode='HTML')

    else :
       bot.send_message(message.chat.id,"<b> Xatolik! Nmadir yuz berdi"+\
                        " Ayni vaqtda bazada ushbu natija topilmadi</b>\n Boshqa narsa kiritib tekshiring ",parse_mode='HTML')

def gen_start(message):
    markup = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True,one_time_keyboard=True)
    button_poisk = types.KeyboardButton(text=config.btntxt['poisk'])
    button_poiskt = types.KeyboardButton(text=config.btntxt['poiskt'])
    button_geo = types.KeyboardButton(text=config.btntxt['help'])
    markup.add(button_poisk, button_poiskt, button_geo)
    bot.send_message(message.chat.id, config.msgtxt['start'],
     reply_markup=markup, parse_mode='HTML')


def gen_territ(message):
    markup = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True,one_time_keyboard=True)
    btns=[]
    btns.append(types.KeyboardButton(text=config.btntxt['myadr'], request_location=True))
    btns.append(types.KeyboardButton(text=config.btntxt['gorod']))
    btns.append(types.KeyboardButton(text=config.btntxt['rayon']))
    btns.append(types.KeyboardButton(config.btntxt['back']))
    markup.add(*btns)
    bot.send_message(message.chat.id, config.msgtxt['territ'],
    reply_markup=markup,parse_mode='HTML')


def gen_gorod(message):
    bot.send_message(message.chat.id, config.msgtxt['gorod'],
                      parse_mode='HTML')

def gen_rayon(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=False)
    markup.add(config.btntxt['alray'])
    for i in range(0, l, 2):
        if i + 1 >= l:
            markup.add(res[i][1] + config.raon)
        else:
            markup.row(res[i][1] + config.raon, res[i + 1][1] + config.raon)
    markup.row(config.btntxt['back'], config.btntxt['main'])
    bot.send_message(message.chat.id, config.msgtxt['rayon'],
            reply_markup=markup,parse_mode='HTML')
def msg_apt(resa,n,k,pr):
    msgapt = ""
    for i in range(n, k):
        row = resa[i]
        msgapt = msgapt + config.razdel + "    \n №" + str(i + 1) + \
                 "\n\U0001f4dd <b>Лекарство: </b>" + row[5] + \
                 "\n\U0001f4e2<b>Производитель:</b>" + row[4] + \
                 "\n\n\U0001f514 <b>Аптека:</b> " + row[0] + \
                 "\n\U0001f50d <b>Адрес:</b>" + row[9] + \
                 "\n\U0001f3e0 <b>Район:</b>" + row[12] + \
                 "\n\U0001f3e0 <b>Ориентир:</b>" + row[13]
        if pr: msgapt = msgapt + "\n<b>Расстояние :</b> " + str(row[8]) + " км."
        msgapt = msgapt + "\n\U0001f501 <b>Режим работы:</b> с " + row[1] + " до " + row[2] + \
                 "\n<b>Телефон:</b> " + '<a href="tel:+998' + row[11] + \
                 row[10] + '">' + '+998' + row[11] + row[10] + '</a> \n\n' + \
                 '<a href="https://www.google.ru/maps?q=' + str(row[7]) + ',' + \
                 str(row[6]) + '&ll=' + str(row[7]) + ',' + \
                 str(row[6]) + '&z=17?">' + config.mapk + 'На карте\n\n\n</a>'
    return msgapt

def gen_orient(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=False)
    markup.add(config.btntxt['alori'])
    spisor = resdi[get_state(str(message.chat.id) + 'msg_r')]
    lo = len(spisor)
    for i in range(0, lo, 2):
        if i + 1 >= lo:
            markup.add(spisor[i] + config.orien)
        else:
            markup.row(spisor[i] + config.orien, spisor[i + 1] + config.orien)
    markup.row(config.btntxt['back'], config.btntxt['main'])
    bot.send_message(message.chat.id, config.msgtxt['orient'],
            reply_markup=markup,parse_mode='HTML')

def gen_poisk(message) :
	if get_state(str(message.chat.id)+'msg_s') == config.btntxt['poiskt'] :
		markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=False)
		for i in range(0, ll, 2):
			if i + 1 >= ll:
				markup.add(tipp[i][1])
			else:
				markup.row(tipp[i][1], tipp[i + 1][1])
		markup.row(config.btntxt['back'], config.btntxt['main'])
		bot.send_message(message.chat.id, config.msgtxt['poisk_tipov'],
					reply_markup=markup,parse_mode='HTML')
	else:
		markup = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True,one_time_keyboard=True)
		markup.row(config.btntxt['back'],config.btntxt['main'])
		bot.send_message(message.chat.id, config.msgtxt['poisk'],
			reply_markup=markup,parse_mode='HTML')

def gen_vibor(message):
    if get_state(str(message.chat.id)+'msg_s') == config.btntxt['poisk'] :
        gen_poisk(message)
        set_state(str(message.chat.id), config.States.S_Poisk.value)
        
    elif get_state(str(message.chat.id)+'msg_s') == config.btntxt['poiskt'] :
        gen_poisk(message)
        set_state(str(message.chat.id), config.States.S_Poisk.value)
    else :
        gen_lekar(message)
        set_state(str(message.chat.id), config.States.S_Lekar.value)
def gen_help(message):
    msg = bot.send_video(message.chat.id, f, None)
    
    #msg = bot.send_message(message.chat.id, config.msgtxt['poisk'])

def gen_apteka(message):
    if get_state(str(message.chat.id)+'msg_t') == config.btntxt['myadr']: pr = True
    else: pr = False
    con = pypyodbc.connect(config.dbname)
    cur = con.cursor()
    resa = cur.execute(get_sqlapt(message)).fetchall()
    lresa = len(resa)
    con.close()
    if lresa == 0:
        bot.send_message(message.chat.id, "<b> Xatolik! Ushbu dori topilmadi.</b> \n", parse_mode='HTML')
        gen_lekar(message)
        set_state(str(message.chat.id), config.States.S_Lekar.value)
    else:
        if lresa<10 : k=lresa
        else : k=10
        n=0
        db[str(message.chat.id) + 'lresa']=lresa
        db[str(message.chat.id) + 'n']=0
        db[str(message.chat.id) + 'k']=10
        db[str(message.chat.id) + 'resa']=resa
        bot.send_message(message.chat.id, msg_apt(resa,n,k,pr), parse_mode='HTML',
           reply_markup=pages_markup(n, k,lresa), disable_web_page_preview=True)
        set_state(str(message.chat.id), config.States.S_Apteka.value)
    #botan.track(config.botan_key, message.chat.id, message, 'Выбор лекарства')

"""
Asosiy kaliaturalar, bunda kc orqali beriladigan buyeruqlar keltiriladi
"""

@bot.message_handler(commands=['start'])
def startids(message):
    #log (message)
    gen_start(message)
    set_state(str(message.chat.id), config.States.S_Start.value)

@bot.callback_query_handler(func=lambda c:TRUE)
def pages(c):
    """
    Foydalanuvchini sahifalar bo'ylab sayr qilinganda xabarni tahrir qiling.
    Quyida dori nomi e'lon qiliib butun dori haqida ma'lumotlari beriladi. Telefoni, dori nomi va boshqalar
    """
    #print(c.data)
    msgapt=""
    for i in range(int(c.data[3:]),int(c.data[3:]) + h) :
        row=res[i]
        msgapt = msgapt + config.razdel +"    \n №" + str(i+1) + \
                     "\n\U0001f4dd <b>Лекарство: </b>" + row[5] + \
                     "\n\U0001f4e2 <b>Производитель:</b>" + row[4] + \
                     "\n\n\U0001f514 <b>Аптека:</b>* " +  row[0] + \
                     "\n\U0001f50d <b>Адрес:</b>" + row[9] + \
                     "\n\U0001f517 <b>Расстояние :</b> " + str(row[8]) \
                     + "\n\U0001f501 <b>Режим работы:</b> с " + row[1] + " до " + row[2] +\
                     "\n\U0001f4f1 <b>Телефон:</b> " + '<a href="tel:+99893' +\
                      row[10]+'">'+row[10]+ '</a> \n\n'+\
                     '<a href="https://www.google.ru/maps?q='+str(row[7])+',' + \
                     str(row[6])+ '&ll='+str(row[7])+',' +\
                     str(row[6])+'&z=17?">'+config.mapk+'На карте\n\n\n</a>'
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=msgapt,
        parse_mode='HTML',
        reply_markup=pages_keyboard(int(c.data[3:]),
            int(c.data[3:]) +10))

@bot.message_handler(content_types=["location"])
def read_loc_data(message):
    #log (message)
    set_state(str(message.chat.id)+'lat',str(message.location.latitude))
    set_state(str(message.chat.id)+'lon',str(message.location.longitude))
    set_state(str(message.chat.id), config.States.S_Geoloc.value)
    set_state(str(message.chat.id)+'msg_t', config.btntxt['myadr'])
    gen_vibor(message)


@bot.message_handler(func=lambda message: get_state(str(message.chat.id))  == config.States.S_Start.value)
def Start_msg(message):
   ##log(message)
   set_state(str(message.chat.id)+'lek_sh', message.text)
   set_state(str(message.chat.id)+'msg_s', message.text)
   if message.text == config.btntxt['help'] :
       bot.send_message(message.chat.id,"<b> Botdan foydalanish tartibi </b>\n"+\
                        " Istalgan dori nomini kiriting, ",parse_mode='HTML')
   else:
       gen_territ(message)
       set_state(str(message.chat.id), config.States.S_Territ.value)


@bot.message_handler(func=lambda message: get_state(str(message.chat.id))  == config.States.S_Help.value)
def Help_msg(message):
    #log(message)
    gen_start(message)
    set_state(str(message.chat.id), config.States.S_Start.value)


@bot.message_handler(func=lambda message: get_state(str(message.chat.id))  == config.States.S_Territ.value)
def Territ_msg(message):
    #log(message)
    if message.text == None:
       set_state(str(message.chat.id)+'msg_t', config.btntxt['myadr'])
    elif message.text == config.btntxt['gorod']:
        set_state(str(message.chat.id)+'msg_t', config.btntxt['gorod'])
        gen_vibor(message)
    elif message.text == config.btntxt['rayon']:
        gen_rayon(message)
        set_state(str(message.chat.id) + 'msg_t', config.btntxt['rayon'])
        set_state(str(message.chat.id), config.States.S_Rayon.value)
    elif message.text == config.btntxt['back']:
        gen_start(message)
        set_state(str(message.chat.id), config.States.S_Start.value)
    else:
        bot.send_message(message.chat.id, config.msgtxt['noreg'], parse_mode='HTML')

@bot.message_handler(func=lambda message: get_state(str(message.chat.id))  == config.States.S_Geoloc.value)
def Geoloc_msg(message):
    #log (message)
    gen_vibor(message)
    set_state(str(message.chat.id), config.States.S_Territ.value)

@bot.message_handler(func=lambda message: get_state(str(message.chat.id))  == config.States.S_Gorod.value)
def Gorod_msg(message):
    #log(message)
    gen_vibor(message)
    set_state(str(message.chat.id), config.States.S_Territ.value)

@bot.message_handler(func=lambda message: get_state(str(message.chat.id))  == config.States.S_Poisk.value)
def Lek_msg(message):
    ##log(message)
    if message.text==config.btntxt['back']:
       if get_state(str(message.chat.id)+'msg_o') == config.btntxt['orient'][:-1]:
            gen_orient(message)
            set_state(str(message.chat.id), config.States.S_Orient.value)
       elif get_state(str(message.chat.id)+'msg_r') == config.btntxt['rayon'][:-1]:
            gen_rayon(message)
            set_state(str(message.chat.id), config.States.S_Rayon.value)
       else:
            gen_territ(message)
            set_state(str(message.chat.id), config.States.S_Territ.value)
    elif message.text == config.btntxt['main']:
        gen_start(message)
        set_state(str(message.chat.id), config.States.S_Start.value)
    else:
        set_state(str(message.chat.id)+'lek_sh',message.text)
        gen_lekar(message)
        set_state(str(message.chat.id), config.States.S_Lekar.value)

@bot.message_handler(func=lambda message: get_state(str(message.chat.id))  == config.States.S_Rayon.value)
def Rayon_msg(message):
    #log (message)
    if message.text==config.btntxt['back']:
        gen_territ(message)
        set_state(str(message.chat.id), config.States.S_Territ.value)
    elif message.text==config.btntxt['main']:
        gen_start(message)
        set_state(str(message.chat.id), config.States.S_Start.value)
    elif message.text == config.btntxt['alray']:
         set_state(str(message.chat.id) + 'msg_r', message.text[:-1])
         gen_vibor(message)
    elif message.text[-1] == config.raon:
         set_state(str(message.chat.id) + 'msg_r', message.text[:-1])
         gen_orient(message)
         set_state(str(message.chat.id), config.States.S_Orient.value)
    else:
        #bot.reply_to(message,config.msgtxt['noray'])
        bot.send_message(message.chat.id, config.msgtxt['noray'], parse_mode='HTML')

@bot.message_handler(func=lambda message: get_state(str(message.chat.id))  == config.States.S_Orient.value)
def Orient_msg(message):
    #log (message)
    if message.text==config.btntxt['back']:
        gen_rayon(message)
        set_state(str(message.chat.id), config.States.S_Rayon.value)
    elif message.text==config.btntxt['main']:
        gen_start(message)
        set_state(str(message.chat.id), config.States.S_Start.value)
    elif  message.text[-1] == config.orien:
            set_state(str(message.chat.id) + 'msg_o', message.text[:-1])
            gen_vibor(message)
    else:
        bot.send_message(message.chat.id, config.msgtxt['noori'], parse_mode='HTML')


@bot.message_handler(func=lambda message: get_state(str(message.chat.id))  == config.States.S_Lekar.value)
def Lekar_msg(message):
    #log (message)
    if message.text==config.btntxt['back']:
            gen_territ(message)
            set_state(str(message.chat.id), config.States.S_Territ.value)
    elif message.text==config.btntxt['drray']:
         gen_rayon(message)
         set_state(str(message.chat.id), config.States.S_Rayon.value)
    elif message.text==config.btntxt['drori']:
         gen_orient(message)
         set_state(str(message.chat.id), config.States.S_Orient.value)
    elif message.text==config.btntxt['main']:
         gen_start(message)
         set_state(str(message.chat.id), config.States.S_Start.value)
    elif message.text[-1] == config.lek :
         gen_apteka(message)
    else:
        set_state(str(message.chat.id)+'lek_sh', message.text)
        gen_lekar(message)
@bot.message_handler(func=lambda message: get_state(str(message.chat.id)) == config.States.S_Apteka.value)
def Apteka_msg(message):
        if get_state(str(message.chat.id) + 'msg_t') == config.btntxt['myadr']: pr = True
        else:  pr = False
        n = db[str(message.chat.id) + 'n']
        k = db[str(message.chat.id) + 'k']
        lresa=db[str(message.chat.id) + 'lresa']
        resa=db[str(message.chat.id) + 'resa']
        #botan.track(config.botan_key, message.chat.id, message, 'Выбор лекарства')
        if message.text == config.btntxt['backl']:
           n=n-10
           k=k-10
           if n<0 : n=0
           db[str(message.chat.id) + 'n']=n
           db[str(message.chat.id) + 'k']=k
           bot.send_message(message.chat.id, msg_apt(resa, n, k, pr), parse_mode='HTML',
                            reply_markup=pages_markup(n, k,lresa),disable_web_page_preview=True)
        elif message.text == config.btntxt['forwd']:
           n=n+10
           k=k+10
           if k>lresa : k=lresa
           db[str(message.chat.id) + 'n'] = n
           db[str(message.chat.id) + 'k'] = k
           """
           bot.edit_message_text(
               chat_id=message.chat.id,
               message_id=message.message_id,
               text=msg_apt(resa, n, k, pr),
               parse_mode='HTML')
           bot.reply_to(message,"")
           """
           bot.send_message(message.chat.id, msg_apt(resa, n, k, pr), parse_mode='HTML',
                            reply_markup=pages_markup(n, k, lresa),disable_web_page_preview=True)
        elif message.text == config.btntxt['back']:
            gen_lekar(message)
            set_state(str(message.chat.id), config.States.S_Lekar.value)
        else:
            bot.send_message(message.chat.id, config.msgtxt['noapt'], parse_mode='HTML')

@bot.message_handler(commands=["geophone"])
def geophone(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_phone, button_geo)
    bot.send_message(message.chat.id,
    text="Отправь мне свой номер телефона или поделись местоположением, жалкий человечишка!",
                     reply_markup=keyboard)



if __name__ == "__main__":
    bot.set_update_listener(handle_messages)
    bot.polling(none_stop=True)

