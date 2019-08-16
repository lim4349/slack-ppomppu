from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from slacker import Slacker


token = '{input your token here}'
slack = Slacker(token)


def observe_ppomppu():
	korea_latest = 0
	abroad_latest = 0

	while True:
		driver1 = webdriver.Chrome('./chromedriver', chrome_options=options)
		driver1.implicitly_wait(3)

		driver2 = webdriver.Chrome('./chromedriver', chrome_options=options)
		driver2.implicitly_wait(3)

		url1 = 'https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu'
		url2 = 'https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu4'

		driver1.get(url1)
		driver2.get(url2)

		recent_index1 = WebDriverWait(driver1, 120).until(EC.presence_of_all_elements_located((By.TAG_NAME,
				'html > body > div > div > div > div> #revolution_main_table > tbody > tr.list1 > td.eng.list_vspace')))

		recent_index2 = WebDriverWait(driver2, 120).until(EC.presence_of_all_elements_located((By.TAG_NAME,
				'html > body > div > div > div > div> #revolution_main_table > tbody > tr.list1 > td.eng.list_vspace')))

		item_link1 = WebDriverWait(driver1, 120).until(EC.presence_of_all_elements_located((By.TAG_NAME,
											'#revolution_main_table > tbody > tr > td > table > tbody > tr > td > a')))

		item_link2 = WebDriverWait(driver2, 120).until(EC.presence_of_all_elements_located((By.TAG_NAME,
											'#revolution_main_table > tbody > tr > td > table > tbody > tr > td > a')))

		recent_title1 = driver1.find_element_by_class_name('list_title').text
		recent_title2 = driver2.find_element_by_class_name('list_title').text

		print('현재 최신 게시물 {} {}'.format(korea_latest, abroad_latest))
		print('국내 {} {} \n'
			  '해외 {} {}'.format(recent_index1[0].text, recent_title1, recent_index2[0].text, recent_title2))

		if korea_latest != int(recent_index1[0].text):
			korea_latest = int(recent_index1[0].text)
			attachments_dict1 = dict()
			attachments_dict1['pretext'] = '뽐뿌게시판 새 게시글 알림'
			attachments_dict1['title'] = str(recent_title1)  # 품목명
			attachments_dict1['title_link'] = str(item_link1[0].get_attribute('href'))  # 품목 링크
			attachments_dict1['fallback'] = str(recent_title1)  # 품목명

			attachments1 = [attachments_dict1]
			slack.chat.post_message(channel='{input your channel here}', text=None, attachments=attachments1, as_user=False,
									icon_emoji=':exclamation:', username='BOT')

		if abroad_latest != int(recent_index2[0].text):
			abroad_latest = int(recent_index2[0].text)
			attachments_dict2 = dict()
			attachments_dict2['pretext'] = '해외 뽐뿌 새 게시글 알림'
			attachments_dict2['title'] = str(recent_title2)  # 품목명
			attachments_dict2['title_link'] = str(item_link2[0].get_attribute('href'))  # 품목 링크
			attachments_dict2['fallback'] = str(recent_title2)  # 품목명
			attachments2 = [attachments_dict2]
			slack.chat.post_message(channel='{input your channel here}', text=None, attachments=attachments2, as_user=False,
								icon_emoji=':exclamation:', username='BOT')
		driver1.quit()
		driver2.quit()

		time.sleep(random.randrange(60, 120))


if __name__ == '__main__':
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('window-size=1920x1080')
	options.add_argument('disable-gpu')
	observe_ppomppu()
