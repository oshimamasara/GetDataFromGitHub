import datetime
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

driver = webdriver.Firefox()
driver.implicitly_wait(10)

language = ["Dart","Kotlin","Java"]
# https://github.com/search?utf8=%E2%9C%93&q=created%3A2018-01-01+language%3AKotlin&type=Repositories&ref=advsearch&l=Kotlin&l=
#sample_url = "https://github.com/search?utf8=%E2%9C%93&q=created%3A" + date + "+language%3A" + language +"&type=Repositories&ref=advsearch&l=" + language +"&l="

r = 0
i = 0

for l in language:
  language_n = language[r]
  print(language_n) #str
  
  today = datetime.date.today() # 今日の日付
  search_start_day = datetime.date(2018,1,1) # 検索開始日
  next_day_old = search_start_day + datetime.timedelta(days=i) # 初期設定
  
  while today > next_day_old:
    with open("error.csv", "a") as csvFile:
      fieldnames = ["Language", "date", "count"]
      writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
      
      next_day_old = search_start_day + datetime.timedelta(days=i) #start day 2018-01-01    data-type datetime
      print(next_day_old)
      day_data = str(next_day_old) # data-type  String

      ## スクレイピング
      url = " https://github.com/search?q=created%3A" + day_data + "+language%3A" + language_n + "&type=Repositories"
      driver.get(url)
      html = driver.page_source.encode('utf-8')
      soup = BeautifulSoup(html, "html.parser")

      div = soup.find("div", {"class":"d-flex flex-column flex-md-row flex-justify-between border-bottom pb-3 position-relative"})
      result = div.findChildren("h3")
      result = result[0]
      result = str(result)
      x = result[5:11] #repository count
      
      language_n = [language_n] # data-type  List
      day_data = [day_data] # data-type  List
      x = [x] # data-type  List
      writer.writerow({"Language":language_n, "date":day_data, "count":x})
      csvFile.close()
      
      i = i + 1 # 次の日へ
      language_n = language_n[0]
      
      #time.sleep(1)
      print(str(i) + "回目終わり")
      time.sleep(7)

  r = r + 1


"""
はじめの内はリポジトリ数をゲットできていますが、10回目付近でアクセスエラーに。結局は github.com ではなく api.github.com にアクセスする必要が。
JSONデータに比べてスクレイピングの方は、データ型の変換を頻繁に行う必要がありました。その分コード量も増えるので、わかりにくくなります。
JSONデータ、馴染みのない方が多いと思いますが、少しずつ慣れておくと作業時間の短縮やデータ活用に役立つと思います。
"""