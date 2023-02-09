import re
import MeCab
import pandas as pd
import csv

from app.models import MyText

post_data = MyText.objects.all()

pn_df = pd.read_csv('sns/app/MeCab/dic/dic.txt',\
                    sep = ':',
                    encoding = 'utf-8',
                    names = ('Word','Reading','POS', 'PN')
                    )

m = MeCab.Tagger('')

def get_diclist(text):
    parsed = m.parse(text)
    lines = parsed.split('\n')
    lines = lines[0:-2]
    diclist = []
    for word in lines:
        l = re.split('\t|,',word)
        d = {'Surface':l[0], 'POS1':l[1], 'POS2':l[2], 'BaseForm':l[7]}
        diclist.append(d)
    return(diclist)

word_list = list(pn_df['Word'])
pn_list = list(pn_df['PN'])
pn_dict = dict(zip(word_list, pn_list))

def add_pnvalue(diclist_old):
    diclist_new = []
    for word in diclist_old:
        base = word['BaseForm']
        if base in pn_dict:
            pn = float(pn_dict[base])
        else:
            pn = 'notfound'
            word['PN'] = pn
        diclist_new.append(word)
    return(diclist_new)