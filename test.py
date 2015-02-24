# -*- coding: utf-8 -*- 
import unicodedata

content = u"Бланк XYZ свидетельства о ???допуске."
print content
# print unicodedata.normalize('NFKD', content).encode('ascii','ignore')
# re.sub(u"(?i)[^-0-9a-zа-яё«»\&\;\/\<\>\.,\s\(\)\*:!\?]", "", content.decode('utf8'))
# u'\u043b\u0430\u043d\u043a \u0441\u0432\u0438\u0434\u0435\u0442\u0435\u043b\u044c\u0441\u0442\u0432\u0430 \u043e \u0434\u043e\u043f\u0443\u0441\u043a\u0435.'
# >>> print re.sub(u"(?i)[^-0-9a-zа-яё«»\&\;\/\<\>\.,\s\(\)\*:!\?]", "", content.decode('utf8'))
# ланк свидетельства о допуске.