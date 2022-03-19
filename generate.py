# coding:utf-8
import requests
import io  
import sys  
import os
import time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 
from bs4 import BeautifulSoup
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}
url_base="http://blog.nanabunnonijyuuni.com/s/n227/diary/blog/list?page="
url_base2="http://blog.nanabunnonijyuuni.com"
base="!![](https://cdn.jsdelivr.net/gh/227WiKi/227WiKi-image@master/blog-image/"
page=96
count=2
same_date=False
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
cpn='' # allow the same date 
def get_info():
    global title
    global authors
    global day
    global toLink
    title=[]
    day=[]
    toLink=[]
    authors=[]
    url=url_base+str(page)
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
    global page
    url=url_base+str(page)
    data=requests.get(url,headers=headers)
    bs=BeautifulSoup(data.text,"html.parser")
    if_no_content=bs.find_all('p')
    if str(if_no_content[0]) == '<p style="padding:0 0 60px;">記事がありません。</p>' :
        return False
    else:
        return True
def getcontents(links):
    global c
    global a
    a=[]
    c=0
    global base
    url_contents=url_base2+links
    data=requests.get(url_contents,headers=headers)
    bs=BeautifulSoup(data.text,"html.parser")
    blog_name=bs.find('div',class_="blog_detail__date")
    nn=blog_name.find('p',attrs={'class':'name'}).text
    dd=blog_name.find('p',attrs={'class':'date'}).text
    dd=dd.replace(".","-")
    blog_contents=bs.find('div',class_="blog_detail__main")
    a=blog_contents.find_all('img')
    if(same_date):
        dir_name=changefilename(nn)+"-"+ dd + "-" + str(count-1)
    if(not(same_date)):
        dir_name=changefilename(nn)+"-"+ dd
    global iml
    con=blog_contents.text
    final_return=''
    for j in range(len(a)):
        try:
            if 'src' in a[j].attrs:
                iml=url_base2 +a[j].get('src')
                imagelink.insert(0,iml)
                c+=1
                the_image = requests.get(iml)
                final_return+=base+dir_name+"_"+str(c)+".jpg)"+"\n\n"
                # with open(os.getcwd()+"/images/"+dir_name+"_"+str(c)+".jpg", "wb+") as f:
                #     f.write(the_image.content)
        except:
            pass
    final_return+=con.replace("      ","\n")
    return final_return
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
    if au == '相川奈央':
        return "nao"
    if au == '麻丘真央':
        return "mao"
    if au == '椎名桜月':
        return "satsuki"
    if au == '雨夜音':
        return "oto"
    if au == '清井美那':
        return "mina"
    if au == '四条月':
        return "luna"
    if au == '月城咲舞':
        return "emma"
    if au == '望月りの':
        return "rino"
def get_pages():
    global page
    while(checkstatus()):
        page+=1
    page-=1
    return page
if __name__ == "__main__":
    # os.mkdir("images")
    get_pages()
    print(page)
    with open("history.txt","r",encoding='utf-8') as f:
        last_get_filename=f.read()
    get_info()
    for i in range(len(title)):
            # if z == 0:
        author_filename.append(changefilename(authors[i]))
        if(last_get_filename == author_filename[i]+"-"+day[i]+".md"):
            print("Don't need to update,exit the program!")
            sys.exit(0)

    if(last_get_filename == ''):
        print("No history record,do you want to patch all the blogs(Y/N):")
        if_patch=input()
        if(if_patch == 'Y' or if_patch =='y'):
            print("Start patch!")
            for z in range(page,-1,-1):
                print('Now page:',page)
                get_info()
                with open("current_page.txt","w",encoding='utf-8') as cp:
                    cp.write(str(page))
                for i in range(len(title)):
                    cpn=last_get_filename
                    author_filename.append(changefilename(authors[i]))
                    last_get_filename= author_filename[i]+"-"+day[i]
                    real_name=''
                    if(not(cpn == '') and cpn == last_get_filename):
                            real_name=last_get_filename + '-' + str(count) + ".md"
                            same_date=True
                            count+=1
                    if(cpn == '' or not(cpn == last_get_filename)):
                            real_name=last_get_filename + ".md"
                            count=2
                            same_date=False
                    with open(real_name,"w",encoding='utf-8') as f:
                        f.write("---\ntitle: "+title[i]+"\n"+"template: comment.html\n"+"author: "+authors[i]+"\n"+"description: "+des[i]+"\n"+"avatar: https://cdn.jsdelivr.net/gh/zzzhxxx/227WiKi@master/docs/assets/photo/avatar/"+author_filename[i]+".jpg"+"\n"+"date: "+'"'+day[i]+'"'+"\n"+"tags:\n  - "+authors[i]+"\n---\n\n"+getcontents(toLink[i]))
                    with open("history.txt","w",encoding='utf-8') as save:
                        save.write(last_get_filename)
                author_filename=[]
                page-=1
        if(if_patch == 'N' or if_patch == 'n'):
            print("Please tell me the page number you want to patch if you want to exit the program plase enter -1:")
            page=input()
            if(page=='-1'):
                sys.exit(0)
            print('Now page:'+page)
            get_info()
            for i in range(len(title)):
                # if z == 0:
                cpn=last_get_filename
                author_filename.append(changefilename(authors[i]))
                last_get_filename= author_filename[i]+"-"+day[i]
                real_name=''
                if(not(cpn == '') and cpn == last_get_filename):
                        real_name=last_get_filename + '-' + str(count) + ".md"        
                        count+=1               
                if(cpn == '' or not(cpn == last_get_filename)):
                        real_name=last_get_filename + ".md"
                        count=2
                with open(real_name,"w",encoding='utf-8') as f:
                    f.write("---\ntitle: "+title[i]+"\n"+"template: comment.html"+"author: "+authors[i]+"\n"+"description: "+des[i]+"\n"+"avatar: https://cdn.jsdelivr.net/gh/zzzhxxx/227WiKi@master/docs/assets/photo/avatar/"+author_filename[i]+".jpg"+"\n"+"date: "+'"'+day[i]+'"'+"\n"+"tags:\n  - "+authors[i]+"\n---\n\n"+getcontents(toLink[i]))
                with open("history.txt","w",encoding='utf-8') as save:
                    save.write(last_get_filename)
            print("finish")
            sys.exit(0)
    if(not(last_get_filename == '')):
        print("Detecting the latest record…")
        with open("current_page.txt",'r',encoding='utf-8') as cp:
            page=cp.read()
        for z in range(int(page),-1,-1):
            print('Current page:',page)
            get_info()
            with open("current_page.txt","w",encoding='utf-8') as cp:
                cp.write(str(page))
            for i in range(len(title)):
                # if z == 0:
                cpn=last_get_filename
                author_filename.append(changefilename(authors[i]))
                last_get_filename= author_filename[i]+"-"+day[i]
                real_name=''
                if(not(cpn == '') and cpn == last_get_filename):
                        real_name=last_get_filename + '-' + str(count) + ".md"
                        count+=1
                if(cpn == '' or not(cpn == last_get_filename)):
                        real_name=last_get_filename + ".md"
                        count=2
                with open(real_name,"w",encoding='utf-8') as f:
                    f.write("---\ntitle: "+title[i]+"\n"+"template: comment.html\n"+"author: "+authors[i]+"\n"+"description: "+des[i]+"\n"+"avatar: https://cdn.jsdelivr.net/gh/zzzhxxx/227WiKi@master/docs/assets/photo/avatar/"+author_filename[i]+".jpg"+"\n"+"date: "+'"'+day[i]+'"'+"\n"+"tags:\n  - "+authors[i]+"\n---\n\n"+getcontents(toLink[i]))
                with open("history.txt","w",encoding='utf-8') as save:
                    save.write(last_get_filename)
            author_filename=[]
            page-=1




    print("finish!The latest blog name:",last_get_filename)