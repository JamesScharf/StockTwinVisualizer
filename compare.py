import itertools
from collections import Counter, defaultdict
from typing import Dict, List, NamedTuple
import numpy as np
from numpy.linalg import norm
from nltk.tokenize import word_tokenize
import statistics
from nltk.stem import SnowballStemmer
from nltk.corpus import wordnet as wn
from sklearn.metrics.pairwise import cosine_similarity
import math
import argparse
import itertools
import re
import string
from nltk.tokenize import sent_tokenize
import Scraper
import csv

def read_stopwords(file):
    with open(file) as f:
        return set([x.strip() for x in f.readlines()])

commons = read_stopwords('common_words')

stemmer = SnowballStemmer('english')
translator=str.maketrans('','',string.punctuation)

#string_name=string_name.translate(translator)
    #for i in range(len(spl)):
    #    spl[i] = stemmer.stem(spl[i])
def trans_lst(l):
    m = []
    for j in range(len(l)):
        k = l[j].translate(translator)
        m.append(k)
    return m
def process_stocks(stocks):
    #stocks is a List, need to stem, translate, and remove stop words
    #go through stocks
    for s in stocks:
        s.texts = trans_lst(s.texts)#s.texts.translate(translator)
        s.titles = trans_lst(s.titles)#s.titles.translate(translator)
        spl1 = s.wikiSummary.split()
        #stocks[i].wikiSummary = spl1

        for word in list(spl1):  # iterating on a copy since removing will mess things up
            if word in commons:
                spl1.remove(word)
        for i in range(len(spl1)):
            spl1[i] = stemmer.stem(spl1[i])

        play_te = []
        for t in s.texts:
            spl2 = t.split()
            for word in list(spl2):  # iterating on a copy since removing will mess things up
                if word in commons:
                    spl2.remove(word)
            for i in range(len(spl2)):
                spl2[i] = stemmer.stem(spl2[i])
            play_te.append(spl2)

        s.texts = play_te

        play_ti = []
        for t in s.titles:
            spl2 = t.split()
            for word in list(spl2):  # iterating on a copy since removing will mess things up
                if word in commons:
                    spl2.remove(word)
            for i in range(len(spl2)):
                spl2[i] = stemmer.stem(spl2[i])
            play_ti.append(spl2)
        s.titles = play_ti
        s.wikiSummary = spl1
        play_ref = []
        for t in s.wikiReferences:
            spl2 = t.split()
            for word in list(spl2):  # iterating on a copy since removing will mess things up
                if word in commons:
                    spl2.remove(word)
            for i in range(len(spl2)):
                spl2[i] = stemmer.stem(spl2[i])
            play_ref.append(spl2)
        s.wikiReferences = play_ref


def create_vocab(stocks):
    voc_s = []
    voc_news = []
    word_to_index_sum  = dict()
    word_to_index_news = dict()
    counter = 0
    #creates vocab for all the summaries
    for s in stocks:
        for word in s.wikiSummary:
            if word not in voc_s:
                voc_s.append(word)
                word_to_index_sum[word] = counter
                counter = counter + 1
    counter = 0
    for s in stocks:
        for t in s.texts:
            for word in t:
                if word not in voc_news:
                    voc_news.append(word)
                    word_to_index_news[word] = counter
                    counter = counter + 1
        for t in s.titles:
            for word in t:
                if word not in voc_news:
                    voc_news.append(word)
                    word_to_index_news[word] = counter
                    counter = counter + 1


    return voc_s, word_to_index_sum, voc_news, word_to_index_news
#give it a list of tf
def to_mat(tf,voc, w2i):
    vec_terms = np.zeros((len(tf), len(voc)))
    for i in range(len(tf)):
        for word in tf[i]:
            if word in voc:
                vec_terms[i][w2i[word]] = tf[i][word]

    return vec_terms

def tf_calc(voc_sum, word_to_index_sum, voc_news, word_to_index_news, voc_ref, word_to_index_ref, s):
    m_lst = [] #holds at 0--> summary 1--> news
    wordfreq_s = dict.fromkeys(voc_sum, 0)
    wordfreq_n = dict.fromkeys(voc_news, 0)
    wordfreq_r = dict.fromkeys(voc_ref, 0)
    sum_l = []
    for word in s.wikiSummary:
        if word in voc_sum:
            wordfreq_s[word] = s.wikiSummary.count(word)
    sum_l.append(wordfreq_s)
    #so each row in the list is a dictionary with the amount of times the word appears
    ste = []
    for t in s.texts:
        new_dict = dict.fromkeys(voc_news, 0)
        for word in t:
            if word in voc_news:
                new_dict[word] = t.count(word)
        ste.append(new_dict)
    sref = []
    for t in s.wikiReferences:
        new_dict = dict.fromkeys(voc_ref, 0)
        for word in t:
            if word in voc_ref:
                new_dict[word] = t.count(word)
        sref.append(new_dict)

    sum_mat = to_mat(sum_l,voc_sum, word_to_index_sum)
    news_mat = to_mat(ste,voc_news, word_to_index_news)
    ref_mat = to_mat(sref, voc_ref, word_to_index_ref)
    m_lst.append(sum_mat)
    m_lst.append(news_mat)
    m_lst.append(ref_mat)
    return m_lst

def separate_stocks(mats):
    sum_mat_dict = {}
    news_mat_dict = {}
    ref_mat_dict = {}
    for key in mats:
        sum_mat_dict[key] = mats[key][0]
        news_mat_dict[key] = mats[key][1]
        ref_mat_dict[key] = mats[key][2]
    return sum_mat_dict, news_mat_dict, ref_mat_dict

def do_cos(a, b):
    cos_sim = (np.dot(a, b))/(norm(a)*norm(b))
    return cos_sim

def find_avg_vec(mat, voc):
    total = len(mat)
    if total == 0:
        total = 1

    sum_vec= []
    sum_holder = 0
    for j in range(len(voc)):
        sum_holder = 0
        for i in range(len(mat)):
            sum_holder = sum_holder + mat[i][j]
        sum_vec.append(sum_holder)
    for i in range(len(sum_vec)):
        sum_vec[i] = sum_vec[i] / total

    return sum_vec




def make_vec_profs(mat, voc):
    di = {}
    #counter = 0
    for key in mat:
        l = find_avg_vec(mat[key], voc)
        di[key] = l
    return di

def get_link_set(lst):
    out_set = []
    for m in lst:
        if m not in out_set:
            out_set.append(m)
    return out_set

def links_comp(s, t):
    score = 0
    t_link_set = get_link_set(t.wikiLinks)
    s_link_set = get_link_set(s.wikiLinks)
    if len(t_link_set) > len(s_link_set):
        for i in t_link_set:
            if i in s_link_set:
                score += 1.0
        return score/len(t_link_set)
    else:
        for i in s_link_set:
            if i in t_link_set:
                score += 1.0
        if len(s_link_set) == 0:
            return 0
        return score/len(s_link_set)




def get_CSV(sum_profs, news_profs, ref_prof, t1, stocks, test_stock):
    out_lst = []
    a = ["stock_SYMBOL", "STOCK_COMPANY", "WIKI_SIMILARITY", "NEWS_SIMILARITY", "LINK_SIMILARITY", "REFERENCE SIMILARITY"]
    for s in stocks:
        d = dict.fromkeys(a, 0)
        d["stock_SYMBOL"] = s.symbol
        d["STOCK_COMPANY"] = s.name
        d["WIKI_SIMILARITY"] = do_cos(sum_profs[s.symbol], t1[0][test_stock.symbol])
        d["NEWS_SIMILARITY"] = do_cos(news_profs[s.symbol], t1[1][test_stock.symbol])
        d["LINK_SIMILARITY"] = links_comp(s, test_stock)
        d["REFERENCE SIMILARITY"] = do_cos(ref_prof[s.symbol], t1[2][test_stock.symbol])
        out_lst.append(d)
    return out_lst, a #hols dictionary with keys as follows

def create_ref_vocab(stocks):
    voc_ref = []
    word_to_index_ref = dict()
    counter = 0
    counter = 0
    for s in stocks:
        for t in s.wikiReferences:
            for word in t:
                if word not in voc_ref:
                    voc_ref.append(word)
                    word_to_index_ref[word] = counter
                    counter = counter + 1
    return voc_ref, word_to_index_ref



def experiment(amount, test_s):
    stocks = Scraper.scrape(amount)
    process_stocks(stocks)
    voc_sum, word_to_index_sum, voc_news, word_to_index_news = create_vocab(stocks)
    voc_ref, word_to_index_ref = create_ref_vocab(stocks)
    stock_mats = {}
    #stock name -->[mat_sum, mat_news]
    for s in stocks:
        stock_mats[s.symbol] = tf_calc(voc_sum, word_to_index_sum, voc_news, word_to_index_news, voc_ref, word_to_index_ref,s)
    sums, news, refs = separate_stocks(stock_mats)

    sum_prof = make_vec_profs(sums, voc_sum)
    news_prof = make_vec_profs(news, voc_news)
    ref_prof = make_vec_profs(refs, voc_ref)

    test = []
    test.append(test_s)
    process_stocks(test)
    #voc_sum_test, word_to_index_sum_test, voc_news_test, word_to_index_news_test = create_vocab(test)
    stock_mats_test = {}
    #stock name -->[mat_sum, mat_news]
    for s in test:
        stock_mats_test[s.symbol] = tf_calc(voc_sum, word_to_index_sum, voc_news, word_to_index_news, voc_ref, word_to_index_ref, s)
    sums_test, news_test, refs_test = separate_stocks(stock_mats_test)
    sum_prof_test = make_vec_profs(sums_test, voc_sum)
    news_prof_test = make_vec_profs(news_test, voc_news)
    refs_prof_test = make_vec_profs(refs_test, voc_ref)
    t_profs = []
    t_profs.append(sum_prof_test)
    t_profs.append(news_prof_test)
    t_profs.append(refs_prof_test)
    toCSV, keys = get_CSV(sum_prof, news_prof, ref_prof, t_profs, stocks, test[0])
    #keys = toCSV[0].keys()
    with open('output.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(toCSV)

if __name__ == '__main__':
    experiment(10, Scraper.Stock("GOOG", "Alphabet Inc", "Technology"))
