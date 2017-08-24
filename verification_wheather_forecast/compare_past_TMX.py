import csv
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import datetime


paths = ["장전2동", "중1동", "동삼2동", "감전동", "복산동"]

forecastTMX = []
AWSTMX = []

for i in range(len(paths)):
    filePath = './' + paths[i]+ '/'
    fileList = os.listdir(filePath)

    f_TMX = []
    aws_TMX = []

    AWSCSVPath = './' + paths[i] + '_AWS.csv'
    AWSCSVFile = open(AWSCSVPath, 'r')
    AWSCSVReader = csv.reader(AWSCSVFile)
    AWSList = []
    index = 24
    count = 0
    max = 0.0
    for AWSRow in AWSCSVReader:
        AWSList.append(AWSRow)

    labels = AWSList.pop(0)
    for AWSRow in AWSList:
        #print(AWSRow)
        if ( AWSRow[2] == ''):
            AWSRow[2] = 0
        if(float(AWSRow[2]) > max):
            max = float(AWSRow[2])
        count = count + 1
        if(count == index):
            count = 0
            aws_TMX.append(max)
            max = 0
    AWSTMX.append(aws_TMX)

    for file in fileList:
        fullPath = filePath + file

        forecastCSVFile = open(fullPath, 'r')
        forecastCSVReader = csv.reader(forecastCSVFile)
        forecastList = []

        for forecastRow in forecastCSVReader:
            if(len(forecastRow) == 1):
                continue
            if(forecastRow[1] == '1100' and forecastRow[2] == '+4'):
                f_TMX.append(forecastRow[3])
    forecastTMX.append(f_TMX)

    print(forecastTMX)
    print(AWSTMX)

compare = []
for i in range(len(forecastTMX)):
    list = []
    for j in range(len(forecastTMX[i])):
        list.append(abs(float(forecastTMX[i][j]) - AWSTMX[i][j]))
    compare.append(list)

for i in range(len(compare)):
    plt.plot(compare[i], label=paths)
plt.show()