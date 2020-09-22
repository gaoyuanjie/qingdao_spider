# coding=gbk
import random
import time
import csv
import os
import requests
import re
from fake_useragent import UserAgent
from lxml import etree

'''
此处是教学部分：
1 本网站无任何明显反爬，因此爬虫步骤如下
    1  安装必要模块
       要访问的url：http://qdtj.qingdao.gov.cn/n28356045/n32561056/n32561073/index.html
       一般在浏览器地址栏输入以上url即可，但是程序讲究自动化，使用 requests模块，模拟人类浏览器访问
       注意：你得安装requests，安装后得导入，上面我已经导入了，但是我的电脑装了你不一定装，
       模块安装的常用方法：
           1 键盘同时按住 win（就是左手alt键左边的那个键） + r
           2 输入cmd
           3 打开cmd后，输入python -m pip install xxx  （注意 xxx是你的库名）
       总之，把上面的库全装了
    2  寻找界面，发送请求
        requests.get()方法的功能是访问网站并获得响应
        响应里头可能包含你想要的数据，也可能是链接
        本例中，青岛统计局包含三个页面
        最好看到这里时，你打开 http://qdtj.qingdao.gov.cn/n28356045/n32561056/n32561073/index.html
        查看一级页面
        打开一级页面后你发现了一坨链接：'2006青岛统计年鉴', '2007青岛统计年鉴', '2008青岛统计年鉴'
        想办法拿到这些链接，下面是方法：
        1 requests.get()方法拿到页面
        2 使用xpath解析，拿到每个页面中，相应节点里头的链接
        3 打开链接
            1 打开链接后，进入二级界面，打开方法也是requests.get()
            2 同理，看到这里你应该浏览器再点进去，比如你点进去2006青岛统计年鉴
            3 发现还是一堆链接，没有数据
            4 使用xpath解析，拿到每个页面中，相应节点里头的链接
                。。。。反正依次打开链接，查看页面内容是链接还是数据；你总能找到你想要的数据，而不是只看到一堆链接
                幸好这个只有三级界面
                下面，进入正确爬取环节，请直接跳转到最下面的函数parse_html      
'''


# 一级页面
# //div[@class="nj"]/ul/li/a/text()  名称
# '//div[@class="nj"]/ul/li/a/@href' 链接

# 二级页面
# //div[@id="listChangeDiv"]//span/a/text()
# //div[@id="listChangeDiv"]//span/a/@href

# 三级界面
# 先提取tr节点
# 在tr节点对象列表中提取响应的td
# 然后写入csv


class QingdaoSpider:
    def __init__(self):
        self.url = 'http://qdtj.qingdao.gov.cn/n28356045/n32561056/n32561073/index.html'

    def get_html(self, url):
        # requests.get方法的参数如下，其中url是你要访问的链接，headers是反爬虫必检查的，这里因为反爬程度不高，我随便写写得了
        headers = {
            'User-Agent': UserAgent().random
        }
        # requests.get得到的是一个对象，（对象.属性）就可以提取到响应的内容，比如Content就是你提取到的响应，注意，这里是字节串，需要解码0.0
        html = requests.get(url=url, headers=headers).content.decode('utf-8', 'ignore')
        # 把页面内容返回回去
        return html

    def xpath_func(self, xpath_bds, html):
        # xpath解析需要你先将html页面通过etree的HTML实例化出一个对象才能进行
        p = etree.HTML(html)
        # 对实例化的对象调用xpath方法，即可获得列表，注意，是列表0.0
        r_list = p.xpath(xpath_bds)
        return r_list

    def parse_html(self, url):
        one_html = self.get_html(url)  # 本网站有三个页面，我把提取页面的内容封装成了一个函数，免得获取3个页面都得写一次，请向上查找这个函数
        with open('one_html.html', 'w', errors='ignore') as f:
            f.write(one_html)
        name1_xpath = '//div[@class="nj"]/ul/li/a/text()'  # 所有年份的 -> ['2006青岛统计年鉴',....]
        link1_xpath = '//div[@class="nj"]/ul/li/a/@href'  # 所有年份对应的链接 ['/n28356045/n32561056/n32561073/n32561266/index.html']
        name1_list = self.xpath_func(name1_xpath, one_html)  # 同样，解析也需要三次，我也封装了，可以去上面看看
        link1_list = self.xpath_func(link1_xpath, one_html)
        print('一级页面名称：', name1_list)  # 一级页面名称： ['2006青岛统计年鉴', '2007青岛统计年鉴',  '2009青岛统计年鉴', ....]
        print('一级页面链接：', link1_list)  # 一级页面链接： ['/n28356045/n32561056/n32561073/n32561266/index.html', ....]
        base_url = 'http://qdtj.qingdao.gov.cn'
        time.sleep(random.uniform(5, 8))
        '''
            以上一坨代码就是获得第一级页面的链接
        '''

        '''
            以下开始二级页面及三级页面的爬取
        '''
        for h in range(1):  # 我就取了一个2006年的统计年鉴，不敢爬太多0.0,正常情况这里应该写 for h in range(len(link1_list)):
            # 以下内容确定爬取的页数
            url = base_url + link1_list[h]
            html = self.get_html(url=url)
            re_bds = '.*?getCreatePageHTML\((.*?),'
            pattern = re.compile(re_bds, re.S)
            number_list = pattern.findall(html)
            number = number_list[0].strip() if number_list else None
            print(name1_list[h] + '共有' + number + '页')
            for i in range(0,int(number)-1):
                print('正在爬取第{}页'.format(i+1))
                # 这里加 if else结构 是因为url有点奇葩，首页是index.html 第二页：index_2.html，格式化不方便
                if i == 0:
                    two_url = base_url + link1_list[h]
                    two_html = self.get_html(url=two_url)
                    name2_xpath = '//div[@id="listChangeDiv"]//span/a/text()'
                    link2_xpath = '//div[@id="listChangeDiv"]//span/a/@href'
                    name2_list = self.xpath_func(name2_xpath, two_html)
                    link2_list = self.xpath_func(link2_xpath, two_html)
                    print('二级页面名称：', name2_list)
                    print('二级页面链接：', link2_list)
                    time.sleep(random.uniform(5, 8))
                else:
                    two_url = base_url + link1_list[h][:-10] + 'index_{}.html'.format(i + 1)
                    two_html = self.get_html(url=two_url)
                    name2_xpath = '//div[@id="listChangeDiv"]//span/a/text()'
                    link2_xpath = '//div[@id="listChangeDiv"]//span/a/@href'
                    # ['行政区划', '气象情况',...]
                    name2_list = self.xpath_func(name2_xpath, two_html)
                    # ['/n28356045/n32561056/n32561073/n32561266/180324190134485883.html',...]
                    link2_list = self.xpath_func(link2_xpath,two_html)
                    print('二级页面名称：', name2_list)
                    print('二级页面链接：', link2_list)
                    with open('kkk.html','w',errors='ignore') as f:
                        f.write(two_html)

                    # 因为我发现它的页面不是很规律，搞了半天，才发现有问题，这个不好跟您解释，这里有点反爬的意思，但是不算很难
                    if not link2_list:
                        two_url = 'http://27.223.1.61:8090/GetDynamicPager.ashx?showtotal=1&templateGuid=180503185536319126&lkocok_pageNo={}&htmlPageCount=20&page=changeInfo'.format(i + 1)
                        print(two_url)
                        two_html = self.get_html(url=two_url)
                        name2_xpath = '//span[@class="fl"]/a/@title'
                        link2_xpath = '//span[@class="fl"]/a/@href'
                        with open('kkk.html','w',errors='ignore') as f:
                            f.write(two_html)
                        # ['行政区划', '气象情况',...]
                        name2_list = self.xpath_func(name2_xpath, two_html)
                        # ['/n28356045/n32561056/n32561073/n32561266/180324190134485883.html',...]
                        link2_list = self.xpath_func(link2_xpath, two_html)
                        print('二级页面名称：', name2_list)
                        print('二级页面链接：', link2_list)
                    time.sleep(random.uniform(5, 8))
                # 三级界面爬取
                for j in range(len(link2_list)):
                    three_url = base_url + link2_list[j]
                    three_html = self.get_html(url=three_url)
                    tr_xpath = '//tr'
                    tr_list = self.xpath_func(tr_xpath, three_html)
                    rows_list = []
                    for tr in tr_list:
                        row_list = []
                        td_list = tr.xpath('.//td//text()')
                        for td in td_list:
                            row_list.append(td)
                        row_list = tuple(row_list)
                        rows_list.append(row_list)

                    # 保存到本地文件
                    filepath = '.\\' + name1_list[h] + '\\' + '第{}页'.format(i + 1) + '\\'
                    if not os.path.exists(filepath):
                        os.makedirs(filepath)
                    filename = filepath + name2_list[j] + '.csv'
                    self.save_data(filename, rows_list)

    def save_data(self, filename, rows_list):
        with open(filename, 'w', errors='ignore') as f:
            writer = csv.writer(f)
            writer.writerows(rows_list)

    def run(self):
        self.parse_html(self.url)


if __name__ == '__main__':
    spider = QingdaoSpider()
    spider.run()
