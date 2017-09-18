# encoding=utf-8

import os, sys, json, types

DIR_ROOT = os.path.dirname(os.path.abspath(__file__))
DIR_SRC  = os.path.join(DIR_ROOT, 'src/app/')
SRC_JSON = os.path.join(DIR_ROOT, 'src/source.json')
SRC_DICT = {}

'''
搜索文件，交给回调处理
'''
def walk(rootdir, call):
    for root, dirs, files in os.walk(rootdir):
        for filename in files:
            if filename == '.DS_Store':
                continue
            filepath = os.path.join(root, filename)
            call(filepath)

'''
调用源码处理方法
拆分方式：配置、数据、管理器、UI、其他
'''
def callSrc(filepath):
    if filepath[-3:] != 'lua':
        return
    if filepath.find('MyApp.lua') != -1:
        return
    base  = os.path.basename(filepath).replace('.lua', '').replace('-', '_')
    sort  = filepath.replace(DIR_SRC, '').split('/')[0]
    SRC_DICT[base] = sort
    

'''
写入源码文件
'''
def writeSrcJson():
    with open(SRC_JSON, 'w') as f:
        f.write(json.dumps(SRC_DICT, indent=4, ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    walk(DIR_SRC, callSrc)
    writeSrcJson()
