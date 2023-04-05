# /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
【少前13-4自动刷图】
"""

# 打包命令pyinstaller main_V4.spec
import os
import sys
import time
from functools import partial

import aircv
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
        self.target_path = self.workspace_path + r'\target\1080p_dpi280\\'
        # 读取作战参数信息保存路径
        self.action_path = self.workspace_path + r'\script\\'
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
        scp_time = time.time() - start_time
        scp_time = time.strftime("%H:%M:%S", time.gmtime(scp_time))
        print("%s ==【O】==" % scp_time)
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

    def find_target_imgV4(self, target_name: str, tap_info: dict):
        """
        【改进后的目标图片搜索方法】
        :param tap_info:
        :param target_name:
        :return:
        """
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
                    self.ld.screenShotnewLd(self.index)
                result = self.isExistV2(target_name, target_img_name_list.index(target_img_name))
                find_result = result[1]
                running_time = time.time() - start_time
                running_time = time.strftime("%H:%M:%S", time.gmtime(running_time))
                if find_result is None and need_screenShot is False:
                    print('%s 未能找到需要的 %s 按钮！' % (running_time, target_img_name))
                    break
                elif find_result is None and search_again_times == 1:
                    print('%s 未能找到需要的 %s 按钮！' % (running_time, target_img_name))
                elif find_result is None and search_again_times > 1:
                    print('%s 未能找到需要的 %s 按钮！' % (running_time, target_img_name), end="")
                    search_times = 1
                    search_times += search
                    search_again_sleep_time_double = int(search_again_sleep_time * 2)
                    for s in range(search_again_sleep_time_double):
                        time.sleep(0.5)
                        print(".", end="")
                        if s == search_again_sleep_time_double - 1:
                            print("", end="\n")
                    print('%s 重新搜索 %s 按钮 %d 次' % (running_time, target_img_name, search_times))
                    if search_times == search_again_times:
                        print('%s 未能找到需要的 %s 按钮！' % (running_time, target_img_name))
                else:
                    x = find_result['result'][0] - moveX
                    y = find_result['result'][1] - moveY
                    for t in range(tap_times):
                        tap = t + 1
                        print('%s 找到按钮: %s [%d , %d]  ' % (running_time, target_img_name, x, y), end="")
                        tap_interval_time = int(tap_interval * 2)
                        for s in range(tap_interval_time):
                            time.sleep(0.5)
                            print(".", end="")
                            if s == tap_interval_time - 1:
                                print("", end="\n")
                        if tap_interval == 0:
                            print("", end="\n")
                        self.ld.inputTap(Ld.index, x, y)
                        running_time = time.time() - start_time
                        running_time = time.strftime("%H:%M:%S", time.gmtime(running_time))
                        print('%s 已点击 %s %d次' % (running_time, target_img_name, tap), end="")
                        if tap_times >= 1:
                            print("", end="\n")
                    break
            if result[0]:
                break
        return result

    def LdactionTapV4(self, target_name: str, tap_info: dict):
        """
        【查找对应按钮】
        :param tap_info:
        :param target_name: 点击事件查询的按钮target
        """
        running_time = time.time() - start_time
        running_time = time.strftime("%H:%M:%S", time.gmtime(running_time))
        tap_result_check_name = tap_info['tap_result_check_name']
        before_tap_wait_time = tap_info['before_tap_wait_time']
        after_tap_wait_time = tap_info['after_tap_wait_time']
        beginning_content = tap_info['beginning_content']
        end_content = tap_info['end_content']
        error_content = tap_info['error_content']
        print('%s +++++START+++++ [目标%s: %s %s]' % (running_time, target_name, beginning_content, running_script))
        if before_tap_wait_time != 0:
            running_time = time.time() - start_time
            running_time = time.strftime("%H:%M:%S", time.gmtime(running_time))
            print('%s ' % running_time, end='', flush=True)
            do_before_tap_wait_time = int(before_tap_wait_time * 2)
            if do_before_tap_wait_time > 10:
                for s in range(do_before_tap_wait_time):
                    time.sleep(0.5)
                    s_10, d = divmod(s, 10)
                    d_10, dd = divmod(do_before_tap_wait_time, 10)
                    if d == 0:
                        print("o", end="")
                    elif s > do_before_tap_wait_time - dd:
                        print(".", end="")
                    if s == do_before_tap_wait_time - 1:
                        print("", end="\n")
            else:
                for s in range(do_before_tap_wait_time):
                    time.sleep(0.5)
                    print(".", end="")
                    if s == do_before_tap_wait_time - 1:
                        print("", end="\n")
        else:
            pass
        result = True
        while result:
            # 点击target
            find_result = self.find_target_imgV4(target_name, tap_info)
            # 判断点击方法处理结果
            if find_result[0]:
                # 处理点击后等待时间
                if after_tap_wait_time != 0:
                    running_time = time.time() - start_time
                    running_time = time.strftime("%H:%M:%S", time.gmtime(running_time))
                    print('%s ' % running_time, end='')
                    do_after_tap_wait_time = int(after_tap_wait_time * 2)
                    for s in range(do_after_tap_wait_time):
                        time.sleep(0.5)
                        print(".", end="")
                        if s == do_after_tap_wait_time - 1:
                            print("", end="\n")
                else:
                    pass
                # 判断是否有校验对象
                if tap_result_check_name is not None:

                    is_not_Exist_result = True
                    # 当有校验对象后执行循环校验
                    while is_not_Exist_result:
                        # 校验前截图
                        self.ld.screenShotnewLd(self.index)
                        running_time = time.time() - start_time
                        running_time = time.strftime("%H:%M:%S", time.gmtime(running_time))
                        print('%s 开始校验 %s' % (running_time, tap_result_check_name))
                        # 执行校验
                        tap_result = self.isExistV2(tap_result_check_name)
                        # 判断校验结果，通过后结束校验
                        if tap_result[0]:
                            running_time = time.time() - start_time
                            running_time = time.strftime("%H:%M:%S", time.gmtime(running_time))
                            print('%s 校验通过' % running_time)
                            is_not_Exist_result = False
                            break
                        # 不通过重新点击target
                        else:
                            running_time = time.time() - start_time
                            running_time = time.strftime("%H:%M:%S", time.gmtime(running_time))
                            print('%s 点击后结果校验不通过，重新点击！' % running_time)
                            # 为了校验执行后重新点击target，需启动截图
                            need_screenShot_tap_info = tap_info.copy()
                            need_screenShot_tap_info.update({'need_screenShot': True})
                            find_result = self.find_target_imgV4(target_name, need_screenShot_tap_info)
                            # 判断重新点击target后的结果
                            if find_result[0]:
                                # 点击target成功后将会重新执行校验
                                print('重新点击 %s 成功' % target_name)
                                if after_tap_wait_time != 0:
                                    running_time = time.time() - start_time
                                    running_time = time.strftime("%H:%M:%S", time.gmtime(running_time))
                                    print('%s ' % running_time, end='')
                                    do_after_tap_wait_time = int(after_tap_wait_time * 2)
                                    for s in range(do_after_tap_wait_time):
                                        time.sleep(0.5)
                                        print(".", end="")
                                        if s == do_after_tap_wait_time - 1:
                                            print("", end="\n")
                                else:
                                    pass
                            # 点击target失败也将重新执行校验
                            else:
                                print('当前界面未能找到 %s ，需重新校验 %s' % (target_name, tap_result_check_name))
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
                win32api.MessageBox(0, "自动执行异常请检查！", "提醒", win32con.MB_OK)
                result_action = input('是否已调整好?enter后再次重试/输入0跳过此步骤: ')
                if result_action == '0':
                    break
                else:
                    tap_info.update({'need_screenShot': True})
        running_time = time.time() - start_time
        running_time = time.strftime("%H:%M:%S", time.gmtime(running_time))
        print('%s +++++ END +++++ [%s]\n' % (running_time, end_content))

    def is_all_ExistV2(self, target_name: str):
        """
        【判断多个指定图片是否包含在截图中】
        :param target_name:
        :return: 图片查询结果和包含详情
        """
        target_yaml = target_yaml_data[target_name]
        target_img_name = target_yaml['target_img_name_list'][0]
        rgb = target_yaml['rgb']
        threshold = target_yaml['threshold']
        screenshot_img = aircv.imread(self.screenshot_img_file)
        target_img_name_file = self.ld.target_path + target_img_name
        target_img = aircv.imread(target_img_name_file)
        result = aircv.find_all_template(screenshot_img, target_img, rgb=rgb, threshold=threshold)
        if result is None:
            return False, result
        else:
            return True, result

    def List_selectV2(self, target_name: str):
        """
        【从人形列表选择人形】
        :param self:
        :param target_name:
        """
        list_result = self.is_all_ExistV2(target_name)[1]
        # print(list_result)
        # print(len(list_result))
        if list_result is not False:
            for result in list_result:
                coordinate = result['result']
                x = coordinate[0] - 100
                y = coordinate[1] + 200
                print('选中人形 X: %s  Y: %s' % (x, y))
                self.ld.inputTap(Ld.index, x, y)
                time.sleep(0.5)


def tap_dict(data_dict: dict):
    """

    :param data_dict:
    """
    # print("dict:")
    for i in data_dict:
        if 'get' in i:
            get_def = data_dict[i]
            def_info_dict(i)
            drive_yaml(get_def)
            continue


def screenShot_dict(data_dict: dict):
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
            running_time = time.time() - start_time
            running_time = time.strftime("%H:%M:%S", time.gmtime(running_time))
            print("%s 截图查询[ %s ]元素不存在！" % (running_time, data_dict.keys()))
            if isExist_target_value == 'exit':
                return True
                # sys.exit()
            elif isExist_target_value == 'break':
                break
            else:
                running_time = time.time() - start_time
                running_time = time.strftime("%H:%M:%S", time.gmtime(running_time))
                print("%s 执行else方法" % running_time)
                tap_list(isExist_target_value)
        elif Ld.isExistV2(isExist_target_key)[0]:
            running_time = time.time() - start_time
            running_time = time.strftime("%H:%M:%S", time.gmtime(running_time))
            print("%s 包含: %s" % (running_time, isExist_target_key))
            # print(isExist_target_key, isExist_target_value)
            isExist_target_key_result = True
            run_yaml = isExist_target_value
            break
    if isExist_target_key_result:
        # 截图对象查询到后，判断后续处理对象还是
        if type(run_yaml) == dict:
            screenShot_dict(run_yaml)
        else:
            if drive_yaml(run_yaml):
                return True


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


def def_info_dict(data_dict: dict):
    """

    :param data_dict:
    :return:
    """
    fun: bool = True
    adv_retire: bool = True
    def_info: dict = {}
    def_info.update(data_dict)
    return def_info


def tap_list(data_target_list: list, data_info: dict = None):
    """

    :param data_info:
    :param data_target_list:
    """
    # print("list:")
    for data_target in data_target_list:
        for target in data_target:
            # 是否截图判断target存在
            if target == 'screenShot':
                if data_target[target] is None:
                    Dc.screenShotnewLd(Ld.index)
                    break
                else:
                    Dc.screenShotnewLd(Ld.index)
                    screenShot_dict_info = data_target[target]
                    # print('%s: %s' % (key, isExist_target[key]))
                    if screenShot_dict(screenShot_dict_info):
                        return True
            # 是否是驱动方法
            elif 'get_' in target:
                get_def_info = data_target[target]
                def_info = def_info_dict(get_def_info)
                get_def_yaml = battle_yaml_data[target]
                if drive_yaml(get_def_yaml, def_info):
                    return True
            elif 'round_' in target:
                round_times = data_target[target]
                round_def_yaml = battle_yaml_data[target]
                for i in range(round_times):
                    drive_yaml(round_def_yaml)
            elif target == 'adv_retire':
                if data_info['adv_retire']:
                    tap_list(data_target[target])
            elif target == 'sleep':
                sleep_time = data_target[target]
                if sleep_time != 0:
                    running_time = time.time() - start_time
                    running_time = time.strftime("%H:%M:%S", time.gmtime(running_time))
                    print('%s ' % running_time, end='')
                    # print('等待 %s 秒后继续' % sleep_time)
                    sleep_time = int(sleep_time * 2)
                    for s in range(sleep_time):
                        time.sleep(0.5)
                        print(".", end="")
                        if s == sleep_time - 1:
                            print("", end="\n")
            else:
                if data_target[target] == 'list':
                    Ld.List_selectV2(target)
                else:
                    tap_info = tap_info_dict(target, data_target[target])
                    # if Ld.LdactionTapV4(target, tap_info):
                    #     return True
                    Ld.LdactionTapV4(target, tap_info)


def drive_yaml(data, data_info: dict = {}, fun_return: bool = False):
    """

    :param fun_return:
    :param data_info:
    :param data:
    """
    if type(data) == dict:
        tap_dict(data)
    elif type(data) == list:
        if tap_list(data, data_info):
            return True
        if 'fun_return' in data_info.keys():
            if data_info['fun_return']:
                return True
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
    if Ld.isExistV2('end_fighting'):
        print("True")
    sys.exit()


if __name__ == '__main__':
    Dc = Dnconsole(r'C:\leidian\LDPlayer9')
    Ld = Ldaction(0, Dc, 'screenshot_tmp.png')
    print(Dc.workspace_path)
    target_yaml_data = Dc.YAML('target.yaml')

    # 载入关卡配置
    battle = '13_4.yaml'
    battle_yaml_data = Dc.YAML(battle)

    get_into_mission = battle_yaml_data['get_into_mission']
    get_13_4 = battle_yaml_data['get_13_4']

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

    # 正式运行

    user_action = True
    while user_action:
        runtimes = int(input("跑几圈:"))
        runtime = float(input("跑多久(分钟）:"))
        runtime_min = runtime * 60
        running_script = '共 %d 次，开始执行' % runtimes
        start_time = time.time()
        if drive_yaml(get_into_mission):
            continue
        ran_time: float = 0
        for is_runtimes in range(runtimes):
            is_runtimes_num = is_runtimes + 1
            running_script = '共 %d 次，正在执行第 %d 次' % (runtimes, is_runtimes_num)
            if ran_time <= runtime_min:
                drive_yaml(get_13_4)
                end_time = time.time()
                ran_time = end_time - start_time
                ran_time_m, ran_time_s = divmod(ran_time, 60)
                ran_time_h, ran_time_m = divmod(ran_time_m, 60)
                print('共 %d 次，已执行 %d 次, 已运行 %02d 时 %02d 分 %02d 秒\n' % (
                    runtimes, is_runtimes_num, ran_time_h, ran_time_m, ran_time_s))
            else:
                break
        win32api.MessageBox(0, "是否继续跑步机?", "提醒", win32con.MB_OK | win32con.MB_TOPMOST)
        action = input('是否继续跑步机?enter后继续/输入exit退出: ')
        if action == 'exit':
            break
        else:
            pass
        # os.system('pause')  # 按任意键继续
