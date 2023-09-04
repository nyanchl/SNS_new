from app.models import Comment

import re
import MeCab
import pandas as pd
import time
import numpy as np


pn_df = pd.read_csv('app/Dic/dic.txt',\
                    sep=':',
                    encoding='utf-8',
                    names=('Word','Reading','POS', 'PN')
                )

mecab = MeCab.Tagger('-d /opt/homebrew/lib/mecab/dic/ipadic')

word_list = list(pn_df['Word'])
pn_list = list(pn_df['PN'])
pn_dict = dict(zip(word_list, pn_list))

def analysiscomment(comment_text):
    comment = comment_text
    come = np.array(comment)
    if come.ndim == 0:
        come = [str(come)]

    def get_diclist(comment):
        parsed = mecab.parse(comment)
        lines = parsed.split('\n')
        lines = lines[0:-2]
        diclist = []
        for word in lines:
            l = re.split('\t|,',word)
            d = {'Surface':l[0], 'POS1':l[1], 'POS2':l[2], 'BaseForm':l[7]}
            diclist.append(d)
        return(diclist)

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

    def get_pnmean(diclist):
        pn_list = []
        for word in diclist:
            pn = word['PN']
            if pn != 'notfound':
                pn_list.append(pn)  
        if len(pn_list) > 0:
            pnmean = sum(pn_list)
        elif len(pn_list) == 0:
            pnmean = 0
        return(pnmean)


    pnmeans_list = []
    for tw in come:
        dl_old = get_diclist(tw)
        dl_new = add_pnvalue(dl_old)
        pnmean = get_pnmean(dl_new)
        pnmeans_list.append(pnmean)

    return pnmean