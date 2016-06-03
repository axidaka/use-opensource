# -*- coding: utf-8 -*-
# flake8: noqa

import time
import os
import sys
reload(sys)
sys.setdefaultencoding('gbk')

import win32clipboard
import win32con

from  qiniu import Auth, put_file, etag, urlsafe_base64_decode
import qiniu.config
from qiniu import BucketManager

myselfres_dom = '![](http://7xst69.com1.z0.glb.clouddn.com/'

def setText(aString):
    """
    写字符串到粘贴板
    :param aString:
    :return:
    """
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_TEXT, aString)
    win32clipboard.CloseClipboard()

def upload_file(localfile):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'aRzVj18_VFA_p4EZ9z8ClWkVwYvAOWuoMStYnJhi'
    secret_key = 'bh_hBotfph77wcmHHIgCwExqKEvQN_eyT5m1r9_c'

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'myselfres'

    # 上传到七牛后保存的文件名

    key = time.strftime("%Y-%m-%d-%H-%M-%S.png", time.localtime())
    print key

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 要上传文件的本地路径

    ret, info = put_file(token, key, localfile)
    print (info)
    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)

    pngOnlinePath = myselfres_dom + key + ')'
    setText(pngOnlinePath)


if __name__ == "__main__":
    print "argv:", sys.argv
    if len(sys.argv) <= 1:
        print 'argv error'
    else:
        pngfile = sys.argv[1]
        print pngfile
        if os.path.exists(pngfile):
            upload_file(unicode(pngfile, 'gbk'))
    raw_input()


