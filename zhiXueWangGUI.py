import tkinter as tk
import zhixuewang as zxw
import time

LOG_LINE_NUM = 0

class zxwWindow:
    
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name
        self.username = str()
        self.passwd = str()
        self.person = zxw.student.student.Student
        self.nowExam = zxw.models.Exam
        self.allExams = zxw.models.ExtendedList
    
    def init_window(self):
        self.init_window_name.title('智学网成绩查询')
        self.init_window_name.geometry('500x540+10+10')
        

        #标签
        self.usernameLabel = tk.Label(self.init_window_name, text='账号:')
        self.usernameLabel.grid(row=1,column=1)

        self.pswdLabel = tk.Label(self.init_window_name, text='密码:')
        self.pswdLabel.grid(row=6,column=1)

        self.selectHelp = tk.Label(self.init_window_name, text='^试卷选择^\n选定后按切换试卷按钮')
        self.selectHelp.grid(row=13, column=10)


        #文本框
        self.inputUsername = tk.Entry(self.init_window_name, width=20)
        self.inputUsername.grid(row=2, column=0, rowspan=3,columnspan=5)

        self.inputPswd = tk.Entry(self.init_window_name, show='*', width=20)
        self.inputPswd.grid(row=7, column=0, rowspan=3,columnspan=5)

        self.log_data = tk.Text(self.init_window_name, width=60, height=22)
        self.log_data.grid(row=15, column=1, columnspan=20)


        #按钮
        self.loginBut = tk.Button(self.init_window_name, text='登录', bg="lightblue", width=8, command=self.login)
        self.loginBut.grid(row=12, column=1)

        self.inquiryBut = tk.Button(self.init_window_name, text='查询成绩', bg="lightblue", width=8, command=self.inquiry)
        self.inquiryBut.grid(row=12, column=3)

        self.changePaperBut = tk.Button(self.init_window_name, text='切换试卷', bg="lightblue", width=8, command=self.change_paper)
        self.changePaperBut.grid(row=13, column=3)

        self.exitBut = tk.Button(self.init_window_name, text='退出登录', bg="lightblue", width=8, command=self.user_exit)
        self.exitBut.grid(row=13, column=1)

        self.exitBut = tk.Button(self.init_window_name, text='清空文本框', bg="lightblue", width=8, command=self.clear_Text)
        self.exitBut.grid(row=14, column=2)


        #列表
        self.examList = tk.Listbox(self.init_window_name, selectmode = tk.BROWSE, width=40, height = 8)
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
            mark = str(self.person.get_self_mark(self.nowExam.id))
            self.write_log_to_Text('查询成绩')
            self.write_log_to_Text('\n'+mark+'\n点击清除按钮清空文本框')
        except KeyError:
            try:
                mark = str(self.person.get_self_mark(self.nowExam.id,False))
                self.write_log_to_Text('查询成绩')
                self.write_log_to_Text('\n'+mark+'\n点击清除按钮清空文本框')
            except KeyError:
                self.write_log_to_Text('无法获取试卷资料，请稍后再试')
                return

    def change_paper(self):
        selectIndex = self.examList.curselection()[0]
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

    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time

    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
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