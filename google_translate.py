from google_trans_new import google_translator

def langTranslator(statement,dest):
    print("text to be translated it : "+statement)
    print("Dest : " + dest)
    destination_lang_code = get_lang_code(dest)
    print("destination_lang_code :" + destination_lang_code)
    translator = google_translator()
    output = translator.translate(statement, lang_tgt=str(destination_lang_code))
    print(output)
    output = str(output)
    return output

def get_lang_code(dest):
    dest = dest.lower()
    LANGUAGES = {
         'af' : 'afrikaans',
         'sq' : 'albanian',
         'ar' : 'arabic',
         'hy' : 'armenian',
         'bn' : 'bengali',
         'ca' : 'catalan',
         'zh' : 'chinese',
         'hr' : 'croatian',
         'cs' : 'czech',
         'da' : 'danish',
         'nl' : 'dutch',
         'en' : 'english',
         'eo' : 'esperanto',
         'fi' : 'finnish',
         'fr' : 'french',
         'de' : 'german',
         'el' : 'greek',
         'hi' : 'hindi',
         'hu' : 'hungarian',
         'is' : 'icelandic',
         'id' : 'indonesian',
         'it' : 'italian',
         'ja' : 'japanese',
         'km' : 'khmer',
         'ko' : 'korean',
         'la' : 'latin',
         'lv' : 'latvian',
         'mr' : 'marathi',
         'mk' : 'macedonian',
         'no' : 'norwegian',
         'pl' : 'polish',
         'pt' : 'portuguese',
         'ro' : 'romanian',
         'ru' : 'russian',
         'sr' : 'serbian',
         'si' : 'sinhala',
         'sk' : 'slovak',
         'es' : 'spanish',
         'sw' : 'swahili',
         'sv' : 'swedish',
         'ta' : 'tamil',
         'th' : 'thai',
         'tr' : 'turkish',
         'uk' : 'ukrainian',
         'vi' : 'vietnamese',
         'cy' : 'welsh'

    }
    try:
        key_list = list(LANGUAGES.keys())
        val_list = list(LANGUAGES.values())
        return key_list[val_list.index(dest)]
    except:
        print("I couldn't find the language you mentioned..\n"
                           "please repeat, You want me to translate in..")


