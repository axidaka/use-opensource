# -*- coding:utf-8 -*-

# 该文件主要用于学习 scrapy 的函数

__author__ = 'zhqs'


def _pop_command_name(argv):
    """
    从程序参数弹出命令
    :param argv: 执行scrapy 传入的参数
    :return:
    """
    i = 0
    for arg in argv[1:]:
        if not arg.startswith('-'):
            del argv[i]
            return arg
        i += 1

def _import_file(filepath):
    """
    通过文件路径来导入模块
    :param filepath:
    :return:
    """
    import os, sys
    from importlib import import_module
    abspath = os.path.abspath(filepath)
    dirname, file = os.path.split(abspath)
    fname, fext = os.path.splitext(file)
    if fext != '.py':
        raise ValueError('Not a Python source file:%s'% abspath)
    try:
        module = import_module(fname)
    finally:
        if dirname:
            sys.path.pop(0)
    return module


def main():
    """
    函数测试
    :return:
    """
    argv = ['runspider', 'SpiderStackOverFlow.py', '-o', 'top-stackoverflow-questions.json']
    print 'argv type:', type(argv).__name__
    print _pop_command_name(argv)

    _import_file('learn-scrapy-function.py')


if __name__ == "__main__":
    main()