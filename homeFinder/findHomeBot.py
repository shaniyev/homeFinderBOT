import requests
from bs4 import BeautifulSoup
import time

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update


def getHTML(url):
	r = requests.get(url)
	print(r)
	return r.text

def sendToBot(data):
	#greet_bot.send_message('9680894', data)
    greet_bot.send_message('-315316517', data) 


def getPageData(html, lastURL):
	soup = BeautifulSoup(html, 'html.parser')
	ads = soup.find('section',class_ = 'a-list a-search-list a-list-with-favs').find_all('a', class_='a-card__image')
	#title, price, address, description, url
	lurl = 'https://krisha.kz' + ads[0].get('href')
	for ad in ads:
		try:
			url = 'https://krisha.kz' + ad.get('href')
		except:
			url = ''
		
		if lastURL == url:
			return lurl
		else:
			sendToBot(url)
	return lurl
	
greet_bot = BotHandler('708963627:AAEEdHSvhjiZj4H7j7dKrsfw6TwhmB8VmAM')

def main():
    m = 0
    lastURL = 'https://krisha.kz/a/show/51004425'
    base_url = 'https://krisha.kz/prodazha/kvartiry/nur-sultan/?das[who]=1'
    while True:
        print('Try', m // 120)
        print('Minutes pass:', m // 60)
        html = getHTML(base_url)
        lastURL = getPageData(html, lastURL)
        print(lastURL)
        time.sleep(120)
        m += 120


if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()