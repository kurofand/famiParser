# -*- coding: utf-8 -*-

import requests
import json
from bs4 import BeautifulSoup

def getHTMLText(url):
	html=requests.get(url)
	data=html.text
	body=BeautifulSoup(data, 'lxml')
	return body

def getInfFromTable(body,shopOnPage=5):
	addr=[]
	tableTag=body.find('div', {'id':'DispListArticle'}).find('table', {'class':'cz_table01 cz_clear'}).find('tbody').findChildren('tr')
	for i in range(shopOnPage):
		row=tableTag[i].findChildren('td')
		ul=tableTag[i].find('ul', {'class': 'cz_terms_icon'})
		img=ul.findChildren('img')
		alt=[]
		for j in img:
			alt.append(j.get('alt', ''))
		shopType=row[0].find('img').get('alt', '')
		addr.append('\n'+shopType+row[0].text+'\n'+row[1].text)
		addr=addr+alt
	return addr

body=getHTMLText('http://as.chizumaru.com/famima/articleList?account=famima&accmd=0&c2=1&c1=1,2,3')
selectTag=body.find('select', {'name':'SelectListAdr1'})
prefecture_list=selectTag.findChildren('option')

for prefecture in prefecture_list:
	if (prefecture["value"]!="00"):#select all except first string
		prIndex=prefecture["value"]
		body=getHTMLText('http://as.chizumaru.com/famima/articleList?c1=1,2,3&template=Ctrl/DispListArticle_g12&pageLimit=10000&pageSize=5&account=famima&accmd=0&bpref=%s&c2=1'%prIndex)
		#get page count
		shopCount=int(body.find('div', {'id':'DispListArticle'}).find('div', {'class':'cz_counter'}).find('strong').text)
		if (shopCount%5==0):
			pageCount=shopCount/5
		else:
			pageCount=int(shopCount/5)+1
		addresses=[]
		addresses=addresses+getInfFromTable(body)
		#cose first page has alreary done start from second
		i=2
		while i<=pageCount:
			body=getHTMLText('http://as.chizumaru.com/famima/articleList?c1=1,2,3&template=Ctrl/DispListArticle_g12&pageLimit=10000&pageSize=5&account=famima&accmd=0&bpref=%s&c2=1&searchType=True&pg=%d'%(prIndex, i))
			if(i<pageCount):
				addresses=addresses+getInfFromTable(body)
			else:
				addresses=addresses+getInfFromTable(body, shopCount%5)
			i=i+1

		file=open('txt_files/'+prefecture.text+'.txt','w')
		for addr in addresses:
			file.write('%s\n'%addr.encode('utf-8'))
		file.close()
		print(prefecture.text+' done')
print('done')
