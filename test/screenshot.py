# /usr/bin/env python
# -*- encoding: utf-8 -*-

import io
import logging.config
# 打包命令pyinstaller main.spec
import os
import subprocess
import time

import PIL.Image
import aircv
import cv2
import numpy as np


class Dnconsole:
    """
    【雷电控制台类】
    version: 9.0
    import该文件会自动实例化为 Dc
    """

    def __init__(self, installation_path: str):
        """
        【构造方法】
        """
        # if 模拟器安装路径存在性检测
        if os.path.exists(installation_path) is False:
            print('模拟器安装路径不存在！')
        # 获取模拟器安装路径
        self.ins_path = installation_path
        # Dnconsole程序路径
        self.console_path = self.ins_path + r'\ldconsole.exe '
        # ld程序路径
        self.ld_path = self.ins_path + r'\ld.exe '
        # if Dnconsole程序路径检测
        if os.path.exists(self.console_path) is False:
            print('Dnconsole程序路径不存在！\n请确认模拟器安装文件是否完整或模拟器版本是否不符！')
        # adb程序路径
        self.adb_path = self.ins_path + r'\adb.exe '
        # if adb程序路径检测
        if os.path.exists(self.adb_path) is False:
            print('Dnconsole程序路径不存在！\n请确认模拟器安装文件是否完整！')
        # 模拟器截屏程序路径
        self.screencap_path = r'/system/bin/screencap'
        # 模拟器截图保存路径
        self.devicess_path = r'/sdcard/Pictures/Screenshots/screenshot_tmp.png'
        # 用户环境
        self.userprofile = os.environ['USERPROFILE']
        self.documents_path = os.path.join(self.userprofile, 'Documents')
        # 本地图片保存路径
        self.images_path = self.documents_path + r'\leidian9\Pictures\Screenshots\\'
        # if 模拟器的截图保存路径
        if os.path.exists(self.images_path) is False:
            print('模拟器截图保存路径不存在！')
        # 获取当前工作目录路径
        self.workspace_path = os.getcwd()
        # 本地图片样本保存路径
        # self.target_path = self.workspace_path + r'\target\1080p_dpi280\\'
        self.target_path = self.workspace_path + r'\target\test\\'
        # 读取作战参数信息保存路径
        self.action_path = self.workspace_path + r'\script\\'
        # 读取作战参数
        # 构造完成
        logging.debug('Class-Dnconsole is ready.(%s)' % self.ins_path)
        # print('Class-Dnconsole is ready.(%s)' % self.ins_path)

    def ldCMD(self, cmd: str):
        """
        【通过ld.exe执行代替adb的命令语句】
        :param cmd: 命令
        :return: 控制台调试内容
        """
        ldCMD = self.ld_path + cmd  # 控制台命令
        process = os.popen(ldCMD)
        result = process.read()
        process.close()
        return result

    def ADB(self, cmd: str):
        """
        【执行ADB命令语句】
        :param cmd: 命令
        :return: 控制台调试内容
        """
        CMD = self.adb_path + cmd  # adb命令
        # os.system('chcp 65001')
        # p = subprocess.Popen(['C:\\leidian\\LDPlayer9\\adb', '-s', '127.0.0.1:5555', 'exec-out', 'screencap', '-p'],
        #                      stdout=subprocess.PIPE)
        p = subprocess.Popen(CMD, stdout=subprocess.PIPE)
        output, _ = p.communicate()
        return output

    def ScreenShot_Adb(self):
        cmd1 = 'devices'
        cmd2 = '-s 127.0.0.1:5555 exec-out screencap -p'
        print(self.ADB(cmd1).decode('utf-8').replace('\r\n', '\n '))
        output = self.ADB(cmd2)
        img = PIL.Image.open(io.BytesIO(output)).convert('RGB')
        # img.save('C:\\Users\\11704\\Documents\\leidian9\\Pictures\\Screenshots\\screenshot_tmp2.png', 'PNG')
        # output = raw_data.decode('utf-8').replace('\r\n', ' ')
        # print(output)
        # img = PIL.Image.open(io.BytesIO(output)).convert('RGB')
        # img_np = np.array(img)
        img_np = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR).astype(np.uint8)
        # # logging.info("%s 已截图")
        print("已截图")
        return img_np
        # return img

    def screenShotnewLd(self, index: int):
        """
        【截屏并保存到本地ld调用方式】
        :param index: 模拟器序号
        """
        cmd = '-s %d " %s -p %s"' % (index, self.screencap_path, self.devicess_path)
        result = self.ldCMD(cmd)
        logging.info("已截图")
        return result


class BlueStacks_Console:
    """
    BlueStacks
    """

    def __init__(self, installation_path: str):
        """
        [BlueStacks]的构造
        :param installation_path:
        """
        # 模拟器安装路径存在性检测
        if os.path.exists(installation_path):
            pass
        else:
            print('模拟器安装路径不存在！')
        # 获取模拟器安装路径
        self.ins_path = installation_path
        # HD-Adb.exe程序路径
        self.adb_path = self.ins_path + r'\HD-Adb.exe '
        self.adb_path_cmd = self.ins_path + r'\HD-Adb.exe '
        if os.path.exists(self.adb_path):
            pass
        else:
            print('HD-Adb.exe程序路径不存在！\n请确认模拟器安装文件是否完整！')
        # 模拟器截屏程序路径
        self.screencap_path = r'/system/bin/screencap'
        # 获取当前工作目录路径
        self.workspace_path = os.getcwd()
        # 本地图片样本保存路径
        self.target_path = self.workspace_path + r'\target\test\\'
        # 读取作战参数信息保存路径
        self.action_path = self.workspace_path + r'\script\\'
        # 读取作战参数
        # 构造完成
        # logging.debug('Class-Dnconsole is ready.(%s)' % self.ins_path)
        print('Class-Dnconsole is ready.(%s)' % self.ins_path)

    def ADB(self, cmd: str):
        """
        【执行ADB命令语句】
        :param cmd: 命令
        :return: 控制台调试内容
        """
        CMD = self.adb_path_cmd + cmd  # adb命令
        # os.system('chcp 65001')
        # p = subprocess.Popen(
        #     ['C:\\Program Files\\BlueStacks_nxt\\HD-Adb', '-s', '127.0.0.1:5555', 'exec-out', 'screencap', '-p'],
        #     stdout=subprocess.PIPE)
        p = subprocess.Popen(CMD, stdout=subprocess.PIPE)
        output, _ = p.communicate()
        return output

    def Adb_Status(self):
        cmd = 'devices'
        output = self.ADB(cmd).decode('utf-8').replace('\r\n', '\n ')
        return output

    def Adb_Connect(self, adb_terminal):
        cmd = 'connect ' + adb_terminal
        output = self.ADB(cmd)
        return output

    def ScreenShot_Adb(self, device):
        # cmd1 = 'devices'
        cmd2 = '-s %s exec-out screencap -p' % device
        # print(self.ADB(cmd1))
        output = self.ADB(cmd2)
        img = PIL.Image.open(io.BytesIO(output)).convert('RGB')
        # img.save('C:\\Users\\11704\\Documents\\leidian9\\Pictures\\Screenshots\\screenshot_tmp2.png', 'PNG')
        # img_np = np.array(img)
        img_np = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR).astype(np.uint8)
        # # logging.info("%s 已截图")
        # print("已截图")
        return img_np

    def inputTap(self, index: str, x: int, y: int):
        """
        【点击操作】
        :param index: 模拟器序号
        :param x: x
        :param y: y
        :return: 控制台调试内容
        """
        cmd = '-s %s shell input tap %d %d' % (index, x, y)
        return self.ADB(cmd)


class Action(object):

    def __init__(self, device: str, BSc):
        self.device = device
        self.BSc = BSc
        images_path = 'C:\\Users\\11704\\Documents\\leidian9\\Pictures\\Screenshots\\'
        # self.screenshot_img_file = images_path + 'screenshot_tmp.png'
        self.screenshot_img_file2 = images_path + 'screenshot_tmp2.png'

    def isExist(self, target_img_name: str, rgb: bool = True, threshold: float = 0.6):
        start_time1 = time.perf_counter()
        screenshot_img = BS.ScreenShot_Adb(self.device)
        end_time1 = time.perf_counter()
        print("截图耗时: %s" % (end_time1 - start_time1))
        start_time2 = time.perf_counter()
        target_img_name_file = self.BSc.target_path + target_img_name
        target_img = aircv.imread(target_img_name_file)
        result = aircv.find_template(screenshot_img, target_img, rgb=rgb, threshold=threshold)
        end_time2 = time.perf_counter()
        print("分析耗时: %s" % (end_time2 - start_time2))
        if result is None:
            print('NO:%s' % result)
            return False, result
        else:
            print('YES:%s' % result)
            return True, result

    def isExistV2(self, target_img_name: str, rgb: bool = True, threshold: float = 0.9):
        start_time1 = time.perf_counter()
        DC.ScreenShot_Ld(0)
        end_time1 = time.perf_counter()
        print("截图耗时: %s" % (end_time1 - start_time1))
        start_time2 = time.perf_counter()
        target_img_name_file = self.BSc.target_path + target_img_name
        screenshot_img = aircv.imread(self.screenshot_img_file)
        target_img = aircv.imread(target_img_name_file)
        result = aircv.find_template(screenshot_img, target_img, rgb=rgb, threshold=threshold)
        end_time2 = time.perf_counter()
        print("分析耗时: %s" % (end_time2 - start_time2))
        if result is None:
            print('NO:%s' % result)
            return False, result
        else:
            print('YES:%s' % result)
            return True, result

    def isExist_bak(self, target_img_name: str, rgb: bool = True, threshold: float = 0.6):
        start_time2 = time.perf_counter()
        target_img_name_file = self.BSc.target_path + target_img_name
        screenshot_img = aircv.imread(self.screenshot_img_file2)
        target_img = aircv.imread(target_img_name_file)
        result = aircv.find_template(screenshot_img, target_img, rgb=rgb, threshold=threshold)
        end_time2 = time.perf_counter()
        print("分析耗时: %s" % (end_time2 - start_time2))
        if result is None:
            print('NO:%s' % result)
            return False, result
        else:
            print('YES:%s' % result)
            return True, result


if __name__ == '__main__':
    start_time = time.perf_counter()
    print(start_time)

    bluestacks_path = "C:\\Program Files\\BlueStacks_nxt"
    adb_terminal = '127.0.0.1:5555'
    device = 'emulator-5554'
    BS = BlueStacks_Console(bluestacks_path)
    print(BS.Adb_Status())

    # dc_path = "C:\\leidian\\LDPlayer9"
    # DC = Dnconsole(dc_path)
    temp_img = 'test2.png'

    ADB_device = Action(device, BS)
    ADB_device.isExist(temp_img)
    BS.inputTap(device, 538, 249)

    # dc_path = "C:\\leidian\\LDPlayer9"
    # DC = Dnconsole(dc_path)
    # ADB_device = Action('127.0.0.1:5555', DC)
    # ADB_device.isExist(temp_img)
    #
    # print("=================================================")
    #
    # dc_path = "C:\\leidian\\LDPlayer9"
    # DC = Dnconsole(dc_path)
    # ADB_device = Action('127.0.0.1:5555', DC)
    # ADB_device.isExistV2(temp_img)

    print("=================================================")

    ADB_device.isExist_bak(temp_img)
    end_time = time.perf_counter()
    print(end_time - start_time)

    # adb_path = "C:\\Program Files\\BlueStacks_nxt" + r'\HD-Adb.exe '
    # if os.path.exists(bluestacks_path):
    #     print("Program Files folder exists at", bluestacks_path)
    # else:
    #     print("Program Files folder does not exist")
    #
    # adb_path = "C:\\Program Files\\BlueStacks_nxt" + r'\HD-Adb.exe '
    # if os.path.exists(adb_path):
    #     print("Program Files folder exists at", adb_path)
    # else:
    #     print("Program Files folder does not exist")
    # result_test = ADB_device.isExist('test.png')
    # print(result_test)
