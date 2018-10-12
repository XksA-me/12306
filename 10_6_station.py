# import re,requests
# def csm(y='黄石'):
#     url = 'https://im0x.com/C/detail/155'
#     date = requests.get(url)
#     html = date.text
#     Citycode =re.findall('[a-z]\|(.*?)\|(.*?)\|(.*?)\|(.*?)\|\d',html,re.S)
#     Citycode=str(Citycode)
#     print(Citycode)
#     Citycode=re.findall("('("+y+".*?), (.*?),(.*?),(.*?))",Citycode,re.S)
#     cou=len(Citycode)
#     if cou>0:
#         for i ,l in enumerate(Citycode):
#             image_list=l[0].split(",")
#             print ('%s：%s'%(i,eval(image_list[0])))
#         i=int(input("请选择："))
#         lit=list(Citycode)
#         chengshima=lit[2]
#         chengshima=eval(chengshima)
#         return chengshima
#     else:
#         return "0"

# from_station = input("请输入始发站点(WHN):")
# csm()

# import re
# a = '''asdfhellopass:
#     worldaf
#     '''
# b = re.findall('hello(.*?)world',a)
# c = re.findall('hello(.*?)world',a,re.S)
# print ('b is %s' %b)
# print ('c is %s' %c)
import requests
import re
import csv,os
import pandas as pd

def file_do(list_info):
	# 获取文件大小
	file_size = os.path.getsize(r'H:\city_station.csv')
	if file_size == 0:
		# 表头
		name = ['站点名','代号']
		# 建立DataFrame对象
		file_test = pd.DataFrame(columns=name, data=list_info)
		# 数据写入
		file_test.to_csv(r'H:\city_station.csv', encoding='utf_8_sig',index=False)
	else:
		with open(r'H:\city_station.csv','a+',encoding='utf_8_sig',newline='') as file_test :
			# 追加到文件后面
			writer = csv.writer(file_test)
			# 写入文件
			writer.writerows(list_info)
# def csm():
#     url = 'https://im0x.com/C/detail/1.55'
#     date = requests.get(url)
#     html = date.text
#     # 正则提取站点中文名和英文缩写
#     city_code =re.findall('[a-z]\|(.*?)\|(.*?)\|.*?\|.*?\|\d',html,re.S)
#     list_info = []
#     for i in range(len(city_code)):
#         list_0 = [city_code[i][0],city_code[i][1]]
#         print(list_0)
#         list_info.append(list_0)
#     file_do(list_info)
    # print(type(t0))
def read_csv():
		city_s = 'HSN'
		import csv
		city_station = []
		with open(r'H:\city_station.csv','r',encoding='utf_8_sig',newline='') as city_file:
			# 读文件
			reader = csv.reader(city_file)
			
			i = 0
			for row in reader:
				if i != 0:
					city_station.append([row[0],row[1]])
					# print(row[1])
				i = i + 1
			city_station_dict = {city_station[i][0]:city_station[i][1] for i in range(len(city_station))}
		#print(city_station_dict)
		
		if city_s in city_station_dict:
			print(city_station_dict[city_s])
# read_csv()
list = [1,2,3]
print(list[-3])