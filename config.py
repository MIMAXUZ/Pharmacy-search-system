# Welcome To Our New Bot
"""
Ushbu bo'lim ma'lumotlar ombori bilan boglaniosh va asosiy sozlamalar keltriladi,
Ya'ni har bir ko'rinayotgan tugmachalar uchun qo'yiladigan Carcode ikonlar, va xatolik yoki tugmalar uchun beriladigna matnlar keltriladi
"""
mapk= u'\U0001F30D'
hot = u'\U0001F525'             # Code: 904
defaultEmoji = u'\U0001F300'    # default emojis
poisk=u'\U0001f50d'
mesto=u'\U0001F4CC'
razd=u'\U0001F538'
raon=u'\U0001f517'
lek=u'\U0001F48A'
razdel=10*razd
orien=u'\U0001F307'
token = ''
msgtxt={'start':'<b>Dorixonalar qidiruvi tizimiga xush kelibsiz!</b>\n\n Izlamoqchi bolgan bolimni tanlang!\n'+\
         ' Yoki izlayotgan dori nomini kiriting (Kamida 3 ta belgi)',
         'territ':'<b>Shahar hududlarini belgilang</b> \n Yoki ayni vaqtdagi manzilingini yuboring',
         'tipovv':'<b>Dori Turlari royxati tugmasini bosing </b> \n Yoki dori turini yozing',
         'poisk_tipov':'<b>Royxatdan dori turini tanlang </b> \n Yoki dori turini yozing kamida 3 ta belgi',
         'gorod':'<b>Siz barcha shaharlar boyicha qidiruvni tanladingiz</b>',
         'lekar':'<b>Royxatdagi dorilardan tanlang</b>\n или отправьте название нового лекарства',
         'rayon':'<b>Barcha shahar yoki tumanlarni tanlang</b>',
        'orient': '<b>Barcha tuman yoki moljalni tanlang </b>',
         'poisk':'<b>Dori nomlanishini kiriting</b> \n ( Kamida 3 ta belgi)',
         'nolek':'<b>Izlayotgan doringiz shahar dorixonalaridan topilmadi</b>\n Boshqa dori nomini kirtib harakat qiing',
         'noreg':'<b>Siz xato tuman kiritdingiz</b>\n Royxatdagi dorixonlardan tanlang',
         'noray':'<b>Siz xato tuman belgiladingiz</b>\n Royxatdagi tumanlardan birini tanlang',
         'noori': '<b>Xato moljal tanladingiz</b>\n Royxatdagilardan tanlang!',
         'noapt': '<b>Xato malumotlar berildi</b>\n Kerakli tugmalarni belgilang!'

}

"""
Bu bo'limda esa tugmachalar uchun beriladigan matnlar keltririladi
"""
btntxt={'poisk':poisk+' Dorilarni Izlashni Boslash',
        'poiskt':poisk+' Dorilarni turi boyicha izlash',
        'back':'\u23EA Orqaga',
        'backl':'\u23EA',
        'forwd': '\u23E9',
        'main':'\u23EB Bosh sahifaga',
        'help':'\U0001f517 Foydalanish shartlari?',
        'myadr': mesto +' Ayni vaqtdagi manzilim',
        'gorod': raon + 'Toshkent shahri',
        'rayon':'\U0001f517 Tuman shaharlari',
        'get_tipov':'\U0001f517 Dori turlari',
        'drray':'\U0001f517 Boshqa tumandan',
        'orient': '\U0001f517 Tuman moljali',
        'drori': '\U0001f517 Boshqa moljal',
        'alray':  '\U0001f517 Barcha shaharlar '+raon,
        'alori':  '\U0001f517 Barcha tumanlar'+orien}
"""
Ma'lumotlar bazasi bilan boglanish qismi
Bu qisimda server sozlamalari beriladi
"""
MySqlserver="DESKTOP-LDGN19S"
MyDatabase="Me_prep_beSQL"
Myuser=""
Mypassword=""
dbname='driver={SQL SERVER};' ' Server='+MySqlserver+';' 'Database='+MyDatabase+\
       ';' ' UID=' + Myuser + ';' ' PWD='+Mypassword +';'
db_file = "dbstate.vdb"
from enum import Enum
class States(Enum):
    """
    Bu qisimda biz Vedia DB ni ishlatamiz, berilayotgan har bir qism string hisoblanadi shu sabab str shaklida olib olamiz har 
    bir buyruqni
    """
    S_Start = '0'  # Начало нового диалога
    S_Territ = '1'
    S_Rayon = '2'
    S_Lekar = '3'
    S_Help = '4'
    S_Apteka = '5'
    S_Geoloc = '6'
    S_Poisk = '7'
    S_Vibor = '8'
    S_Orient = '9'
    S_Gorod = '10'
    S_Tipov = '2'
#pyinstaller --onedir --onefile --name=myprogram "D:\1.py"
