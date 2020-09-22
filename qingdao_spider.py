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
�˴��ǽ�ѧ���֣�
1 ����վ���κ����Է�����������沽������
    1  ��װ��Ҫģ��
       Ҫ���ʵ�url��http://qdtj.qingdao.gov.cn/n28356045/n32561056/n32561073/index.html
       һ�����������ַ����������url���ɣ����ǳ��򽲾��Զ�����ʹ�� requestsģ�飬ģ���������������
       ע�⣺��ð�װrequests����װ��õ��룬�������Ѿ������ˣ������ҵĵ���װ���㲻һ��װ��
       ģ�鰲װ�ĳ��÷�����
           1 ����ͬʱ��ס win����������alt����ߵ��Ǹ����� + r
           2 ����cmd
           3 ��cmd������python -m pip install xxx  ��ע�� xxx����Ŀ�����
       ��֮��������Ŀ�ȫװ��
    2  Ѱ�ҽ��棬��������
        requests.get()�����Ĺ����Ƿ�����վ�������Ӧ
        ��Ӧ��ͷ���ܰ�������Ҫ�����ݣ�Ҳ����������
        �����У��ൺͳ�ƾְ�������ҳ��
        ��ÿ�������ʱ����� http://qdtj.qingdao.gov.cn/n28356045/n32561056/n32561073/index.html
        �鿴һ��ҳ��
        ��һ��ҳ����㷢����һ�����ӣ�'2006�ൺͳ�����', '2007�ൺͳ�����', '2008�ൺͳ�����'
        ��취�õ���Щ���ӣ������Ƿ�����
        1 requests.get()�����õ�ҳ��
        2 ʹ��xpath�������õ�ÿ��ҳ���У���Ӧ�ڵ���ͷ������
        3 ������
            1 �����Ӻ󣬽���������棬�򿪷���Ҳ��requests.get()
            2 ͬ������������Ӧ��������ٵ��ȥ����������ȥ2006�ൺͳ�����
            3 ���ֻ���һ�����ӣ�û������
            4 ʹ��xpath�������õ�ÿ��ҳ���У���Ӧ�ڵ���ͷ������
                ���������������δ����ӣ��鿴ҳ�����������ӻ������ݣ��������ҵ�����Ҫ�����ݣ�������ֻ����һ������
                �Һ����ֻ����������
                ���棬������ȷ��ȡ���ڣ���ֱ����ת��������ĺ���parse_html      
'''


# һ��ҳ��
# //div[@class="nj"]/ul/li/a/text()  ����
# '//div[@class="nj"]/ul/li/a/@href' ����

# ����ҳ��
# //div[@id="listChangeDiv"]//span/a/text()
# //div[@id="listChangeDiv"]//span/a/@href

# ��������
# ����ȡtr�ڵ�
# ��tr�ڵ�����б�����ȡ��Ӧ��td
# Ȼ��д��csv


class QingdaoSpider:
    def __init__(self):
        self.url = 'http://qdtj.qingdao.gov.cn/n28356045/n32561056/n32561073/index.html'

    def get_html(self, url):
        # requests.get�����Ĳ������£�����url����Ҫ���ʵ����ӣ�headers�Ƿ�����ؼ��ģ�������Ϊ�����̶Ȳ��ߣ������дд����
        headers = {
            'User-Agent': UserAgent().random
        }
        # requests.get�õ�����һ�����󣬣�����.���ԣ��Ϳ�����ȡ����Ӧ�����ݣ�����Content��������ȡ������Ӧ��ע�⣬�������ֽڴ�����Ҫ����0.0
        html = requests.get(url=url, headers=headers).content.decode('utf-8', 'ignore')
        # ��ҳ�����ݷ��ػ�ȥ
        return html

    def xpath_func(self, xpath_bds, html):
        # xpath������Ҫ���Ƚ�htmlҳ��ͨ��etree��HTMLʵ������һ��������ܽ���
        p = etree.HTML(html)
        # ��ʵ�����Ķ������xpath���������ɻ���б�ע�⣬���б�0.0
        r_list = p.xpath(xpath_bds)
        return r_list

    def parse_html(self, url):
        one_html = self.get_html(url)  # ����վ������ҳ�棬�Ұ���ȡҳ������ݷ�װ����һ����������û�ȡ3��ҳ�涼��дһ�Σ������ϲ����������
        with open('one_html.html', 'w', errors='ignore') as f:
            f.write(one_html)
        name1_xpath = '//div[@class="nj"]/ul/li/a/text()'  # ������ݵ� -> ['2006�ൺͳ�����',....]
        link1_xpath = '//div[@class="nj"]/ul/li/a/@href'  # ������ݶ�Ӧ������ ['/n28356045/n32561056/n32561073/n32561266/index.html']
        name1_list = self.xpath_func(name1_xpath, one_html)  # ͬ��������Ҳ��Ҫ���Σ���Ҳ��װ�ˣ�����ȥ���濴��
        link1_list = self.xpath_func(link1_xpath, one_html)
        print('һ��ҳ�����ƣ�', name1_list)  # һ��ҳ�����ƣ� ['2006�ൺͳ�����', '2007�ൺͳ�����',  '2009�ൺͳ�����', ....]
        print('һ��ҳ�����ӣ�', link1_list)  # һ��ҳ�����ӣ� ['/n28356045/n32561056/n32561073/n32561266/index.html', ....]
        base_url = 'http://qdtj.qingdao.gov.cn'
        time.sleep(random.uniform(5, 8))
        '''
            ����һ�������ǻ�õ�һ��ҳ�������
        '''

        '''
            ���¿�ʼ����ҳ�漰����ҳ�����ȡ
        '''
        for h in range(1):  # �Ҿ�ȡ��һ��2006���ͳ�������������̫��0.0,�����������Ӧ��д for h in range(len(link1_list)):
            # ��������ȷ����ȡ��ҳ��
            url = base_url + link1_list[h]
            html = self.get_html(url=url)
            re_bds = '.*?getCreatePageHTML\((.*?),'
            pattern = re.compile(re_bds, re.S)
            number_list = pattern.findall(html)
            number = number_list[0].strip() if number_list else None
            print(name1_list[h] + '����' + number + 'ҳ')
            for i in range(0,int(number)-1):
                print('������ȡ��{}ҳ'.format(i+1))
                # ����� if else�ṹ ����Ϊurl�е����⣬��ҳ��index.html �ڶ�ҳ��index_2.html����ʽ��������
                if i == 0:
                    two_url = base_url + link1_list[h]
                    two_html = self.get_html(url=two_url)
                    name2_xpath = '//div[@id="listChangeDiv"]//span/a/text()'
                    link2_xpath = '//div[@id="listChangeDiv"]//span/a/@href'
                    name2_list = self.xpath_func(name2_xpath, two_html)
                    link2_list = self.xpath_func(link2_xpath, two_html)
                    print('����ҳ�����ƣ�', name2_list)
                    print('����ҳ�����ӣ�', link2_list)
                    time.sleep(random.uniform(5, 8))
                else:
                    two_url = base_url + link1_list[h][:-10] + 'index_{}.html'.format(i + 1)
                    two_html = self.get_html(url=two_url)
                    name2_xpath = '//div[@id="listChangeDiv"]//span/a/text()'
                    link2_xpath = '//div[@id="listChangeDiv"]//span/a/@href'
                    # ['��������', '�������',...]
                    name2_list = self.xpath_func(name2_xpath, two_html)
                    # ['/n28356045/n32561056/n32561073/n32561266/180324190134485883.html',...]
                    link2_list = self.xpath_func(link2_xpath,two_html)
                    print('����ҳ�����ƣ�', name2_list)
                    print('����ҳ�����ӣ�', link2_list)
                    with open('kkk.html','w',errors='ignore') as f:
                        f.write(two_html)

                    # ��Ϊ�ҷ�������ҳ�治�Ǻܹ��ɣ����˰��죬�ŷ��������⣬������ø������ͣ������е㷴������˼�����ǲ������
                    if not link2_list:
                        two_url = 'http://27.223.1.61:8090/GetDynamicPager.ashx?showtotal=1&templateGuid=180503185536319126&lkocok_pageNo={}&htmlPageCount=20&page=changeInfo'.format(i + 1)
                        print(two_url)
                        two_html = self.get_html(url=two_url)
                        name2_xpath = '//span[@class="fl"]/a/@title'
                        link2_xpath = '//span[@class="fl"]/a/@href'
                        with open('kkk.html','w',errors='ignore') as f:
                            f.write(two_html)
                        # ['��������', '�������',...]
                        name2_list = self.xpath_func(name2_xpath, two_html)
                        # ['/n28356045/n32561056/n32561073/n32561266/180324190134485883.html',...]
                        link2_list = self.xpath_func(link2_xpath, two_html)
                        print('����ҳ�����ƣ�', name2_list)
                        print('����ҳ�����ӣ�', link2_list)
                    time.sleep(random.uniform(5, 8))
                # ����������ȡ
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

                    # ���浽�����ļ�
                    filepath = '.\\' + name1_list[h] + '\\' + '��{}ҳ'.format(i + 1) + '\\'
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
