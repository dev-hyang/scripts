import requests
import bs4
from bs4 import BeautifulSoup
from EncodeConsts import *
import os
import sys, getopt

class GenerateChristianBookTxt:

	def __init__(self, _urlPrefix, _pageIndex, *args):
		self.urlPrefix = _urlPrefix
		self.pageIndex = _pageIndex
		if len(args) > 0:
			self.bookname = args[0]
		self.nextURLs = []
		self.listIndex = ''
		self.outputfile = ''

	def sendRequest(self, url):
		"""
		"""
		# resp = requests.get(URL)
		# 406 - Can have a different User-Agent or Add Accept header param
		# resp = requests.get(URL, headers={"Accept":"text/html"})
		# 406 - The default Python User-Agent 'python-requests/2.21.0' was being probably blocked by the hosting company.
		resp = requests.get(url, headers={"Accept":"text/html", "User-Agent": USER_AGENT})
		# print(resp.status_code, resp.text)
		# 显示乱码
		# print(resp.encoding) #网页返回字符集类型 iso-8859-1
		# print(resp.apparent_encoding) #自动判断字符集类型 gb2312
		# 解决办法 - https://www.zhihu.com/question/27062410
		# Requests 推测的文本编码（也就是网页返回即爬取下来后的编码转换）与源网页编码不一致，由此可知其正是导致乱码原因
		resp.encoding = resp.apparent_encoding

		soup = BeautifulSoup(resp.text, "html.parser")
		return soup

	def generateBook(self, urlPrefix, pageIndex):
		"""
		"""
		# URL_Prefix = 'http://www.wellsofgrace.com/books/pcwife/htm/'
		# mainPage = 'main.html'
		if (pageIndex == 'main.html'):
			url = urlPrefix + pageIndex
			soup = self.sendRequest(url)
			self.bookname = str(soup.find('title').string).strip()
			# name is reserved keyword in soup, replace using attrs
			# self.listIndex = soup.find('frame', name="contents") # -> cast TypeError
			frameTag = soup.find('frame', attrs={'name':"contents"})
			print(frameTag)
			if (frameTag != None):
				self.listIndex = frameTag.get('src')
			else:
				self.listIndex = pageIndex
			# print(self.listIndex)
			self.outputfile = "outputs/" + self.bookname + ".txt"
			self.generateChapters(urlPrefix, self.listIndex, self.outputfile)
		else:
			url = urlPrefix + pageIndex
			soup = self.sendRequest(url)
			self.bookname = str(soup.find('title').string).strip()
			self.outputfile = "outputs/" + self.bookname + ".txt"
			self.generateChapters(urlPrefix, pageIndex, self.outputfile)

		print(self.bookname, self.listIndex, self.outputfile)

	def generateChapters(self, urlPrefix, pageIndex, outputfile):
		url = urlPrefix + pageIndex 
		soup = self.sendRequest(url)

		nextPages = soup.find_all('a');
		self.nextURLs = [urlPrefix + x['href'] for x in nextPages if (x['href'].endswith('html') or x['href'].startswith('htm'))]

		for i in range(len(self.nextURLs)):
			title, texts = self.handleDetailTexts(self.nextURLs[i])
			self.writeToFile(i, title, texts, outputfile)

	def handleDetailTexts(self, url):
		"""
		"""
		soup = self.sendRequest(url)
		# http://cclw.net/soul/qzdgdll/htm/qizidgdll01.htm

		if (not url.startswith('http://cclw.net/soul/qzdgdll')):

			title = soup.find('title')
			fonts = soup.find_all('font', size="2")
			temp_texts = ''
			for font in fonts:
				if len(font.contents) > 1:
					for ele in font.contents:
						if (type(ele) is bs4.element.NavigableString) and len(ele) > 4:
							temp_texts = temp_texts + ele
			# print(title.string)
			texts = temp_texts.replace('����', '').replace('\r\n', '\n')
			return (title.string, texts)
		else:
			title = soup.find_all('b')[0].string
			paras = soup.find_all('p')
			temp_texts = ''
			for para in paras:
				if len(para.contents) > 1:
					for ele in para.contents:
						if (type(ele) is bs4.element.NavigableString) and len(ele) > 4:
							temp_texts = temp_texts + ele
			# print(title.string)
			texts = temp_texts.replace('����', '').replace('\r\n', '\n')
			# print(texts)
			return (title.string, texts)

	def writeToFile(self, chapterIndex, title, texts, outputfile):
		"""
		"""
		with open(outputfile,"a+") as outfile:
				try:
					outfile.write("\n")
					outfile.write("\n")
					outfile.write("第"+str(chapterIndex)+"章 " + title)
					outfile.write("\n")
					outfile.write("\n")
					outfile.write(texts)
				except TypeError:
					os.remove(outputfile)