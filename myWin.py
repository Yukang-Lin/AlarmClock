import tkinter as tk
import tkinter.messagebox
import os
import sys
import re
import Calendar
'''
these following functions need to be fullfilled: 
2. calculating logic
3. good-looking background
4. remember historical input digit
'''

class datepicker:
    def __init__(self,window,date1,date2):
        self.window=window

        self.start_date=tk.StringVar()
        self.end_date=tk.StringVar()
        self.bt1 = tk.Button(self.window, text='开始日期',font=("微软雅黑",16), command=lambda: self.getdate('start'))  # 开始按钮
        self.bt1.place(x=date1[0],y=date1[1])
        self.ent1 = tk.Entry(self.window, font=("微软雅黑",16), textvariable=self.start_date)  # 开始输入框
        self.ent1.place(x=date1[2],y=date1[3])
        self.bt2 = tk.Button(self.window, text='截止日期',font=("微软雅黑",16), command=lambda: self.getdate('end'))
        self.bt2.place(x=date2[0],y=date2[1])
        self.ent2 = tk.Entry(self.window, font=("微软雅黑",16),textvariable=self.end_date)
        self.ent2.place(x=date2[2], y=date2[3])

    def getdate(self, type):  # 获取选择的日期
        for date in [Calendar.Calendar().selection()]:
            if date:
                if (type == 'start'):  # 如果是开始按钮，就赋值给开始日期
                    self.start_date.set(date)
                elif (type == 'end'):
                    self.end_date.set(date)

class MainForm:
    def __init__(self):
        self.root=tk.Tk()
        # root.maxsize(1000,400)
        self.root.geometry("540x640")
        self.root.title("滞纳金计算器")
        self.root["background"]="LightSlateGray"
        # self.entry1=tk.Entry(self.root,font=("微软雅黑",16))
        # self.entry1.place(x=250,y=100)
        # self.entry2 = tk.Entry(self.root, font=("微软雅黑", 16))
        # self.entry2.place(x=250,y=200)

        self.entry3=tk.Entry(self.root,font=("微软雅黑",16))
        self.entry3.insert(0,"1000")
        self.entry3.place(x=250,y=300)
        self.entry4=tk.Entry(self.root,font=("微软雅黑",16))
        self.entry4.insert(0,"5.0%")
        self.entry4.place(x=250,y=400)

        # label1=tk.Label(self.root,text="开始日期",font=("微软雅黑",16))
        # label1.place(x=100,y=100)
        # label2=tk.Label(self.root,text="截止日期",font=("微软雅黑",16))
        # label2.place(x=100,y=200)
        label3=tk.Label(self.root,text="金额",font=("微软雅黑",16))
        label3.place(x=100,y=300)
        label4=tk.Label(self.root,text="比率",font=("微软雅黑",16))
        label4.place(x=100,y=400)

        self.button1=tk.Button(self.root,text="计算",font=("微软雅黑",16))
        self.button1.bind("<Button-1>",lambda event:self.cal_num(event))
        self.button1.place(x=250,y=500)

        date1=(100,100,250,100)
        date2=(100,200,250,200)
        self.cal=datepicker(self.root,date1,date2)

        self.root.mainloop()
    def cal_num(self,event):
        pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
        start_date=self.cal.ent1.get()
        end_date=self.cal.ent2.get()
        money=self.entry3.get().strip()
        if not pattern.match(money):
            tk.messagebox.showinfo(title="信息提示", message="请不要输入非数字字符")
        money=float(money)
        rate=self.entry4.get().strip()
        if rate[-1]=='%':
            rate=rate[0:-1]
            if not pattern.match(rate):
                tk.messagebox.showinfo(title="信息提示", message="请不要输入非数字字符")
            else:
                rate=float(rate)/100
        elif not pattern.match(rate):
            tk.messagebox.showinfo(title="信息提示", message="请不要输入非数字字符")
        rate=float(rate)
        delta=self.cal_date(start_date,end_date)
        if delta <= 31:
            penalty=0.0
        else:
            penalty = (delta-31) * money * rate
        all=money+penalty
        str="您好，根据合同约定从",start_date,"到",end_date,"您已经逾期",(delta-31),\
            "天未缴清费用",money,"元，按照逾期5%的比率，一共需要支付",all,"元，（包含滞纳金）",penalty,"元。"
        tk.messagebox.showinfo(title="信息提示",message=str)
    def cal_date(self,date1,date2):
        if date1>=date2:
            return 0
        y1=int(date1[0:4])
        y2=int(date2[0:4])
        m1=int(date1[5:7])
        m2=int(date2[5:7])
        d1=int(date1[8:10])
        d2=int(date2[8:10])
        sw={1:0,2:1,3:-1,4:0,5:0,6:1,7:1,8:2,9:3,10:3,11:4,12:4}
        delta=sw[m2]+(m2-1)*30-sw[m1]-(m1-1)*30+d2-d1
        if y2-y1>0:
            delta+=365*(y2-y1)
        return delta


def main():
    MainForm()
if __name__ == '__main__':
    main()