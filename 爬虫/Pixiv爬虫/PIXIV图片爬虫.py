import os
import requests
import re
import time

header = {'referer': 'https://www.pixiv.net/',
          'user-agent': '<user-agent>',
          'accept-language': 'zh-CN,zh;q=0.9',
          'cookie':'<cookie>'
          }
def GetResponse(url, parm=""):
    try:
        if parm == "":
            res = requests.get(url=url, headers=header, timeout=300)
        else:
            res = requests.get(url=url, headers=header, timeout=300, params=parm)
    except Exception as e:
        for i in range(30):
            time.sleep(3)
            print(url + "请求失败")
            try:
                if parm == "":
                    res = requests.get(url=url, headers=header, timeout=300)
                else:
                    res = requests.get(url=url, headers=header, timeout=300, params=parm)
            except Exception as e2:
                pass
            if res.elapsed.total_seconds() < 30:
                break
    return re

if __name__ == '__main__':
    Total_Start = time.time()
    word = input("Search for:")
    cnt = 1
    page = 1
    Maxpage = 20
    param = {
        'word': word,
        'order': 'date_d',
        'mode': 'r18',  # 有all和r18模式，不过感觉没用
        'p': 'page',
        's_mode': 's_tag',
        'type': 'illust_and_ugoira',
        'lang': 'zh',
        'version': '756be60366a5fe018a9a6dad3939c8a57e00ec57'
    }
    # 路径名
    DicPath = './Data/' + word
    if not os.path.exists(DicPath):
        os.makedirs(DicPath)
        print(DicPath + "创建成功")
    ex2 = "https://i.pximg.net/img-original/img/(.*?)_p0.jpg"
    ex = '{"id":"(.*?)",.*?}'
    while True:
        page = str(page)
        url = 'https://www.pixiv.net/ajax/search/artworks/' + word
        param['p'] = page
        print(param)
        page_start = time.time()
        print("正在下载第" + page + "页")
        page = int(page)
        # 通过正则表达式获得此页下所以ID
        Tempjson = GetResponse(url=url, parm=param).text
        if len(Tempjson) == 0 or page > Maxpage:
            break;
        page += 1
        # print(Tempjson)
        IdList = re.findall(ex, Tempjson, re.S)
        # 通过ID获得图片url
        PurlList = list()
        for ID in IdList:
            IDurl = 'https://www.pixiv.net/artworks/' + ID
            response = GetResponse(IDurl).text
            TempList = re.findall(ex2, response, re.S)
            for each in TempList:
                start_time = time.time()
                url_str = "https://i.pximg.net/img-original/img/" + each + "_p0.jpg"
                Picture = ""
                Picture = GetResponse(url_str).content
                no = str(cnt)
                PictureName = word + '_' + no + '.png'
                with open(DicPath + '/' + PictureName, 'wb') as fp:
                    fp.write(Picture)
                    end_time = time.time()
                    print(url_str + ": " + PictureName + "已获取，用时%s秒" % (end_time - start_time))
                    time.sleep(0.3)
                cnt += 1
        page_end = time.time()
        print("第" + str(page - 1) + "页用时%s秒" % (page_end - page_start))
    Total_End = time.time()
    print("共获取" + cnt + "张图片，用时%s秒" % (Total_End - Total_Start))
