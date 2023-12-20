from bs4 import BeautifulSoup
import requests

headers = {
  'sec-ch-ua': '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
  'Referer': 'https://lumaticai.com/',
  'sec-ch-ua-mobile': '?1',
  'User-Agent':
  'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36',
  'sec-ch-ua-platform': '"Android"',
}


def scrape(link="https://lumaticai.com/"):
  resp = requests.get(link, headers=headers)

  soup = BeautifulSoup(resp.content, 'html5lib')

  print(soup.script.decompose())
  # print(soup.select("#mainContent")[0].get_text())

  with open('./Datasets/dataset_01.txt', 'w', encoding="utf-8") as f:
    f.write(" ".join(soup.select("#mainContent")[0].get_text().split()))

  print("SCRAPED")