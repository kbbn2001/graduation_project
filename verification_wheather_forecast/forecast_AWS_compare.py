import csv
import os
import math
import matplotlib.pyplot as plt

import copy
maxint = 2**32 - 1
#특정 지역의 3시간뒤 예측 온도가 얼마나 정확한지 테스트하는 코드

'''
def DTW(A, B, window=maxint, d=lambda x, y: abs(x - y)):
    # 비용 행렬 초기화
    A, B = np.array(A), np.array(B)
    M, N = len(A), len(B)
    cost = maxint * np.ones((M, N))

    # 첫번째 로우,컬럼 채우기
    cost[0, 0] = d(A[0], B[0])
    for i in range(1, M):
        cost[i, 0] = cost[i - 1, 0] + d(A[i], B[0])

    for j in range(1, N):
        cost[0, j] = cost[0, j - 1] + d(A[0], B[j])
    # 나머지 행렬 채우기
    for i in range(1, M):
        for j in range(max(1, i - window), min(N, i + window)):
            choices = cost[i - 1, j - 1], cost[i, j - 1], cost[i - 1, j]
            cost[i, j] = min(choices) + d(A[i], B[j])

    # 최적 경로 구하기
    n, m = N - 1, M - 1
    path = []

    while (m, n) != (0, 0):
        path.append((m, n))
        m, n = min((m - 1, n), (m, n - 1), (m - 1, n - 1), key=lambda x: cost[x[0], x[1]])

    path.append((0, 0))
    return cost[-1, -1], path
'''


def main():
    forecastTimes = ['0200', '0500', '0800', '1100', '1400', '1700', '2000', '2300']
    AWSTimes = ['0300', '0600', '0900', '1200', '1500', '1800', '2100', '0000']
    AWSCSVFile = open('./부산_금정구_장전2동/aws/201708.csv', 'r')
    AWSCSVReader = csv.reader(AWSCSVFile)
    AWSList = []
    for AWSRow in AWSCSVReader:
        AWSList.append(AWSRow)
    TeuclideanDistanceList = []
    ReuclideanDistanceList = []
    filePath = './부산_금정구_장전2동/csv/'
    fileList = os.listdir(filePath)
    maxIndex = 0
    forecastThermalList = []
    AWSThermalList = []
    AWSThermalList2 = []
    for file in fileList:
        fullPath = filePath + file

        forecastCSVFile = open(fullPath, 'r')
        forecastCSVReader = csv.reader(forecastCSVFile)
        forecastList = []

        for forecastRow in forecastCSVReader:
            forecastList.append(forecastRow)



        #예보파일 기준으로 3시간뒤 값들을 비교
        forecastDate = file[0:12]
        for i in range(len(forecastTimes)):
            if ( forecastTimes[i] == forecastDate[8:]):
                forecast3 = file[0:8] + AWSTimes[(i+1)%len(forecastTimes)]
        flag = 0
        for forecastRow in forecastList:
            #print(forecast3[0:8] ,forecast3[8:] )

            if (forecastRow[2] == 'T3H' and forecastRow[3] == forecast3[0:8] and forecastRow[4] == forecast3[8:]):
                forecastThermalList.append(float(forecastRow[5]))
                for i in range(len(AWSList)):
                    AWSDate = AWSList[i][1][0:4] + AWSList[i][1][5:7] + AWSList[i][1][8:10]
                    AWSTime = AWSList[i][1][11:13] + AWSList[i][1][14:16]
                    if (forecastRow[3] == AWSDate and forecastRow[4] == AWSTime):
                        AWSThermalList.append((float(AWSList[i][2]) + float(AWSList[i+1][2]) + float(AWSList[i+2][2]))/3)
                        AWSThermalList2.append(float(AWSList[i][2]))
                        break

    #print(AWSThermalList)
    plt.plot(AWSThermalList, 'red')
    plt.plot(AWSThermalList2, 'black')
    plt.plot(forecastThermalList, 'blue')
    plt.show()
    '''
        TeuclideanDistance = 0
        ReuclideanDistance = 0
        foreTList = []
        AWSTList = []
        #예보 발표 기준으로 그날 예보의 온도, 강수량 차이를 기록.
        for forecastRow in forecastList:
            for AWSRow in AWSList:
                AWSDate = AWSRow[1][0:4] + AWSRow[1][5:7] + AWSRow[1][8:10]
                AWSTime = AWSRow[1][11:13] + AWSRow[1][14:16]
                if (forecastRow[2] == 'T3H'):
                    if (forecastRow[3] == AWSDate and forecastRow[4] == AWSTime):
                        foreTList.append(float(forecastRow[5]))
                        AWSTList.append(float(AWSRow[2]))
                        # print('온도', abs(float(forecastRow[5]) - float(AWSRow[2])))
                        TeuclideanDistance += abs(float(AWSRow[2]) - float(forecastRow[5]))
                elif(forecastRow[2] == 'R06'):
                    if (forecastRow[3] == AWSDate and forecastRow[4] == AWSTime):
                        ReuclideanDistance += abs(float(AWSRow[5]) - float(forecastRow[5]))
        #print(fullPath, math.sqrt(TeuclideanDistance))
        TeuclideanDistanceList.append(TeuclideanDistance)
        ReuclideanDistanceList.append(ReuclideanDistance)
        '''
    #print(maxTime)
    #plt.plot(maxAWSList)
    #plt.plot(maxforeList)
    #plt.plot(TeuclideanDistanceList, 'red')
    #plt.plot(ReuclideanDistanceList, 'blue')
    #plt.show()
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