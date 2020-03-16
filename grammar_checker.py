import os
import sys
import stanfordnlp
from nltk.parse.stanford import StanfordParser
from nltk import Tree, ProbabilisticTree
from nltk.tree import ParentedTree
import nltk
from nltk.tokenize import sent_tokenize

from subject import subject, subject_NPP
from object import object, object_by_tree
from attributive import attrib, attrib_TwoComma
from AdvClause import advclause, advclause_OneComma, advclause_TwoComma
from predicative import predicat
from special import special
from paralel import paralel
from inverse import inverse
from nonFinite import nonFinite
from comparative import compara

os.environ['STANFORD_PARSER'] = "/Users/xugang/Desktop/NLP/stanford-parser-full-2018-10-17/stanford-parser-full-2018-10-17/stanford-parser.jar"
os.environ['STANFORD_MODELS'] = "/Users/xugang/Desktop/NLP/stanford-parser-full-2018-10-17/stanford-parser-full-2018-10-17/stanford-parser-3.9.2-models.jar"

parser = StanfordParser(model_path="edu/stanford/nlp/models/lexparser/englishFactored.ser.gz")

nlp = stanfordnlp.Pipeline(processors='tokenize,mwt,pos')

text = open('demo.txt').read()
sentences = sent_tokenize(text)
for n in range(0,len(sentences)):
    sentence = ''
    sentence = sentences[n]
    print('**************************************************************************************************************************')
    print('第 %d 句话:' %(n+1),sentence)
    sentence_input = parser.raw_parse(sentence)
    for line in sentence_input:
        for t in line:
            print('------------------------------------------------------------------------------------------------------------------')
            pass
# sentences_input = input("sentence input:").lower()
# sentences = parser.raw_parse(sentences_input)
    str = sentence
    doc = nlp(str)
    res1=[f'{word.text}' for sent in doc.sentences for word in sent.words]
    res2=[f'{word.upos}' for sent in doc.sentences for word in sent.words]
    res3=[f'{word.xpos}' for sent in doc.sentences for word in sent.words]
    res = [[res1[i],res2[i],res3[i]]for i in range(len(res1))]
    # print('原句：',res1)
    # print('--------------------------------------------------------')


    p1=[]
    p2=[]
    p3=[]
    p4=[]
    p5=[]
    count_comma = 0
    cc=0
    trigger=int

    for item in res1:
        if item == ',':
            count_comma = res1.count(item)
    print('整句中有 %d 个逗号' %(count_comma))


    if count_comma == 0:
        subject(res)
        object(res)
        object_by_tree(t)
        attrib(res)
        advclause(res)
        predicat(res)
        special(res)
        nonFinite(res)
        compara(res)


        for j in range(0,len(t)):
            for k in t[j].treepositions()[1:]:
                if type(t[j]) == nltk.tree.Tree and t[j].label() == 'VP':
                    if t[j,0,0] in ['am','is','are']:
                        print('主系表结构','一般现在时','系动词为: %s'%(t[j,0,0]))
                        for i in range(len(t[j])):
                            if t[j,i].label()=='VP':
                                for k in range(len(t[j,i])):
                                    if t[j,i,k].label() == 'VBG':
                                        print('一般现在进行时')
                        break
                    elif t[j,0,0] in ['were','was']:
                        print('主系表结构','一般过去时','系动词为: %s'%(t[j,0,0]))
                        for i in range(len(t[j])):
                            if t[j,i].label()=='VP':
                                for k in range(len(t[j,i])):
                                    if t[j,i,k].label() == 'VBG':
                                        print('一般过去进行时')
                        break
                    elif t[j,0,0] in ['has','have']:
                        for m in range(len(t[j])):
                            if t[j,m].label() == 'VP' and t[j,m,0,0] == 'been':
                                print('主系表结构','一般完成时')
                                for i in range(len(t[j])):
                                    if t[j,i].label()=='VP':
                                        for k in range(len(t[j,i])):
                                            if t[j,i,k].label() == 'S' and t[j,i,k,0,0].label()=='VBG':
                                                print('一般完成现在时')
                            elif t[j,m].label() == 'VP' and t[j,m,0,0] != 'been':
                                print('主谓宾结构','一般完成时','动词：%s'%(t[j,m,0,0]))
                        break
                    elif t[j,0,0] == 'had':
                        for m in range(len(t[j])):
                            if t[j,m].label() == 'VP' and t[j,m,0,0] == 'been':
                                print('主系表结构','过去完成时')
                                for i in range(len(t[j])):
                                    if t[j,i].label()=='VP':
                                        for k in range(len(t[j,i])):
                                            if t[j,i,k].label() == 'S' and t[j,i,k,0,0].label()=='VBG':
                                                print('过去完成进行时')
                            elif t[j,m].label() == 'VP' and t[j,m,0,0] != 'been':
                                print('主谓宾结构','过去完成时','动词：%s'%(t[j,m,0,0]))
                        break
                    elif t[j,0].label() == 'MD' and t[j,0,0] == 'will':
                        print('情态动词:',t[j,0,0])
                        trigger=1
                        break
                    elif t[j,0].label() == 'MD' and t[j,0,0] == 'would':
                        print('情态动词:',t[j,0,0])
                        trigger=2
                        break
                    else:
                        print('主谓宾结构')
                        print('动词:',''.join(t[j,0].leaves()))
                        verb = ''.join(t[j,0].leaves())

                        doc = nlp(verb)
                        res_1=[f'{word.text}' for sent in doc.sentences for word in sent.words]
                        res_2=[f'{word.upos}' for sent in doc.sentences for word in sent.words]
                        res_3=[f'{word.xpos}' for sent in doc.sentences for word in sent.words]
                        res = [[res_1[i],res_2[i],res_3[i]]for i in range(len(res_1))]
                        print(res)
                        if res[0][2] == 'VBD':
                            print('一般过去式')
                        elif res[0][2] == 'VBZ' or 'VBP':
                            print('一般现在时')

                        break
        # 对含情态动词句子的结构判断：
        if trigger == 1:
            for i in range(len(res)):
                if res[i][0] == 'been':
                    print('主系表结构，一般将来完成时')
                    break
                elif res[i][0] == 'be' and res[i+1][2] == 'VBG'  :
                    print('主系表结构，一般将来进行时时' )
                    break
            else:
                print('主谓宾,一般将来时')
        elif trigger == 2:
            # would 的情况
            for i in range(len(res)):
                if res[i][0] in ['been','have']:
                    print('虚拟结构')
                    break
                elif res[i][0] == 'be' and res[i+1][2] == 'VBG'  :
                    print('主系表结构，过去将来进行时时' )
                    break
            else:
                print('主谓宾,过去将来时')




    elif count_comma ==1:
        # 先对非限制性定语和状语从句进行判断
        attrib(res)
        advclause_OneComma(res)
        object(res)
        special(res)
        inverse(res)
        paralel(res)
        predicat(res)
        compara(res)
        nonFinite(res)

        for i in range(len(t)):
            if t[i].label() == ',':
                if t[i-1].label() in ['PP','ADVP','S']:
                    print('-----------------修辞部分-----------------------------')
                    print(t[i-1].leaves())
                    print('-----------------从句部分-----------------------------')
                    for j in range(i+1,len(t)):
                        for k in t[j].treepositions()[1:]:
                            if type(t[j]) == nltk.tree.Tree and t[j].label() == 'VP':
                            # print(t[j,0].label())
                                if t[j,0,0] in ['am','is','are','were','was']:
                                    print('主系表结构')
                                    break

                                elif t[j,0].label() in ['VBZ','VBD','VBP'] and len(t[j])==1:
                                    print('主谓结构')
                                    print('简单句')
                                    break

                                elif t[j,0].label() in ['VBZ','VBD','VBP'] and t[j,1].label() in ['ADVP','PRT']:
                                    print('主谓结构')
                                    print('简单句')
                                    break

                                else:
                                    print('主谓宾结构')
                                    break

                    for n in range(1,len(t)-i):
                        p2.extend(t[i+n].leaves())
                    clause = ' '.join(p2)
                    print('从句成分:',clause)
                    print('----------------------从句成分判断-------------------------')
                 #主、宾、定、状、补、表、特殊

                    str = clause
                    doc = nlp(str)
                    PPres1=[f'{word.text}' for sent in doc.sentences for word in sent.words]
                    PPres2=[f'{word.upos}' for sent in doc.sentences for word in sent.words]
                    PPres3=[f'{word.xpos}' for sent in doc.sentences for word in sent.words]
                    PPres = [[PPres1[i],PPres2[i],PPres3[i]]for i in range(len(PPres1))]

                    object(PPres)
                    attrib(PPres)
                    subject(PPres)
                    advclause(PPres)
                    predicat(PPres)
                    special(PPres)
                    compara(PPres)
                    nonFinite(PPres)

                elif t[i-1].label() not in ['PP','ADVP','S']:


                        # print('--------------------前半句----------------------------')
                        # print(t[i-1].leaves())
                        # for x in t[i-1].leaves():
                        #     if 'is' in x or 'am' in x or 'are' in x or 'were' in x or 'was' in x or 'been' in x or 'be' in x :
                        #         print('主系表结构')
                        #         break
                        #     else:
                        #         print('主谓宾结构')
                        #         break
                        firstHalf=[]
                        secondHalf=[]

                        for i in range(len(res1)):
                            if res1[i]==',':
                                print('--------------------前半句----------------------------')
                                firstHalf=res1[:i]
                                print(firstHalf)
                                for item in firstHalf:
                                    if item in ['be','are','am','is','were','was','been']:
                                        print('前半句：主系表结构')
                                        break
                                else:
                                    print('前半句：主谓宾结构')

                                print('--------------------后半句----------------------------')
                                print(res1[i+1:])
                                secondHalf=res1[i+1:]
                                for item in secondHalf:
                                    if item in ['be','are','am','is','were','was','been']:
                                        print('后半句：主系表结构')
                                        break
                                else:
                                    print('后半句:主谓宾结构')



                        clause=' '.join(res1).lower()
                        # print(clause)

                        str = clause
                        doc = nlp(str)
                        NPPres1=[f'{word.text}' for sent in doc.sentences for word in sent.words]
                        NPPres2=[f'{word.upos}' for sent in doc.sentences for word in sent.words]
                        NPPres3=[f'{word.xpos}' for sent in doc.sentences for word in sent.words]
                        NPPres = [[NPPres1[i],NPPres2[i],NPPres3[i]]for i in range(len(NPPres1))]


                        attrib(NPPres)
                        advclause(NPPres)
                        special(NPPres)
                        subject_NPP(NPPres)
                        object(NPPres)
                        predicat(NPPres)
                        compara(NPPres)
                        nonFinite(NPPres)
                else:
                    print('Other Story@@@')

    elif  count_comma == 2:
        for i in range(len(t)):
            if t[i].label() != ',' and t[i].label() == 'VP':
                attrib_TwoComma(res)
                advclause(res)
                object(res)
                special(res)
                inverse(res)
                paralel(res)
                subject(res)
                predicat(res)
                compara(res)
                nonFinite(res)
                break
            elif t[i].label() == ',':
                print('let\'s do it again')
                if t[i-1].label() in ['PP','ADVP']:
                    print('-----------------修辞部分-----------------------------')
                    print(t[i-1].leaves())
                    print('-----------------主要内容部分-----------------------------')
                    for n in range(len(res1)):
                        if res1[n] == ',':
                            print(res1[n+1:])
                            break


                    main=res1[n+1:]
                    main_str = ' '.join(main).lower()

                    str = main_str
                    doc = nlp(str)
                    main_res1=[f'{word.text}' for sent in doc.sentences for word in sent.words]
                    main_res2=[f'{word.upos}' for sent in doc.sentences for word in sent.words]
                    main_res3=[f'{word.xpos}' for sent in doc.sentences for word in sent.words]
                    main_res = [[main_res1[i],main_res2[i],main_res3[i]]for i in range(len(main_res1))]

                    print('----------------------主要内容判断-------------------------')
                    #主、宾、定、状、补、表、特殊
                    attrib(main_res)
                    advclause_OneComma(main_res)
                    compara(main_res)
                    object(main_res)
                    subject_NPP(main_res)
                    predicat(main_res)
                    special(main_res)
                    inverse(main_res)
                    nonFinite(main_res)

                else:
                    print('let do it.')
                    subject(res)
                    object(res)
                    attrib_TwoComma(res)
                    advclause_TwoComma(res)
                    predicat(res)
                    special(res)
                    paralel(res)
                    inverse(res)
                    compara(res)
                    nonFinite(res)


    else:
        # 两个以上逗号
        subject(res)
        object(res)
        attrib(res)
        advclause_TwoComma(res)
        predicat(res)
        special(res)
        paralel(res)
        inverse(res)
        compara(res)
        nonFinite(res)
