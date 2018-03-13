import urllib
import time
import  guoxiaoyi.xiciProxies
import re
import csv

def nextpage(browser):#查找下一页
     time.sleep(1)
     nextpage=browser.find_elements_by_xpath('//*[@id="1"]/div/div[5]/p/span[7]')
     nextpage.click()
     return browser


page_no=0
header=('User-Agent',"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36")
IPfp=r'E:\GitHub\测试文件\IP_Pool.xls'
opener=urllib.request.build_opener()
opener.addheaders=[header]
ip=guoxiaoyi.xiciProxies.getPoxiesRand(IPfp)
proxy=urllib.request.ProxyHandler({"http":ip})#设立代理IP
opener=urllib.request.build_opener(proxy,urllib.request.HTTPHandler)#封装opener



name=[]
ID_no=[]
duty=[]
caseCode=[]
publishDate=[]

dicInput={'失信人名称': '', '证件号': '', '判决详情': '','文案号': '','发布时间': ''}

with open('E:\GitHub\测试文件\江西失信人名单.csv','a+',newline='') as csvfile:
     fieldnames=['失信人名称','证件号','判决详情','文案号','发布时间']
     writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
     writer.writeheader()




name_pat='"iname":"(.*?)"'
ID_pat='"cardNum":"(.*?)"'
duty_pat='"duty":"(.*?)"'
caseCode_pat='"caseCode":"(.*?)"'
publishDate_pat='"publishDate":"(.*?)"'

for page_no in range(0,10000):
     try:
          print(page_no*10)
          url='https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=6899&query=%E6%B1%9F%E8%A5%BF%E5%A4%B1%E4%BF%A1%E4%BA%BA%E6%9F%A5%E8%AF%A2%E7%B3%BB%E7%BB%9F&pn='+str(page_no*10)+'&rn=10&ie=utf-8&oe=utf-8&format=json'
          print("正在访问"+url)
          data=opener.open(url,timeout=1).read().decode('utf-8','ignore')
          name.append(re.compile(name_pat).findall(data))
          ID_no.append(re.compile(ID_pat).findall(data))
          duty.append(re.compile(duty_pat).findall(data))
          caseCode.append(re.compile(caseCode_pat).findall(data))
          publishDate.append(re.compile(publishDate_pat).findall(data))
          print("第"+str(page_no+1)+"页共有"+str(len(name[page_no]))+"数据")

          with open("E:\GitHub\测试文件\江西失信人名单.csv",'a+',newline='') as csvfile:
               fieldnames=['失信人名称','证件号','判决详情','文案号','发布时间']
               writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
               for i in range(0,len(name[page_no])):
                    dicInput['失信人名称']=name[page_no][i]
                    dicInput['证件号']=ID_no[page_no][i]
                    dicInput['判决详情']=duty[page_no][i]
                    dicInput['文案号']=caseCode[page_no][i]
                    dicInput['发布时间']=publishDate[page_no][i]
                    writer.writerow(dicInput)
          time.sleep(1)
     except Exception as e:
          print(e)
          ip=guoxiaoyi.xiciProxies.getPoxiesRand(IPfp)
          proxy=urllib.request.ProxyHandler({"http":ip})#设立代理IP
          print("正在更换代理...")
          continue
