from bs4 import BeautifulSoup
import requests, lxml


def search_google(query,page_limit=1):

    params = {
        "q": query,
        "hl": "en",
        "gl": "in",
        "start": 0,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }


    page_num = 0

    search_results = {
        "results":[],
        "featured_ans": None

    }

    data = []

    while True:
        page_num += 1

        resp = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
        soup = BeautifulSoup(resp.content.decode('utf-8'), 'lxml')

        try:
            featured_ans = soup.select_one(".hgKElc").text
        except:
            featured_ans = None

        search_results['featured_ans'] = featured_ans


        for result in soup.select(".tF2Cxc"):

            title = result.select_one(".DKV0Md").text

            try:
                desc = result.select_one(".lEBKkf span").next_sibling.text.replace('\xa0', ' ').strip()
            except:
                desc = None

            links = result.select_one(".yuRUbf a")["href"]

            search_results['results'].append({
            "title": title,
            "links": links,
            "desc":desc
            })

        if page_num == page_limit:
            break

        if soup.select_one(".d6cvqb a[id=pnnext]"):
            params["start"] += 10
        else:
            break

    return search_results


# search_google("who is the ceo of google")
import html
import re
def escape_ansi(line):
    clean_output = re.sub(r"[\n\xa0\t]+", " ", line).strip()
    ansi_escape =re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
    return ansi_escape.sub('', html.escape(clean_output))

def get_website_article(url,title):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
    resp = requests.get(url,headers=headers)
    soup = BeautifulSoup(resp.content, 'lxml')
    article = ' '.join([p.get_text() for p in soup.find_all('p')])
    try:
        title = soup.select_one('title').text
    except:
        title = title
    # article = soup.get_text(separator=' ')
    return {"title": title, "body": escape_ansi(article)}


def compile_results_content(query):
    google_results = search_google(query)
    for result in google_results['results']:
        scraped = get_website_article(result['links'],result['title'])
        result['content'] = scraped['body']
        result['website_title'] = scraped['title']
    return google_results

# get_website_article("https://abcnews.com.co/obama-signs-executive-order-banning-national-anthem/")
# compile_results_content("Obama Signs Executive Order Banning National Anthem")