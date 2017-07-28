# -*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup

url="http://as.chizumaru.com/famima/articleList?account=famima&accmd=0&c2=1&c1=1"
html=requests.get(url)
data=html.text

body=BeautifulSoup(data, "lxml")
selectTag=body.find('select', {'name':'SelectListAdr1'})
prefecture_list=selectTag.findChildren('option')

#-----just preparation for send request-----#
#param=""
#action="./articleList"
#targetId="DispListArticle"
#session=requests.Session();
#-------------------------------------------#

#-----preparation for scrape a table-----#
#tableTag=body.find('table',{'class':'cz_table01 cz_clear'})
#trTag_list=tableTag.findChildren('tr')
#
#----------------------------------------#

#http://as.chizamaru.com/famima/articleList?c1=1&template=Ctrl/DispListArticle_g12&pageLimit=10000&pageSize=5&account=famima&accmd=0&bpref=01&c2=1

for prefecture in prefecture_list:
	if (prefecture["value"]!="00"):#select all except first string
		print(prefecture.text)	
#		file=open('txt_files/'+prefecture.text+'.txt','w')
#		file.close()
#	print(prefecture.text)


#text file struct - name\n address\n latitude&longitude
