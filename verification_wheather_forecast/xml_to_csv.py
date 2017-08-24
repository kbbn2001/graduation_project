import xml.etree.ElementTree as ET
import csv
import os


paths = ["대구_동구_신암동" , "서울_종로구_교남동" , "충북청주_흥덕구_복대동","강원도_평창군_대관령면" , "광주_북구_동림동", "부산_금정구_청룡동", "부산_금정구_장전2동", "부산_해운대구_중1동", "부산_영도구_동삼2동", "부산_사상구_감전동", "부산_동래구_복산동"]

for path in paths:
    filePath = './' + path
    fileList = os.listdir(filePath)

    for xmlFile in fileList:
        #fullPath = os.path.join(path, xmlFile)
        fullPath = './' + path + '/' + xmlFile
        print(fullPath)

        if ( os.path.isdir(fullPath)):
            continue
        print(fullPath)
        tree = ET.parse(fullPath)
        root = tree.getroot()


        # open a file for writing
        csvFilePath = path + '/csv/' +  xmlFile + '.csv'
        csvFilePath = csvFilePath.replace('.xml','')
        print(csvFilePath)
        directory = os.path.dirname(csvFilePath)

        try:
            os.stat(directory)
        except:
            os.mkdir(directory)

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

