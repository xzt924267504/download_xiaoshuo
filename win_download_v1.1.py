import time
import requests
import re
import lxml
import random

class Download_xiaoshuo():
    def __init__(self):
        self.user_agent = [
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
        ]
        self.headers = {
            "accept": "*/*",
            'User-Agent': random.choice(self.user_agent)
        }
        self.se = requests.session()
        self.download_url_list = []
        self.num = 0
    def mulu(self,book_id):
        """
        ????????????id  ????????????????????????
        :param book_id: ???????????????????????????
        :return:
        """
        self.book_id = book_id
        bookurl = "http://77kshu.win/{}".format(book_id)
        print(bookurl)
        self.mulu_response = self.se.get(bookurl,headers = self.headers)
        self.mulu_response.encoding = 'gbk'
        self.mulu_response_text = self.mulu_response.text

        # ????????????
        self.book_name  = re.findall('title="?????????(.*?)????????????'.format(book_id),self.mulu_response_text)
        for k in self.book_name:
            self.book_name = k
        print(self.book_name)



    def get_booklist(self):
        """
        ?????????????????????????????????????????????????????????????????????
        ??????????????????????????????????????????
        :return:
        """
        #??????class list div
        self.booklist_div = re.findall(r'<div class="list">(.*?)class="bookfoot"', self.mulu_response_text)
        for i in self.booklist_div:
            self.booklist_div = i

        # ??????div????????????
        self.booklist = re.findall(r'href="/{}/(.*?).html"'.format(self.book_id),self.booklist_div)
        self.booklist = [ int(x) for x in self.booklist ]
        print(self.booklist)

        #????????????????????????
        for i in self.booklist:
            print('?????????'+str(i)+'???')
            print('\n')
            #?????????????????????url, ???????????????
            url = 'http://77kshu.win/{}/{}.html'.format(self.book_id,i)
            print(url)
            self.response = self.se.get(url,headers = self.headers)
            self.response.encoding = "gbk"
            self.responsetext = self.response.text
            self.download_url_list.append(url)
            # print(self.responsetext)

            #???????????????????????????
            self.all_page = re.search('\d\)',self.responsetext).group().replace(')','')

            print('????????????' + str(self.all_page) + '???')
            if int(self.all_page) != 1:
                for j in range(2,int(self.all_page)+1):
                    ii = str(i)+'-'+str(j)
                    self.all_page_url = r"http://77kshu.win/{}/{}.html".format(self.book_id,ii)
                    self.download_url_list.append(self.all_page_url)
                    print(self.all_page_url)
            else:
                continue

        print('url??????:',self.download_url_list)

    def get_bookcontent(self):
        """
        ??????url??????, ?????????????????????url????????????????????????????????????
        :return:
        """
        with open('./?????????/{}.txt'.format(self.book_name), 'w')as self.f:

            for i in self.download_url_list:
                print('???',len(self.download_url_list),'??????????????????',self.num+1,)
                self.num+=1
                self.bookcontent = self.se.get(url=i,headers = self.headers)
                self.bookcontent_text = self.bookcontent.text
                self.__rehtml_download()
                self.__download_response()

    def __rehtml_download(self):
        """
        ?????????????????????p?????????????????????????????????
        :return:
        """
        self.booktext = re.findall(r'<div class="chapter">(.*?)<br>',self.bookcontent_text)
        for p in self.booktext:
            self.booktext = p
        self.booktext = self.booktext.replace('<p>','')
        self.booktext = self.booktext.replace('</p>', '')
        self.booktext = self.booktext.replace('???', '.\n')

        return self.booktext

    def __download_response(self):
        """
        ????????????????????????????????????????????????????????????????????????
        :return:
        """
        self.f.write(self.__rehtml_download())
        self.f.write('\n')


d = Download_xiaoshuo()
d.mulu(input())
d.get_booklist()
d.get_bookcontent()


"""
164968
180289
166700
172305

"""






