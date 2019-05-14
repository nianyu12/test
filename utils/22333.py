from urllib.request import urlopen
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import process_pdf, PDFResourceManager
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba
from io import StringIO


class MyWordCloud():
    def __init__(self):
        pass

    # 此函数用于读取和返回pdf文件的内容
    def getPdfText(self, pdf_url):
        pdf_file_obj = urlopen(pdf_url)

        pdf_rm = PDFResourceManager()
        ret_str = StringIO()
        lap = LAParams()
        tc = TextConverter(pdf_rm, ret_str, laparams=lap)

        process_pdf(pdf_rm, tc, pdf_file_obj)
        tc.close()
        pdf_text = ret_str.getvalue()
        ret_str.close()
        return pdf_text

    def genWordCloud(self, pdf_url):
        pdf_text = self.getPdfText(pdf_url)

        # WordCloud（按英文习惯）以空格分词，中文不用空格所以WordCloud不能正确对中文进行分词
        # 为了使用WordCloud我们就需要先自己自己想办法完成分词，并将所有分词以空格隔开
        # 我们的方法是先用结巴生成中文序列，然后使用join方法使用空格拼接所有序列
        jieba_cut_seq = jieba.cut(pdf_text)
        pdf_cut_text = " ".join(jieba_cut_seq)

        # 默认字体不支中文，需要指定要使用的中文字体路径；可从自己电脑已安装的字体中选，目录C:\Windows\Fonts
        font_path = "C:\\Windows\\Fonts\\simfang.ttf"
        wc = WordCloud(font_path, width=1000, height=880).generate(pdf_cut_text)

        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.show()

    def __del__(self):
        pass


if __name__ == '__main__':
    # 深圳十三五规划纲要文件的URL链接，要生成其他pdf文件的词云修改成该文件的URL即可
    pdf_url = 'http://www.sz.gov.cn/fzggj/home/zwgk/ghjh/fzgh/201604/P020160412518770846515.pdf'
    mwc = MyWordCloud()
    mwc.genWordCloud(pdf_url)