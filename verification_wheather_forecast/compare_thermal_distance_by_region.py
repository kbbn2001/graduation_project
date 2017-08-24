import csv
import os
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import datetime



gap_value = 0.7


def main():
    paths = ["부산_금정구_청룡동", "부산_금정구_장전2동", "부산_해운대구_중1동", "부산_영도구_동삼2동", "부산_사상구_감전동", "부산_동래구_복산동"]
    locations = ['939', '939', '937', '910', '904', '940']
    forecastTimes = ['0200', '0500', '0800', '1100', '1400', '1700', '2000', '2300']
    AWSTimes = ['0300', '0600', '0900', '1200', '1500', '1800', '2100', '0000']
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)
    y = [1,2,3,4,5,6]

    matrix = [] #동네예보와 AWS값 차이를 저장해놓을 공간.

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day - 1

    if (month < 10):
        month = "0" + str(month)
    if (day < 10):
        day = "0" + str(day)
    today = str(year) + str(month) + str(day)

    #AWS 파일 로드 (AWS파일에는 부산 모든지역의 AWS 자료가 담겨있음)
    AWSCSVPath = './AwsHourData.csv'
    AWSCSVFile = open(AWSCSVPath, 'r')
    AWSCSVReader = csv.reader(AWSCSVFile)
    AWSList = []
    for AWSRow in AWSCSVReader:
        AWSList.append(AWSRow)
    labels = AWSList.pop(0)
    labels[0] = 'location'
    labels[1] = 'date'
    labels[2] = 'thermal'
    labels[3] = 'wind_direction'
    labels[4] = 'wind_power'
    labels[5] = 'rain'
    labels.append("gap")
    #labels  는 csv파일 첫번째 row에 들어갈 자료. Decision tree 학습에 한글이 들어가면 오류가 나기 때문에 영어로 변환

    # Decision tree 학습결과를 지도(supervised)하기 위해 추가로 넣어줌
    for row in AWSList:
        row.append('0')

    #모아놓은 동네예보 자료들을 load 하여 AWS자료와 비교.
    for i in range(len(paths)):
        filePath = './' + paths[i] + '/csv/'
        fileList = os.listdir(filePath)

        distances = []

        for file in fileList:
            fullPath = filePath + file

            forecastCSVFile = open(fullPath, 'r')
            forecastCSVReader = csv.reader(forecastCSVFile)
            forecastList = []

            for forecastRow in forecastCSVReader:
                forecastList.append(forecastRow)



            #예보파일 기준으로 3시간뒤 값들을 비교
            flag = 0
            distance = 0
            for forecastRow in forecastList:
                if (flag == 0 and forecastRow[2] == 'T3H'):
                    if(int(forecastRow[3]) > int(today)):
                        break;
                    for j in range(len(AWSList)):
                        if( AWSList[j][0] == locations[i]):
                            #print(AWSList[j])
                            AWSDate = AWSList[j][1][0:4] + AWSList[j][1][5:7] + AWSList[j][1][8:10]
                            AWSTime = AWSList[j][1][11:13] + AWSList[j][1][14:16]
                            if (forecastRow[3] == AWSDate and forecastRow[4] == AWSTime):
                                if (AWSList[j][2] == ''):
                                    AWSList[j][2] = AWSList[j - 1][2]
                                if (AWSList[j + 1][2] == ''):
                                    AWSList[j + 1][2] = AWSList[j][2]
                                if (AWSList[j + 2][2] == ''):
                                    AWSList[j + 2][2] = AWSList[j + 1][2]
                                distance += abs(((float(AWSList[j][2]) + float(AWSList[j+1][2]) + float(AWSList[j+2][2]))/3) - float(forecastRow[5]))
                                if( forecastRow[4] == '2100'):
                                    distances.append(distance)
                                    distance = 0
                                flag = 1
                                break
        matrix.append(distances)

    #print(matrix)
    for i in range(len(matrix)):
        for j in range(len(matrix[i]) - 1):
            if( matrix[i][j+1] - matrix[i][j] > gap_value  ):   #gap_value 이상 차이가 증가하는 경우
                print(paths[i],locations[i],j)
                gapDate = '2017-08-'
                if((j+1) < 10):
                    gapDate += '0' + str(j+1)
                else:
                    gapDate += str(j+1)
                for row in AWSList:
                    if(row[0] == locations[i] and row[1][0:10] == gapDate): #차이가 나는부분의 날짜와 일치하는 AWS데이터에 1 이라고 label을 붙임
                        row[6] = '1'
                        #print(row)

    # decision Tree에 사용 될 데이터를 저장하는 부분
    DTFilePath = './total_aws.csv'
    f = open(DTFilePath, 'w', newline='')
    wr = csv.writer(f)
    labels.insert(0,'number')
    wr.writerow(labels)
    index = 1
    for AWSRow in AWSList:
        AWSRow.insert(0,index)
        if (AWSRow[4] == ''):
            AWSRow[4] = '-1'
        if (AWSRow[5] == ''):
            AWSRow[5] = '-1'
        if (AWSRow[6] == ''):
            AWSRow[6] = '-1'
        AWSRow[2] = AWSRow[2][11:13]
        #print(AWSRow)
        if (AWSRow[2][1] == ':'):
            AWSRow[2] = '0' + AWSRow[2][0]
        AWSRow[2] = int(int(AWSRow[2]) / 6)
        wr.writerow(AWSRow)
        index = index + 1
    f.close()

    for i in range(len(paths)):
        DTFilePath = './' + paths[i] + '_label_aws.csv'
        f = open(DTFilePath, 'w', newline='')
        wr = csv.writer(f)
        wr.writerow(labels)
        index = 1
        for AWSRow in AWSList:
            if(AWSRow[1] == locations[i]):
                AWSRow[0] = index
                wr.writerow(AWSRow)
                index += 1
        f.close()

    for i in range(len(paths)):
        plt.plot(matrix[i], label=paths[i])
        plt.ylim([0,5])
        plt.legend()
        plt.savefig('./graph/' + paths[i] + '.png')
        plt.clf()

    for i in range(len(matrix)):
        plt.plot(matrix[i], label=paths[i])
    plt.ylim([0, 4])
    plt.legend()
    plt.savefig('./graph/total.png')
    plt.show()


if __name__ == '__main__':
    main()

