from PyQt5.QtCore import *
# 如果全部引入connect会出错
from PyQt5.QtWidgets import QApplication, QWidget, QRadioButton, QTextEdit, QLineEdit,QFrame,QVBoxLayout,QDialog
from PyQt5.QtWidgets import  QHBoxLayout,QGridLayout,QGroupBox,QPushButton,QTextBrowser
from PyQt5.QtGui import *

import sys
from final import *


class WidegtGallery(QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("信息检索系统")
        self.resize(600,600)
        self.setFixedSize(self.width(), self.height())


        # frame1 两个按钮
        self.frame1 = QGroupBox("查询方式")
        self.frame1layout = QVBoxLayout(self.frame1)
        boolratiobotton = QRadioButton("布尔查询")
        boolratiobotton.setChecked(True)
        shortratiobotton = QRadioButton("短语查询")
        self.frame1layout.addWidget(boolratiobotton)
        self.frame1layout.addWidget(shortratiobotton)
        self.frame1.setVisible(True)

        # 设置两种不同的布局
        # 布尔查询界面
        self.bool_group = QGroupBox("布尔查询")
        self.creat_bool_group()
        main_layout = QGridLayout()
        main_layout.addWidget(self.frame1,0,0)
        main_layout.addWidget(self.bool_group,1,0)
        self.setLayout(main_layout)

        # 短语查询界面
        self.short_group = QGroupBox("短语查询")
        self.create_short_window()
        main_layout.addWidget(self.short_group,2,0)

        # 结果展示界面

        # self.show_group = QGroupBox("搜索结果")
        # self.create_show_window()
        # main_layout.addWidget(self.show_group,3,0)

        self.textBrowser = QTextBrowser()
        main_layout.addWidget(self.textBrowser, 3, 0)
        # self.textBrowser.setObjectName("textBrowser")

        # 设置逻辑关系
        boolratiobotton.clicked.connect(self.enter_bool_search)
        shortratiobotton.clicked.connect(self.enter_short_search)
        # 默认状态
        self.bool_group.setVisible(True)
        self.short_group.setVisible(False)

    def creat_bool_group(self):
        # 布尔检索的四个选项
        self.and_ratiobotton1 = QRadioButton("and")
        self.or_ratiobotton2 = QRadioButton("or")
        self.andnot_ratiobotton3 = QRadioButton("and not")
        self.ornot_ratiobotton4 = QRadioButton("or not")
        resumebotton = QPushButton("查询")
        resumebotton.clicked.connect(lambda :self.bool_show())# 传递参数要用lambda

        # 布尔检索的两个输入框
        self.textedit1 = QTextEdit()
        self.textedit2 = QTextEdit()


        self.textedit1.setPlainText("请输入短语1")
        self.textedit2.setPlainText("请输入短语2")
        self.input1 = self.textedit1.toPlainText()
        self.input2 = self.textedit2.toPlainText()
        boollayout = QGridLayout()

        boollayout.addWidget(self.and_ratiobotton1,0,0)
        boollayout.addWidget(self.or_ratiobotton2,1,0)
        boollayout.addWidget(self.andnot_ratiobotton3,2,0)
        boollayout.addWidget(self.ornot_ratiobotton4,3,0)
        boollayout.addWidget(self.textedit1,1,1)
        boollayout.addWidget(self.textedit2,2,1)
        boollayout.addWidget(resumebotton,5,0)

        self.bool_group.setLayout(boollayout)

    def create_show_window(self):
        # 显示搜索结果的窗体
        # self.show_line = QTextBrowser()
        show_line = QTextEdit()
        show_line.setReadOnly(True)
        show_layout = QHBoxLayout()
        show_layout.addWidget(show_line)

        self.show_group.setLayout(show_layout)



    def create_short_window(self):
        # 设置短语查询窗体
        self.shorttextedit1 = QTextEdit()
        resumebotton = QPushButton("查询")
        resumebotton.clicked.connect(lambda :self.short_show())# 传递参数要用lambda
        short_layout = QGridLayout()
        short_layout.addWidget(self.shorttextedit1,0,0)
        short_layout.addWidget(resumebotton,1,0)

        self.short_group.setLayout(short_layout)


    def enter_bool_search(self):
        self.bool_group.setVisible(True)
        self.short_group.setVisible(False)
        pass

    def enter_short_search(self):
        self.short_group.setVisible(True)
        self.bool_group.setVisible(False)
        pass

    def printf(self, mypstr):
        # 重写printf函数显示到broswer
        self.textBrowser.append(mypstr)
        self.cursor=self.textBrowser.textCursor()
        self.textBrowser.moveCursor(self.cursor.End)
        QApplication.processEvents()

    def short_show(self):
        duanyu = self.shorttextedit1.toPlainText()
        result = quest_words(dp,duanyu)
        # if result == False:
        #     self.printf("查无此短语")
        # else:
        self.printf(str("短语 "+duanyu+" 的查询结果:"))
        for i in result:
            str1 = "在第"+str(i[0]+1)+"篇文档查询到短语，词项位置为"+str(i[1])
            self.printf(str1)
            self.printf(get_pre_info(paths ,i[0], i[1]))
            self.printf("\n")




    def bool_show(self):
        input1 =self.textedit1.toPlainText()# 传递textedit的值
        input2 = self.textedit2.toPlainText()
        action = "and"


        if self.and_ratiobotton1.isChecked():
            self.printf("and查询")
            action = "and"


        if self.andnot_ratiobotton3.isChecked():
            self.printf("and_not查询")
            action = "and_not"

        if self.or_ratiobotton2.isChecked():
            self.printf("or查询")
            action = "or"

        if self.ornot_ratiobotton4.isChecked():
            self.printf("or_not查询")
            action = "or_not"

        result = bool_retreive(dp, input1, input2, action)
        self.printf(result)# 显示搜索结果







if __name__ == "__main__":
    '''
        词项集初始化
    '''
    paths = [os.path.join(doc_path, i) for i in get_file(doc_path)]
    print(paths)
    for i in range(len(paths)):
        after_jieba = cut_words(paths[i])  # jieba分词
        after_rm_stop = del_stop_words(after_jieba)  # 删除停用词以及标点符号 *** 记录了包含词项顺序的这篇文档的词项情况 ***
        after_rm_redundency = clean_redundance(after_rm_stop)

        for word in after_rm_redundency:
            if word not in list(dp.keys()):  # 补充倒排记录表的词项，将原来没有的词项添加进来
                dp[word] = dict()
            each_word_in_doc = [index for (index, value) in enumerate(after_rm_stop) if value == word]  # 统计得到这个词项在这篇文章里的倒排记录表
            dp[word][i] = each_word_in_doc  #将 word 词项在 i 这篇文档下面的dp记录表赋值
    '''
        界面启动
    '''
    app = QApplication(sys.argv)
    dialog = WidegtGallery()
    if dialog.exec_() == QDialog.Accepted:
        sys.exit(app.exec_())







