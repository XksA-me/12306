'''
date : 2018.10.12
author : 极简XksA
goal : 登录12306，实现抢票
'''

import requests
import os
from fake_useragent import UserAgent
from prettytable import PrettyTable

from config import Password,Account_number

class login():
	# 1.1 cookie保持
	session = requests.Session()
	# 请求头，反爬伪装
	headers = {
	    # "User-Agent": UserAgent(verify_ssl=False).random,
	    "Host":"kyfw.12306.cn",
	    "Referer":"https://kyfw.12306.cn/otn/passport?redirect=/otn/"
	}
	
	# 1.获取登录
	def login_f(self):
		login_url = 'https://kyfw.12306.cn/otn/login/init'
		# 1.2 get请求
		login_response = self.session.get(login_url,headers = self.headers)
		
	def login_captcha(self):
		# 2.获取并破解验证操作
		# 2.1 下载验证图片
		captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.8854830207575652'
		captcha_response = self.session.get(captcha_url,headers = self.headers)
		# 文件保存路径
		image_path = os.path.abspath('image') + '/captcha_image.jpg'
		# 以二进制写入文件
		with open(image_path,'wb') as image_file:
			image_file.write(captcha_response.content)
		# 2.2 验证
		check_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
		positions = input("请输入验证码: ")
		# 发送验证码
		data = {
			"answer": positions,
			"login_site": "E",
			"rand": "sjrand"
		}
		check_response = self.session.post(check_url,data = data,headers = self.headers)
		check_result = check_response.json()
		# 测试发现，result_code = 4 时，表示验证成功
		
		if not check_result['result_code'] == '4':
			exit("验证失败")
			
		print(check_result)
		
		
	def login_check(self):
		# 3.开始登录操作
		login_check_url = 'https://kyfw.12306.cn/passport/web/login'
		login_check_data = {
		'username': Account_number,
		'password': Password,
		'appid': 'otn'
		}
		login_check_response = self.session.post(login_check_url,data=login_check_data,headers = self.headers)
		print(login_check_response.json())
		
		# 4. 获取权限 authority
		# 4.1 获取权限密钥：newapptk
		uamtk_data = {
			"appid":"otn"
		}
		uamtk_url = "https://kyfw.12306.cn/passport/web/auth/uamtk"
		uamtk_response = self.session.post(uamtk_url, headers=self.headers, data=uamtk_data)
		uamtk_dict = uamtk_response.json()
		newapptk = uamtk_dict['newapptk']
		# print(uamtk_dict['newapptk'])
		
		# 4.2 传递密钥，获取权限
		uamauthclient_data = {
			"tk" : newapptk
		}
		uamauthclient_url = "https://kyfw.12306.cn/otn/uamauthclient"
		uamauthclient_response = self.session.post(uamauthclient_url, headers=self.headers, data=uamauthclient_data)
		
		# 5 正真的登录
		initMy_url = "https://kyfw.12306.cn/otn/index/initMy12306"
		initMy_response = self.session.get(initMy_url, headers=self.headers)
		my_name = initMy_response.text.find("张建华")
		if not my_name == -1:
			print("用户已经登录成功")
	
	def conversion_en(self,from_station,to_station):
		import csv
		city_station = []
		with open(r'H:\city_station.csv', 'r', encoding='utf_8_sig', newline='') as city_file:
			# 读文件
			reader = csv.reader(city_file)
			
			i = 0
			for row in reader:
				if i != 0:
					city_station.append([row[0], row[1]])
				# print(row[1])
				i = i + 1
			city_station_dict = {city_station[i][0]: city_station[i][1] for i in range(len(city_station))}
		# print(city_station_dict)
		
		if from_station in city_station_dict:
			from_station_en = city_station_dict[from_station]
		else:
			print("出发站输入错误！")
		if to_station in city_station_dict:
			to_station_en = city_station_dict[to_station]
		else:
			print("目的站输入错误！")
		return [from_station_en,to_station_en]
	
	def conversion_ch(self, station01, station02):
		import csv
		city_station = []
		with open(r'H:\city_station.csv', 'r', encoding='utf_8_sig', newline='') as city_file:
			# 读文件
			reader = csv.reader(city_file)
			
			i = 0
			for row in reader:
				if i != 0:
					city_station.append([row[0], row[1]])
				# print(row[1])
				i = i + 1
			city_station_dict = {city_station[i][1]: city_station[i][0] for i in range(len(city_station))}
		# print(city_station_dict)
		
		if station01 in city_station_dict:
			station01_ch = city_station_dict[station01]
		else:
			print("%s站点不存在"%station01)
		if station02 in city_station_dict:
			station02_ch = city_station_dict[station02]
		else:
			print("%s站点不存在！"%station02)
		return [station01_ch, station02_ch]
	
	# 解析json文件数据
	def jx(self, search_result):
		import re
		tick_res = search_result['data']['result']
		search_res = len(tick_res)
		checi = []
		from_station = []
		to_station = []
		from_time = []
		to_time = []
		total_time = []
		from_datetime = []
		no_seat = []
		high_soft = []
		common_soft = []
		special_seat = []
		move_down = []
		first_seat = []
		second_seat = []
		hard_seat = []
		for each in tick_res:
			need_data = re.split(r'\|预订\|', each)[1]
			need_data = need_data.split('|')
			# print(need_data)
			# print(len(need_data))
			checi.append(need_data[1])
			# print(checi)
			conversion_ch_reslut = self.conversion_ch(need_data[2], need_data[3])
			from_station.append(conversion_ch_reslut[0])
			to_station.append(conversion_ch_reslut[1])
			from_time.append(need_data[6])
			to_time.append(need_data[7])
			total_time.append(need_data[8])
			from_datetime.append(need_data[11])
			high_soft.append(need_data[-16])
			common_soft.append(need_data[-14])
			no_seat.append(need_data[-11])
			move_down.append(need_data[-4])
			special_seat.append(need_data[-5])
			first_seat.append(need_data[-6])
			second_seat.append(need_data[-7])
			hard_seat.append(need_data[-9])
		return search_res, checi, from_station, to_station, from_time, to_time, total_time, from_datetime, high_soft, common_soft, no_seat, move_down, special_seat, second_seat, first_seat, hard_seat
	
	# 将提取到的数据用图表的格式打印出来
	# 这里用到模块PrettyTable
	# 安装方法：cmd下 ：
	#          pip install prettytable
	def print_TicketInfo(self, search_result, raw_from_station, raw_to_station):
		search_res,checi, from_station, to_station, from_time, to_time, total_time, from_datetime, high_soft, common_soft, no_seat, move_down, special_seat, second_seat, first_seat, hard_seat = self.jx(
			search_result)
		
		pt = PrettyTable(['车次','始发站','终点站','出发时间','到达时间','历时','出发日期','软卧','无座','动卧', '商务座', '一等座', '二等座', '硬卧'])
		pt.align["车次"] = "l"
		pt.padding_width = 1
		print("---------从" + str(raw_from_station) + '到' + str(raw_to_station) + '共' + str(
			search_res) + '个车次' + '---------')
		for i in range(len(checi)):
			pt.add_row([checi[i],from_station[i],to_station[i],from_time[i],to_time[i],total_time[i],from_datetime[i],common_soft[i],no_seat[i],move_down[i],special_seat[i],second_seat[i],first_seat[i],hard_seat[i]])
		pt.reversesort = True
		return pt
	
	# 车票查询
	def search_ticket(self):
		train_date = input("请输入查询时间(2018-10-12):")
		from_city_station = input("请输入始发站点(中文全称:黄石北):")
		to_city_station = input("请输入终点站(中文全称:北京西):")
		en_station = self.conversion_en(from_city_station,to_city_station)
		search_ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/queryO?leftTicketDTO.train_date={0}&leftTicketDTO.from_station={1}&leftTicketDTO.to_station={2}&purpose_codes=ADULT'.format(train_date,en_station[0],en_station[1])
		# print(search_ticket_url)
		headers = {
			"Host": "kyfw.12306.cn",
			"Referer": "https://kyfw.12306.cn/otn/leftTicket/init"
		}
		# self.session
		search_response = requests.get(search_ticket_url,headers = headers)
		search_result = search_response.json()
		pt0 = self.print_TicketInfo(search_result,from_city_station,to_city_station)
		print(pt0)
		
	
	
t0 = login()
t0.search_ticket()