# -*- coding: utf-8 -*-
from googletrans import Translator
translator = Translator()
#translator('en', 'zh-TW', 'Hello World!')
from langdetect import detect
import json
# if you are using python 3, you should 
#import urllib.request 
import urllib2

import urllib

with open("queries.txt", 'r') as f:
    contents = f.read()

document_list_with_no=contents.splitlines()

outfn = 'translatedandall(output).txt'
outf = open(outfn, 'a+')

for x in document_list_with_no:
	z=x.split()
	qid=z[0]
	query1=z[1:]
	query=""
	for xyz in query1:
		query=query+xyz+" "
	query=query.replace(":","")
	query_of_3=[None] * 3 
	print("################")
	print(query)
	if(True):
		query_of_3[0]=(translator.translate(query, dest='en')).text
		query_of_3[1]=(translator.translate(query, dest='de')).text
		query_of_3[2]=(translator.translate(query, dest='ru')).text

	for y in query_of_3:
		print y
	query_of_3[0]= urllib.pathname2url(query_of_3[0])
	query_of_3[1]= urllib.pathname2url('u'+query_of_3[2].encode('utf8'))
	#u+appName.encode("utf-8")
	query_of_3[2]= urllib.pathname2url('u'+query_of_3[2].encode('utf8'))
	k=0
	for xquery in query_of_3:
		# change the url according to your own corename and query
		#xquery.replace(":", "\:")
		print(xquery)
		inurl = 'http://localhost:8983/solr/IRF19P2_1/select?q='+xquery+'&fl=id%2Cscore&wt=json&indent=true&rows=20'
		print(inurl)
		# change query id and IRModel name accordingly
		qid = qid
		IRModel='default'
		print(k)
		k=k+1
		data = urllib2.urlopen(inurl)
		# if you're using python 3, you should use
		# data = urllib.request.urlopen(inurl)

		docs = json.load(data)['response']['docs']
		# the ranking should start from 1 and increase
		rank = 1
		for doc in docs:
			outf.write(qid + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + IRModel + '\n')
			rank += 1
outf.close()
