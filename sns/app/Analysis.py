from app.models import MyText
from django.views import generic
from .forms import TextPointForm
from django.shortcuts import get_object_or_404


import re
import MeCab
import pandas as pd
import time
import numpy as np

analytext = MyText.objects.get(pk=3)
reanalytext = str(analytext)
tex = np.array(reanalytext)
if tex.ndim == 0:
    tex = [str(tex)]

pn_df = pd.read_csv('app/Dic/dic.txt',\
                    sep=':',
                    encoding='utf-8',
                    names=('Word','Reading','POS', 'PN')
                )

mecab = MeCab.Tagger('-d /opt/homebrew/lib/mecab/dic/ipadic')

def get_diclist(reanalytext):
    parsed = mecab.parse(reanalytext)
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

def get_pnmean(diclist):
    pn_list = []
    for word in diclist:
        pn = word['PN']
        if pn != 'notfound':
            pn_list.append(pn)  
    # print(len(pn_list))
    if len(pn_list) > 0:
        pnmean = sum(pn_list)
    elif len(pn_list) == 0:
        pnmean = 0
    # print(sum(pn_list))
    print(pnmean)
    return(pnmean)


start_time = time.time()
pnmeans_list = []
for tw in tex:
    dl_old = get_diclist(tw)
    dl_new = add_pnvalue(dl_old)
    pnmean = get_pnmean(dl_new)
    pnmeans_list.append(pnmean)

# class TextPointCreateView(generic.CreateView):
#     model = MyText
#     form = TextPointForm

#     def form_valid(self, form):
#         text_pk = self.kwargs.get('pk')
#         text = get_object_or_404(MyText, pk=text_pk)
#         if request.method == 'POST':
#             form = TextPointForm(instance=pnmean)

analytext.textpoint = pnmean
analytext.save()


# MyText.objects.create(pnmean)