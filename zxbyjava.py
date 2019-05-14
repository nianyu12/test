# -*- coding: utf-8 -*-
# __author__="ZJL"

import os, subprocess, tempfile,io

# 创建临时文件夹,返回临时文件夹路径
TempFile = tempfile.mkdtemp(suffix='_test', prefix='java_')
# javac 和 Java 编译器位置
JAVAC_EXEC = "C:\java\jdk1.8.0_121\\bin\javac"
JAVA_EXEC = "C:\java\jdk1.8.0_121\\bin\java"


# 获得java文件名
def get_javaname(code):
    if code:
        if "public class" in code and "{" in code:
            FileName = code.split("public class ")[1].split("{")[0].strip()
        else:
            FileName = "test"
        return FileName


# 接收代码写入文件
def write_file(jname, code):
    fpath = os.path.join(TempFile, '%s.java' % jname)#路径组合，文件名加路径
    with io.open(fpath, 'w', encoding='utf-8') as f:
        f.write(code)
    print('file path: %s' % fpath)
    return fpath


# 编码
def decode(s):
    try:
        return s.decode('utf-8')
    except UnicodeDecodeError:
        return s.decode('gbk')


# 主执行函数
def main(code):
    r = dict()
    jname = get_javaname(code)
    fpath = write_file(jname, code)
    try:
        # subprocess.check_output 是 父进程等待子进程完成，返回子进程向标准输出的输出结果
        # stderr是标准输出的类型
        # 编译Java代码
        outdata = decode(subprocess.check_output([JAVAC_EXEC, fpath], stderr=subprocess.STDOUT))
    except subprocess.CalledProcessError as e:
        # e.output是错误信息标准输出
        # 错误返回的数据
        r["运行"] = '失败'
        outdata = decode(e.output)
        r["output"] = ' ' + outdata[51:]
        return r
    else:
        # 执行Java代码
        # 因为调用原因，bat写绝对路径
        outdata = decode(
            subprocess.check_output(["C:\\Users\\nianyu\\PycharmProjects\\zhiliao\\test.bat", TempFile, JAVA_EXEC, jname],
                                    stderr=subprocess.STDOUT))
        # 成功返回的数据
        r["运行"] = "成功"
        r['output'] = ' ' + outdata[51:]

        return r

# if __name__ == '__main__':
#     code ="""public class hello {public static void main(String []args) {System.out.println("Hello World");}}"""
#     print(main(code))