# -*- codeing = utf-8 -*-
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，进行文字匹配`
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行excel操作
import pandas as pd
import time


# 对于要获取的每个内容创建正则表达式对象
LinkPattern = re.compile(r'<a href="(.*?)">')
ImgSrcPattern = re.compile(r'<img.*src="(.*?)"', re.S)
TitlePattern = re.compile(r'<span class="title">(.*)</span>')
RatingPattern = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
JudgePattern = re.compile(r'<span>(\d*)人评价</span>')
InqPattern = re.compile(r'<span class="inq">(.*)</span>')
BdPattern = re.compile(r'<p class="">(.*?)</p>', re.S)


def main():
  BaseUrl = "https://movie.douban.com/top250?start="
  DataList = getData(BaseUrl)
  SavePath = "豆瓣电影Top250.xls"
  saveData(DataList, SavePath)
  transfer(SavePath)

# 爬取网页内容
def getData(BaseUrl):
  datalist = []
  for i in range (0, 10):
    url = BaseUrl + str(i*25)
    html = askUrl(url)
    # 2.逐一解析数据
    soup = BeautifulSoup(html, "html.parser")
    # 查找符合要求的字符串
    for item in soup.find_all('div', class_="item"):
      # 保存一部电影所有信息
      data = []
      item = str(item)
      link = re.findall(LinkPattern, item)[0]  # 通过正则表达式查找
      data.append(link)
      imgSrc = re.findall(ImgSrcPattern, item)[0]
      data.append(imgSrc)
      titles = re.findall(TitlePattern, item)[0]
      data.append(titles)
      data.append(' ')
      rating = re.findall(RatingPattern, item)[0]
      data.append(rating)
      judgeNum = re.findall(JudgePattern, item)[0]
      data.append(judgeNum)
      inq = re.findall(InqPattern, item)
      if len(inq) != 0:
          inq = inq[0].replace("。", "")
          data.append(inq)
      else:
          data.append(" ")
      bd = re.findall(BdPattern, item)[0]
      # 导演: 陈凯歌 Kaige Chen&nbsp;&nbsp;&nbsp;主演: 张国荣 Leslie Cheung / 张丰毅 Fengyi Zha...<br>
      # 1993&nbsp;/&nbsp;中国大陆 中国香港&nbsp;/&nbsp;剧情 爱情 同性
      bd = re.sub('<br(\s+)?/>(\s+)?', "", bd)
      bd = re.sub('/', "", bd)
      data.append(bd.strip())
      datalist.append(data)

      time.sleep(10)

  return datalist

# 获取指定网页源码
def askUrl(url):
  # 构造请求信息
  # 模拟浏览器头部信息，向豆瓣服务器发送消息
  head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "Referer": "https://movie.douban.com/",
  }
  request = urllib.request.Request(url, headers=head)
  
  html = ""
  try:
    response = urllib.request.urlopen(request)
    html = response.read().decode("utf-8")
  except urllib.error.URLError as e:
    if hasattr(e, "code"):
      print(e.code)
    if hasattr(e, "reason"):
      print(e.reason)
  return html

# 保存数据
def saveData(DataList, SavePath):
  print("save.......")
  book = xlwt.Workbook(encoding="utf-8", style_compression=0) #创建workbook对象
  sheet = book.add_sheet('豆瓣电影Top250', cell_overwrite_ok=True) #创建工作表
  col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")
  for i in range(0, 8):
    # 列名
    sheet.write(0, i, col[i])
  for i in range(0, 250):
    # 输出语句，用来测试
    # print("第%d条" %(i+1))
    data = DataList[i]
    for j in range(0, 8):
      sheet.write(i + 1, j, data[j])
  book.save(SavePath)

def transfer(SavePath):
  csv_file = "./豆瓣电影.csv"
  df = pd.read_excel(SavePath)  # xlwt 适用于 .xls 文件
  df.to_csv(csv_file, index=False, header=True, encoding="utf-8-sig")  # 确保编码正确，防止中文乱码
  print(f"转换完成，CSV 文件已保存为 {csv_file}")

if __name__ == "__main__":
  main()
  print("爬取完毕")