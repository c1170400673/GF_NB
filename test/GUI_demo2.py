import tkinter as tk  # GUI库
from tkinter import ttk


class test():
    def __init__(self, win, PHYSN_TYPE, POS_NAME):
        self.win = win
        self.PHYSN_TYPE = PHYSN_TYPE
        self.POS_NAME = POS_NAME

    def my_GUI(self):
        tk.Label(self.win, text='机具类型：', bd=3, relief='groove', width=16, anchor='e').grid(row=2, column=2,
                                                                                               padx=5)

        number = tk.StringVar()  # 是否选中
        valus = ['mpos', '大POS', '电蓝POS', '经典蓝POS']  # 选项值设置
        self.PHYSN_TYPE = ttk.Combobox(self.win, width=16, height=4, textvariable=number,
                                       state='readonly')  # 高度,下拉显示的条目数量
        self.PHYSN_TYPE.grid(row=2, column=3, columnspan=3)
        self.PHYSN_TYPE['values'] = valus
        self.PHYSN_TYPE.current(1)  # 设置下拉列表默认显示的值
        self.PHYSN_TYPE.bind('<<ComboboxSelected>>', self.Chosen)  # 绑定选项（输出选中内容）
        print(self.PHYSN_TYPE.current(), self.PHYSN_TYPE.get())  # 输出选项内容

        tk.Label(self.win, text='机具名称：', bd=3, relief='groove', width=16, anchor='e').grid(row=3, column=2, padx=5)
        number1 = tk.StringVar()
        valus2 = ['00-小蓝(MPos)', '01-小蓝-会员(Mpos)', '02-大蓝(大Pos)', '03-炫蓝(大Pos)', '04-电蓝(EPos)',
                  '05-经典蓝(大Pos)',
                  '06:Epos(4G版本)', '07:大Pos(4G版)', '08:EPos-Plus', '09:大机虎力版', '10:epos(买断版)',
                  '11:大pos(买断版)', '12:epos(买断版)']
        self.POS_NAME = ttk.Combobox(self.win, width=16, textvariable=number1, height=5, values=valus2,
                                     state='readonly')
        self.POS_NAME.grid(row=3, column=3, columnspan=3)
        # self.POS_NAME.current(10)  #设置下拉框内默认显示第10个选择（10为values的下标值）
        number1.set('09:大机虎力版')  # 设置下拉框内默认显示内容
        print(self.POS_NAME.current(), self.POS_NAME.get())
        self.POS_NAME.bind('<<ComboboxSelected>>', self.Chosen2)
        # 打印选项内容

    def Chosen(self, event):
        print('机具类型：', self.PHYSN_TYPE.get())
        print('机具类型：', self.PHYSN_TYPE.current())
        print('机具名称：', self.POS_NAME.current())
        # -----机具类型关联机具名称选项框
        if self.PHYSN_TYPE.current() == 0:
            self.POS_NAME.configure(values=['00-小蓝(MPos)', '01-小蓝-会员(Mpos)'])
            self.POS_NAME.current(0)
        elif self.PHYSN_TYPE.current() == 1:
            self.POS_NAME.configure(
                values=['02-大蓝(大Pos)', '03-炫蓝(大Pos)', '07:大Pos(4G版)', '09:大机虎力版', '11:大pos(买断版)'])
            self.POS_NAME.current(0)
        elif self.PHYSN_TYPE.current() == 2:
            self.POS_NAME.configure(values=['04-电蓝(EPos)', '06:Epos(4G版本)', '08:EPos-Plus', '12:epos(买断版)'])
            self.POS_NAME.current(0)
        elif self.PHYSN_TYPE.current() == 3:
            self.POS_NAME.configure(values=['05-经典蓝(大Pos)'])
            self.POS_NAME.current(0)

    def Chosen2(self, event):
        print('机具名称：', self.POS_NAME.get())
        print('机具名称：', self.POS_NAME.current())


win = tk.Tk()  # 创建窗口
win.geometry('600x400')  # 设置窗口大小
# win.config(background='pink')
win.title("TEST")  # 创建窗口标题
test(win, None, None).my_GUI()
win.mainloop()  # 运行
