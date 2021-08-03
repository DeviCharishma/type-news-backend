import requests
import flask
from flask import Flask
from bs4 import BeautifulSoup as bs
from flask import jsonify

app = Flask(__name__)

def get_news():
    res = requests.get("https://timesofindia.indiatimes.com/")
    soup = bs(res.text,"html.parser")
    news = []
    for x in soup.select(".nEjlO")[0].select("figure"):
        if len(x.select("a")) != 0 and len(x.select(".suxSu")) == 0 and len(x.select("a")[0]['href'].split('/')) > 0:
            if "articleshow" in x.select("a")[0]['href'].split('/'):
                res1 = requests.get(x.select("a")[0]['href'])
                soup1 = bs(res1.text,"html.parser")
                if len(soup1.select(".HNMDR")) > 0:
                    try:
                        news_article = {'heading':soup1.select(".HNMDR")[0].text.strip(),'paras':[]}
                        temp3 = soup1.select("._s30J")[0]
                        for div in temp3.find_all("div"): 
                            div.decompose()
                        temp3 = temp3.text.strip()
                        temp3 = temp3.split("\n\n")
                        for x in temp3:
                            para = ""
                            indx = 0
                            while len(x) > 3 and len(para) < 40 and len(x.split(".")) > indx:
                                para += x.split(".")[indx] + '.'
                                indx += 1
                            if len(para) > 3:
                                news_article['paras'].append(para.replace('\n',''))
                                news.append(news_article)
                    except:
                        i = 1
    response = flask.jsonify({"news": [news]})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/')
def news():
    return get_news()

if __name__ == "__main__":
        app.run(debug=False)