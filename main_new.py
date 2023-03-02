# /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
【少前13-4自动刷图】
"""
import os
import sys
import time

import aircv


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
        # 构造完成
        print('Class-Dnconsole is ready.(%s)' % self.ins_path)

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

    def LdactionTap(self, target_img_name_first: str, target_img_name_second: str = None, rgb: bool = False,
                    need_screenShot: bool = True, threshold: float = 0.9, moveX: int = 0, moveY: int = 0,
                    tap_times: int = 1, wait_time: float = 0, sleep_time: float = 1, reload_times: int = 1,
                    reload_sleep_time: float = 0.5, beginning_content: str = None, end_content: str = None,
                    error_content: str = '请检查界面！', tap_result_check: bool = False):
        """
        【查找对应按钮】
        :param rgb: 比对rgb通道开关
        :param need_screenShot: 是否需要调用截图程序
        :param error_content: 异常打印信息
        :param tap_times: 连续点击次数
        :param end_content: 结束文本
        :param beginning_content: 开始文本
        :param reload_sleep_time: 重试间隔休眠时长
        :param threshold: 模糊匹配阀值
        :param reload_times: 重试次数
        :param wait_time:
        :param sleep_time: 固定休眠时长
        :param target_img_name_first: 匹配目标图片名称1
        :param target_img_name_second: 匹配目标图片名称2
        :param moveX: 偏移X轴量
        :param moveY: 偏移Y轴量
        :param tap_result_check: 点击结果检查开关
        """
        if beginning_content is None:
            print('\n+++++START+++++   %s' % running_script)
        else:
            print('\n+++++START+++++ %s  %s' % (beginning_content, running_script))
        if need_screenShot:
            if target_img_name_second is None:
                find_result_first = self.find_target_img(target_img_name_first, rgb, moveX, moveY, reload_sleep_time,
                                                         reload_times, wait_time, tap_times,
                                                         threshold)
                if find_result_first[0] is False:
                    sys.exit()
            else:
                find_result_first = self.find_target_img(target_img_name_first, rgb, moveX, moveY, reload_sleep_time,
                                                         reload_times, wait_time, tap_times,
                                                         threshold)
                if find_result_first[0] is False:
                    find_result_second = self.find_target_img(target_img_name_second, rgb, moveX, moveY,
                                                              reload_sleep_time, reload_times, wait_time, tap_times,
                                                              threshold)
                    if find_result_second[0] is False:
                        sys.exit()
        else:
            if target_img_name_second is None:
                find_result_first = self.isExist(target_img_name_first, rgb=rgb, threshold=threshold)[1]
                if find_result_first is None:
                    print('未能找到需要的 %s 按钮！' % target_img_name_first)
                    sys.exit()
                else:
                    x = find_result_first['result'][0] - moveX
                    y = find_result_first['result'][1] - moveY
                    for t in range(tap_times):
                        tap = t + 1
                        print('找到按钮: %s [%d , %d]' % (target_img_name_first, x, y))
                        time.sleep(wait_time)
                        self.ld.inputTap(Ld.index, x, y)
                        print('已点击 %s %d次' % (target_img_name_first, tap))
            else:
                find_result_first = self.isExist(target_img_name_first, rgb=rgb, threshold=threshold)[1]
                if find_result_first is None:
                    print('未能找到需要的 %s 按钮！' % target_img_name_first)
                    find_result_second = self.isExist(target_img_name_second, rgb=rgb, threshold=threshold)[1]
                    if find_result_second is None:
                        print('未能找到需要的 %s 按钮！' % target_img_name_second)
                        sys.exit()
                    else:
                        x = find_result_second['result'][0] - moveX
                        y = find_result_second['result'][1] - moveY
                        for t in range(tap_times):
                            tap = t + 1
                            print('找到按钮: %s [%d , %d]' % (target_img_name_second, x, y))
                            time.sleep(wait_time)
                            self.ld.inputTap(Ld.index, x, y)
                            print('已点击 %s %d次' % (target_img_name_second, tap))
                else:
                    x = find_result_first['result'][0] - moveX
                    y = find_result_first['result'][1] - moveY
                    for t in range(tap_times):
                        tap = t + 1
                        print('找到按钮: %s [%d , %d]' % (target_img_name_first, x, y))
                        time.sleep(wait_time)
                        self.ld.inputTap(Ld.index, x, y)
                        print('已点击 %s %d次' % (target_img_name_first, tap))
        time.sleep(sleep_time)
        if end_content is None:
            print('+++++END+++++')
        else:
            print('+++++END+++++ %s' % end_content)

    def LdactionTapV2(self, target_img_name_list: list, tap_result_check_img_name: str = None, rgb: bool = False,
                      threshold: float = 0.9, need_screenShot: bool = True, moveX: int = 0, moveY: int = 0,
                      tap_times: int = 1, tap_interval: float = 0, before_tap_wait_time: float = 0,
                      after_tap_wait_time: float = 1, search_again_times: int = 1, search_again_sleep_time: float = 0.5,
                      tap_result_check: bool = False, beginning_content: str = None, end_content: str = None,
                      error_content: str = '请检查界面！'):
        """
        【查找对应按钮】
        :param running_script:
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
            print('\n+++++START+++++   %s' % running_script)
        else:
            print('\n+++++START+++++ %s  %s' % (beginning_content, running_script))
        if before_tap_wait_time != 0:
            # print('等待 %s 秒后继续' % before_tap_wait_time)
            time.sleep(before_tap_wait_time)
        if need_screenShot:
            for target_img_name in target_img_name_list:
                find_result = self.find_target_imgV2(target_img_name, rgb, threshold, moveX, moveY,
                                                     search_again_sleep_time, search_again_times, after_tap_wait_time,
                                                     tap_times, tap_interval)
                if find_result[0]:
                    if tap_result_check and tap_result_check_img_name is not None:
                        self.ld.screenShotnewLd(self.index)
                        tap_result = self.isExist(tap_result_check_img_name, rgb, threshold)
                        if tap_result[0]:
                            break
                    else:
                        break
            if find_result[0] is False:
                print(error_content)
                sys.exit()
        else:
            for target_img_name in target_img_name_list:
                result = self.isExist(target_img_name, rgb, threshold)
                find_result = result[1]
                if result[0] is False:
                    print('未能找到需要的 %s 按钮！' % target_img_name)
                    sys.exit()
                else:
                    break
            x = find_result['result'][0] - moveX
            y = find_result['result'][1] - moveY
            time.sleep(before_tap_wait_time)
            for t in range(tap_times):
                tap = t + 1
                print('找到按钮: %s [%d , %d]' % (target_img_name, x, y))
                time.sleep(tap_interval)
                self.ld.inputTap(Ld.index, x, y)
                print('已点击 %s %d次' % (target_img_name, tap))
        time.sleep(after_tap_wait_time)
        if end_content is None:
            print('+++++END+++++')
        else:
            print('+++++END+++++ %s' % end_content)

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
            self.ld.screenShotnewLd(self.index)
            result = self.isExist(target_img_name, rgb, threshold)
            find_result = result[1]
            if find_result is None and search_again_times == 1:
                print('未能找到需要的 %s 按钮！' % target_img_name)
            elif find_result is None and search_again_times > 1:
                print('未能找到需要的 %s 按钮！' % target_img_name)
                search_times = 1
                search_times += search
                time.sleep(search_again_sleep_time)
                print('重新搜索 %s 按钮 %d 次' % (target_img_name, search_times))
                if search_times == search_again_times:
                    print('未能找到需要的 %s 按钮！' % target_img_name)
            else:
                break
        x = find_result['result'][0] - moveX
        y = find_result['result'][1] - moveY
        for t in range(tap_times):
            tap = t + 1
            print('找到按钮: %s [%d , %d]' % (target_img_name, x, y))
            time.sleep(tap_interval)
            self.ld.inputTap(Ld.index, x, y)
            print('已点击 %s %d次' % (target_img_name, tap))
        time.sleep(after_tap_wait_time)
        return result

    def find_target_img(self, target_img_name, rgb, moveX, moveY, reload_sleep_time, reload_times, wait_time, tap_times,
                        threshold):
        """
        【需要截图的模板图片搜索处理】
        :param moveX:
        :param moveY:
        :param reload_sleep_time:
        :param reload_times:
        :param rgb:
        :param tap_times:
        :param target_img_name:
        :param threshold:
        :param wait_time:
        :return:
        """

        for sleep in range(reload_times):
            self.ld.screenShotnewLd(self.index)
            result = self.isExist(target_img_name, rgb=rgb, threshold=threshold)
            find_result = result[1]
            if find_result is None and reload_times == 1:
                print('未能找到需要的 %s 按钮！' % target_img_name)
            elif find_result is None and reload_times > 1:
                print('未能找到需要的 %s 按钮！' % target_img_name)
                sleep_times = 1
                sleep_times += sleep
                time.sleep(reload_sleep_time)
                print('重新搜索 %s 按钮 %d 次' % (target_img_name, sleep_times))
                if sleep_times == reload_times:
                    print('未能找到需要的 %s 按钮！' % target_img_name)
            else:
                x = find_result['result'][0] - moveX
                y = find_result['result'][1] - moveY
                for t in range(tap_times):
                    tap = t + 1
                    print('找到按钮: %s [%d , %d]' % (target_img_name, x, y))
                    time.sleep(wait_time)
                    self.ld.inputTap(Ld.index, x, y)
                    print('已点击 %s %d次' % (target_img_name, tap))
                break
        return result

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
        for result in list_result:
            coordinate = result['result']
            x = coordinate[0] - 100
            y = coordinate[1] + 200
            print('选中人形 X: %s  Y: %s' % (x, y))
            self.ld.inputTap(Ld.index, x, y)
            time.sleep(0.5)


def T_Dolls_retire(adv_retire: bool = False):
    """
    【人形回收】
    :param adv_retire:
    :return:
    """
    Ld.LdactionTap('standing_by_T_Dolls.png', beginning_content='选择角色回收')
    Ld.LdactionTap('intelligent_selection.png', end_content='点击智能选择')
    Ld.LdactionTap('select_confirm.png', end_content='选择确定')
    Ld.LdactionTap('retire.png', end_content='开始回收', sleep_time=3)
    if adv_retire:
        Ld.LdactionTap('standing_by_T_Dolls.png', beginning_content='选择角色回收', sleep_time=1)
        Ld.LdactionTap('show_all.png', sleep_time=1, wait_time=1)
        Ld.LdactionTap('legendary_III.png', sleep_time=0.5)
        Ld.LdactionTap('confirm.png', need_screenShot=False, sleep_time=0.5)
        Ld.List_select('lv_III.png')
        Ld.LdactionTap('select_confirm.png', end_content='选择确定')
        Ld.LdactionTap('retire.png', end_content='开始回收', sleep_time=2)
        Ld.LdactionTap('retire_confirm.png')


def ep_13_4(debug_mode: bool = False):
    """
    【关卡13-4步骤】

    :return:
    """
    # 判断选择13章节
    Dc.screenShotnewLd(Ld.index)
    if Ld.isExist('isep13.png', threshold=0.9)[0]:
        Ld.LdactionTap('13_4.png', threshold=0.9, reload_times=2, beginning_content='选择关卡',
                       end_content='已选择关卡13-4')
    else:
        Ld.LdactionTap('ep13.png', 'isep13.png', threshold=0.9, beginning_content='选择作战章节',
                       end_content='已选择章节13')
        Ld.LdactionTap('13_4.png', threshold=0.9, reload_times=2, beginning_content='选择关卡',
                       end_content='已选择关卡13-4')
    Ld.LdactionTap('common_battle.png', sleep_time=5, wait_time=1, end_content='进入关卡战斗')

    Dc.screenShotnewLd(Ld.index)
    if Ld.isExist('unit_recycle.png')[0]:
        print('\n+++++单位已满,请回收处理+++++')
        Ld.LdactionTap('unit_recycle.png', need_screenShot=False, sleep_time=2, beginning_content='准备回收单位')
        T_Dolls_retire(adv_retire=True)
        Ld.LdactionTap('return.png', sleep_time=2, reload_times=2)
        return get_into_mission()
    else:
        Ld.LdactionTap('zhb.png', 'zhb_bak.png', threshold=0.6, beginning_content='....准备投放第一战队....')
    # 判断选择第一梯队，进入梯队编辑
    if Ld.isExist('isechelon1.png', rgb=True)[0]:
        Ld.LdactionTap('echelon_editing.png', need_screenShot=False, sleep_time=1.5, end_content='进入队伍编辑')
    else:
        Ld.LdactionTap('echelon1.png', 'isechelon1.png')
        Ld.LdactionTap('echelon_editing.png', need_screenShot=False, sleep_time=2, end_content='进入队伍编辑')

    Ld.LdactionTap('victor.png', moveY=100, wait_time=1.5, sleep_time=1.5, reload_times=5, end_content='选择维克托人形')

    Ld.LdactionTap('show_all.png', sleep_time=0.5)
    Ld.LdactionTap('legendary_v.png', sleep_time=0.5)
    Ld.LdactionTap('smg.png', need_screenShot=False, sleep_time=0.5)
    Ld.LdactionTap('at_max_lv.png', need_screenShot=False, sleep_time=0.5)
    Ld.LdactionTap('desc.png', need_screenShot=False)
    Ld.LdactionTap('confirm.png', need_screenShot=False, sleep_time=0.5)

    Ld.LdactionTap('victor_bak.png', sleep_time=2)
    Ld.LdactionTap('return.png', sleep_time=3, reload_times=2)
    Ld.LdactionTap('zhb.png', 'zhb_bak.png', threshold=0.6, reload_times=2)

    if Ld.isExist('isechelon1.png')[0]:
        Ld.LdactionTap('echelon_confirm.png')
    else:
        Ld.LdactionTap('echelon1.png', 'isechelon1.png', threshold=0.7)
        Ld.LdactionTap('echelon_confirm.png')
    Ld.LdactionTap('13_4_fjc.png', '13_4_fjc_bak.png', rgb=True, threshold=0.6, reload_times=4)

    if Ld.isExist('isselect_echelon.png', rgb=True)[0]:
        if Ld.isExist('isechelon2.png')[0]:
            Ld.LdactionTap('echelon_confirm.png', sleep_time=2)
        else:
            Ld.LdactionTap('echelon2.png', 'isechelon2.png')
            Ld.LdactionTap('echelon_confirm.png', sleep_time=2)
    else:
        Ld.LdactionTap('select_echelon.png')
        if Ld.isExist('isechelon2.png')[0]:
            Ld.LdactionTap('echelon_confirm.png', sleep_time=2)
        else:
            Ld.LdactionTap('echelon2.png', 'isechelon2.png')
            Ld.LdactionTap('echelon_confirm.png', sleep_time=2)

    Ld.LdactionTap('start_fighting.png', wait_time=0.5, sleep_time=1.5)
    Ld.LdactionTap('echelon2_bak.png', 'echelon2_bak2.png', threshold=0.95, moveX=124, moveY=-41, tap_times=2,
                   reload_times=2, wait_time=0.3)
    Ld.LdactionTap('supply.png', sleep_time=1.5)
    Ld.LdactionTap('echelon1_bak.png', wait_time=1, threshold=0.9, moveX=118, moveY=-39)
    Ld.LdactionTap('planning_mode.png', wait_time=1)
    Ld.LdactionTap('17.png', need_screenShot=False, threshold=0.7, sleep_time=0.5, reload_times=2)
    Ld.LdactionTap('18.png', need_screenShot=False, threshold=0.6, sleep_time=0.5, reload_times=2)
    Ld.LdactionTap('19.png', rgb=True, need_screenShot=False, threshold=0.7, sleep_time=0.5, reload_times=2,
                   moveX=51, moveY=-9)
    Ld.LdactionTap('execution_plan.png')
    # Ld.LdactionTap('result_settlement.png', sleep_time=5, wait_time=2, reload_times=80, reload_sleep_time=8)
    Ld.LdactionTapV2(['result_settlement.png'], search_again_times=20, search_again_sleep_time=8, tap_interval=1,
                     before_tap_wait_time=100, after_tap_wait_time=7)
    print('开始结算')
    for tap in range(3):
        taps = tap + 1
        Dc.screenShotnewLd(Ld.index)
        if Ld.isExist('new_unit.png')[0]:
            Ld.LdactionTapV2(['new_unit.png'], moveX=-423, moveY=-521, before_tap_wait_time=2, after_tap_wait_time=6,
                             beginning_content='检查是否有新单位获得', end_content='结算获得1个新单位',
                             error_content='结算未获得新单位', need_screenShot=False)
            print('已获得%s个' % taps)
            Dc.screenShotnewLd(Ld.index)
        elif Ld.isExist('result_settlement.png')[0]:
            Ld.LdactionTap('result_settlement.png', sleep_time=3, end_content='已完成关卡')
        else:
            break


def get_into_mission():
    """
    【准备进入关卡】
    """
    # 初始化到主界面操作
    print('....准备当前界面分析....')
    Dc.screenShotnewLd(Ld.index)
    # 以兼容的界面判断
    if Ld.isExist('main.png', threshold=0.8)[0]:
        # 当前在主界面
        print('当前在主界面')
        # 进入战斗菜单
        Ld.LdactionTapV2(['main_battle.png'], end_content='进入战斗界面')
        # 选择战斗类型
        Dc.screenShotnewLd(Ld.index)
        if Ld.isExist('iscombat_mission.png', rgb=True, threshold=0.95)[0]:
            print('已在作战任务')
        else:
            Ld.LdactionTapV2(['combat_mission.png'], beginning_content='开始选择作战任务')
        # ep_13_4()
    elif Ld.isExist('battle.png', threshold=0.9)[0]:
        # 当前在战斗界面
        print('当前在战斗界面')
        # 选择战斗类型
        Dc.screenShotnewLd(Ld.index)
        if Ld.isExist('iscombat_mission.png', rgb=True, threshold=0.95)[0]:
            print('已在作战任务')
        else:
            Ld.LdactionTapV2(['combat_mission.png'], beginning_content='开始选择作战任务')
        # ep_13_4()
    elif Ld.isExist('research.png', threshold=0.9)[0]:
        # 当前在研发界面
        # 返回主界面
        print('当前在研发界面')
        Ld.LdactionTapV2(['return.png'])
        print('返回主界面')
        # 进入战斗菜单
        Ld.LdactionTapV2(['main_battle.png'])
        print('进入战斗界面')
        # 选择战斗类型
        Dc.screenShotnewLd(Ld.index)
        if Ld.isExist('iscombat_mission.png', rgb=True, threshold=0.95)[0]:
            print('已在作战任务')
        else:
            Ld.LdactionTapV2(['combat_mission.png'], beginning_content='开始选择作战任务')
        # ep_13_4()
    else:
        print('....当前页面无法自动返回主界面请手动返回后重试！....')
        sys.exit()


if __name__ == '__main__':
    Dc = Dnconsole(r'C:\leidian\LDPlayer9')
    Ld = Ldaction(0, Dc, 'screenshout_tmp.png')

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
    # ep_13_4()
    runtimes = int(input("跑几圈:"))
    get_into_mission()
    for isruntimes in range(runtimes):
        isruntimes_num = isruntimes + 1
        running_script = '共 %d 次，正在执行第 %d 次' % (runtimes, isruntimes_num)
        ep_13_4(running_script)
        print('共 %d 次，已执行 %d 次' % (runtimes, isruntimes_num))
