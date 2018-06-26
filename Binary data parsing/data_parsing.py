import struct

student_list = []
kim_list = []
lee_list = []
num_list = []
person_list = []
name_list =[]

f=open("/home/miji/studentinfo.txt",'rb')
for x in range(45):
	dic = {}

	student_num = f.read(1)
	stuNum = struct.unpack("!1b",student_num)

	name = f.read(9)
	stuName = name.decode("utf-8")

	grade = f.read(2)
	stuGrade = struct.unpack("!1h",grade)

	age = f.read(4)
	stuAge = struct.unpack("!1i",age)
	
	print("학번은 " + str(stuNum[0]) + " 이름은 " + stuName + " 학점은 " + str(stuGrade[0]) + " 나이는 " + str(stuAge[0]))

	dic['Studendt_Number'] = stuNum
	dic['NAME'] = stuName
	dic['GRADE'] = stuGrade
	dic['AGE'] = stuAge
	
	student_list.append(dic) #list

	if '김' in stuName[0]:
		kim_list.append(stuAge[0])

	if '이' in stuName[0]:
		lee_list.append(stuAge[0])
	if '이' in stuName[0]:
		person_list.append(dic)
	

	num_list.append(stuNum[0])

def largest(list):
	maxValue = list[0]
	for i in range (len(list)):
		if list[i] > maxValue:
			maxValue = list[i]
	return maxValue

def name(list):
	for i in person_list:	
		if i['AGE'][0]==largest(lee_list):
			name = i['NAME']
			name_list.append(name)
	return name_list

#print(person_list)
print("이 씨중 가장 많은나이를 가진 사람은 {} 나이는 {}".format(name(name_list),largest(lee_list)))


def average(list):
	num = 0
	for i in range (len(list)):
		num = num + list[i]
	return (num)/len(list)

print("김씨들의 평균 나이는 : {}".format(average(kim_list)))


def counting(list):
	count = {}	
	for i in list:
		try: count[i] += 1
		except: count[i] = 1
	return count

print("각 학번 : 학생인원 수  {}".format(counting(num_list)))




