import tkinter as tk
import tkinter.font as tkfont
import zhixuewang as zxw
import time

LOG_LINE_NUM = 0

class zxwWindow:
    
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name
        self.username : str() = None
        self.passwd : str() = None
        self.person : zxw.student.student.Student = None
        self.nowExam : zxw.models.Exam = None
        self.allExams : zxw.models.ExtendedList = None
        self.fonts = tkfont.Font(family='Arial')
    
    def init_window(self):
        self.init_window_name.title('智学网成绩查询')
        self.init_window_name.geometry('630x680+10+10')


        #菜单
        self.menuBar = tk.Menu(self.init_window_name)

        self.filemenu = tk.Menu(self.menuBar, tearoff=0)
        self.helpmenu = tk.Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label='File', menu=self.filemenu)
        self.menuBar.add_cascade(label='Help', menu=self.helpmenu)

        self.filemenu.add_command(label='Exit', command=self.init_window_name.quit)
        self.helpmenu.add_command(label='About', command=self.about)
        self.init_window_name.config(menu=self.menuBar)
        

        #标签
        self.usernameLabel = tk.Label(self.init_window_name, text='账号:', font=self.fonts)
        self.usernameLabel.grid(row=1,column=0)

        self.pswdLabel = tk.Label(self.init_window_name, text='密码:', font=self.fonts)
        self.pswdLabel.grid(row=6,column=0)

        self.selectHelp = tk.Label(self.init_window_name, text='^试卷选择^\n选定后按切换试卷按钮', font=self.fonts)
        self.selectHelp.grid(row=13, column=9)


        #文本框
        self.inputUsername = tk.Entry(self.init_window_name, width=20, font=self.fonts)
        self.inputUsername.grid(row=2, column=0, rowspan=3,columnspan=5)

        self.inputPswd = tk.Entry(self.init_window_name, show='*', width=20, font=self.fonts)
        self.inputPswd.grid(row=7, column=0, rowspan=3,columnspan=5)

        self.log_data = tk.Text(self.init_window_name, width=60, height=22, font=self.fonts)
        self.log_data.grid(row=15, column=1, columnspan=20)


        #按钮
        self.loginBut = tk.Button(self.init_window_name, text='登录', bg="lightblue", width=8, font=self.fonts, command=self.login)
        self.loginBut.grid(row=12, column=1)

        self.inquiryBut = tk.Button(self.init_window_name, text='查询成绩', bg="lightblue", width=8, font=self.fonts, command=self.inquiry)
        self.inquiryBut.grid(row=13, column=3)

        self.changePaperBut = tk.Button(self.init_window_name, text='切换试卷', bg="lightblue", width=8, font=self.fonts, command=self.change_paper)
        self.changePaperBut.grid(row=12, column=3)

        self.exitBut = tk.Button(self.init_window_name, text='退出登录', bg="lightblue", width=8, font=self.fonts, command=self.user_exit)
        self.exitBut.grid(row=13, column=1)

        self.exitBut = tk.Button(self.init_window_name, text='清空文本框', bg="lightblue", width=8, font=self.fonts, command=self.clear_Text)
        self.exitBut.grid(row=14, column=1)

        self.getPaperBut = tk.Button(self.init_window_name, text='获取原卷', bg='lightblue', width=8, font=self.fonts, command=self.callSubSubjectWindow)
        self.getPaperBut.grid(row=14, column=3)

        #列表
        self.examList = tk.Listbox(self.init_window_name, selectmode = tk.BROWSE, width=40, height=8, font=self.fonts)
        self.examList.grid(row=3, column=5, rowspan=10, columnspan=10)

    
    def login(self):
        self.username = self.inputUsername.get().strip()
        self.passwd = self.inputPswd.get().strip()
        try:
            self.person = zxw.login(str(self.username),str(self.passwd))
            self.nowExam = self.person.get_exam()
            self.write_log_to_Text('登录成功')
            try:
                self.allExams = self.person.get_exams()
                length = len(self.allExams)
                for i in range(0,length):
                    self.examList.insert(tk.END,self.allExams[i].name)
            except KeyError:
                self.write_log_to_Text('无法获取所有试卷列表,请稍后再试')
        except:
            self.write_log_to_Text('账号或者密码错误,请重试')
            self.inputPswd.delete(0,tk.END)
            return

    def inquiry(self):
        mark = str()
        try:
            try:
                mark = str(self.person.get_self_mark(self.nowExam.id))
                self.write_log_to_Text('查询成绩')
                self.write_log_to_Text('\n'+mark+'\n(若有排名为也许为未赋分排名，也许为赋分排名)'+'\n点击清除按钮清空文本框')
            except AttributeError:
                self.write_log_to_Text('您还未登录，请登录之后再试')
                return

        except KeyError:
            try:
                mark = str(self.person.get_self_mark(self.nowExam.id,False))
                self.write_log_to_Text('查询成绩')
                self.write_log_to_Text('\n'+mark+'\n(若有排名为也许为未赋分排名，也许为赋分排名)'+'\n点击清除按钮清空文本框')
            except KeyError:
                self.write_log_to_Text('无法获取试卷资料，请稍后再试')
                return
            except AttributeError:
                self.write_log_to_Text('您还未登录，请登录之后再试')
                return

    def change_paper(self):
        try:
            selectIndex = self.examList.curselection()[0]
        except IndexError:
            self.write_log_to_Text('您还未登录，请登录之后再试')
        else:
            try:
                self.nowExam = self.allExams[selectIndex]
                self.write_log_to_Text('已选择:\n'+ self.nowExam.name)
            except (IndexError,KeyError):
                self.write_log_to_Text('无法获取试卷资料，请稍后再试')

    def user_exit(self):
        self.inputUsername.delete(0,tk.END)
        self.inputPswd.delete(0,tk.END)
        self.__init__(self.init_window_name)
        self.examList.delete(0,tk.END)
        self.write_log_to_Text('成功退出登录')

    def clear_Text(self):
        global LOG_LINE_NUM
        LOG_LINE_NUM = 0
        self.log_data.delete(1.0,tk.END)

    def about(self):
        self.write_log_to_Text('\nzhiXueWangGUI:\nMade by chafiprc.')
        self.write_log_to_Text('\n免责声明:\n本软件仅供个人学习、研究。我们不保证内容的正确性。通过使用本软件随之而来的风险与软件制作者无关\n软件仅用于个人学习、研究以及其他非商业性或非盈利性用途，但同时应遵守著作权法及其他相关法律的规定，不得相关人的合法权利。\n如果用户下载、使用本软件，即表明用户信任该软件作者\n对任何原因在使用本软件时可能对用户自己或他人造成的任何形式的损失和伤害,软件制作者不承担任何责任。')


    def callSubSubjectWindow(self):
        if self.nowExam == None:
            self.write_log_to_Text('您还未登录,请登录之后再试')
        else:
            self.subWindow = tk.Tk()
            self.subWindow.title('选择科目')
            self.subjectList = ['语文','数学','英语','物理','化学','地理','历史','政治','生物']

            #标签
            helpLabel = tk.Label(self.subWindow, text='请注意:部分久远考试无法获取原卷', font=self.fonts)
            helpLabel.grid(row=0,column=0)

            #按钮
            chooseSubjectBut = tk.Button(self.subWindow, text='选定科目', width=8, font=self.fonts, command=self.__subSubjectChoose)
            chooseSubjectBut.grid(row=11,column=0)

            #列表
            self.subjectListbox = tk.Listbox(self.subWindow, selectmode = tk.BROWSE, width=20, height=9, font=self.fonts)
            for i in self.subjectList:
                self.subjectListbox.insert(tk.END,i)
            self.subjectListbox.grid(row=1, column=0, rowspan=9)
            self.subWindow.mainloop()

    def __subSubjectChoose(self):
        selectSub = self.subjectList[self.subjectListbox.curselection()[0]]
        try:
            paperUrl = self.person.get_original(selectSub,self.nowExam.id)
        except KeyError:
            self.write_log_to_Text('无法获取原卷列表,请稍后再试')
        else:
            if paperUrl == []:
                self.write_log_to_Text('抱歉，无法获取' + selectSub + '原卷地址')
            else:
                self.write_log_to_Text('\n' + selectSub +'-试卷链接为:')
                for i in paperUrl:
                    self.write_log_to_Text(i,False)
        finally:
            self.subWindow.destroy()
        
    

    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time

    def write_log_to_Text(self,logmsg,timeVis=True):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        if timeVis:
            logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
        else:
            logmsg_in = str(logmsg) + "\n"
        if LOG_LINE_NUM <= 8:
            self.log_data.insert(tk.END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data.delete(1.0,2.0)
            self.log_data.insert(tk.END, logmsg_in)


def startGUI():
    init_window = tk.Tk()
    mainEXE = zxwWindow(init_window)
    mainEXE.init_window()
    init_window.mainloop()

if __name__ == '__main__':
    startGUI()