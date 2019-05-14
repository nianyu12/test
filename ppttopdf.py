'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#作者：cacho_37967865
#博客：https://blog.csdn.net/sinat_37967865
#文件：pdfConverter.py
#日期：2018-04-22
#备注：通过调用Python访问COM对象的comtypes包，批量将ppt或者word转换为PDF文件，先要在python环境安装comtypes       
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# F:\python_env\PaChong_env
# -*- coding: utf-8 -*-

from comtypes.client import CreateObject
import os


class pdfConverter:
    def __init__(self):
        # ppt文档转化为pdf文档时使用的格式为32
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


if __name__ == "__main__":
    converter = pdfConverter()
    converter.ppt_to_pdf("C:\\Users\\nianyu\Desktop\毕设")
