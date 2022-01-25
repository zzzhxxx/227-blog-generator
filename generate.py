# coding:utf-8
from itertools import count
from operator import truediv
from tabnanny import check
import requests
import io  
import sys  
import os
import time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 
from bs4 import BeautifulSoup
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}
url_base="http://blog.nanabunnonijyuuni.com/s/n227/diary/blog/list?ima=2304&page="
url_base2="http://blog.nanabunnonijyuuni.com"
page=0
iml="http://blog.nanabunnonijyuuni.com"
toLink=[]
a=[]
title=[]
authors=[]
author_filename=[]
day=[]
des=[]
c=0
contents=[]
imagelink=[]
def get_info():
    url=url_base+str(page)+"&cd=blog"
    data=requests.get(url,headers=headers)
    bs=BeautifulSoup(data.text,"html.parser")
    blog_title=bs.find_all('div',class_="blog-list__title")
    blog_descripiton=bs.find_all('div',class_="blog-list__txt")
    blog_link=bs.find_all('div',class_="blog-list__more")
    for i in blog_descripiton:
        desc=i.find('p',class_="txt").text
        desc=desc.replace("\n","")
        desc=desc.replace("\ufeff","")
        des.insert(0,desc)
    for i in blog_title:
        dates=i.find('p',class_="date").text
        day.insert(0,dates.replace(".","-"))
        name=i.find('p',class_="title").text
        title.insert(0,name)
        author=i.find('p',class_="name").text
        authors.insert(0,author)
    for i in blog_link:
        l=i.find('a').get('href')
        toLink.insert(0,l)
def checkstatus():
    url=url_base+str(page)+"&cd=blog"
    data=requests.get(url,headers=headers)
    bs=BeautifulSoup(data.text,"html.parser")
    if_no_content=bs.find_all('p')
    if str(if_no_content[0]) == '<p style="padding:0 0 60px;">記事がありません。</p>' :
        return False
def getcontents(links):
    global c
    global a
    a=[]
    c=0
    url_contents=url_base2+links
    data=requests.get(url_contents,headers=headers)
    bs=BeautifulSoup(data.text,"html.parser")
    blog_name=bs.find('div',class_="blog_detail__date")
    nn=blog_name.find('p',class_="name").text
    dd=blog_name.find('p',class_="date").text
    dd=dd.replace(".","-")
    blog_contents=bs.find('div',class_="blog_detail__main")
    con=blog_contents.text
    a=blog_contents.find_all('img')
    global iml
    if len(a) > 0:
         os.mkdir(changefilename(nn)+"-"+dd)
    for j in range(len(a)):
        try:
            if 'src' in a[j].attrs:
                iml=url_base2 +a[j].get('src')
                print(iml)
                imagelink.insert(0,iml)
                c+=1
                the_image = requests.get(iml)
                with open(os.getcwd()+"/"+changefilename(nn)+"-"+dd+"/"+str(c)+".jpg", "wb+") as f:
                    f.write(the_image.content)
        except:
            pass
    return con.replace(" ","\n\n")
def changefilename(au):
    if au == '西條和':
        return "nagomi"
    if au == '涼花萌':
        return "moe"
    if au == '天城サリー':
        return "sally"
    if au == '河瀬詩':
        return "uta"
    if au == '白沢かなえ':
        return "kanae"
    if au == '宮瀬玲奈':
        return "reina"
get_info()
for i in range(len(title) ):
    # author_filename.insert(0,changefilename(authors[i]))
    getcontents(toLink[i])
    # os.mkdir(author_filename+"-"+day[i])
    # with open(author_filename+"-"+day[i]+".md","w",encoding='utf-8') as f:
    #     f.write("---\ntitle: "+title[i]+"\n"+"author: "+authors[i]+"\n"+"description: "+des[i]+"\n"+"avatar: https://cdn.jsdelivr.net/gh/zzzhxxx/227WiKi@master/docs/assets/photo/avatar/"+author_filename+".jpg"+"\n"+"date: "+'"'+day[i]+'"'+"\n---\n"+ getcontents(toLink[i]))

# while(checkstatus()):

#     page+=1

print("finish!")
