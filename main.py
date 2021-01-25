# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import json
import time
from lxml import etree
import html
import re


class Weibospider:
    def __init__(self):
        self.start_url = 'https://weibo.com/rmrb?is_all=1&stat_date=202004#feedtop'
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",
            "cookie": "SINAGLOBAL=5309047095116.235.1608858668078; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whus_oBTbMkhydB0oy.4uQp5JpX5KMhUgL.FoMX1K2NShMcSo.2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNSh.pS0BNSoq4; UOR=,,www.baidu.com; wvr=6; ALF=1643020619; SSOLoginState=1611484620; SCF=Ai3s0J7z81LTjZv8y7xP3igLTXVwvleUdfkMy7AI2ela_T447d3NwVOh1nn3M3o5k8NgL-Xl33bbBXoPkojevGs.; SUB=_2A25NCT2dDeRhGeFK4lMW9CnKzTWIHXVufyhVrDV8PUNbmtANLRHYkW9NQt3XUDAmb6OUJdJhjK9spkl_dU-1fXJ-; _s_tentry=login.sina.com.cn; Apache=4238000816921.6167.1611484629596; ULV=1611484629656:7:4:1:4238000816921.6167.1611484629596:1611332494332; webim_unReadCount=%7B%22time%22%3A1611556108801%2C%22dm_pub_total%22%3A1%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A43%2C%22msgbox%22%3A0%7D; WBStorage=8daec78e6a891122|undefined",
            "referer": "https://weibo.com/rmrb?is_all=1&stat_date=202001",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36",
        }
        #伪装浏览器信息


    def parse_home_url(self, url):    # 处理解析首页面的详细信息
        res = requests.get(url, headers=self.headers)
        response = res.content.decode().replace("\\","")
        every_id = re.compile('name=(\d+)', re.S).findall(response)  # 获取次级页面需要的id
        home_url = []
        for id in every_id:
            base_url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id={}&from=singleWeiBo'
            url = base_url.format(id)
            home_url.append(url)
        return home_url

    def parse_comment_info(self, url): #爬取信息
        res = requests.get(url, headers=self.headers)
        response = res.json()
        count = response['data']['count']
        html = etree.HTML(response['data']['html'])
        #text = html.xpath("//div[@node-type='feed_list_content']/text()")  # 微博正文
        info = html.xpath("//div[@node-type='replywrap']/div[@class='WB_text']/text()")  # 评论信息
        info = "".join(info).replace(" ", "").split("\n")
        info.pop(0)
        comment_time = html.xpath("//div[@class='WB_from S_txt2']/text()")  # 评论时间
        comment_info_list = []
        #item = {}
        #item["mainBody"] = text  #存储微博内容
        #comment_info_list.append(item)
        comment_info_list.append([]) #分隔不同微博的评论
        for i in range(len(info)):
            item = {}
            item["comment_info"] = info[i]  # 存储评论的信息
            item["comment_time"] = comment_time[i]  # 存储评论时间
            comment_info_list.append(item)
        return count, comment_info_list

    def write_file(self, path_name, content_list): #保存数据
        for content in content_list:
            with open(path_name, "a", encoding="UTF-8") as f:
                f.write(json.dumps(content, ensure_ascii=False))
                f.write("\n")

    def run(self,path_name,n): #运行，n为微博页数
        start_url = 'https://weibo.com/rmrb?is_all=1&stat_date=202006&page={}#feedtop'
        for i in range(n):
            home_url = self.parse_home_url(start_url.format(i + 1)) #页码
            all_url = home_url
            print(all_url[0])
            all_count, comment_info_list = self.parse_comment_info(all_url[0])
            self.write_file(path_name, comment_info_list)
            comment_url = all_url[0]
            print(comment_url)
            time.sleep(0.2) #应对反爬程序


if __name__ == '__main__':
    path_name = "2020年6月微博评论.txt"
    weibo = Weibospider()
    weibo.run(path_name,37) #数字为当月微博页数
