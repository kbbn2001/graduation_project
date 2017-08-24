import csv
import os
import math
import matplotlib.pyplot as plt
import datetime

#한 예보에 대해 예보가 얼마나 정확한가 판단해보는 코드
def main():
    AWSCSVFile = open('./부산_금정구_장전2동/aws/201708.csv', 'r')
    AWSCSVReader = csv.reader(AWSCSVFile)
    AWSList = []
    for AWSRow in AWSCSVReader:
        AWSList.append(AWSRow)
    AWSList.pop(0)

    TeuclideanDistanceList = []
    ReuclideanDistanceList = []
    filePath = './부산_금정구_장전2동/csv/'
    fileList = os.listdir(filePath)

    xtick = []

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day - 1
    if (month < 10):
        month = "0" + str(month)
    if (day < 10):
        day = "0" + str(day)
    today = str(year) + str(month) + str(day)

    for file in fileList:
        fullPath = filePath + file
        xtick.append(file[0:12])
        forecastCSVFile = open(fullPath, 'r')
        forecastCSVReader = csv.reader(forecastCSVFile)
        forecastList = []

        for forecastRow in forecastCSVReader:
            forecastList.append(forecastRow)
        forecastList.pop(0)

        TeuclideanDistance = 0
        ReuclideanDistance = 0
        foreTList = []
        AWSTList = []
        #if ( )
        #예보 발표 기준으로 그날 예보의 온도, 강수량 차이를 기록.
        for forecastRow in forecastList:
            if(int(forecastRow[3]) > int(today)):
                break
            for i in range(len(AWSList)):
                AWSDate = AWSList[i][1][0:4] + AWSList[i][1][5:7] + AWSList[i][1][8:10]
                AWSTime = AWSList[i][1][11:13] + AWSList[i][1][14:16]
                if (forecastRow[2] == 'T3H'):
                    if (forecastRow[3] == AWSDate and forecastRow[4] == AWSTime):
                        foreTList.append(float(forecastRow[5]))
                        AWSTList.append(float(AWSList[i][2]))
                        # print('온도', abs(float(forecastRow[5]) - float(AWSRow[2])))
                        TeuclideanDistance += abs((float(AWSList[i][2]) + float(AWSList[i+1][2]) + float(AWSList[i+2][2]))/3 - float(forecastRow[5]))
                elif(forecastRow[2] == 'R06'):
                    if (forecastRow[3] == AWSDate and forecastRow[4] == AWSTime):
                        ReuclideanDistance += abs(float(AWSList[i][5]) - float(forecastRow[5]))

        TeuclideanDistanceList.append(TeuclideanDistance)
        ReuclideanDistanceList.append(ReuclideanDistance)

    #print(maxTime)
    plt.xticks(range(len(xtick)), xtick)
    plt.xticks(rotation = 90, fontsize = 8)
    plt.plot(TeuclideanDistanceList)
    #plt.plot(ReuclideanDistanceList, 'blue')
    plt.show()
    '''
        A = np.array([1,2,3,4,2,3])
        B = np.array([7,8,5,9,11,9])

        cost, path = DTW(foreTList, AWSTList, window = len(foreTList))
        print('Total Distance is ', cost)
        import matplotlib.pyplot as plt
        offset = 6
        plt.xlim([-1, max(len(foreTList), len(AWSTList)) + 1])
        plt.plot(foreTList)
        plt.plot(AWSTList)
        for (x1, x2) in path:
            plt.plot([x1, x2], [foreTList[x1], AWSTList[x2]])
        plt.show()
        '''

if __name__ == '__main__':
    main()


'''
AWSCSVFile = open('./20170807115658.csv', 'r')

forecastCSVReader = csv.reader(forecastCSVFile)
AWSCSVReader = csv.reader(AWSCSVFile)

forecastList = []
AWSList = []

for forecastRow in forecastCSVReader:
    forecastList.append(forecastRow)

for AWSRow in AWSCSVReader:
    AWSList.append(AWSRow)

for forecastRow in forecastList:
    for AWSRow in AWSList:
        AWSDate =  AWSRow[1][0:4] + AWSRow[1][5:7] + AWSRow[1][8:10]
        AWSTime = AWSRow[1][11:13] + AWSRow[1][14:16]
        if(forecastRow[3] == AWSDate and forecastRow[4] == AWSTime ):
            if(forecastRow[2] == 'T3H'):
                print('온도',abs(float(forecastRow[5]) - float(AWSRow[2])))
            if (forecastRow[2] == 'WSD'):
                print('풍향', abs(float(forecastRow[5]) - float(AWSRow[4])))



forecastCSVFile.close()
AWSCSVFile.close()
    '''