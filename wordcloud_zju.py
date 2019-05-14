# -*- coding:utf-8 -*-
from scipy.misc import imread,imsave
from wordcloud import WordCloud
import jieba



sw_path = './utils/stop_words.txt'
wc = "C:\\Users\\nianyu\PycharmProjects\\3cilri\static\\th.jpg"




class word_spliter():
    def __init__(self,text,stop_path = sw_path):
        self.text = text
        self.stop_word = stop_path

    def get_stopword(self):
        stopwords = {}.fromkeys([line.rstrip() for line in open(self.stop_word, encoding='utf-8')])
        return stopwords

    def text_wash(self):
        self.text = self.text.encode(encoding="utf-8",errors='ignore').decode("utf-8")
        return self.text

    def split_word(self):
        seq = ''
        stopwords = self.get_stopword()
        text = self.text_wash()
        segs = jieba.cut(text,cut_all=False)#结巴分词
        for seg in segs:
            if seg not in stopwords:
                seq = seq + seg +" "
        return seq


class wordclouder():
    def __init__(self,text,image):
        self.text = text
        self.imag = image

    # 生成词云图
    def word_cloud(self):
        mask_image = imread(self.imag,flatten=False)
        word_pic = WordCloud(
            font_path='./utils/msyh.ttc',
            background_color='white',
            mask=mask_image
        ).generate(self.text)
        imsave(wc,word_pic)


# sp_word = word_spliter(test_text)
# text = sp_word.split_word()
# g_word = wordclouder(text,'./static/pic/mask.jpg')
# g_word.word_cloud()