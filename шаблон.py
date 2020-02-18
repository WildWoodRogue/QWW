"""
Приложение 'Калькулятор'
"""
import sys
from PyQt5.QtWidgets import QApplication,QLabel,QWidget, QPushButton,QMessageBox,QLCDNumber,QLineEdit,QGridLayout,QMainWindow,QAction, qApp
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont, QIcon

size=65
board=5

countRowButton=5
countColumnButton=5

widthWindow=8*size
hightWindow=8*size

widthButton=widthWindow//8- board
hightButton=hightWindow//8- board

widthLabelBig=widthWindow*5//8 - board
hightLabelBig=hightWindow//4- 2*board

widthLabelSmall=widthWindow*5//8- board
hightLabelSmall=hightWindow//8- 2*board

widthLabelHistory = widthWindow*3//8- 2*board
hightLabelHistory=hightWindow*7//8- 2*board



class Calculator(QMainWindow):


    def Big(self):

        if self.buttonAdd.text()=="add":

            bigWidthWindow=widthWindow+(widthWindow//3)
            self.labelHistory.move(bigWidthWindow*(9/2)//7+board,hightWindow//8+board)
            self.resize(QSize(widthWindow+(widthWindow//((275/105)))-(widthWindow+(widthWindow//2))/10, hightWindow))
            # self.buttonAdd.setText("add")
            self.buttonList[0][6].show()
            self.buttonList[1][6].show()
            self.buttonList[2][6].show()
            self.buttonList[3][6].show()
            self.buttonList[4][6].show()
            self.buttonList[0][5].show()
            self.buttonList[1][5].show()
            self.buttonList[2][5].show()
            self.buttonList[3][5].show()
            self.buttonList[4][5].show()

            self.buttonAdd.setText("less")

        elif self.buttonAdd.text()=="less":
            self.labelHistory.move(widthWindow*5//8+board,hightWindow//8+board)
            self.resize(QSize(widthWindow, hightWindow))
            self.buttonAdd.setText("add")
            self.buttonList[0][6].hide()
            self.buttonList[1][6].hide()
            self.buttonList[2][6].hide()
            self.buttonList[3][6].hide()
            self.buttonList[4][6].hide()
            self.buttonList[0][5].hide()
            self.buttonList[1][5].hide()
            self.buttonList[2][5].hide()
            self.buttonList[3][5].hide()
            self.buttonList[4][5].hide()

    def deleteHistory(self):
        self.labelHistory.setText("")
    def point(self,key):
        if key not in self.labelSmall.text() and self.labelSmall.text()!="":
            self.labelSmall.setText(self.labelSmall.text()+key)
    def brackets(self,key):
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
    def signs(self,key):
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
    def deleteLastChar(self):
        self.labelSmall.setText(self.labelSmall.text()[:-1])
    def numbers(self,key):
        """"""
        if '=' not in self.labelBig.text():
            self.labelSmall.setText(self.labelSmall.text()+key)
            if self.labelBig.text()!="":
                if self.labelBig.text()[-1]==")":
                    self.labelBig.setText(self.labelBig.text()+"×")


        else:
            self.labelBig.clear();
            self.labelSmall.setText(key)
    #
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
        sender=self.sender()
        key=sender.text()
        print(key)

        #вычесления
        if key =="=":
            self.score()
        #смена знака
        elif key=="±":
            if self.labelSmall.text()!="":
                if "-" in self.labelSmall.text():
                    self.labelSmall.setText(self.labelSmall.text()[1:])
                else:
                    self.labelSmall.setText("-"+self.labelSmall.text())
        #факториал
        elif key=='X!':
            if self.labelSmall.text()!="":
                try:
                    resultFact=1
                    fact=str(self.labelSmall.text())
                    for i in range(1,int(fact)+1):
                        resultFact*=i
                    self.labelSmall.setText(str(resultFact))
                except:
                    pass

        #скобки
        elif key in '()':
            self.brackets(key)
        #корень
        elif key=="√x":
            if self.labelSmall.text()!="":
                resultRoot=float(self.labelSmall.text())
                resultRoot**=0.5
                print(resultRoot)
                self.labelSmall.setText(str(resultRoot))
        #X²
        elif key=="X²":
            if self.labelSmall.text()!="":
                resultRoot=float(self.labelSmall.text())
                resultRoot**=2
                print(resultRoot)
                self.labelSmall.setText(str(resultRoot))
        #1/X
        elif key=="⅟ₓ":
            try:
                if self.labelSmall.text()!="" or self.labelSmall.text()!="0":
                    resultRoot=float(self.labelSmall.text())
                    resultRoot=1/resultRoot
                    print(resultRoot)
                    self.labelSmall.setText(str(resultRoot))
            except ZeroDivisionError:
                pass
        #исключение множественности точек
        elif key==".":
            self.point(key)

        #ввод цифр
        elif key in "1234567890":
            self.numbers(key)


        # очистка окон кроме истории
        elif key=="C":
            self.labelSmall.setText("")
            self.labelBig.setText("")
        # смена функционала
        elif key=="↑" or key=="↓":
            if self.buttonList[2][3].text()=="X!":
                self.buttonList[2][3].setText("X²")
                self.buttonList[2][4].setText("^")
                self.buttonList[4][2].setText("↑")
            else:
                self.buttonList[2][3].setText('X!')
                self.buttonList[2][4].setText('⅟ₓ')
                self.buttonList[4][2].setText("↓")
        # удаление последнего символа
        elif key=="<":
            self.deleteLastChar()
        # выполнение основных арифметических операций
        elif key in "+-×÷^":
            self.signs(key)

    def __init__(self):                                                           #создание окна
        super().__init__()
        self.initUI()



        #self.setWindowIcon(QIcon('qww.jpg'))
        self.resize(QSize(widthWindow, hightWindow))
        self.setFixedSize(widthWindow,hightWindow) #..........................................Размер окна (Ширина, Высота)
        self.setWindowTitle('калькулятор') #......................................Заголовок окна


    def initUI(self):
        # Стили
        self.setStyleSheet("""
            QWidget {
                background-color: #8d2222;;
                position:relative;
                text-align: center;
                border: 5px solid;
                }
            QLineEdit {
                background-color: #6b0000;
                border-radius: 20px;
                color:#fff;
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
            #fileMenu{
            background-color: #fff;
            }
        """)

        #ссоздание labels
        self.labelBig=QLabel("",self,objectName="labelBig")
        self.labelBig.resize(widthLabelBig,hightLabelBig)
        self.labelBig.move(board,board)
        self.labelBig.setFont(QFont("Trattatello",size//8))
        self.labelBig.show()

        self.labelSmall=QLabel("",self,objectName="labelSmall")
        self.labelSmall.resize(widthLabelSmall,hightLabelSmall)
        self.labelSmall.move(board,board+hightWindow//4)
        self.labelSmall.setFont(QFont("Trattatello",size//4))
        self.labelSmall.show()

        self.labelHistory=QLabel("",self,objectName="labelHistory")
        self.labelHistory.resize(widthLabelHistory,hightLabelHistory)
        self.labelHistory.move(widthWindow*5//8+board,hightWindow//8+board)
        self.labelHistory.show()




        #
        #создание кнопок
        countRowButton=5
        countColumnButton=7
        buttonTextList=[['+','-','×','÷','C',"1","6t"],
                        ['7','8','9','±','<',"2","ed"],
                        ['4','5','6','X²','^',"3","er"],
                        ['1','2','3','(',')',"4","qw"],
                        ['.','0','↑','√x','=',"5","ww"]]
        self.buttonList=[]
        for row in range(countRowButton):
            self.buttonList.append([])

            for col in range(countColumnButton):
                btn = QPushButton(buttonTextList[row][col],self,objectName=("button"+str(row)+str(col)))
                btn.resize(widthButton,hightButton)
                btn.clicked.connect(self.calculation)
                btn.move(board+(board+widthButton)*col,hightWindow*3//8+(board + hightButton)*row)
                self.buttonList[row].append(btn)
                self.buttonList[row][col].show()

        self.buttonList[0][6].hide()
        self.buttonList[1][6].hide()
        self.buttonList[2][6].hide()
        self.buttonList[3][6].hide()
        self.buttonList[4][6].hide()
        self.buttonList[0][5].hide()
        self.buttonList[1][5].hide()
        self.buttonList[2][5].hide()
        self.buttonList[3][5].hide()
        self.buttonList[4][5].hide()

        self.buttonDeleteHistory=QPushButton('del',self)
        self.buttonDeleteHistory.resize(widthWindow//9,widthWindow//9)
        self.buttonDeleteHistory.move(widthWindow-(widthWindow//8),1)
        self.buttonDeleteHistory.clicked.connect(self.deleteHistory)

        self.buttonAdd=QPushButton('add',self)
        self.buttonAdd.resize(widthWindow//9,widthWindow//9)
        self.buttonAdd.move(widthWindow-(widthWindow//4),1)
        self.buttonAdd.clicked.connect(self.Big)

        self.buttonNewWindow=QPushButton('???',self)
        self.buttonNewWindow.resize(widthWindow//9,widthWindow//9)
        self.buttonNewWindow.move(widthWindow-(widthWindow//(26/10)),1)
        self.buttonNewWindow.clicked.connect(self.buts)

        exitAction = QAction( '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.show()
    def buts(self):
        print("1")



# Выполнение программы
if __name__ == '__main__':
    window = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(window.exec_())

class addWindow(QMainWindow):
     def __init__(self):
        super().__init__()
        self.initUI()

     def initUI(self):

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Icon')


        self.show()
if __name__ == '__main__':
    window2 = QApplication(sys.argv)
    calc2 = addWindow()
    calc2.show()
    sys.exit(window2.exec_())
