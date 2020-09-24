import jieba
import gensim
import re
import os
from functools import reduce
from sys import argv


def read_file_to_cut(filepath):
    # 读文件并将行都连接
    wrapper_str = open(filepath, 'r', encoding='utf-8')
    str = reduce(lambda old_str, new_str: old_str +
                 new_str, wrapper_str.readlines())
    # 使用jieba进行分词
    # 对分词进行过滤，只保留字母和中文
    # def filter(string):
    filter_str = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]").sub("", str)
    return list(jieba.lcut(filter_str))


def calc_similarity(cut_str1, cut_str2):
    cut_strs = [cut_str1, cut_str2]
    dictionary = gensim.corpora.Dictionary(cut_strs)
    corpus = [dictionary.doc2bow(cut_str) for cut_str in cut_strs]
    similarity = gensim.similarities.Similarity(
        '-Similarity-index', corpus, num_features=len(dictionary))
    test_corpus_1 = dictionary.doc2bow(cut_str1)
    cosine_sim = similarity[test_corpus_1][1]
    return cosine_sim
# './test/orig.txt'
# './test/orig_0.8_add.txt'
# './result.txt'


def main():
    if(len(argv) < 3):
        print('参数不足，请依次输入源文件路径，对比文件路径和结果保存路径')
        exit()
    elif(not(os.path.exists(argv[1]) and os.path.exists(argv[2]))):
        print('源文件或对比文件不存在')
        exit()
    elif(os.path.getsize(argv[1]) == 0 or os.path.getsize(argv[2]) == 0){
        print('源文件或对比文件为空')
        exit()
    }
    similarity = calc_similarity(read_file_to_cut(
        argv[1]), read_file_to_cut(argv[2]))
    # similarity = calc_similarity(read_file_to_cut(
    # './test/orig.txt'), read_file_to_cut('./test/orig_0.8_add.txt'))
    f = open(argv[3], 'w', encoding="utf-8")
    f.write("文章相似度： %.4f" % similarity)
    f.close()
    print('文章相似度：%.4f' % (similarity))


main()
