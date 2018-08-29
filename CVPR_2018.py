'''
  This script downloads the papers from CVPR 2018 and creates a CSV file with institution and the papers published by those institutions. 
'''
import PyPDF2
import urllib2
import requests
from bs4 import BeautifulSoup
import glob 
import pandas as pd 
import re
from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import string
pdf_link = []
title_link = []
url = 'http://openaccess.thecvf.com/CVPR2018.py'
folder_path = '/Users/Janjua/Desktop/CVPR_Institute/'

def parse_pdf(url):
	title_list = []
	author_lst = []
	inst_list = []

	fp = open(url, 'rb')
	parser = PDFParser(fp)
	doc = PDFDocument(parser)
	for i in doc.info:
		author_lst = i["Author"].split()
		title_list = i["Title"].split()
	author_lst = map(lambda x:x.lower(), author_lst)
	author_lst = map(lambda x:x.replace(',',''), author_lst)
	title_list = map(lambda x:x.lower(), title_list)

	def convert(fname, pages=None):
	    output = StringIO()
	    manager = PDFResourceManager()
	    converter = TextConverter(manager, output, laparams=LAParams())
	    interpreter = PDFPageInterpreter(manager, converter)

	    infile = file(fname, 'rb')
	    for page in PDFPage.get_pages(infile, 0):
	       interpreter.process_page(page)
	       break
	    infile.close()
	    converter.close()
	    text = output.getvalue()
	    output.close
	    return text

	some_variable = convert(url) 
	some_v = str(some_variable)
	head, sep, tail = some_v.partition('Abstract')
	head = ''.join(re.sub(r'\S*@\S*\s?', '', head).replace('\n', ' '))
	head = re.sub(r'[^\x00-\x7f]',r'', head) 
	head = head.lower()
	head = re.sub(r'[0-9]+', '', head)
	little_clean = [i for i in head.split() if i not in title_list]
	little_clean = [i.replace(',','') for i in little_clean]
	little_clean = [i for i in little_clean if i not in author_lst]
	inst = ' '.join([x.upper() for x in little_clean])
	inst, _, _ = inst.partition('{')
	for i in (str(inst).split(',')):
		if 'UNIVERSITY' in i or 'FACEBOOK' in i or 'GOOGLE' in i or 'SCHOOL' in i or 'CENTER' in i or 'INSTITUTE' in i or 'TECH' in i or 'COMPANY' in i or 'CENTRE' in i or 'RESEARCH' in i or 'GROUP' in i or 'DEPARTMENT' in i or 'LABS' in i or 'LAB' in i or 'INC' in i or 'COLLEGE' in i or 'ETH':
			inst_list.append(i)
	return ' '.join(inst_list)

def get_pdf():
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")
	titles_ = soup.find_all('dt', attrs={'class':'ptitle'})
	pdfs_ = soup.find_all('dd')
	for i in pdfs_:
		if '[<a href' in str(i):
			link_ = str(i).split('\n')[1].split('=')[1].split(">")[0].replace('"','')
			comp_link = 'http://openaccess.thecvf.com/'+link_
			pdf_link.append(comp_link)
	for i in titles_:
		title = str(i).split('>')[3].split('<')[-2]
		title_link.append(title)

def download_file(download_url, title):
	try:
		response = urllib2.urlopen(download_url)
		file = open("{}.pdf".format(title), 'wb')
	except:
		print("Couldn't Download: ", title)
	file.write(response.read())
	file.close()
	print("Completed {}".format(title))

def bulk_download():
	get_pdf()
	assert len(pdf_link) == len(title_link)
	for xi in range(len(pdf_link)):
		download_file(pdf_link[xi], title_link[xi])

def enum_files():
	#bulk_download()
	wr_file = open('stats_cvpr_2018.csv', 'w')
	wr_file.write('Title'+','+'Institution'+'\n')
	for i in glob.glob(folder_path+"*.pdf"):
		title = i.split('/')[-1].split('.')[0]
		title = title.replace('/', '')
		title = title.replace(',', '')
		parsed_info = parse_pdf(i)
		print(title, parsed_info)
		try:
			wr_file.write(title+',')
			wr_file.write(parsed_info)
			wr_file.write('\n')
		except:
			print("None Value: ", title)
	wr_file.close()
		
enum_files()
