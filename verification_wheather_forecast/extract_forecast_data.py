import urllib.request
import datetime
import xml.etree.ElementTree as ET
import csv
import os

paths = ["부산_중구_대청동" , "대구_동구_신암동" , "서울_종로구_교남동" , "충북청주_흥덕구_복대동","강원도_평창군_대관령면" , "광주_북구_동림동", "부산_금정구_청룡동", "부산_금정구_장전2동", "부산_해운대구_중1동", "부산_영도구_동삼2동", "부산_사상구_감전동", "부산_동래구_복산동"]

# 부산 중구 대청동(97, 74), 대구 동구 신암동(89,91) , 서울 종로구 교남동(60, 127) , 충북 청주 흥덕구 복대동(68, 107) , 강원도 평찬군 대관령면(89, 130) , 광주 북구 동림동(59, 75)   :  종관기상관측(ASOS)
# 부산 금정구 청룡동(98, 78), 부산 금정구 장전2동(98, 77), 부산 해운대구 중1동(99, 75), 부산 영도구 동삼2동(98, 73), 부산 사상구 감전동(96, 75) 부산 동래구 복산동(98, 76)   :   방재기상관측(AWS)

times = ['0200', '0500', '0800', '1100', '1400', '1700', '2000' , '2300']

# 동네예보 발표 시간

nxs = [97, 89, 60, 68, 89, 59, 98, 98, 99, 98, 96, 98]
nys = [74, 91, 127, 107, 130, 75, 78, 77, 75, 73, 75, 76]


def getTime():
    year = datetime.datetime.now().year
    #month = datetime.datetime.now().month
    #day = datetime.datetime.now().day
    month = 8
    day = 1
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute

    if (month < 10):
        month = "0" + str(month)
    if (day < 10):
        day = "0" + str(day)
    if (hour < 10):
        hour = "0" + str(hour)
    if (minute < 10):
        minute = "0" + str(minute)

    return year, month, day, hour, minute


def dirCheck(path):
    directory = os.path.dirname(path)
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)


def getXMLData(index, year, month, day, time):
    url = 'http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastSpaceData'
    ServiceKey = 'uHNgVQh82tze7tpxOfBUAGU5D6hqqbVB5v3756zzuY4roqutD8W7Rao1h1ZZnbLXcyH8hcfLl4FOxpRb2%2Buu5g%3D%3D'
    base_date = str(year) + str(month) + str(day)
    base_time = time
    nx = nxs[index]
    ny = nys[index]
    numOfRows = '999'
    pageNo = '1'
    _type = 'xml'

    requestUrl = url + '?' + 'serviceKey=' + ServiceKey + \
                 '&base_date=' + base_date + \
                 '&base_time=' + base_time + \
                 '&nx=' + str(nx) + \
                 '&ny=' + str(ny) + \
                 '&numOfRows=' + numOfRows + \
                 '&pageNo=' + pageNo + \
                 '&_type=' + _type

    #request = urllib.request(requestUrl)
    #request.get_method = lambda: 'GET'
    response_body = urllib.request.urlopen(requestUrl).read()
    #print(response_body)
    return response_body


def saveXMLFile(xmlFilePath, xmlResult):
    dirCheck(xmlFilePath)
    xmlFile = open(xmlFilePath, 'w')
    xmlFile.write(xmlResult.decode("utf-8"))
    xmlFile.close()


def XMLToCSV(xmlFilePath, csvFilePath):
    tree = ET.parse(xmlFilePath)
    root = tree.getroot()

    dirCheck(csvFilePath)
    forecast_csv = open(csvFilePath, 'w', newline='')
    # create the csv writer object

    csvwriter = csv.writer(forecast_csv)
    forecast_head = []

    count = 0
    for member in root.findall('body'):
        for items in member.findall('items'):
            for item in items.findall('item'):
                forecast_data = []
                if count == 0:
                    baseDate = item.find('baseDate').tag
                    forecast_head.append(baseDate)
                    baseTime = item.find('baseTime').tag
                    forecast_head.append(baseTime)
                    category = item.find('category').tag
                    forecast_head.append(category)
                    fcstDate = item.find('fcstDate').tag
                    forecast_head.append(fcstDate)
                    fcstTime = item.find('fcstTime').tag
                    forecast_head.append(fcstTime)
                    fcstValue = item.find('fcstValue').tag
                    forecast_head.append(fcstValue)
                    nx = item.find('nx').tag
                    forecast_head.append(nx)
                    ny = item.find('ny').tag
                    forecast_head.append(ny)

                    csvwriter.writerow(forecast_head)
                    count = count + 1

                baseDate = item.find('baseDate').text
                forecast_data.append(baseDate)
                baseTime = item.find('baseTime').text
                forecast_data.append(baseTime)
                category = item.find('category').text
                forecast_data.append(category)
                fcstDate = item.find('fcstDate').text
                forecast_data.append(fcstDate)
                fcstTime = item.find('fcstTime').text
                forecast_data.append(fcstTime)
                fcstValue = item.find('fcstValue').text
                forecast_data.append(fcstValue)
                nx = item.find('nx').text
                forecast_data.append(nx)
                ny = item.find('ny').text
                forecast_data.append(ny)

                csvwriter.writerow(forecast_data)
    forecast_csv.close()


#this is main code
for i in range(len(paths)):
    year, month, day, hour, minute = getTime()
    currentTime = str(year) + str(month) + str(day)


    for time in times:
        xmlFilePath = "./" + paths[i] + "/" + currentTime + time + ".xml"
        xmlResult = getXMLData(i, year, month, day, time)
        saveXMLFile(xmlFilePath, xmlResult)

        # xml to csv convert
        csvFilePath = './' + paths[i] + '/csv/' + currentTime + time + '.csv'
        print(csvFilePath)
        print(xmlFilePath)
        XMLToCSV(xmlFilePath, csvFilePath)






