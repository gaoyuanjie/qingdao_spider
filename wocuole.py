# coding=gbk
import requests
import re
from fake_useragent import UserAgent
url = 'http://qdtj.qingdao.gov.cn/n28356045/n32561056/n32561073/n32561267/index.html'
url = 'http://27.223.1.61:8090/GetDynamicPager.ashx?showtotal=1&templateGuid=180503185536335165&lkocok_pageNo=21&htmlPageCount=20&page=changeInfo'
headers = {
    'User-Agent': UserAgent().random
}
html = requests.get(url=url, headers=headers).content.decode('utf-8', 'ignore')
print(html)


