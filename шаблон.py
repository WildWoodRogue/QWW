
"""
Приложение 'Калькулятор'
"""

import sys
import math
from PyQt5.QtWidgets import QFileDialog, QApplication, QLabel, QWidget, QPushButton, QMessageBox, QLCDNumber, QLineEdit, QGridLayout, QMainWindow, QAction, qApp
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont, QIcon

size  = 65
board = 10

countRowButton    = 5
countColumnButton = 5

countAdditionalColumnButton = 2

heigthMenuBar = 30

widthWindow = 8*size
hightWindow = 8*size

widthButton = widthWindow//8- board
hightButton = hightWindow//8- board

widthLabelBig = widthWindow*5//8 - 2*board
hightLabelBig = hightWindow//4- 2*board

widthLabelSmall = widthWindow*5//8- 2*board
hightLabelSmall = hightWindow//8- 2*board

widthLabelHistory = widthWindow*3//8- 2*board
hightLabelHistory = hightWindow*7//8- 2*board



class Calculator(QMainWindow):

    # ???
    def buts(self):
        """ """
        print("1")
    # Сохранение файла
    def saveFileDialog(self):
        """ """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","Text Files (*.txt)", options=options)
        file = open(fileName,'w')
        file.write(self.labelHistory.text())
    # Открытие файла
    def openFile(self):
        """ """
        fileName = QFileDialog.getOpenFileName()
        print(str(fileName[0]))
        file = open(str(fileName[0]),'r')
        string = file.read()
        self.labelHistory.setText(string)
    # Расширение окна
    def expansion(self):
        """ """
        if self.buttonAdd.text()=="→":

            bigWidthWindow = widthWindow+(size*countAdditionalColumnButton*2)
            self.labelHistory.move((widthButton+board)*(countColumnButton+2*countAdditionalColumnButton)+board,hightWindow//8+board+heigthMenuBar)
            self.buttonDeleteHistory.move(widthWindow-(widthWindow//8)+(2*size*countAdditionalColumnButton),heigthMenuBar+board)
            self.buttonAdd.move(widthWindow-(widthWindow//4)+(2*size*countAdditionalColumnButton),heigthMenuBar+board)
            self.buttonNewWindow.move(widthWindow-(widthWindow//(26/10))+(2*size*countAdditionalColumnButton),heigthMenuBar+board)

            self.resize(QSize(bigWidthWindow, hightWindow+heigthMenuBar))
            self.setFixedSize(bigWidthWindow, hightWindow+heigthMenuBar)

            for row in range(countRowButton):
                for col in range(countAdditionalColumnButton):
                    self.buttonList[row][countColumnButton+col].show()

            self.buttonAdd.setText("←")
        elif self.buttonAdd.text()=="←":
            self.labelHistory.move(widthWindow*5//8+board,hightWindow//8+board+heigthMenuBar)
            self.buttonDeleteHistory.move(widthWindow-(widthWindow//8),heigthMenuBar+board)
            self.buttonAdd.move(widthWindow-(widthWindow//4),heigthMenuBar+board)
            self.buttonNewWindow.move(widthWindow-(widthWindow//(26/10)),heigthMenuBar+board)
            self.resize(QSize(widthWindow, hightWindow+heigthMenuBar))
            self.setFixedSize(widthWindow, hightWindow+heigthMenuBar)
            self.buttonAdd.setText("→")
            for row in range(countRowButton):
                for col in range(countAdditionalColumnButton):
                    self.buttonList[row][countColumnButton+col].hide()
    # Кнопка удаления истории
    def deleteHistory(self):
        """ """
        self.labelHistory.setText("")
    # Точка
    def point(self,key):
        """ """
        if key not in self.labelSmall.text() and self.labelSmall.text()!="":
            self.labelSmall.setText(self.labelSmall.text()+key)
    # Скобки
    def brackets(self,key):
        """ """
        if key == "(":
            if self.labelBig.text() != '':
                if self.labelBig.text()[-1] == ')':
                    self.labelBig.setText(self.labelBig.text() + '*(')
                else:
                    self.labelBig.setText(self.labelBig.text() + '(')
            else:
                self.labelBig.setText('(')
        elif key == ")":
                countOpenBrackets = (list(self.labelBig.text())).count('(')
                countClosedBrackets = (list(self.labelBig.text())).count(')')

                if self.labelBig.text() != '':
                    if self.labelBig.text()[-1] == '(':
                        self.labelBig.setText(self.labelBig.text() + '0' + ')')
                    elif countClosedBrackets < countOpenBrackets:
                        self.labelBig.setText(self.labelBig.text() + self.labelSmall.text() + ')')
                        self.labelSmall.setText('')
    # Арифметика
    def signs(self,key):
        """ """
        if "-" not in self.labelSmall.text():
            if '=' not in self.labelBig.text():

                if self.labelSmall.text()!='' and (self.labelSmall.text() !="-"):
                    self.labelBig.setText(self.labelBig.text()+self.labelSmall.text()+key)
                    self.labelSmall.setText("")
                else:
                    if key=="-":
                        self.labelSmall.setText('-')
            else:
                self.labelBig.setText(self.labelSmall.text()+key)
                self.labelSmall.setText("")
        else:
            if '=' not in self.labelBig.text():
                if self.labelSmall.text()!='' and (self.labelSmall.text() !="-"):
                    self.labelBig.setText(self.labelBig.text()+'('+self.labelSmall.text()+')'+key)
                    self.labelSmall.setText("")
                else:
                    if key=="-":
                        self.labelSmall.setText('-')
            else:
                self.labelBig.setText('('+self.labelSmall.text()+')'+key)
                self.labelSmall.setText("")
    # Удаление последнего символа
    def deleteLastChar(self):
        """ """
        self.labelSmall.setText(self.labelSmall.text()[:-1])
    # Числа
    def numbers(self,key):
        """ """
        if '=' not in self.labelBig.text():
            self.labelSmall.setText(self.labelSmall.text()+key)
            if self.labelBig.text()!="":
                if self.labelBig.text()[-1]==")":
                    self.labelBig.setText(self.labelBig.text()+"×")


        else:
            self.labelBig.clear();
            self.labelSmall.setText(key)
    # Счёт
    def score(self):
        """счёт по нажатию равно или enter"""
        try :
            if "-" not in self.labelSmall.text():
                output = (self.labelBig.text()+self.labelSmall.text())
            else:
                output = (self.labelBig.text()+'('+self.labelSmall.text()+')')
            countOpenBrackets=output.count("(")
            countClosedBrackets=output.count(")")
            if countOpenBrackets>countClosedBrackets and "1234567890" in self.labelSmall.text() and  self.labelSmall.text():
                output+=(countOpenBrackets-countClosedBrackets)*")"
            else:
                if self.labelSmall.text()[0]=="(":
                    output+="0"+(countOpenBrackets-countClosedBrackets)*")"

            result = eval("*".join(("/".join(("**".join(output.split("^"))).split("÷"))).split("×")))
            self.labelBig.setText(output+"=")
            self.labelSmall.setText(str(int(result)))
            #добавление в labelHistory
            historyBefore=(output+"="+str(result))
            historyAfter=''
            counter=0
            for char in historyBefore:
                counter+=1
                historyAfter+=char
                if counter%21==0:
                     historyAfter+='\n'
                     counter=0
                elif char == "=":
                    historyAfter=historyAfter[:-1]+'\n='
                    counter=0
            self.labelHistory.setText(historyAfter+"\n\n"+self.labelHistory.text())
        except:
            print(output)
    # Работа калькулятора с помощью клавиатуры
    def keyPressEvent(self, event):
        # Двумерный массив сопоставления кодов клавиш к их ключам: 1строка - код, 2строка - ключ
        arrayOfKeys = [['48','49','50','51','52','53','54','55','56','57','16777220','43','45','42','47','16777221','16777219','42','40','41', '46'],
                       ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ,'='       ,'+', '-' , '×','÷',  '='      , '<',      '×',  '(', ')', '.']]
        if (str(event.key()) in arrayOfKeys[0]):
            for ind in range(len(arrayOfKeys[0])):
                if str(event.key()) == arrayOfKeys[0][ind]:
                    key = arrayOfKeys[1][ind]
                    # Счёт
                    if key == "=":
                        self.score()
                    # Цифры
                    elif key in "1234567890":
                        self.numbers(key)
                    # Удаление символа BackSpace
                    elif key=="<":
                        self.deleteLastChar()
                    # Арифметика
                    elif key in "+-×÷^":
                        self.signs(key)
                    # Cкобки
                    elif key in "()":
                        self.brackets(key)
                    # Точка (исправить)
                    elif key=="." :
                        self.point(key)
    # Работа калькулятора с помощью мыши
    def calculation(self):
        sender = self.sender()
        key = sender.text()
        #print(key)

        # Вычесления
        if key =="=":
            self.score()
        # Смена знака
        elif key=="±":
            if self.labelSmall.text()!="":
                if "-" in self.labelSmall.text():
                    self.labelSmall.setText(self.labelSmall.text()[1:])
                else:
                    self.labelSmall.setText("-"+self.labelSmall.text())
        # Факториал
        elif key=='x!':
            if self.labelSmall.text()!="":
                try:
                    self.labelSmall.setText(str(math.factorial(int(self.labelSmall.text()))))
                except:
                    pass
        # Cкобки
        elif key in '()':
            self.brackets(key)
        # Корень
        elif key=="√x":
            if self.labelSmall.text()!="":
                resultRoot=math.sqrt(float(self.labelSmall.text()))
                # resultRoot**=0.5
                # print(resultRoot)
                if resultRoot%1 == 0:
                    resultRoot = int(resultRoot)
                self.labelSmall.setText(str(resultRoot))
        # X²
        elif key=="x²":
            if self.labelSmall.text()!="":
                resultRoot = float(self.labelSmall.text())
                resultRoot **= 2
                #print(resultRoot)
                if resultRoot%1 == 0:
                    resultRoot = int(resultRoot)
                self.labelSmall.setText(str(resultRoot))
        # 1/X
        elif key=="⅟ₓ":
            try:
                if self.labelSmall.text()!="" or self.labelSmall.text()!="0":
                    resultRoot=float(self.labelSmall.text())
                    resultRoot=1/resultRoot
                    print(resultRoot)
                    self.labelSmall.setText(str(resultRoot))
            except ZeroDivisionError:
                pass
        # Точка
        elif key==".":
            self.point(key)
        # xʸ
        elif key == "xʸ":
            if "-" not in self.labelSmall.text():
                if '=' not in self.labelBig.text():

                    if self.labelSmall.text()!='' and (self.labelSmall.text() !="-"):
                        self.labelBig.setText(self.labelBig.text()+self.labelSmall.text()+"^")
                        self.labelSmall.setText("")
                    else:
                        if key=="-":
                            self.labelSmall.setText('-')
                else:
                    self.labelBig.setText(self.labelSmall.text()+"^")
                    self.labelSmall.setText("")
            else:
                if '=' not in self.labelBig.text():
                    if self.labelSmall.text()!='' and (self.labelSmall.text() !="-"):
                        self.labelBig.setText(self.labelBig.text()+'('+self.labelSmall.text()+')'+"^")
                        self.labelSmall.setText("")
                    else:
                        if key=="-":
                            self.labelSmall.setText('-')
                else:
                    self.labelBig.setText('('+self.labelSmall.text()+')'+"^")
                    self.labelSmall.setText("")
        # ʸ√x
        elif key == "ʸ√x": # ???
            pass
        # exp(x)
        elif key == "eˣ":
            if self.labelSmall.text()!="":
                resultRoot=math.exp(float(self.labelSmall.text()))
                if resultRoot%1 == 0:
                    resultRoot = int(resultRoot)
                self.labelSmall.setText(str(resultRoot))
        # ln(x)
        elif key == "ln(x)":
            if self.labelSmall.text()!="":
                resultRoot=math.log(float(self.labelSmall.text()))
                if resultRoot%1 == 0:
                    resultRoot = int(resultRoot)
                self.labelSmall.setText(str(resultRoot))
        # 10^x
        elif key == "10ˣ":
            if self.labelSmall.text()!="":
                resultRoot=10**(float(self.labelSmall.text()))
                if resultRoot%1 == 0:
                    resultRoot = int(resultRoot)
                self.labelSmall.setText(str(resultRoot))
        # lg(x)
        elif key == "lg(x)":
            if self.labelSmall.text()!="":
                resultRoot=math.log10(float(self.labelSmall.text()))
                if resultRoot%1 == 0:
                    resultRoot = int(resultRoot)
                self.labelSmall.setText(str(resultRoot))
        # sin(x)
        elif key == "sin(x)":
            pass
        # cos(x)
        elif key == "cos(x)":
            pass
        # tg(x)
        elif key == "tg(x)":
            pass
        # ctg(x)
        elif key == "ctg(x)":
            pass
        # arcsin(x)
        elif key == "arcsin(x)":
            pass
        # arccos(x)
        elif key == "arccos(x)":
            pass
        # arctg(x)
        elif key == "arctg(x)":
            pass
        # arcctg(x)
        elif key == "arcctg(x)":
            pass
        # sh(x)
        elif key == "sh(x)":
            pass
        # ch(x)
        elif key == "ch(x)":
            pass
        # th(x)
        elif key == "th(x)":
            pass
        # cth(x)
        elif key == "cth(x)":
            pass
        #

        # Ввод цифр
        elif key in "1234567890π":
            self.numbers(key)
        # Очистка окон кроме истории
        elif key=="C":
            self.labelSmall.setText("")
            self.labelBig.setText("")
        # Смена функционала
        elif key=="↑" or key=="↓":
            if self.buttonList[0][5].text() == '↑':
                for row in range(countRowButton):
                    for col in range(countColumnButton+countAdditionalColumnButton):
                        self.buttonList[row][col].setText(self.buttonTextListAfter[row][col])
            else:
                for row in range(countRowButton):
                    for col in range(countColumnButton+countAdditionalColumnButton):
                        self.buttonList[row][col].setText(self.buttonTextList[row][col])
        # удаление последнего символа
        elif key=="<":
            self.deleteLastChar()
        # выполнение основных арифметических операций
        elif key in "+-×÷":
            self.signs(key)
    # Иницализация окна
    def __init__(self):
        super().__init__()
        self.initUI()
        #self.setWindowIcon(QIcon('qww.jpg'))
        self.resize(QSize(widthWindow, hightWindow+heigthMenuBar))
        self.setFixedSize(widthWindow, hightWindow+heigthMenuBar) #..........................................Размер окна (Ширина, Высота)
        self.setWindowTitle('калькулятор') #......................................Заголовок окна
    # Инициализация виджетов
    def initUI(self):
        # Стили
        self.setStyleSheet("""
            Calculator{
                background-color: #8d2222;;
                position:relative;
                text-align: center;
                border: 5px solid;
                }

            #labelBig {
                background-color: #6b0000;
                border-radius: 20px;
                color:#fff;
                border: 5px solid;
            }
            #labelSmall {
                background-color: #6b0000;
                border-radius: 20px;
                color:#fff;
                border: 5px solid;
            }
            #labelHistory {
                background-color: #6b0000;
                border-radius: 20px;
                color:#fff;
                font-size: 19px;
                border: 5px solid;
            }
            QPushButton{
            background-color: #ee6e40;
            color: black;
            border-radius: 13px;
            border: 5px solid;
            font-size: 25px;
            }
            #
        """)

        # Создание labels

        self.labelBig=QLabel("",self,objectName="labelBig")
        self.labelBig.resize(widthLabelBig,hightLabelBig)
        self.labelBig.move(board,board+heigthMenuBar)
        self.labelBig.setFont(QFont("Trattatello",size//8))
        self.labelBig.show()

        self.labelSmall=QLabel("",self,objectName="labelSmall")
        self.labelSmall.resize(widthLabelSmall,hightLabelSmall)
        self.labelSmall.move(board,board+hightWindow//4+heigthMenuBar)
        self.labelSmall.setFont(QFont("Trattatello",size//4))
        self.labelSmall.show()

        self.labelHistory=QLabel("",self,objectName="labelHistory")
        self.labelHistory.resize(widthLabelHistory,hightLabelHistory)
        self.labelHistory.move(widthWindow*5//8+board,hightWindow//8+board+heigthMenuBar)
        self.labelHistory.show()

        # Список клавиш до переключения
        self.buttonTextList=[['+', '-', '×', '÷',  'C',  "↑",     "sin(x)"],
                             ['7', '8', '9', '±',  '<',  "eˣ",    "cos(x)"],
                             ['4', '5', '6', 'x²', '√x', "10ˣ",   "tg(x)"],
                             ['1', '2', '3', 'xʸ', 'x!', "π",     "ctg(x)"],
                             ['.', '0', '(', ')',  '=',  "sh(x)", "ch(x)"]]
        # Список клавиш после переключения
        self.buttonTextListAfter=[['+', '-', '×', '÷',  'C',  "↓",     "arcsin(x)"],
                                  ['7', '8', '9', '±',  '<',  "ln(x)", "arccos(x)"],
                                  ['4', '5', '6', 'x²', '√x', "lg(x)", "arctg(x)"],
                                  ['1', '2', '3', 'xʸ', 'x!', "ʸ√x",   "arcctg(x)"],
                                  ['.', '0', '(', ')',  '=',  "th(x)", "cth(x)"]]

        self.buttonList=[]
        # Создание клавиш
        for row in range(countRowButton):
            self.buttonList.append([])

            for col in range(countColumnButton+countAdditionalColumnButton):
                btn = QPushButton(self.buttonTextList[row][col],self,objectName=("button"+str(row)+str(col)))

                btn.clicked.connect(self.calculation)


                if col < countColumnButton:
                    btn.resize(widthButton,hightButton)
                    btn.move(board+(board+widthButton)*col,hightWindow*3//8+(board + hightButton)*row+heigthMenuBar)
                    self.buttonList[row].append(btn)
                    self.buttonList[row][col].show()
                elif col == countColumnButton:
                    btn.resize(widthButton*2,hightButton)
                    btn.move(board+(board+widthButton)*col,hightWindow*3//8+(board + hightButton)*row+heigthMenuBar)
                    self.buttonList[row].append(btn)
                    self.buttonList[row][col].hide()
                else:
                    btn.resize(widthButton*2,hightButton)
                    btn.move((board+(board+widthButton)*(col+1)),hightWindow*3//8+(board + hightButton)*row+heigthMenuBar) # +1 надо поменять
                    self.buttonList[row].append(btn)
                    self.buttonList[row][col].hide()
        # Кнопка очищения истории
        self.buttonDeleteHistory=QPushButton('del',self)
        self.buttonDeleteHistory.resize(widthWindow//9,widthWindow//9)
        self.buttonDeleteHistory.move(widthWindow-(widthWindow//8),heigthMenuBar+board)
        self.buttonDeleteHistory.clicked.connect(self.deleteHistory)
        # Кнопка расширения и сужения окна
        self.buttonAdd=QPushButton('→',self)
        self.buttonAdd.resize(widthWindow//9,widthWindow//9)
        self.buttonAdd.move(widthWindow-(widthWindow//4),heigthMenuBar+board)
        self.buttonAdd.clicked.connect(self.expansion)
        # Кнопка вызова окна вставки из истории
        self.buttonNewWindow=QPushButton('???',self)
        self.buttonNewWindow.resize(widthWindow//9,widthWindow//9)
        self.buttonNewWindow.move(widthWindow-(widthWindow//(26/10)),heigthMenuBar+board)
        self.buttonNewWindow.clicked.connect(self.buts)


        # МенюБар
        exitAction = QAction( '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        openAction = QAction('Open File', self)
        openAction.triggered.connect(self.openFile)

        saveAction = QAction('Save File',self)
        saveAction.triggered.connect(self.saveFileDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        editMenu = menubar.addMenu('&Edit')
        editMenu.addAction(openAction)
        editMenu.addAction(saveAction)


# Выполнение программы
if __name__ == '__main__':
    window = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(window.exec_())
