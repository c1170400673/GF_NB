# /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
【少前13-4自动刷图】
"""
import os
import sys
import time

import aircv
import yaml


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
        self.devicess_path = r'/sdcard/Pictures/Screenshots/screenshout_tmp.png'
        # 本地图片保存路径
        self.images_path = r'C:\Users\11704\Documents\leidian9\Pictures\Screenshots\\'
        # 本地图片样本保存路径
        # self.target_path = r'D:\GF_NB\target\1080p_dpi280\\'
        self.target_path = r'D:\MyCode\GF_NB\target\1080p_dpi280\\'
        # 读取作战参数信息保存路径
        self.action_path = r'D:\MyCode\GF_NB\script\\'
        # 读取作战参数
        # 构造完成
        print('Class-Dnconsole is ready.(%s)' % self.ins_path)

    def YAML(self, script_name: str):
        """
        【读取Yaml文件】
        :param script_name:
        :return:
        """
        # 读取YAML参数
        yaml_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                 self.action_path + script_name)
        try:
            # 打开文件
            with open(yaml_path, "r", encoding="utf-8") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
                return data
        except:
            return None

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
        process = os.popen(CMD)
        result = process.read()
        process.close()
        return result

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

    def isruningAPP(self, index: int, packagename: str):
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

    def screenShotnew(self, index: int):
        """
        【截屏并保存到本地】
        :param index: 模拟器序号
        """
        cmd = 'adb --index %d --command "shell %s -p %s"' % (index, self.screencap_path, self.devicess_path)
        result = self.CMD(cmd)
        return result

    def screenShotnewLd(self, index: int):
        """
        【截屏并保存到本地ld调用方式】
        :param index: 模拟器序号
        """
        cmd = '-s %d " %s -p %s"' % (index, self.screencap_path, self.devicess_path)
        result = self.ldCMD(cmd)
        scp_time = time.time() - star_time
        scp_time = time.strftime("%H:%M:%S", time.gmtime(scp_time))
        print("==O== %s" % scp_time)
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


class Ldaction(object):
    """
    【雷电操作类】
    import该文件需先实例化 Dconsole
    """

    def __init__(self, index: int, ld, screenshot_img_name: str):
        """
        【构造方法】
        :param index: 模拟器号
        :param ld: 传入的Dconsole对象
        :param screenshot_img_name:
        :return:
        """
        self.screenshot_img_file = ld.images_path + screenshot_img_name
        # self.screenshot_img = aircv.imread(self.screenshot_img_file)
        self.index = index
        self.ld = ld
        self.tap_info = self.ld.YAML

    def isExist(self, target_img_name: str, rgb: bool = False, threshold: float = 0.9):
        """
        【判断指定图片是否包含在截图中】
        :param self:
        :param rgb: 比对rgb通道开关
        :param threshold:
        :param target_img_name:
        :return: 图片查询结果和包含详情
        """
        screenshot_img = aircv.imread(self.screenshot_img_file)
        target_img_name_file = self.ld.target_path + target_img_name
        target_img = aircv.imread(target_img_name_file)
        result = aircv.find_template(screenshot_img, target_img, rgb=rgb, threshold=threshold)
        if result is None:
            return False, result
        else:
            return True, result

    def isExistV2(self, target_name: str, target_img_num: int = 0):
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
        screenshot_img = aircv.imread(self.screenshot_img_file)
        target_img_name_file = self.ld.target_path + target_img_name
        target_img = aircv.imread(target_img_name_file)
        result = aircv.find_template(screenshot_img, target_img, rgb=rgb, threshold=threshold)
        if result is None:
            return False, result
        else:
            return True, result

    def LdactionTapV2(self, target_img_name_list: list, tap_result_check_img_name: str = None, rgb: bool = False,
                      threshold: float = 0.9, need_screenShot: bool = True, moveX: int = 0, moveY: int = 0,
                      tap_times: int = 1, tap_interval: float = 0, before_tap_wait_time: float = 0,
                      after_tap_wait_time: float = 1, search_again_times: int = 1, search_again_sleep_time: float = 0.5,
                      tap_result_check: bool = False, beginning_content: str = None, end_content: str = None,
                      error_content: str = '请检查界面！'):
        """
        【查找对应按钮】
        :param target_img_name_list: list: 目标图片名称列表
        :param tap_result_check_img_name: 点击结果检查的目标图片
        :param rgb: 比对rgb通道开关
        :param threshold: 模糊匹配阀值
        :param need_screenShot: 是否需要截图
        :param moveX: 偏移X轴量
        :param moveY: 偏移Y轴量
        :param tap_times: 连续点击次数
        :param tap_interval: 点击间隔时间
        :param before_tap_wait_time 点击前等待时间
        :param after_tap_wait_time 点击后等待时间
        :param search_again_times 重新查找次数
        :param search_again_sleep_time 重新查找间隔休眠时长
        :param tap_result_check: 点击结果检查开关
        :param beginning_content: 开始文本
        :param end_content: 结束文本
        :param error_content: 异常打印信息
        """
        if beginning_content is None:
            print('\n+++++START+++++   %s  ' % running_script)
        else:
            print('\n+++++START+++++ %s  %s' % (beginning_content, running_script))
        if before_tap_wait_time != 0:
            # print('等待 %s 秒后继续' % before_tap_wait_time)
            before_tap_wait_time = int(before_tap_wait_time * 2)
            for s in range(before_tap_wait_time):
                time.sleep(0.5)
                print(".", end="")
                if s == before_tap_wait_time - 1:
                    print("", end="\n")
        if need_screenShot:
            for target_img_name in target_img_name_list:
                find_result = self.find_target_imgV2(target_img_name, rgb, threshold, moveX, moveY,
                                                     search_again_sleep_time, search_again_times, after_tap_wait_time,
                                                     tap_times, tap_interval)
                if find_result[0]:
                    if tap_result_check and tap_result_check_img_name is not None:
                        self.ld.ScreenShot_Ld(self.index)
                        tap_result = self.isExist(tap_result_check_img_name, rgb, threshold)
                        if tap_result[0]:
                            break
                        else:
                            print('点击后结果校验不通过，重新点击！')
                            find_result = self.find_target_imgV2(target_img_name, rgb, threshold, moveX, moveY,
                                                                 search_again_sleep_time, search_again_times,
                                                                 after_tap_wait_time, tap_times, tap_interval)
                    else:
                        break
            if find_result[0] is False:
                print(error_content)
                sys.exit()
        else:
            for target_img_name in target_img_name_list:
                find_result = self.isExist(target_img_name, rgb, threshold)
                if find_result[0]:
                    if tap_result_check and tap_result_check_img_name is not None:
                        self.ld.ScreenShot_Ld(self.index)
                        tap_result = self.isExist(tap_result_check_img_name, rgb, threshold)
                        if tap_result[0]:
                            break
                        else:
                            print('点击后结果校验不通过，重新点击！')
                            find_result = self.find_target_imgV2(target_img_name, rgb, threshold, moveX, moveY,
                                                                 search_again_sleep_time, search_again_times,
                                                                 after_tap_wait_time, tap_times, tap_interval)
                    else:
                        break
            if find_result[0] is False:
                print('未能找到需要的 %s 按钮！' % target_img_name)
                sys.exit()
            result = find_result[1]
            x = result['result'][0] - moveX
            y = result['result'][1] - moveY
            for t in range(tap_times):
                tap = t + 1
                print('找到按钮: %s [%d , %d]' % (target_img_name, x, y))
                tap_interval = int(tap_interval * 2)
                for s in range(tap_interval):
                    time.sleep(0.5)
                    print(".", end="")
                    if s == tap_interval - 1:
                        print("", end="\n")
                self.ld.inputTap(Console_Action.index, x, y)
                print('已点击 %s %d次' % (target_img_name, tap), end="")
            after_tap_wait_time = int(after_tap_wait_time * 2)
            for s in range(after_tap_wait_time):
                time.sleep(0.5)
                print(".", end="")
                if s == after_tap_wait_time - 1:
                    print("", end="\n")
        chuji_time = time.time() - star_time
        chuji_time = time.strftime("%H:%M:%S", time.gmtime(chuji_time))
        if end_content is None:
            print('+++++END+++++  %s' % chuji_time)
        else:
            print('+++++END+++++  %s  %s' % (end_content, chuji_time))

    def find_target_imgV2(self, target_img_name, rgb, threshold, moveX, moveY,
                          search_again_sleep_time, search_again_times, after_tap_wait_time, tap_times, tap_interval):
        """
        【改进后的目标图片搜索方法】
        :param target_img_name: 目标图片名称
        :param rgb: 比对rgb通道开关
        :param threshold: 模糊匹配阀值
        :param moveX: 偏移X轴量
        :param moveY: 偏移Y轴量
        :param search_again_sleep_time: 重新查找间隔休眠时长
        :param search_again_times: 重新查找次数
        :param after_tap_wait_time: 点击后等待时间
        :param tap_times: 连续点击次数
        :param tap_interval: 点击间隔时间
        :return:
        """
        for search in range(search_again_times):
            self.ld.ScreenShot_Ld(self.index)
            result = self.isExist(target_img_name, rgb, threshold)
            find_result = result[1]
            if find_result is None and search_again_times == 1:
                print('未能找到需要的 %s 按钮！' % target_img_name)
            elif find_result is None and search_again_times > 1:
                print('未能找到需要的 %s 按钮！' % target_img_name, end="")
                search_times = 1
                search_times += search
                search_again_sleep_time_double = int(search_again_sleep_time * 2)
                for s in range(search_again_sleep_time_double):
                    time.sleep(0.5)
                    print(".", end="")
                    if s == search_again_sleep_time_double - 1:
                        print("", end="\n")
                print('重新搜索 %s 按钮 %d 次' % (target_img_name, search_times))
                if search_times == search_again_times:
                    print('未能找到需要的 %s 按钮！' % target_img_name)
            else:
                x = find_result['result'][0] - moveX
                y = find_result['result'][1] - moveY
                for t in range(tap_times):
                    tap = t + 1
                    print('找到按钮: %s [%d , %d]  ' % (target_img_name, x, y))
                    tap_interval = int(tap_interval * 2)
                    for s in range(tap_interval):
                        time.sleep(0.5)
                        print(".", end="")
                        if s == tap_interval - 1:
                            print("", end="\n")
                    self.ld.inputTap(Console_Action.index, x, y)
                    print('已点击 %s %d次' % (target_img_name, tap), end="")
                after_tap_wait_time = int(after_tap_wait_time * 2)
                for s in range(after_tap_wait_time):
                    time.sleep(0.5)
                    print(".", end="")
                    if s == after_tap_wait_time - 1:
                        print("", end="\n")
                break
        return result

    def find_target_imgV3(self, target_yaml: dict, target_name: str, need_screenShot: bool):
        """
        【改进后的目标图片搜索方法】
        :param need_screenShot:
        :param target_name:
        :param target_yaml:
        :return:
        """
        target_img_name_list = target_yaml['target_img_name_list']
        moveX = target_yaml['moveX']
        moveY = target_yaml['moveY']
        tap_times = target_yaml['tap_times']
        tap_interval = target_yaml['tap_interval']
        search_again_times = target_yaml['search_again_times']
        search_again_sleep_time = target_yaml['search_again_sleep_time']
        for target_img_name in target_img_name_list:
            for search in range(search_again_times):
                if need_screenShot:
                    self.ld.ScreenShot_Ld(self.index)
                result = self.isExistV2(target_name, target_img_name_list.index(target_img_name))
                find_result = result[1]
                if find_result is None and need_screenShot is False:
                    print('未能找到需要的 %s 按钮！' % target_img_name)
                    break
                elif find_result is None and search_again_times == 1:
                    print('未能找到需要的 %s 按钮！' % target_img_name)
                elif find_result is None and search_again_times > 1:
                    print('未能找到需要的 %s 按钮！' % target_img_name, end="")
                    search_times = 1
                    search_times += search
                    search_again_sleep_time_double = int(search_again_sleep_time * 2)
                    for s in range(search_again_sleep_time_double):
                        time.sleep(0.5)
                        print(".", end="")
                        if s == search_again_sleep_time_double - 1:
                            print("", end="\n")
                    print('重新搜索 %s 按钮 %d 次' % (target_img_name, search_times))
                    if search_times == search_again_times:
                        print('未能找到需要的 %s 按钮！' % target_img_name)
                else:
                    x = find_result['result'][0] - moveX
                    y = find_result['result'][1] - moveY
                    for t in range(tap_times):
                        tap = t + 1
                        print('找到按钮: %s [%d , %d]  ' % (target_img_name, x, y))
                        tap_interval = int(tap_interval * 2)
                        for s in range(tap_interval):
                            time.sleep(0.5)
                            print(".", end="")
                            if s == tap_interval - 1:
                                print("", end="\n")
                        self.ld.inputTap(Console_Action.index, x, y)
                        print('已点击 %s %d次' % (target_img_name, tap), end="")
                    break
            if result[0]:
                break
        return result

    def LdactionTapV3(self, target_name: str, tap_result_check_name: str = None, need_screenShot: bool = True):
        """
        【查找对应按钮】
        :param need_screenShot:
        :param tap_result_check_name: 点击事件结果校验的按钮target
        :param target_name: 点击事件查询的按钮target
        """
        target_yaml = target_yaml_data[target_name]
        before_tap_wait_time = target_yaml['before_tap_wait_time']
        after_tap_wait_time = target_yaml['after_tap_wait_time']
        tap_result_check = target_yaml['tap_result_check']
        beginning_content = target_yaml['beginning_content']
        end_content = target_yaml['end_content']
        error_content = target_yaml['error_content']

        if beginning_content is None:
            print('\n+++++START+++++   %s  ' % running_script)
        else:
            print('\n+++++START+++++ %s  %s' % (beginning_content, running_script))
        if before_tap_wait_time != 0:
            # print('等待 %s 秒后继续' % before_tap_wait_time)
            before_tap_wait_time = int(before_tap_wait_time * 2)
            for s in range(before_tap_wait_time):
                time.sleep(0.5)
                print(".", end="")
                if s == before_tap_wait_time - 1:
                    print("", end="\n")
        find_result = self.find_target_imgV3(target_yaml, target_name, need_screenShot)
        after_tap_wait_time = int(after_tap_wait_time * 2)
        for s in range(after_tap_wait_time):
            time.sleep(0.5)
            print(".", end="")
            if s == after_tap_wait_time - 1:
                print("", end="\n")
        if find_result[0]:
            if tap_result_check and tap_result_check_name is not None:
                self.ld.ScreenShot_Ld(self.index)
                tap_result = self.isExistV2(tap_result_check_name)
                if tap_result[0] is False:
                    print('点击后结果校验不通过，重新点击！')
                    self.find_target_imgV3(target_yaml, target_name)
        else:
            print(error_content)
            sys.exit()
        running_time = time.time() - star_time
        running_time = time.strftime("%H:%M:%S", time.gmtime(running_time))
        if end_content is None:
            print('+++++END+++++  %s' % running_time)
        else:
            print('+++++END+++++  %s  %s' % (end_content, running_time))

    def is_all_Exist(self, target_img_name: str, rgb: bool = False, threshold: float = 0.9):
        """
        【判断多个指定图片是否包含在截图中】
        :param self:
        :param rgb:
        :param threshold:
        :param target_img_name:
        :return: 图片查询结果和包含详情
        """
        screenshot_img = aircv.imread(self.screenshot_img_file)
        target_img_name_file = self.ld.target_path + target_img_name
        target_img = aircv.imread(target_img_name_file)
        result = aircv.find_all_template(screenshot_img, target_img, rgb=rgb, threshold=threshold)
        if result is None:
            return False, result
        else:
            return True, result

    def List_select(self, target_img_name: str, rgb: bool = True, threshold: float = 0.94):
        """
        【从人形列表选择人形】
        :param self:
        :param rgb:
        :param threshold:
        :param target_img_name:
        """
        list_result = self.is_all_Exist(target_img_name, rgb=rgb, threshold=threshold)[1]
        # print(list_result)
        # print(len(list_result))
        if list_result is not False:
            for result in list_result:
                coordinate = result['result']
                x = coordinate[0] - 100
                y = coordinate[1] + 200
                print('选中人形 X: %s  Y: %s' % (x, y))
                self.ld.inputTap(Console_Action.index, x, y)
                time.sleep(0.5)


def T_Dolls_retire(adv_retire: bool = False):
    """
    【人形回收】
    :param adv_retire:
    :return:
    """
    Console_Action.LdactionTapV2(['standing_by_T_Dolls.png'], beginning_content='选择角色回收', search_again_times=2)
    Console_Action.LdactionTapV2(['intelligent_selection.png'], end_content='点击智能选择')
    Console_Action.LdactionTapV2(['select_confirm.png'], end_content='选择确定')
    Console_Action.LdactionTapV2(['retire.png'], after_tap_wait_time=3, end_content='开始回收')
    if adv_retire:
        Console_Action.LdactionTapV2(['standing_by_T_Dolls.png'], beginning_content='选择角色回收')
        Console_Action.LdactionTapV2(['show_all.png'], before_tap_wait_time=1)
        Console_Action.LdactionTapV2(['legendary_III.png'], after_tap_wait_time=0.5)
        Console_Action.LdactionTapV2(['confirm.png'], need_screenShot=False, after_tap_wait_time=0.5)
        Console.screenShotnewLd(Console_Action.index)
        Console_Action.List_select('lv_III.png')
        Console_Action.LdactionTapV2(['select_confirm.png'], end_content='选择确定')
        Console_Action.LdactionTapV2(['retire.png'], after_tap_wait_time=2, end_content='开始回收')
        Console_Action.LdactionTapV2(['retire_confirm.png'])


def ep_13_4(debug_mode: bool = False):
    """
    【关卡13-4步骤】
    :return:
    """
    # 判断选择13章节
    Console.screenShotnewLd(Console_Action.index)
    if Console_Action.isExistV2('isep13')[0]:
        Console_Action.LdactionTapV3('13_4')
    else:
        Console_Action.LdactionTapV2(['ep13.png', 'isep13.png'], threshold=0.9, beginning_content='选择作战章节',
                                     end_content='已选择章节13', need_screenShot=False)
        Console_Action.LdactionTapV2(['13_4.png'], threshold=0.9, search_again_times=2, beginning_content='选择关卡',
                                     end_content='已选择关卡13-4')
    Console_Action.LdactionTapV2(['common_battle.png'], after_tap_wait_time=5, tap_interval=1,
                                 end_content='进入关卡战斗')

    # 进入关卡，兼容单位仓库已满
    Console.screenShotnewLd(Console_Action.index)
    if Console_Action.isExist('unit_recycle.png')[0]:
        print('\n+++++单位已满,请回收处理+++++')
        Console_Action.LdactionTapV2(['unit_recycle.png'], need_screenShot=False, after_tap_wait_time=2,
                                     beginning_content='准备回收单位')
        T_Dolls_retire(adv_retire=True)
        Console_Action.LdactionTapV2(['return.png'], after_tap_wait_time=2, search_again_times=2)
        return get_into_mission()
    else:
        Console_Action.LdactionTapV2(['zhb.png', 'zhb_bak.png'], threshold=0.6, after_tap_wait_time=1.5,
                                     beginning_content='....准备投放第一战队....')

    # 判断选择第一梯队，进入梯队编辑
    Console.screenShotnewLd(Console_Action.index)
    if Console_Action.isExist('isechelon1.png', rgb=True)[0]:
        Console_Action.LdactionTapV2(['echelon_editing.png'], need_screenShot=False, after_tap_wait_time=1.5,
                                     end_content='进入队伍编辑')
    else:
        Console_Action.LdactionTapV2(['echelon1.png', 'isechelon1.png'], after_tap_wait_time=1.5, need_screenShot=False)
        Console_Action.LdactionTapV2(['echelon_editing.png'], after_tap_wait_time=2, end_content='进入队伍编辑')

    Console_Action.LdactionTapV2(['victor.png'], moveY=100, tap_interval=2, before_tap_wait_time=2,
                                 after_tap_wait_time=2,
                                 end_content='选择维克托人形', search_again_times=2, search_again_sleep_time=0.5)

    # 筛选victor
    Console_Action.LdactionTapV2(['show_all.png'], after_tap_wait_time=0.5)
    Console_Action.LdactionTapV2(['legendary_v.png'], after_tap_wait_time=0.5)
    Console_Action.LdactionTapV2(['smg.png'], need_screenShot=False, after_tap_wait_time=0.5)
    Console_Action.LdactionTapV2(['at_max_lv.png'], need_screenShot=False, after_tap_wait_time=0.5)
    Console_Action.LdactionTapV2(['desc.png'], need_screenShot=False)
    Console_Action.LdactionTapV2(['confirm.png'], need_screenShot=False, after_tap_wait_time=0.5)
    Console_Action.LdactionTapV2(['victor_bak.png'], after_tap_wait_time=2)
    Console_Action.LdactionTapV2(['return.png'], 'start_fighting.png', moveX=20, after_tap_wait_time=3,
                                 search_again_times=2)

    # 投放换人后的第一梯队
    Console_Action.LdactionTapV2(['zhb.png', 'zhb_bak.png'], threshold=0.6, search_again_times=2,
                                 after_tap_wait_time=1.5,
                                 end_content='选中指挥部')
    Console.screenShotnewLd(Console_Action.index)
    if Console_Action.isExist('isechelon1.png', rgb=True)[0]:
        Console_Action.LdactionTapV2(['echelon_confirm.png'], need_screenShot=False, tap_interval=0.5,
                                     end_content='投放第一梯队')
    else:
        Console_Action.LdactionTapV2(['echelon1.png', 'isechelon1.png'], after_tap_wait_time=1.5, need_screenShot=False,
                                     end_content='选中第一梯队')
        Console_Action.LdactionTapV2(['echelon_confirm.png'], tap_interval=0.5, end_content='投放第一梯队')

    # 投放第二梯队
    Console_Action.LdactionTapV2(['13_4_fjc.png', '13_4_fjc_bak.png'], rgb=True, threshold=0.6, search_again_times=4,
                                 end_content='准备投放第二梯队', after_tap_wait_time=1.5)
    Console.screenShotnewLd(Console_Action.index)
    if Console_Action.isExist('isselect_echelon.png', rgb=True, threshold=0.98)[0]:
        if Console_Action.isExist('isechelon2.png')[0]:
            Console_Action.LdactionTapV2(['echelon_confirm.png'], after_tap_wait_time=2,
                                         beginning_content='已在梯队选择，默认第二梯队',
                                         end_content='投放第二梯队', need_screenShot=False)
        else:
            Console_Action.LdactionTapV2(['echelon2.png', 'isechelon2.png'], need_screenShot=False,
                                         beginning_content='已在梯队选择',
                                         end_content='选择第二梯队')
            Console_Action.LdactionTapV2(['echelon_confirm.png'], after_tap_wait_time=2, end_content='投放第二梯队')
    else:
        Console_Action.LdactionTapV2(['select_echelon.png'], need_screenShot=False, end_content='选择投放梯队')
        Console.screenShotnewLd(Console_Action.index)
        if Console_Action.isExist('isechelon2.png')[0]:
            Console_Action.LdactionTapV2(['echelon_confirm.png'], after_tap_wait_time=2,
                                         beginning_content='默认第二梯队',
                                         end_content='投放第二梯队', need_screenShot=False)
        else:
            Console_Action.LdactionTapV2(['echelon2.png', 'isechelon2.png'], need_screenShot=False,
                                         end_content='选择第二梯队')
            Console_Action.LdactionTapV2(['echelon_confirm.png'], after_tap_wait_time=2, end_content='投放第二梯队')

    # 开始战斗
    Console_Action.LdactionTapV2(['start_fighting.png'], tap_interval=1, after_tap_wait_time=1.5,
                                 end_content='开始作战')

    # 补给第二梯队
    Console_Action.LdactionTapV2(['echelon2_bak.png', 'echelon2_bak2.png'], 'supply.png', threshold=0.94, moveX=124,
                                 moveY=-41,
                                 tap_times=2, search_again_times=2, tap_interval=0.3, rgb=True)
    Console_Action.LdactionTapV3('supply')

    # 选择第一梯队，配置战斗计划
    Console_Action.LdactionTapV2(['echelon1_bak.png'], tap_interval=1, threshold=0.9, moveX=118, moveY=-39)
    Console_Action.LdactionTapV2(['planning_mode.png'], after_tap_wait_time=1, end_content='计划模式')
    Console_Action.LdactionTapV2(['17.png'], need_screenShot=False, threshold=0.7, after_tap_wait_time=0.5,
                                 search_again_times=2)
    Console_Action.LdactionTapV2(['18.png'], need_screenShot=False, threshold=0.6, after_tap_wait_time=0.5,
                                 search_again_times=2)
    Console_Action.LdactionTapV2(['19.png'], rgb=True, need_screenShot=False, threshold=0.7, after_tap_wait_time=0.5,
                                 search_again_times=2, moveX=51, moveY=-9)
    Console_Action.LdactionTapV2(['execution_plan.png'], beginning_content='开始执行计划战斗', tap_interval=0.5)

    # 等待战斗结束，并结算
    Console_Action.LdactionTapV2(['result_settlement.png'], search_again_times=20, search_again_sleep_time=8,
                                 tap_interval=1,
                                 before_tap_wait_time=110, after_tap_wait_time=6, beginning_content='等待战斗完毕结算')
    print('开始结算')
    for tap in range(3):
        Console.screenShotnewLd(Console_Action.index)
        if Console_Action.isExist('new_unit.png')[0]:
            Console_Action.LdactionTapV2(['new_unit.png'], moveX=-423, moveY=-521, after_tap_wait_time=6,
                                         beginning_content='检查是否有新单位获得', end_content='结算获得1个新单位',
                                         error_content='结算未获得新单位', need_screenShot=False)
            taps = tap + 1
            print('已获得%s个' % taps)
        elif Console_Action.isExist('result_settlement.png')[0]:
            Console_Action.LdactionTapV2(['result_settlement.png'], after_tap_wait_time=3.5, end_content='已完成关卡',
                                         need_screenShot=False)
        else:
            print("未搜索到获得新单位，结束结算")
            break


# def get_into_mission():
#     """
#     【准备进入关卡】
#     """
#     # 初始化到主界面操作
#     print('....准备当前界面分析....')
#     Dc.screenShotnewLd(Ld.index)
#     # 以兼容的界面判断
#     if Ld.isExistV2('main')[0]:
#         # 当前在主界面
#         # 进入战斗菜单
#         Ld.LdactionTapV3('main_battle', need_screenShot=False)
#         # 选择战斗类型
#         Dc.screenShotnewLd(Ld.index)
#         if Ld.isExistV2('iscombat_mission')[0] is False:
#             Ld.LdactionTapV3('combat_mission', need_screenShot=False)
#     elif Ld.isExistV2('battle')[0]:
#         # 当前在战斗界面
#         # 选择战斗类型
#         if Ld.isExistV2('iscombat_mission')[0] is False:
#             Ld.LdactionTapV3('combat_mission', need_screenShot=False)
#     elif Ld.isExist('research.png', threshold=0.9)[0]:
#         # 当前在研发界面
#         Ld.LdactionTapV3('return', need_screenShot=False)
#         # 进入战斗菜单
#         Ld.LdactionTapV3('main_battle')
#         # 选择战斗类型
#         Dc.screenShotnewLd(Ld.index)
#         if Ld.isExistV2('iscombat_mission')[0] is False:
#             Ld.LdactionTapV3('combat_mission', need_screenShot=False)
#     else:
#         print('....当前页面无法自动返回主界面请手动返回后重试！....')
#         sys.exit()

def get_into_mission():
    """
    【准备进入关卡】
    """
    # 初始化到主界面操作
    print('....准备当前界面分析....')
    Console.screenShotnewLd(Console_Action.index)
    # 以兼容的界面判断
    if Console_Action.isExistV2('main')[0]:
        # 当前在主界面
        # 进入战斗菜单
        Console_Action.LdactionTapV3('main_battle', need_screenShot=False)
        # 选择战斗类型
        Console.screenShotnewLd(Console_Action.index)
        if Console_Action.isExistV2('iscombat_mission')[0]:
            pass
        else:
            Console_Action.LdactionTapV3('combat_mission', need_screenShot=False)
    elif Console_Action.isExistV2('battle')[0]:
        # 当前在战斗界面
        # 选择战斗类型
        if Console_Action.isExistV2('iscombat_mission')[0]:
            pass
        else:
            Console_Action.LdactionTapV3('combat_mission', need_screenShot=False)
    elif Console_Action.isExist('research.png', threshold=0.9)[0]:
        # 当前在研发界面
        Console_Action.LdactionTapV3('return', need_screenShot=False)
        # 进入战斗菜单
        Console_Action.LdactionTapV3('main_battle')
        # 选择战斗类型
        Console.screenShotnewLd(Console_Action.index)
        if Console_Action.isExistV2('iscombat_mission')[0]:
            pass
        else:
            Console_Action.LdactionTapV3('combat_mission', need_screenShot=False)
    else:
        print('....当前页面无法自动返回主界面请手动返回后重试！....')
        sys.exit()

def test():
    """
    【调试测试类】
    :return:
    """

    Console_Action.LdactionTapV3('supply', 'echelon2_bak')
    sys.exit()


if __name__ == '__main__':
    Console = Dnconsole(r'C:\leidian\LDPlayer9')
    Console_Action = Ldaction(0, Console, 'screenshout_tmp.png')
    target_yaml_data = Console.YAML('target.yaml')
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
    # star_time = time.time()
    # running_script = '1'
    # test()

    # 载入关卡配置
    battle = '13_4.yaml'
    battle_yaml_data = Console.YAML(battle)

    # 正式运行
    runtimes = int(input("跑几圈:"))
    runtime = float(input("跑多久(分钟）:"))
    runtime_min = runtime * 60
    running_script = '共 %d 次，开始执行' % runtimes
    star_time = time.time()
    get_into_mission()
    ran_time: float = 0
    for is_runtimes in range(runtimes):
        is_runtimes_num = is_runtimes + 1
        running_script = '共 %d 次，正在执行第 %d 次' % (runtimes, is_runtimes_num)
        if ran_time <= runtime_min:
            ep_13_4()
            end_time = time.time()
            ran_time = end_time - star_time
            ran_time_m, ran_time_s = divmod(ran_time, 60)
            ran_time_h, ran_time_m = divmod(ran_time_m, 60)
            print('共 %d 次，已执行 %d 次, 已运行 %02d 时 %02d 分 %02d 秒' % (
                runtimes, is_runtimes_num, ran_time_h, ran_time_m, ran_time_s))
        else:
            break
