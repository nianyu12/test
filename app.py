# coding:utf-8
import flask
from wordcloud_zju import word_spliter,wordclouder
from pdfminer.converter import TextConverter
from io import StringIO
#
from comtypes.client import CreateObject
from flask import Flask, render_template, request,redirect,url_for
from flask_bootstrap import Bootstrap
#
import os
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import *
app = Flask(__name__)
bootstrap = Bootstrap(app)
from flask import Flask,render_template,request,redirect,url_for
import config
import zxby
import zxbyjava
app = Flask(__name__)
app.config.from_object(config)
from flask_cors import CORS



# 上传pdf模块

test = "C:\\Users\\nianyu\PycharmProjects\\3cilri\static\\uploads\\test.pdf"
test1 = "C:\\Users\\nianyu\PycharmProjects\\3cilri\static\\uploads\\test1.pdf"
test2 = "C:\\Users\\nianyu\PycharmProjects\\3cilri\static\\upload2\\test2.pptx"
test3= "C:\\Users\\nianyu\PycharmProjects\\3cilri\static\\upload1\\test1.ppt"




# 在线编程模块
@app.route('/')
def index():
    return redirect(url_for('runpy'))

@app.route('/runhtml/')
def runhtml():
    return render_template('runhtml.html')

@app.route('/runjs/')
def runjs():
    return render_template('runjs.html')

@app.route('/runpy1/')
def runpy1():
    return render_template('runpy1.html')



# python编译部分
@app.route('/runpy', methods=['POST','GET'])
def runpy():
    if request.method=='GET':
        return render_template('runpy.html')
    elif request.method == 'POST':
        code = request.form['code']
        print(code)
        jsondata = zxby.main(code)
        data=jsondata["output"]
        return "aaa"
        # return Response_headers(str(jsondata))
    else:
        return redirect(url_for('runpy'))





# java部分
@app.route('/runjava/',methods=['POST','GET'])
def runjava():
    if request.method=='GET':
        return render_template('runjava.html')
    elif request.method == 'POST' and request.form['code']:
        code = request.form['code']
        jsondata = zxbyjava.main(code)
        return render_template('runjava.html', data=jsondata)
    else:
        return redirect(url_for('runjava'))


# 课件辅助模块
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        # pdf文件写入
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        new_filename =test
        f.save(os.path.join(basepath, 'static\\uploads', new_filename))

        # pdf转化后生成词云
        pdf_to_txt('C:\\Users\\nianyu\PycharmProjects\\3cilri\static\\uploads\\test.pdf', "c.txt")
        file1 = open('c.txt','r')
        text = file1.read()
        pic_path = "C:\\Users\\nianyu\PycharmProjects\\3cilri\static\\pic\\th.jpg"
        generate_wordcloud(text, pic_path)
        return render_template('uploadok.html')
    else:
        err = "post method required"
    return  flask.render_template('upload.html',error=err)

@app.route('/uploadok', methods=['POST', 'GET'])

def uploadok():
    if request.method == 'POST':
        # pdf文件写入保存在本地
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        new_filename =test
        f.save(os.path.join(basepath, 'static\\uploads', new_filename))
        # pdf转化后生成词云
        pdf_to_txt('C:\\Users\\nianyu\PycharmProjects\\3cilri\static\\uploads\\test.pdf', 'c.txt') #生成txt函数调用
        file1 = open('c.txt','r') #读取txt文件内容
        text = file1.read()
        # 生成词云图片
        pic_path = "C:\\Users\\nianyu\PycharmProjects\\3cilri\static\\pic\\th.jpg"
        generate_wordcloud(text, pic_path)
        return render_template('uploadok.html')
    else:
        err = "post method required"
    return  flask.render_template('upload.html',error=err)



@app.route('/uploadpdf', methods=["GET", "POST"])
def uploadpdf():
    if request.method == 'GET':
        return render_template("uploadpdf.html")
    elif request.method == 'POST'and request.files['pdf']:
        # pdf文件写入保存在本地
        f = request.files['pdf']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        new_filename =test1
        f.save(os.path.join(basepath, 'static\\uploads', new_filename))
        return redirect(url_for('pdfonline'))
    else:
        return render_template("uploadpdf.html")

@app.route('/uploadppt', methods=["GET", "POST"])
def uploadppt():
    if request.method == 'GET':
        return render_template("uploadppt.html")
    elif request.method == 'POST':
        # pdf文件写入保存在本地
        f = request.files['ppt']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        new_filename =test3
        f.save(os.path.join(basepath, 'static\\upload1', new_filename))
        import pythoncom
        pythoncom.CoInitialize()
        converter = pdfConverter()
        converter.ppt_to_pdf("C:\\Users\\nianyu\PycharmProjects\\3cilri\static\\upload1")
        return redirect(url_for('pptonline'))
    else:
        return render_template("uploadppt.html")

@app.route('/uploadpptx', methods=["GET", "POST"])
def uploadpptx():
    if request.method == 'GET':
        return render_template("uploadpptx.html")
    elif request.method == 'POST':
        # pdf文件写入保存在本地
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        new_filename =test2
        f.save(os.path.join(basepath, 'static\\upload2', new_filename))
        import pythoncom
        pythoncom.CoInitialize()
        converter = pdfConverter()
        converter.ppt_to_pdf("C:\\Users\\nianyu\PycharmProjects\\3cilri\static\\upload2")
        return redirect(url_for('pptxonline'))
    else:
        return render_template("uploadpptx.html")

@app.route('/pdfonline', methods=["GET", "POST"])
def pdfonline():
    return render_template("pdfonline.html")

@app.route('/pptxonline', methods=["GET", "POST"])
def pptxonline():
    return render_template("pptxonline.html")

@app.route('/pptonline', methods=["GET", "POST"])
def pptonline():
    return render_template("pptonline.html")



def generate_wordcloud(text,pic):
    sp_word = word_spliter(text)
    words = sp_word.split_word() #分词
    g_word = wordclouder(words,pic)
    g_word.word_cloud()

# pdf转txt函数
def pdf_to_txt(path,save_name):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 10000
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    try:
        with open("%s"%save_name,"w") as f:
            for i in str:
                f.write(i)
        print ("%s Writing Succeed!"%save_name)
    except:
        print ("Writing Failed!")
# ppttopdf

class pdfConverter:
    def __init__(self):
        #ppt文档转化为pdf文档时使用的格式为32
        self.pptFormatPDF = 32
        self.pptToPDF = CreateObject("Powerpoint.Application")
        self.pptToPDF.Visible = 1

    def ppt_to_pdf(self, folder):
        files = os.listdir(folder)
        pptfiles = [f for f in files if f.endswith((".ppt", ".pptx"))]
        for pptfile in pptfiles:
            pptPath = os.path.join(folder, pptfile)
            pdfPath = pptPath
            if pdfPath[-3:] != 'pdf':
                pdfPath = pdfPath + ".pdf"
            pdfCreate = self.pptToPDF.Presentations.Open(pptPath)
            pdfCreate.SaveAs(pdfPath, self.pptFormatPDF)
            pdfCreate.Close()


if __name__ == '__main__':
    app.run(debug=True)