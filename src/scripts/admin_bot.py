#todo: add project_dir = os.path.dirname(os.path.abspath(__file__)) for all hardcoded paths
from selenium import webdriver
import os, time, threading

creds = [
	['admin1','adminpass1','csrf1'],
	['admin2','adminpass2','csrf2'],
	['admin3','adminpass3','csrf3'],
	['admin4','adminpass4','csrf4'],
	['admin5','adminpass5','csrf5'],
	['admin6','adminpass6','csrf6']
]

creds2 = [
	['admin7','adminpass7','click1'],
	['admin8','adminpass8','click2']
]

project_dir = os.path.dirname(os.path.abspath(__file__))
bot_file = project_dir+'/../bot_ip.txt'

while not os.path.exists(bot_file):
    time.sleep(2)

if os.path.isfile(bot_file):
	with open(bot_file) as f:
		ip_addr = f.readlines()[0]

target_file_path = project_dir+'/../another_server/'
attacker_domain = 'http://'+ip_addr+':8000'
victim_domain = 'http://'+ip_addr

def read_messages(username, password, chall):
	driver.get(victim_domain+'/info/'+chall)
	driver.get(victim_domain+'/login?chall='+chall)
	driver.implicitly_wait(10)
	user = driver.find_element_by_id('username')
	pwd = driver.find_element_by_id('password')
	submit = driver.find_element_by_id('submit')

	user.send_keys(username)
	pwd.send_keys(password)
	submit.click()
	driver.get(victim_domain+'/admin_messages')
	driver.get(victim_domain+'/logout')


def open_pages(username, password, chall):
	driver.get(victim_domain+'/info/'+chall)
	driver.get(victim_domain+'/login?chall='+chall)
	driver.implicitly_wait(10)
	user = driver.find_element_by_id('username')
	pwd = driver.find_element_by_id('password')
	submit = driver.find_element_by_id('submit')

	user.send_keys(username)
	pwd.send_keys(password)
	submit.click()
	
	chall_file = "%s%s.txt" % (target_file_path,chall)
	
	with open(chall_file) as f:
		external_links = f.readlines()

	for link in external_links:
		driver.get(attacker_domain+link)
		content = driver.find_element_by_tag_name('body').get_attribute('innerHTML')
		print content

	open(chall_file,'w').close()
	driver.get(victim_domain+'/logout')
	

def click_single():
	chall = 'click1'
	driver.get(victim_domain+'/info/'+chall)
	driver.get(victim_domain+'/login?chall='+chall)
	driver.implicitly_wait(10)
	user = driver.find_element_by_id('username')
	pwd = driver.find_element_by_id('password')
	submit = driver.find_element_by_id('submit')

	user.send_keys('admin7')
	pwd.send_keys('adminpass7')
	submit.click()
	
	chall_file = "%s%s.txt" % (target_file_path,chall)
	
	with open(chall_file) as f:
		external_links = f.readlines()

	for link in external_links:
		try:
			driver.get(attacker_domain+link)
			button1 = driver.find_element_by_id('button1')
			webdriver.ActionChains(driver).move_to_element(button1).click().perform()
		except:
			pass

	open(chall_file,'w').close()
	driver.get(victim_domain+'/logout')


def click_double():
	chall = 'click2'
	driver.get(victim_domain+'/info/'+chall)
	driver.get(victim_domain+'/login?chall='+chall)
	driver.implicitly_wait(10)
	user = driver.find_element_by_id('username')
	pwd = driver.find_element_by_id('password')
	submit = driver.find_element_by_id('submit')

	user.send_keys('admin8')
	pwd.send_keys('adminpass8')
	submit.click()
	
	chall_file = "%s%s.txt" % (target_file_path,chall)
	
	with open(chall_file) as f:
		external_links = f.readlines()

	for link in external_links:
		try:
			driver.get(attacker_domain+link)
			button1 = driver.find_element_by_id('button1')
			webdriver.ActionChains(driver).move_to_element(button1).click().perform()
			button2 = driver.find_element_by_id('button2')
			webdriver.ActionChains(driver).move_to_element(button2).click().perform()
		except:
			pass

	open(chall_file,'w').close()
	driver.get(victim_domain+'/logout')


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.binary_location = "/usr/bin/chromium-browser"
driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=chrome_options, service_args=['--verbose', '--log-path=/tmp/chromedriver.log'])


def read_page_bot():
	print "[*] Admin is reading messages"
	for cred in creds:
		read_messages(cred[0],cred[1],cred[2])
	print "[*] Admin is paused"


def open_page_bot():
	print "[*] Admin is opening pages"
	for cred in creds:
		open_pages(cred[0],cred[1],cred[2])
	print "[*] Admin is sleeping"


def start_bot():
	threading.Timer(60, start_bot).start()
	read_page_bot()
	time.sleep(3)
	open_page_bot()
	time.sleep(3)
	click_single()
	time.sleep(3)
	click_double()

start_bot()
