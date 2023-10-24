# /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
【少前13-4自动刷图】
"""
import io
# 打包命令 pyinstaller main.spec
import logging.config
import os
import subprocess
import sys
import threading
import time
from functools import partial

import PIL.Image
import aircv
import cv2
import numpy as np
import win32api
import win32con
import yaml

# 全局覆盖print函数参数
print = partial(print, flush=True)


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
        self.target_path = self.workspace_path + r'\target\720p_dpi240\\'
        # 读取作战参数信息保存路径
        self.action_path = self.workspace_path + r'\script\\'
        # 读取作战参数
        # 构造完成
        logging.debug('Class-Dnconsole is ready.(%s)' % self.ins_path)
        # print('Class-Dnconsole is ready.(%s)' % self.ins_path)

    def CMD(self, cmd: str):
        """
        【执行控制台命令语句】
        :param cmd: 命令
        :return: 控制台调试内容
        """
        CMD = self.console_path + cmd  # 控制台命令
        process = os.popen(CMD)
        result = process.read()
        process.close()
        return result

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
        p = subprocess.Popen(CMD, stdout=subprocess.PIPE)
        output, _ = p.communicate()
        return output

    def launch(self, index: int = 0):
        """
        【启动模拟器】
        :param index: 模拟器序号
        :return: True=已启动 / False=不存在
        """
        cmd = 'launch --index %d' % index
        if self.CMD(cmd) == '':
            return True
        else:
            return False

    def runninglist(self):
        """
        【获取正在运行的模拟器列表（仅标题）】
        :return: 控制台调试内容
        """
        cmd = 'runninglist'
        return self.CMD(cmd)

    def isrunning(self, index: int = 0):
        """
        【检测模拟器是否启动】
        :param index: 模拟器序号
        :return: True=已启动 / False=未启动
        """
        cmd = 'isrunning --index %d' % index
        if self.CMD(cmd) == 'running':
            return True
        else:
            return False

    def runApp(self, index: int, packagename: str):
        """
        【运行App】
        :param index: 模拟器序号
        :param packagename: 包名
        :return: 控制台调试内容
        """
        cmd = 'runapp --index %d --packagename %s' % (index, packagename)
        return self.CMD(cmd)

    def isrunningAPP(self, index: int, packagename: str):
        """
        【检测应用是否启动】
        :param packagename: App包名
        :param index: 模拟器序号
        :return: True=已启动 / False=未启动
        """
        cmd = 'adb --index %d --command "shell dumpsys window | grep mCurrentFocus"' % index
        if packagename in self.CMD(cmd):
            return True
        else:
            return False

    def appIsrunning(self, index: int, packagename: str):
        """
        【获取App运行状态】
        :param index: 模拟器序号
        :param packagename: 包名
        :return: 控制台调试内容
        """
        cmd = 'adb --index %d --command "shell pidof %s"' % (index, packagename)
        return self.CMD(cmd)

    def killApp(self, index: int, packagename: str):
        """
        【终止App】
        :param index: 模拟器序号
        :param packagename: 包名
        :return: 控制台调试内容
        """
        cmd = 'killapp --index %d --packagename %s' % (index, packagename)
        return self.CMD(cmd)

    def screenShot(self, index: int):
        """
        【截屏并保存到本地】
        :param index: 模拟器序号
        """
        cmd1 = 'adb --index %d --command "shell %s -p %s"' % (index, self.screencap_path, self.devicess_path)
        cmd2 = 'adb --index %d --command "pull %s %s"' % (index, self.devicess_path, self.images_path)
        self.CMD(cmd1)
        self.CMD(cmd2)

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

    def ScreenShot_v1(self, index: int):
        """
        【截屏并保存到本地】
        :param index: 模拟器序号
        """
        cmd = 'adb --index %d --command "shell %s -p %s"' % (index, self.screencap_path, self.devicess_path)
        result = self.CMD(cmd)
        return result

    def ScreenShot_Ld(self, index: int):
        """
        【截屏并保存到本地ld调用方式】
        :param index: 模拟器序号
        """
        cmd = '-s %d " %s -p %s"' % (index, self.screencap_path, self.devicess_path)
        result = self.ldCMD(cmd)
        scp_time = time.time() - start_time
        scp_time = time.strftime("%H:%M:%S", time.gmtime(scp_time))
        logging.info("%s 已截图" % scp_time)
        return result

    def actionOfTap(self, index: int, x: int, y: int):
        """
        【点击操作】
        :param index: 模拟器序号
        :param x: x
        :param y: y
        :return: 控制台调试内容
        """
        cmd = 'adb --index %d --command "shell input tap %d %d"' % (index, x, y)
        return self.CMD(cmd)

    def inputTap(self, index: int, x: int, y: int):
        """
        【点击操作】
        :param index: 模拟器序号
        :param x: x
        :param y: y
        :return: 控制台调试内容
        """
        cmd = '-s %d input tap %d %d' % (index, x, y)
        return self.ldCMD(cmd)

    def inputSwipe(self, index: int, x0: int, y0: int, x1: int, y1, ms: int = 200):
        """
        【滑动操作】
        :param index:
        :param x0:
        :param y0:
        :param x1:
        :param y1:
        :param ms:
        :return:
        """
        cmd = '-s %d input swipe %d %d %d %d %d' % (index, x0, y0, x1, y1, ms)
        return self.ldCMD(cmd)


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
        self.target_path = self.workspace_path + '\\target\\' + target_path + '\\'
        # 读取作战参数信息保存路径
        self.action_path = self.workspace_path + '\\script\\'
        # 读取作战参数
        # 构造完成
        # logging.debug('Class-Dnconsole is ready.(%s)' % self.ins_path)
        print('BlueStacks is ready.(%s)' % self.ins_path)

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

    def ScreenShot_Adb(self, index):
        cmd2 = '-s %s exec-out screencap -p' % index
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

    def inputSwipe(self, index: str, x0: int, y0: int, x1: int, y1, ms: int = 200):
        """
        【滑动操作】
        :param index:
        :param x0:
        :param y0:
        :param x1:
        :param y1:
        :param ms:
        :return:
        """
        cmd = '-s %s shell input swipe %d %d %d %d %d' % (index, x0, y0, x1, y1, ms)
        return self.ADB(cmd)


class Action(object):
    """
    【事件操作类】
    import该文件需先实例化 对应模拟器的console
    """

    def __init__(self, index: str, console):
        """
        【构造方法】
        :param index: 模拟器号
        :param console: 传入的Console对象
        """
        self.index = index
        self.console = console

    def is_Exist_V3(self, target_name: str, target_img_num: int = 0):
        """
        【判断指定图片是否包含在截图中】
        :param target_name:
        :param target_img_num:
        :return: 图片查询结果和包含详情
        """
        target_yaml = target_yaml_data[target_name]
        target_img_name = target_yaml['target_img_name_list'][target_img_num]
        rgb = target_yaml['rgb']
        threshold = target_yaml['threshold']
        screenshot_img = ScreenShot_Img
        target_img_name_file = self.console.target_path + target_img_name
        target_img = aircv.imread(target_img_name_file)
        result = aircv.find_template(screenshot_img, target_img, rgb=rgb, threshold=threshold)
        if result is None:
            return False, result
        else:
            return True, result

    def find_target_img_V5(self, target_name: str, tap_info: dict):
        """
        【改进后的目标图片搜索方法】
        :param tap_info:
        :param target_name:
        :return:
        """
        global ScreenShot_Img
        logging.debug('target: %s, 配置信息: %s' % (target_name, tap_info))
        target_img_name_list = tap_info['target_img_name_list']
        need_screenShot = tap_info['need_screenShot']
        moveX = tap_info['moveX']
        moveY = tap_info['moveY']
        tap_times = tap_info['tap_times']
        tap_interval = tap_info['tap_interval']
        search_again_times = tap_info['search_again_times']
        search_again_sleep_time = tap_info['search_again_sleep_time']
        for target_img_name in target_img_name_list:
            for search in range(search_again_times):
                if need_screenShot:
                    ScreenShot_Img = self.console.ScreenShot_Adb(self.index)
                target_img_num = target_img_name_list.index(target_img_name)
                result = self.is_Exist_V3(target_name, target_img_num)
                find_result = result[1]
                if find_result is None and need_screenShot is False and search_again_times == 1:
                    running_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                    # print('%s 未能找到需要的 %s 按钮！' % (running_time, target_img_name))
                    logging.error('%s 未能找到需要的 %s 按钮！' % (running_time, target_img_name))
                    break
                elif find_result is None and search_again_times == 1:
                    running_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                    # print('%s 未能找到需要的 %s 按钮！' % (running_time, target_img_name))
                    logging.error('%s 未能找到需要的 %s 按钮！' % (running_time, target_img_name))
                elif find_result is None and search_again_times > 1:
                    running_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                    # print('%s 未能找到需要的 %s 按钮！' % (running_time, target_img_name), end="")
                    logging.warning('%s 未能找到需要的 %s 按钮！' % (running_time, target_img_name))
                    search_times = 1
                    search_times += search
                    if search_again_sleep_time != 0:
                        search_again_sleep_time_double = int(search_again_sleep_time * 2)
                        for s in range(search_again_sleep_time_double + 1):
                            running_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                            half_second = s
                            s_10, d = divmod(half_second, 10)
                            print("\r%s %-40s" % (running_time, 'o' * s_10 + '.' * d), end="")
                            if s == search_again_sleep_time_double:
                                pass
                            else:
                                time.sleep(0.5)
                        print('\n', end='')
                    else:
                        pass
                    running_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                    # print('%s 重新搜索 %s 按钮 %d 次' % (running_time, target_img_name, search_times))
                    logging.info('%s 重新搜索 %s 按钮 %d 次' % (running_time, target_img_name, search_times))
                    # 判断当不用截图的target节点当search_again_times大于1时重试时触发截图
                    if need_screenShot is False:
                        ScreenShot_Img = self.console.ScreenShot_Adb(self.index)
                    if search_times == search_again_times:
                        running_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                        # print('%s 未能找到需要的 %s 按钮！' % (running_time, target_img_name))
                        logging.error('%s 未能找到需要的 %s 按钮！' % (running_time, target_img_name))
                else:
                    # 按钮坐标
                    x = find_result['result'][0]
                    y = find_result['result'][1]
                    # 点击坐标
                    tap_x = x - moveX
                    tap_y = y - moveY
                    for t in range(tap_times):
                        tap = t + 1
                        running_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                        print('%s 找到按钮: %s [%d , %d]  ' % (running_time, target_img_name, x, y))
                        if tap_interval != 0 and tap_times > 1:
                            tap_interval_time = int(tap_interval * 2)
                            for s in range(tap_interval_time + 1):
                                running_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                                half_second = s
                                s_10, d = divmod(half_second, 10)
                                print("\r%s %-40s" % (running_time, 'o' * s_10 + '.' * d), end="")
                                if s == tap_interval_time:
                                    pass
                                else:
                                    time.sleep(0.5)
                            print('\n', end='')
                        else:
                            pass
                        self.console.inputTap(Console_Action.index, tap_x, tap_y)
                        running_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                        print('%s 已点击按钮 %s [%d , %d] %d次' % (running_time, target_img_name, tap_x, tap_y, tap))
                    break
            if result[0]:
                break
        return result

    def Action_Tap_V5(self, target_name: str, tap_info: dict):
        """
        【查找对应按钮】
        :param tap_info:
        :param target_name: 点击事件查询的按钮target
        """
        global ScreenShot_Img
        running_time = time.time() - start_time
        running_time = time.strftime("%H:%M:%S", time.gmtime(running_time))
        tap_result_check_name = tap_info['tap_result_check_name']
        before_tap_wait_time = tap_info['before_tap_wait_time']
        after_tap_wait_time = tap_info['after_tap_wait_time']
        beginning_content = tap_info['beginning_content']
        end_content = tap_info['end_content']
        error_content = tap_info['error_content']
        print('%s +++++START+++++ [目标%s:%s %s]' % (running_time, target_name, beginning_content, running_script))
        if before_tap_wait_time != 0:
            do_before_tap_wait_time = int(before_tap_wait_time * 2)
            for s in range(do_before_tap_wait_time + 1):
                running_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                half_second = s
                s_10, d = divmod(half_second, 10)
                print("\r%s %-40s" % (running_time, 'o' * s_10 + '.' * d), end="")
                if s == do_before_tap_wait_time:
                    pass
                else:
                    time.sleep(0.5)
            print('\n', end='')
        else:
            pass
        result = True
        while result:
            # 点击target
            find_result = self.find_target_img_V5(target_name, tap_info)
            # 判断点击方法处理结果
            if find_result[0]:
                # 处理点击后等待时间
                if after_tap_wait_time != 0:
                    do_after_tap_wait_time = int(after_tap_wait_time * 2)
                    for s in range(do_after_tap_wait_time + 1):
                        running_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                        half_second = s
                        s_10, d = divmod(half_second, 10)
                        print("\r%s %-40s" % (running_time, 'o' * s_10 + '.' * d), end="")
                        if s == do_after_tap_wait_time:
                            pass
                        else:
                            time.sleep(0.5)
                    print('\n', end='')
                else:
                    pass
                # 判断是否有校验对象
                if tap_result_check_name is not None:
                    # 赋值未校验标记
                    is_not_Exist_result = True
                    # 当有校验对象后执行循环校验
                    while is_not_Exist_result:
                        # 校验前截图
                        ScreenShot_Img = self.console.ScreenShot_Adb(self.index)
                        running_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                        # print('%s 开始校验 %s' % (running_time, tap_result_check_name))
                        logging.info('%s 开始校验 %s' % (running_time, tap_result_check_name))
                        # 执行校验
                        tap_result = self.is_Exist_V3(tap_result_check_name)
                        # 判断校验结果，通过后结束校验
                        if tap_result[0]:
                            running_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                            # print('%s 校验通过' % running_time)
                            logging.info('%s 校验通过' % running_time)
                            is_not_Exist_result = False
                            break
                        # 不通过重新点击target
                        elif tap_result[0] is False:
                            running_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                            # print('%s 点击后结果校验不通过，重新点击！' % running_time)
                            logging.error('%s 点击后结果校验不通过，重新点击！' % running_time)
                            # 为了校验执行后重新点击target，需启动截图
                            need_screenShot_tap_info = tap_info.copy()
                            need_screenShot_tap_info.update({'need_screenShot': True})
                            find_result = self.find_target_img_V5(target_name, need_screenShot_tap_info)
                            # 判断重新点击target后的结果
                            if find_result[0]:
                                # 点击target成功后将会重新执行校验
                                # print('重新点击 %s 成功' % target_name)
                                logging.info('重新点击 %s 成功' % target_name)
                                if after_tap_wait_time != 0:
                                    do_after_tap_wait_time = int(after_tap_wait_time * 2)
                                    for s in range(do_after_tap_wait_time + 1):
                                        running_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                                        half_second = s
                                        s_10, d = divmod(half_second, 10)
                                        print("\r%s %-40s" % (running_time, 'o' * s_10 + '.' * d), end="")
                                        if s == do_after_tap_wait_time:
                                            pass
                                        else:
                                            time.sleep(0.5)
                                    print('\n', end='')
                                else:
                                    pass
                            # 点击target失败也将重新执行校验
                            else:
                                # print('当前界面未能找到 %s ，需重新校验 %s' % (target_name, tap_result_check_name))
                                logging.error(
                                    '当前界面未能找到 %s ，需重新校验 %s' % (target_name, tap_result_check_name))
                    if is_not_Exist_result is False:
                        break
                    else:
                        pass
                # 无校验的直接结束点击处理
                else:
                    break
            else:
                print(error_content)
                # 暂停后手动操作
                result_action = win32api.MessageBox(0, "自动执行异常请检查！请手动调整！是再次重试/否跳过此步骤:", "提醒",
                                                    win32con.MB_TOPMOST | win32con.MB_YESNO)
                if result_action == win32con.IDNO:
                    logging.info('选择了跳过 %s 步骤' % target_name)
                    break
                elif result_action == win32con.IDYES:
                    tap_info.update({'need_screenShot': True})
                    logging.info('重置截图触发为启动截图')
        running_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
        print('%s +++++ END +++++ [%s]\n' % (running_time, end_content))

    def is_all_Exist_V3(self, target_name: str):
        """
        【判断多个指定图片是否包含在截图中】
        :param target_name:
        :return: 图片查询结果和包含详情
        """
        target_yaml = target_yaml_data[target_name]
        target_img_name = target_yaml['target_img_name_list'][0]
        rgb = target_yaml['rgb']
        threshold = target_yaml['threshold']
        screenshot_img = ScreenShot_Img
        target_img_name_file = self.console.target_path + target_img_name
        target_img = aircv.imread(target_img_name_file)
        result = aircv.find_all_template(screenshot_img, target_img, rgb=rgb, threshold=threshold)
        if result is None:
            return False, result
        else:
            return True, result

    def List_select_V3(self, target_name: str):
        """
        【从人形列表选择人形】
        :param self:
        :param target_name:
        """
        list_result = self.is_all_Exist_V3(target_name)[1]
        # print(list_result)
        # print(len(list_result))
        if list_result is not False:
            for result in list_result:
                coordinate = result['result']
                x = coordinate[0] - 100
                y = coordinate[1] + 200
                print('选中人形 X: %s  Y: %s' % (x, y))
                self.console.inputTap(Console_Action.index, x, y)
                time.sleep(0.5)


class Tools:
    """
    tools:工具类
    """

    def __init__(self):
        # 获取当前工作目录路径
        self.workspace_path = os.getcwd()
        # 本地图片样本保存路径
        self.target_path = self.workspace_path + '\\target\\'
        # 读取作战参数信息保存路径
        self.action_path = self.workspace_path + '\\script\\'

    def YAML(self, script_name: str):
        """
        【读取Yaml文件】
        :param script_name:
        :return:
        """
        # 读取YAML参数
        yaml_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                 self.action_path + script_name)
        logging.debug('yaml_path: %s' % yaml_path)
        try:
            # 打开文件
            with open(yaml_path, "r", encoding="utf-8") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                return data
        except:
            return None


def tap_info_dict(target: str, data_dict: dict):
    """

    :param target:
    :param data_dict:
    :return:
    """
    # 获取target中的默认的beginning_content与end_content值
    target_yaml = target_yaml_data[target]
    # 默认初始化的tap_info
    default_tap_info: dict = battle_yaml_data['default_tap_info']
    tap_info = default_tap_info.copy()
    tap_info.update(target_yaml)
    if data_dict is None:
        return tap_info
    else:
        tap_info.update(data_dict)
        return tap_info


class Yaml_Drive:
    """
    基于Yaml文件驱动的脚本执行器
    """

    def __init__(self, console, console_action):
        self.console_action = console_action
        self.console = console

    def tap_dict(self, data_dict: dict):
        """

        :param data_dict:
        """
        # print("dict:")
        for i in data_dict:
            if 'get' in i:
                get_def = data_dict[i]
                self.def_info_dict(i)
                self.drive_yaml(get_def)
                continue

    def screenShot_dict(self, data_dict: dict):
        """

        :param data_dict:
        """
        isExist_target_key_result = False
        run_yaml = ''
        for key in data_dict:
            isExist_target_key = key
            isExist_target_value = data_dict[key]
            # print(isExist_target_key)
            if isExist_target_key == 'else':
                running_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                # print("%s 截图查询[ %s ]元素不存在！" % (running_time, data_dict.keys()))
                dict_keys = list(data_dict.keys())
                logging.warning("%s 截图查询 %s 元素不存在！" % (running_time, dict_keys))
                if isExist_target_value == 'exit':
                    logging.debug('执行exit方法')
                    return True
                    # sys.exit()
                elif isExist_target_value == 'break':
                    logging.debug('执行break方法')
                    break
                else:
                    running_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                    # print("%s 执行else方法" % running_time)
                    logging.debug("执行else方法")
                    self.tap_list(isExist_target_value)
            elif self.console_action.is_Exist_V3(isExist_target_key)[0]:
                running_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                # print("%s 包含: %s" % (running_time, isExist_target_key))
                logging.debug("%s 包含: %s" % (running_time, isExist_target_key))
                if isExist_target_value == 'break':
                    logging.debug('执行break方法')
                    break
                # print(isExist_target_key, isExist_target_value)
                isExist_target_key_result = True
                run_yaml = isExist_target_value
                break
        if isExist_target_key_result:
            # 截图对象查询到后，判断后续处理对象还是
            if type(run_yaml) == dict:
                self.screenShot_dict(run_yaml)
            else:
                if self.drive_yaml(run_yaml):
                    return True

    def def_info_dict(self, data_dict: dict):
        """
        :param data_dict:
        :return:
        """
        fun: bool = True
        adv_retire: bool = True
        def_info: dict = {}
        def_info.update(data_dict)
        return def_info

    def tap_list(self, data_target_list: list, data_info: dict = None):
        """

        :param data_info:
        :param data_target_list:
        """
        # print("list:")
        global ScreenShot_Img
        for data_target in data_target_list:
            for target in data_target:
                # 是否截图判断target存在
                if target == 'screenShot':
                    if data_target[target] is None:
                        ScreenShot_Img = self.console.ScreenShot_Adb(device)
                        break
                    else:
                        ScreenShot_Img = self.console.ScreenShot_Adb(device)
                        screenShot_dict_info = data_target[target]
                        # print('%s: %s' % (key, isExist_target[key]))
                        if self.screenShot_dict(screenShot_dict_info):
                            return True
                # 是否是驱动方法
                elif 'get_' in target:
                    get_def_info = data_target[target]
                    def_info = self.def_info_dict(get_def_info)
                    get_def_yaml = battle_yaml_data[target]
                    drive_yaml_result = self.drive_yaml(get_def_yaml, def_info)
                    if drive_yaml_result:
                        return True
                    elif drive_yaml_result is False:
                        return False
                elif 'round_' in target:
                    round_times = data_target[target]
                    round_def_yaml = battle_yaml_data[target]
                    for i in range(round_times):
                        round_result = self.drive_yaml(round_def_yaml)
                        if round_result:
                            return True
                        elif round_result is False:
                            return False
                        else:
                            pass
                elif target == 'adv_retire':
                    if data_info['adv_retire']:
                        self.tap_list(data_target[target])
                elif target == 'sleep':
                    sleep_time = data_target[target]
                    if sleep_time != 0:
                        do_sleep_time = int(sleep_time * 2)
                        for s in range(do_sleep_time + 1):
                            running_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))
                            half_second = s
                            s_10, d = divmod(half_second, 10)
                            print("\r%s 请稍等 %-30s" % (running_time, 'o' * s_10 + '.' * d), end="")
                            if s == do_sleep_time:
                                pass
                            else:
                                time.sleep(0.5)
                        print('\n', end='')
                    else:
                        pass
                elif target == 'swipe':
                    swipe_info = data_target[target]
                    x0 = swipe_info[0]
                    y0 = swipe_info[1]
                    x1 = swipe_info[2]
                    y1 = swipe_info[3]
                    ms = swipe_info[4]
                    self.console.inputSwipe(device, x0, y0, x1, y1, ms)
                elif target == 'loop':
                    pass
                elif target == 'goto':
                    pass
                else:
                    if data_target[target] == 'list':
                        self.console_action.List_select_V3(target)
                    else:
                        tap_info = tap_info_dict(target, data_target[target])
                        self.console_action.Action_Tap_V5(target, tap_info)

    def drive_yaml(self, data, data_info: dict = {}, fun_return: bool = False):
        """

        :param fun_return:
        :param data_info:
        :param data:
        """
        if type(data) == dict:
            self.tap_dict(data)
        elif type(data) == list:
            if self.tap_list(data, data_info):
                return True
            if 'fun_return' in data_info.keys():
                data_info_result = data_info['fun_return']
                if data_info_result:
                    return True
                else:
                    return False
        else:
            pass


def test():
    """
    【调试测试类】
    :return:
    """
    # get_into_mission = battle_yaml_data['get_into_mission']
    # get_13_4 = battle_yaml_data['get_13_4']
    # drive_yaml(get_into_mission)
    # for i in range(2):
    #     drive_yaml(get_13_4)
    if Console_Action.isExistV2('end_fighting'):
        print("True")
    sys.exit()


class Job(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()  # 用于暂停线程的标识
        self.__flag.set()  # 设置为True
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()  # 将running设置为True

    # def run(self):
    #     while self.__running.isSet():
    #         print("thread is run")
    #         self.__flag.wait()  # 为True时立即返回, 为False时阻塞直到self.__flag为True后返回
    #         print("run = ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    #         time.sleep(1)

    def pause(self):
        logging.debug("thread is pause")
        self.__flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        logging.debug("thread is resume")
        self.__flag.set()  # 设置为True, 让线程停止阻塞

    def stop(self):
        logging.debug("thread is stop")
        self.__flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()  # 设置为False


def run_config():
    """
    构建基础配置

    """
    Girl_Frontline = Tools()
    basic_config = 'config.yaml'
    basic_config_data = Girl_Frontline.YAML(basic_config)
    global console_name, target_path, device, Console, Console_Action, battle_list
    # 模拟器配置
    console_config = basic_config_data['console_config']
    console_name = console_config['console']
    # target调用配置
    target_config = basic_config_data['target_config']
    target_path = target_config['target']
    battle_battle = basic_config_data['battle']
    battle_list = battle_battle['battle_list']
    global target_yaml_data, battle_yaml_data, get_into_mission, select_battle_name, battle_name_1, battle_name_2, \
        end_combat_1, end_combat_2
    # 模拟器adb终端默认地址
    adb_terminal = '127.0.0.1:5555'
    # 判断调用模拟器的方法
    if console_name == 'BlueStacks':
        # bluestacks模拟器目录
        bluestacks_path = "C:\\Program Files\\BlueStacks_nxt"
        # 模拟器终端名称
        device = 'emulator-5554'
        Console = BlueStacks_Console(bluestacks_path)
        # 获取判断bluestacks模拟器的连接状态
        if device in Console.Adb_Status():
            pass
        else:
            Console.ADB('kill-server')
            time.sleep(1)
            Console.ADB('start-server')
        Console_Action = Action(device, Console)
    elif console_name == 'LDplayer':
        # 雷电模拟器目录
        ldplayer_path = r'C:\leidian\LDPlayer9'
        Console = Dnconsole(ldplayer_path)
        Console_Action = Action('0', Console)
        # print(Dc.workspace_path)
        logging.debug(Girl_Frontline.workspace_path)
    target_yaml_data = Girl_Frontline.YAML('target.yaml')
    # 展示可用的关卡
    for battle_name in battle_list:
        battle_num = battle_list.index(battle_name)
        print('(%s)  %s' % (battle_num, battle_name))
    # 选择关卡
    try:
        select_battle_num = int(input("选择战斗的关卡(序号）:"))
    except ValueError:
        print("请正确输入关卡序号,未输入将默认执行序号0的关卡")
        select_battle_num = 0
    # 载入关卡配置
    logging.info('开始加载关卡配置')
    battle_name = battle_list[select_battle_num]
    battle_yaml = battle_name + '.yaml'
    battle_yaml_data = Girl_Frontline.YAML(battle_yaml)
    get_into_mission = battle_yaml_data['get_into_mission']
    select_battle_name = battle_yaml_data['get_select_%s' % battle_name]
    battle_name_1 = battle_yaml_data['battle_%s_1' % battle_name]
    battle_name_2 = battle_yaml_data['battle_%s_2' % battle_name]
    end_combat_1 = battle_yaml_data['end_combat_1']
    end_combat_2 = battle_yaml_data['end_combat_2']


def battle():
    global running_script, start_time, battle_list
    yaml_drive = Yaml_Drive(Console, Console_Action)
    user_action = True
    while user_action:
        try:
            runtimes = int(input("跑几圈:"))
        except ValueError:
            print("请正确输入圈数,未输入将默认执行1次")
            runtimes = 1
        try:
            runtime = float(input("跑多久(分钟）:"))
        except ValueError:
            print("请正确输入执行时间，未输入将默认执行999分钟限制")
            runtime = 999
        finally:
            runtime_min = runtime * 60
        running_script = '共 %d 次，开始执行' % runtimes
        start_time = time.time()
        if yaml_drive.drive_yaml(get_into_mission):
            continue
        ran_time: float = 0
        if runtimes == 1:
            yaml_drive.drive_yaml(select_battle_name)
            yaml_drive.drive_yaml(battle_name_1)
            yaml_drive.drive_yaml(end_combat_1)
        elif runtimes > 1:
            # 执行次数大于1，默认执行再次战斗流程
            fight_again: bool = True
            yaml_drive.drive_yaml(select_battle_name)
            for is_runtimes in range(runtimes):
                is_runtimes_num = is_runtimes + 1
                running_script = '共 %d 次，正在执行第 %d 次' % (runtimes, is_runtimes_num)
                if is_runtimes_num > 1 and fight_again is True:
                    yaml_drive.drive_yaml(battle_name_2)
                elif is_runtimes_num == 1 and fight_again is True:
                    yaml_drive.drive_yaml(battle_name_1)
                elif is_runtimes_num > 1 and fight_again is False:
                    yaml_drive.drive_yaml(battle_name_1)
                end_time = time.time()
                ran_time = end_time - start_time
                if ran_time < runtime_min and is_runtimes_num < runtimes:
                    fight_again = True
                    end_result = yaml_drive.drive_yaml(end_combat_2)
                    # 【结束流程】校验执行了特殊方法后判断，是否是使用再次战斗执行的战斗流程
                    if end_result:
                        fight_again = False
                    end_time = time.time()
                    ran_time = end_time - start_time
                    ran_time_m, ran_time_s = divmod(ran_time, 60)
                    ran_time_h, ran_time_m = divmod(ran_time_m, 60)
                    logging.info('共 %d 次，已执行 %d 次, 已运行 %02d 时 %02d 分 %02d 秒\n' % (
                        runtimes, is_runtimes_num, ran_time_h, ran_time_m, ran_time_s))
                    # print('共 %d 次，已执行 %d 次, 已运行 %02d 时 %02d 分 %02d 秒\n' % (
                    #     runtimes, is_runtimes_num, ran_time_h, ran_time_m, ran_time_s))
                elif ran_time < runtime_min and is_runtimes_num == runtimes:
                    yaml_drive.drive_yaml(end_combat_1)
                    end_time = time.time()
                    ran_time = end_time - start_time
                    ran_time_m, ran_time_s = divmod(ran_time, 60)
                    ran_time_h, ran_time_m = divmod(ran_time_m, 60)
                    logging.info('共 %d 次，已执行 %d 次, 已运行 %02d 时 %02d 分 %02d 秒\n' % (
                        runtimes, is_runtimes_num, ran_time_h, ran_time_m, ran_time_s))
                else:
                    yaml_drive.drive_yaml(end_combat_1)
                    end_time = time.time()
                    ran_time = end_time - start_time
                    ran_time_m, ran_time_s = divmod(ran_time, 60)
                    ran_time_h, ran_time_m = divmod(ran_time_m, 60)
                    logging.info('共 %d 次，已执行 %d 次, 已运行 %02d 时 %02d 分 %02d 秒\n' % (
                        runtimes, is_runtimes_num, ran_time_h, ran_time_m, ran_time_s))
                    break
        result_action = win32api.MessageBox(0, "是否继续跑步机?", "提醒", win32con.MB_TOPMOST | win32con.MB_YESNO)
        # action = input('是否继续跑步机?enter后继续/输入exit退出: ')
        # if action == 'exit':
        #     break
        # else:
        #     pass
        if result_action == win32con.IDYES:
            logging.info('继续执行跑步机')
            pass
        else:
            logging.info('结束跑步机')
            break
        # os.system('pause')  # 按任意键继续


if __name__ == '__main__':
    CON_LOG = 'logger.conf'  # 配置文件路径
    logging.config.fileConfig(CON_LOG)  # '读取日志配置文件'
    logger = logging.getLogger('exampleLogger')  # 创建一个日志器logger
    logging.getLogger('PIL').setLevel(logging.WARNING)

    # 获取程序工作目录
    workspace = os.getcwd()
    global console_name, target_path, ScreenShot_Img, device, Console, Console_Action, battle_list
    global target_yaml_data, battle_yaml_data, get_into_mission, select_battle_name, battle_name_1, battle_name_2, \
        end_combat_1, end_combat_2, running_script, start_time
    # base_run = threading.Thread(target=run_config)
    # battle_run = threading.Thread(target=battle)
    # 基础数据和环境初始化
    run_config()
    # 启动战斗运行
    battle_run = Job(target=battle)
    battle_run.start()
    battle_run.join()

    # battle_run.pause()

    # AppPackage = 'com.sunborn.girlsfrontline.cn'
    # App = '少女前线'
    # if Dc.isrunning(0):
    #     print('模拟器已启动')
    #     time.sleep(5)
    # else:
    #     Dc.launch(0)
    #     print('模拟器启动中')
    #     time.sleep(15)
    #
    # if Dc.isruningAPP(0, AppPackage):
    #     print('%s is running' % AppPackage)
    # else:
    #     Dc.runApp(0, AppPackage)
    #     print('%s is ran' % AppPackage)
    #
    # time.sleep(10)
    # print('%s 已启动' % App)

    # # 登录（暂不支持需要输入密码）
    # Ld.LdactionTap(0, Dc, r'screenshout_tmp.png', r'sign_in.png', sleeptime=3)
    # # 开始游戏，进入主界面
    # Ld.LdactionTap(0, Dc, r'screenshout_tmp.png', r'start_game.png')

    # 调试方法
    # start_time = time.time()
    # running_script = '1'
    # test()
