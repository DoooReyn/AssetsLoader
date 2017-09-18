# encoding=utf-8

import os, sys, json, types

DIR_ROOT = os.path.dirname(os.path.abspath(__file__))
DIR_RES  = os.path.join(DIR_ROOT, 'res/')
RES_SKIP = ['csb/UI', 'csb/Default', 'csb/Font', 'Map/Block', 'UI']
RES_JSON = os.path.join(DIR_ROOT, 'src/resource.json')
RES_DICT = {}
RES_SPEC = {'Map/MinMap': 'MinMap_'}
SORT_TYPE = {
    # "png"  : "image",
    "jpg"  : "Image",
    "fnt"  : "fnt",
    "plist": "animate",
    "tmx"  : "map",
    "pb"   : "proto",
    "mp3"  : "sound",
    "csb"  : "csb",
    "sheet": "texture",
    "json" : "jsonfont"
}

'''
调用资源处理方法
拆分方式：字体、图片、图集、地图、帧动画、Proto
'''
def callRes(filepath):
    if filepath[-7:] == 'pvr.ccz':
        return

    if filepath.find(' ') != -1:
        return

    for item in RES_SKIP:
        dirname = os.path.join(DIR_RES, item)
        if filepath.find(dirname) != -1:
            return
    
    prefix = ''
    if 'Map/MinMap' in filepath:
        prefix = 'MinMap_'

    base = os.path.basename(filepath)
    ext  = base.split('.')[1]
    path = filepath.replace(DIR_RES, '')
    sort = path.split('/')[0]

    if ext == 'plist' and sort.find('.plist') != -1:
        sort = ext = 'sheet'
    sort_type = SORT_TYPE.get(ext)

    if not sort_type:
        # print(ext, sort)
        return
    
    base = prefix + base
    RES_DICT[base] = {'path':path, 'type': sort_type}


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
写入资源文件
'''
def writeResJson():
    with open(RES_JSON, 'w') as f:
        f.write(json.dumps(RES_DICT, indent=4, ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    walk(DIR_RES, callRes)
    writeResJson()