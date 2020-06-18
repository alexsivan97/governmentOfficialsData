import requests
from bs4 import BeautifulSoup
import bs4
import re
import traceback
import pandas
import json

#获得中央领导url列表函数、姓名
def getCentralOfficialsURL(oDictList,url):
    print("获得中央领导页面 URLS")
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()
        print(r.status_code)
        if r.encoding!=r.apparent_encoding:
            r.encoding = r.apparent_encoding
    except:
        print("获取"+url+"失败")

    try:
        count=0
        oDict = {'姓名': '', '性别': '', '民族': '', '出生年月': '', '现任职务': '', '籍贯': '', '党派': '', '学历': '', '参加工作时间': '','个人履历': '', '资料链接': '', '是否缺资料': ''}
        html=r.text
        soup = BeautifulSoup(html, "html.parser")
        #找到所有 含有url 和名字的p标签
        pat_tag = re.compile(r'<p><a href= ></p >')
        pas = pat_tag.findall(str(soup))
        for pa in pas:
            #print(pa)

            #获得url们
            pat_urlrs = re.compile(r'/n1/.*?.html')
            cUrlrs = pat_urlrs.search(str(pa))
            cUrl="http://cpc.people.com.cn" + cUrlrs.group(0)
            oDict['资料链接']=cUrl

            #获得名字
            pat_name = re.compile(r'_blank">.*?</a >')
            namestring=pat_name.search(str(pa))
            name = re.split('_blank">|</a >',namestring.group(0))[1]
            oDict['姓名']=name

            #添加到oDictList里面去
            oDictList.append(oDict.copy())#记住是Dict的copy因为oDict是传引用而不是传值 不加上.copy() 所以就会一直变成一一样的
            count+=1

        print("获得了"+str(count)+"个领导姓名和链接信息")

#原来的版本
        # for divptab in soup.find_all('div',attrs={'class':'p_tab'}):
        #     for p in divptab.find_all('p'):
        #         pat1 = re.compile(r'<a href=.*?</a >')
        #         atags = pat1.findall(str(p))
        #         #print(atags)
        #         #print(p)
        #         pat = re.compile(r'/n1/.*?.html')
        #         urlrs = pat.finditer(str(p))
        #         for u in urlrs:
        #             cUrl = "http://cpc.people.com.cn" + u.group(0)
        #             cUrlList.append(cUrl)
        #             oDict['资料链接']