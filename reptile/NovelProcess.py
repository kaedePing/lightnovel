import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os
import logging
from multiprocessing import Pool

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[Line：%(lineno)d] - %(levelname)s %(message)s',
                    filename='Logs/log.txt',
                    filemode='a')
session = requests.Session()  # 创建一个全局Session对象


def is_existence_path(path):  # 判断文件是否存在，不存在就创建
    if not os.path.exists(path):
        os.mkdir(path)


def construct_main_pages(main_page='https://www.wenku8.net/modules/article/toplist.php?sort=allvisit', start_page=1,
                         end_page=134):
    """
    根据传来的主页和页码数返回第一层构造的网页
    :param end_page: 网页截至页数
    :param start_page: 网页起止页数
    :param main_page: 网站主页
    :return: 返回一个包含构造的网页的列表
    """
    url_sum = []
    for page in range(start_page, end_page + 1):
        url_sum.append(main_page + '&page={}'.format(str(page)))
    return url_sum


def set_session():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
    }
    param = {
        'username': 'ReasonBetray',
        'password': 'liuping1235',
        'usecookie': '0',
        'action': 'login',
        'submit': ''
    }
    time.sleep(3)
    global session
    session.post('https://www.wenku8.net/login.php', headers=headers, data=param)  # 使用post登录后，保留当前会话，来获取数据


def get_novels_per_page(url):
    """
    根据网页，获取每个网页包含的小说数量
    :param url: 目标网页
    :return: 包含这个网页所有小说的列表
    """
    time.sleep(0.5)
    try:
        novel_sum = []  # 用于存储小说详情页面的列表
        set_session()
        res = session.get(url)
        res = res.text.encode('ISO-8859-1').decode('gbk')
        html = BeautifulSoup(res, 'html.parser')
        table = html.find('table', class_='grid')  # 找到包含小说的table
        b_s = table.find_all('b')  # 进一步找到所有小说的b
        for b in b_s:
            href = b.a['href']  # 得到b标签下的a标签中的href属性
            novel_sum.append(href)  # 获得小说的详细连接，存入列表中
        return novel_sum
    except:
        logging.error('scrap {}   failed!'.format(url))


def get_novel_detail(novel_url):
    """
    根据传来的每个网页
    :param session: 利用session请求网页
    :param novel_url: 目标地址
    :return: 包含当前目标地址的小说的提取信息的字典
    """
    time.sleep(0.5)
    try:
        detail = dict()
        set_session()
        res = session.get(novel_url)
        try:
            res = res.text.encode('ISO-8859-1').decode('gbk')
        except:
            res = res.text.encode('ISO-8859-1').decode('gb18030')
        res = BeautifulSoup(res, 'html.parser')
        div = res.find(id='content')  # 找到第一个id为content的div标签
        div = div.find_all('div')[0]
        ntitle = div.find_all('tr')[0].find('b').text  # 找到b标签下面的小说标题
        content = div.find_all('tr')[2].find_all('td')  # 找到文库分类，小说作者，文章状态，最后更新，全文长度
        nclassification = content[0].text
        nclassification = nclassification.split('：')[1]  # 数据清洗，需要提取第二部分
        nauthor = content[1].text
        nauthor = nauthor.split('：')[1]
        nstatus = content[2].text
        nstatus = nstatus.split('：')[1]
        try:  # 有的小说并没有包含下面的全部信息，加容错，如果未找到，都设置为None
            nupdate = content[3].text
            nupdate = nupdate.split('：')[1]
            nlength = content[4].text
            nlength = int(float(nlength.split('：')[1][0:-1]))
        except:
            nupdate = None
            nlength = None

        ncover = div.find_all('tr')[3].find('img')['src']  # 获取到封面地址
        detail['小说名称'] = ntitle
        detail['文库分类'] = nclassification
        detail['小说作者'] = nauthor
        detail['文章状态'] = nstatus
        detail['最后更新'] = nupdate
        detail['全文长度'] = nlength
        detail['小说封面'] = ncover
        print(detail)
        return detail
    except:
        logging.error('scrap {} failed'.format(novel_url))


def get_light_novel_library_solo():  # 获取轻小说文库内容的函数，安排调用关系，单
    set_session()
    path = os.getcwd() + '\\results\\'  # 结果保存文件路径以及文件名
    is_existence_path(path)  # 判断路径是否存在
    logging.info('start scraping Solo')
    url_sum = construct_main_pages()  # 调用构造网页的函数，得到一个包含所有网页数的列表

    novel_sum = []  # 保存小说详情网页的列表
    for url in url_sum:  # 依次遍历所有网页，获取所有网页中包含的目标小说的网址，使用novel_sum列表保存
        if not novel_sum:
            novel_sum = get_novels_per_page(url)
        else:
            novels = get_novels_per_page(url)
            for novel in novels:
                novel_sum.append(novel)
    novel_detail = []  # 保存所有小说的列表，每个列表元素是一个包含提取信息的字典
    for novel in novel_sum:
        novel_detail.append(get_novel_detail(novel))
    logging.info('end scraping,' + '  Novels have {number} '.format(number=len(novel_detail)))
    df = pd.DataFrame(novel_detail)  # 将所有结果构造的列表保存为DataFrame对象
    df.to_csv(path + 'novel.csv', encoding='utf-8_sig', index=False)


def get_light_novel_library_process():  # 获取轻小说文库内容的函数，安排调用关系，进程
    logging.info('start process function!')

    path = os.getcwd() + '\\results\\'  # 结果保存文件路径以及文件名
    is_existence_path(path)  # 判断路径是否存在
    logging.info('start scraping Process')
    url_sum = construct_main_pages()  # 调用构造网页的函数，得到一个包含所有网页数的列表
    pool = Pool()
    novel_sum = []
    sum_list = pool.map(get_novels_per_page, url_sum)
    time.sleep(2)
    for i in sum_list:
        for j in i:
            novel_sum.append(j)
    novel_detail = pool.map(get_novel_detail, novel_sum)  # 保存所有小说的列表，每个列表元素是一个包含提取信息的字典
    logging.info('end scraping,' + '  Novels have {number} '.format(number=len(novel_detail)))
    df = pd.DataFrame(novel_detail)  # 将所有结果构造的列表保存为DataFrame对象
    df.to_csv(path + 'novel.csv', encoding='utf-8_sig', index=False)
    logging.info('end process function!')


if __name__ == '__main__':
    get_light_novel_library_process()
