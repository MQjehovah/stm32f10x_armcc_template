# coding: UTF-8
"""
将项目描述文件解析为任务队列并执行
"""
import json
import glob
import os
import sys
import argparse
import time
from multiprocessing import Pool


class ArmccParser(object):
    '''
    gcc工具链项目文件解析
    '''
    VERSION = "1.0.0"
    NAME = ""
    AS = ""
    CC = ""
    LD = ""
    OBJCOPY = ""
    AR = ""
    Type = ""
    OutPath = ""
    IsCreateBin = False
    IsCreateHex = False
    IsCreateMap = False
    ASFlag = []
    CCFlag = []
    LDFlag = []
    LDFile = ""
    Includes = []
    LibPaths = []
    LibFiles = []
    SrcFiles = []

    def __init__(self, filename="project.json"):
        # jsonfile = filename if filename else "project.json"
        if not os.path.isfile(filename):
            print("未找到项目描述文件%s" % (filename))
            exit()
        else:
            data = json.load(open(filename, encoding='utf8'))
        if not data.get('version', "") == self.VERSION:
            print("项目描述文件版本不兼容")
            exit()
        # 项目名称
        self.NAME = data.get('name', "")
        # 工具链
        if data.get("toolchain", ""):
            path = data["toolchain"].get("path", "")
            prefix = data["toolchain"].get("prefix", "")
            self.AS = "%s%s%s" % (
                path, prefix, data["toolchain"]["as"]) if data["toolchain"].get("as", "") else ""
            self.CC = "%s%s%s" % (
                path, prefix, data["toolchain"]["cc"]) if data["toolchain"].get("cc", "") else ""
            self.LD = "%s%s%s" % (
                path, prefix, data["toolchain"]["ld"]) if data["toolchain"].get("ld", "") else ""
            self.OBJCOPY = "%s%s%s" % (
                path, prefix, data["toolchain"]["objcopy"]) if data["toolchain"].get("objcopy", "") else ""
            self.AR = "%s%s%s" % (
                path, prefix, data["toolchain"]["ar"]) if data["toolchain"].get("as", "") else ""
        # 编译参数
        if data.get("flag", ""):
            self.ASFlag = " ".join(data["flag"].get("as", []))
            self.CCFlag = " ".join(data["flag"].get("cc", []))
            self.LDFlag = " ".join(data["flag"].get("ld", []))

        # 输出设置
        if data.get("output", ""):
            self.Type = data['output'].get("type", "elf")
            self.OutPath = data['output'].get("path", "")
            self.IsCreateBin = data['output'].get("bin", False)
            self.IsCreateHex = data['output'].get("hex", False)
        # 头文件路径
        if data.get("include", []):
            self.Includes = " ".join(map(lambda x: "-I " + x, data['include']))
        # 源文件
        if data.get("src", []):
            for item in data['src']:
                self.SrcFiles.extend(glob.glob(item))
    def GetTargetFile(self, Ext):
        return self.OutPath + self.NAME + Ext

    def GetOutFile(self, infile):
        return self.OutPath + os.path.basename(infile).split(".")[0] + ".o"

    def CheckUpdate(self):
        pass

    def GetCompileCMD(self):
        pass

    def GetArCMD(self):
        return "@%s -r %s %s" % (project.AR, self.OutPath + "lib" + self.NAME + ".a", " ".join(
            glob.glob(self.OutPath + "*.o")))

    def GetLinkCMD(self):
        return "@%s %s %s -o %s" % (project.LD, " ".join(
            glob.glob(self.OutPath + "*.o")), self.LDFlag, project.GetTargetFile(".axf"))

    def GetCreateBinCMD(self):
        return "@%s --bin -o %s %s" % (project.OBJCOPY, project.GetTargetFile(".bin"), project.GetTargetFile(".axf"))

    def GetCreateHexCMD(self):
        return "@%s --i32combined -o %s %s" % (project.OBJCOPY, project.GetTargetFile(".hex"), project.GetTargetFile(".axf"))

    def GetCompileTasks(self):
        _taskList = []
        for infile in self.SrcFiles:
            outfile = self.GetOutFile(infile)
            if os.path.exists(outfile):  # 跳过没有变化文件
                if os.path.getmtime(outfile) > os.path.getmtime(infile):
                    continue
            if os.path.splitext(infile)[1] == ".c":
                _taskList.append("@%s -c %s -o %s %s %s" %
                                 (self.CC, infile, outfile, self.Includes, self.CCFlag))
            if os.path.splitext(infile)[1] == ".s":
                _taskList.append("@%s %s -o %s %s %s" %
                                 (self.AS, infile, outfile, self.Includes, self.ASFlag))
        return _taskList

class GccParser(object):
    '''
    gcc工具链项目文件解析
    '''
    VERSION = "1.0.0"
    NAME = ""
    AS = ""
    CC = ""
    LD = ""
    OBJCOPY = ""
    AR = ""
    Type = ""
    OutPath = ""
    IsCreateBin = False
    IsCreateHex = False
    IsCreateMap = False
    ASFlag = []
    CCFlag = []
    LDFlag = []
    LDFile = ""
    Includes = []
    LibPaths = []
    LibFiles = []
    SrcFiles = []

    def __init__(self, filename="project.json"):
        # jsonfile = filename if filename else "project.json"
        if not os.path.isfile(filename):
            print("未找到项目描述文件%s" % (filename))
            exit()
        else:
            data = json.load(open(filename, encoding='utf8'))
        if not data.get('version', "") == self.VERSION:
            print("项目描述文件版本不兼容")
            exit()
        # 项目名称
        self.NAME = data.get('name', "")
        # 工具链
        if data.get("toolchain", ""):
            path = data["toolchain"].get("path", "")
            prefix = data["toolchain"].get("prefix", "")
            self.AS = "%s%s%s" % (
                path, prefix, data["toolchain"]["as"]) if data["toolchain"].get("as", "") else ""
            self.CC = "%s%s%s" % (
                path, prefix, data["toolchain"]["cc"]) if data["toolchain"].get("cc", "") else ""
            self.LD = "%s%s%s" % (
                path, prefix, data["toolchain"]["ld"]) if data["toolchain"].get("ld", "") else ""
            self.OBJCOPY = "%s%s%s" % (
                path, prefix, data["toolchain"]["objcopy"]) if data["toolchain"].get("objcopy", "") else ""
            self.AR = "%s%s%s" % (
                path, prefix, data["toolchain"]["ar"]) if data["toolchain"].get("as", "") else ""
        # 编译参数
        if data.get("flag", ""):
            self.ASFlag = " ".join(data["flag"].get("as", []))
            self.CCFlag = " ".join(data["flag"].get("cc", []))
            self.LDFlag = " ".join(data["flag"].get("ld", []))
        # 单独配置的一些参数
        if data.get('ldfile', ""):
            if not "-T" in self.LDFlag:
                self.LDFlag += " -T%s" % (data['ldfile'])
            else:  # 如果重复定义-T参数的做法
                print('ERROR:  already define -T in LDFlag')
        if data.get('lib', ""):
            if data['lib'].get('path', ""):
                self.LDFlag += " %s" % (" ".join(map(lambda x: "-L" +
                                                     x, data['lib']['path'])))
            if data['lib'].get('file', ""):
                self.LDFlag += " %s" % (" ".join(map(lambda x: "-l" +
                                                     x, data['lib']['file'])))
        self.LDFile = data.get('ldfile', "")
        # 输出设置
        if data.get("output", ""):
            self.Type = data['output'].get("type", "elf")
            self.OutPath = data['output'].get("path", "")
            self.IsCreateBin = data['output'].get("bin", False)
            self.IsCreateHex = data['output'].get("hex", False)
            self.IsCreateMap = data['output'].get("map", False)
        # 头文件路径
        if data.get("include", []):
            self.Includes = " ".join(map(lambda x: "-I " + x, data['include']))
        # 源文件
        if data.get("src", []):
            for item in data['src']:
                self.SrcFiles.extend(glob.glob(item))
    def GetTargetFile(self, Ext):
        return self.OutPath + self.NAME + Ext

    def GetOutFile(self, infile):
        return self.OutPath + os.path.basename(infile).split(".")[0] + ".o"

    def CheckUpdate(self):
        pass

    def GetCompileCMD(self):
        pass

    def GetArCMD(self):
        return "@%s -r %s %s" % (project.AR, self.OutPath + "lib" + self.NAME + ".a", " ".join(
            glob.glob(self.OutPath + "*.o")))

    def GetLinkCMD(self):
        return "@%s %s -o %s %s %s" % (project.LD, " ".join(
            glob.glob(self.OutPath + "*.o")), project.GetTargetFile(".elf"), self.LDFlag, "-Wl,-Map=" + self.GetTargetFile(".map") if self.IsCreateMap else "")

    def GetCreateBinCMD(self):
        return "@%s %s %s -Obinary" % (project.OBJCOPY, project.GetTargetFile(".elf"), project.GetTargetFile(".bin"))

    def GetCreateHexCMD(self):
        return "@%s %s %s -Oihex" % (project.OBJCOPY, project.GetTargetFile(".elf"), project.GetTargetFile(".hex"))

    def GetCompileTasks(self):
        _taskList = []
        for infile in self.SrcFiles:
            outfile = self.GetOutFile(infile)
            if os.path.exists(outfile):  # 跳过没有变化文件
                if os.path.getmtime(outfile) > os.path.getmtime(infile):
                    continue
            if os.path.splitext(infile)[1] == ".c":
                _taskList.append("@%s -c %s -o %s %s %s" %
                                 (self.CC, infile, outfile, self.Includes, self.CCFlag))
            if os.path.splitext(infile)[1] == ".s":
                _taskList.append("@%s -c %s -o %s %s %s" %
                                 (self.AS, infile, outfile, self.Includes, self.ASFlag))
        return _taskList

def excute_shell(cmd):
    """执行shell命令"""
    os.system(cmd)


if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", help="project file")
    parser.add_argument(
        "-c", "--clean", help="clean output file", action="store_true")
    parser.add_argument(
        "-d", "--download", help="download bin file", action="store_true")
    args = parser.parse_args()
    # 解析json文件
    if args.file:
        project = ArmccParser(args.file)
    else:
        project = ArmccParser()
    # clean指令
    if args.clean:
        for delfile in glob.glob(project.OutPath + "*.*"):
            os.remove(delfile)
        exit()
    # flash指令
    if args.download:
        os.system("%s/mqjlink -o 0x08000000 -d STM32F405RG -f %s" %
                  (sys.path[0], project.GetTargetFile(".bin")))
        exit()
    # make指令
    # 开始编译
    if not os.path.exists(project.OutPath):  # 检查输出目录
        os.makedirs(project.OutPath)
    start = time.clock()
    print("正在编译。。。")
    # 多线程并发
    pool = Pool()
    pool.map(excute_shell, project.GetCompileTasks())
    pool.close()
    pool.join()
    # 多线程并发
    # exit()
    # 链接
    if project.Type == "lib":  # 生成库
        os.system(project.GetArCMD())
    else:  # 连接
        os.system(project.GetLinkCMD())
        if project.IsCreateBin:
            os.system(project.GetCreateBinCMD())
        if project.IsCreateHex:
            os.system(project.GetCreateHexCMD())
    # 完成
    end = time.clock()
    print("编译完成，耗时%s" % (end - start))
    exit()
