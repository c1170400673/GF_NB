import win32ui

dlg = win32ui.CreateFileDialog(1)  # 参数 1 表示打开文件对话框
dlg.SetOFNInitialDir('C://')  # 设置打开文件对话框中的初始显示目录
dlg.DoModal()
filename = dlg.GetPathName()
print(filename)
