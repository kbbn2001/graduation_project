import csv
import datetime as dt
import glob
from bgfunc import dirCheck

def data_refine(months,dic_elem,unit,dic_tloc):
    dirCheck("./data/integrated_data/")

    fpath = "./data/integrated_data/*_AWS.csv"
    flist = glob.glob(fpath)
    AWSList={}
    monList={}
    day_max_thermal = []
    day_max = 0.0
    taget='PokPoong'
    paths = ["부산(레)", "사상", "영도", "기장", "해운대", "부산진", "금정구", "동래", "북구", "대연", "사하", "남항", "북항"]
    for i in range(len(dic_tloc)):
        if dic_tloc[i]:
            taget=paths[i]
            #print(taget)
    templist = flist.copy()
    flag = False
    for i in range(len(flist)):
        if taget in flist[i]:
            templist[0] = flist[i]
            flag = True
        else:
            if flag:
                templist[i] = flist[i]
            else:
                templist[i + 1] = flist[i]
    flist=templist.copy()
    for j in range(len(flist)):
        AWSCSVFile = open(flist[j], 'r')
        AWSCSVReader = csv.reader(AWSCSVFile)
        pre_AWSList = []
        for AWSRow in AWSCSVReader:
            pre_AWSList.append(AWSRow)
        #모든 _aws.csv의 행이 pre_awslist에.
        AWSList[j]=[]
        monList[j]=[]
        hours = range(24)
        first_flag = False
        time_index = 0
        #print(j,'a site')
        for i in range(len(pre_AWSList)):
            if(first_flag == False):
                first_flag = True
                continue

            #print(j,i, 'b site')
            if( int(pre_AWSList[i][1][11:13]) != hours[(time_index%24)]):
                pre_date = dt.datetime.strptime(pre_AWSList[i - 1][1], '%Y-%m-%d %H:%M')
                i_date = dt.datetime.strptime(pre_AWSList[i][1], '%Y-%m-%d %H:%M')
                date_gap = i_date - pre_date

                loop_index = date_gap.days * 24 + int(date_gap.seconds / 3600) - 1

                for k in range(loop_index):
                    AWSList[j].append(pre_AWSList[i - 1])
                    time_index += 1

            AWSList[j].append(pre_AWSList[i])
            time_index += 1
        for i in AWSList[j]:
            if (i[1][5:7] in months):
                monList[j].append(i)
        #print(j, 'd site')
        index = 0

        if taget in flist[j]:

            for i in range(len(monList[j])):
                if (index >= 24):
                    index = 0
                    day_max_thermal.append(day_max)
                    day_max = 0.0
                if (monList[j][i][2] == ''):
                    monList[j][i][2] = monList[j][i - 1][2]

                if (monList[j][i][3] == ''):
                    monList[j][i][3] = monList[j][i - 1][3]
                if (monList[j][i][4] == ''):
                    monList[j][i][4] = monList[j][i - 1][4]
                if (monList[j][i][5] == ''):
                    monList[j][i][5] = monList[j][i - 1][5]
                elif (float(monList[j][i][2]) > day_max):
                    day_max = float(monList[j][i][2])
                index += 1
            #break
        else:
            for i in range(len(monList[j])):
                if (monList[j][i][2] == ''):
                    monList[j][i][2] = monList[j][i - 1][2]

                if (monList[j][i][3] == ''):
                    monList[j][i][3] = monList[j][i - 1][3]
                if (monList[j][i][4] == ''):
                    monList[j][i][4] = monList[j][i - 1][4]
                if (monList[j][i][5] == ''):
                    monList[j][i][5] = monList[j][i - 1][5]

        #print(j, 'e site')
    #augList[j]
    #print('f site')
    # 데이터 생성
    train_list = []

    for i in range(len(day_max_thermal) - 45):
        train_item = []
        for m in range(24*unit):
            for j in range(len(flist)):
                if dic_elem[1]:
                    train_item.append(float(monList[j][i * 24 + m][2]))
                if dic_elem[2]:
                    train_item.append(float(monList[j][i * 24 + m][3]))
                if dic_elem[3]:
                    train_item.append(float(monList[j][i * 24 + m][4]))
                if dic_elem[0]:
                    train_item.append(float(monList[j][i * 24 + m][5]))

        train_item.append(float(day_max_thermal[i + unit]))

        train_list.append(train_item)
    #print('j site')
    # 테스팅 데이터 생성
    test_list = []
    for i in range(len(day_max_thermal) - 45, len(day_max_thermal) - 30):
        test_item = []
        for m in range(24*unit):
            for j in range(len(flist)):
                if dic_elem[1]:
                    test_item.append(float(monList[j][i * 24 + m][2]))
                if dic_elem[2]:
                    test_item.append(float(monList[j][i * 24 + m][3]))
                if dic_elem[3]:
                    test_item.append(float(monList[j][i * 24 + m][4]))
                if dic_elem[0]:
                    test_item.append(float(monList[j][i * 24 + m][5]))

        test_item.append(float(day_max_thermal[i + unit]))

        test_list.append(test_item)

        #AWSList에 _aws.csv로 저장된 파일들에서 다 읽어와서 넣음.



    '''
    augList = []
    augList_1 = []
    augList_2 = []
    augList_3 = []
    augList_4 = []

    for i in AWSList:
        if (i[1][5:7] == '08'):
            augList.append(i)

    AWSCSVPath = './raw_data/금정구_AWS.csv'
    AWSCSVFile = open(AWSCSVPath, 'r')
    AWSCSVReader = csv.reader(AWSCSVFile)
    pre_AWSList = []
    for AWSRow in AWSCSVReader:
        pre_AWSList.append(AWSRow)

    AWSList_1 = []

    hours = range(24)
    first_flag = 0
    time_index = 0
    for i in range(len(pre_AWSList)):
        if(first_flag == 0):
            first_flag += 1
            AWSList_1.append(pre_AWSList[i])
            continue
        else:

            if( int(pre_AWSList[i][1][11:13]) != hours[(time_index%24)]):
                pre_date = dt.datetime.strptime(pre_AWSList[i - 1][1], '%Y-%m-%d %H:%M')
                i_date = dt.datetime.strptime(pre_AWSList[i][1], '%Y-%m-%d %H:%M')
                date_gap = i_date - pre_date

                loop_index = date_gap.days * 24 + int(date_gap.seconds / 3600) - 1

                for k in range(loop_index):
                    AWSList_1.append(pre_AWSList[i - 1])
                    time_index += 1

        AWSList_1.append(pre_AWSList[i])
        time_index += 1

    AWSList_1.pop(0)

    for i in AWSList_1:
        if (i[1][5:7] == '08'):
            augList_1.append(i)

    AWSCSVPath = './raw_data/기장_AWS.csv'
    AWSCSVFile = open(AWSCSVPath, 'r')
    AWSCSVReader = csv.reader(AWSCSVFile)
    pre_AWSList = []
    for AWSRow in AWSCSVReader:
        pre_AWSList.append(AWSRow)

    AWSList_2 = []

    hours = range(24)
    first_flag = 0
    time_index = 0
    for i in range(len(pre_AWSList)):
        if(first_flag == 0):
            first_flag += 1
            AWSList_2.append(pre_AWSList[i])
            continue
        else:

            if( int(pre_AWSList[i][1][11:13]) != hours[(time_index%24)]):
                pre_date = dt.datetime.strptime(pre_AWSList[i - 1][1], '%Y-%m-%d %H:%M')
                i_date = dt.datetime.strptime(pre_AWSList[i][1], '%Y-%m-%d %H:%M')
                date_gap = i_date - pre_date

                loop_index = date_gap.days * 24 + int(date_gap.seconds / 3600) - 1

                for k in range(loop_index):
                    AWSList_2.append(pre_AWSList[i - 1])
                    time_index += 1

        AWSList_2.append(pre_AWSList[i])
        time_index += 1

    AWSList_2.pop(0)

    for i in AWSList_2:
        if (i[1][5:7] == '08'):
            augList_2.append(i)

    AWSCSVPath = './raw_data/동래_AWS.csv'
    AWSCSVFile = open(AWSCSVPath, 'r')
    AWSCSVReader = csv.reader(AWSCSVFile)
    pre_AWSList = []
    for AWSRow in AWSCSVReader:
        pre_AWSList.append(AWSRow)

    AWSList_3 = []

    hours = range(24)
    first_flag = 0
    time_index = 0
    for i in range(len(pre_AWSList)):
        if(first_flag == 0):
            first_flag += 1
            AWSList_3.append(pre_AWSList[i])
            continue
        else:

            if( int(pre_AWSList[i][1][11:13]) != hours[(time_index%24)]):
                pre_date = dt.datetime.strptime(pre_AWSList[i - 1][1], '%Y-%m-%d %H:%M')
                i_date = dt.datetime.strptime(pre_AWSList[i][1], '%Y-%m-%d %H:%M')
                date_gap = i_date - pre_date

                loop_index = date_gap.days * 24 + int(date_gap.seconds / 3600) - 1

                for k in range(loop_index):
                    AWSList_3.append(pre_AWSList[i - 1])
                    time_index += 1

        AWSList_3.append(pre_AWSList[i])
        time_index += 1

    AWSList_3.pop(0)

    for i in AWSList_3:
        if (i[1][5:7] == '08'):
            augList_3.append(i)

    AWSCSVPath = './raw_data/대연_AWS.csv'
    AWSCSVFile = open(AWSCSVPath, 'r')
    AWSCSVReader = csv.reader(AWSCSVFile)
    pre_AWSList = []
    for AWSRow in AWSCSVReader:
        pre_AWSList.append(AWSRow)

    AWSList_4 = []

    hours = range(24)
    first_flag = 0
    time_index = 0
    for i in range(len(pre_AWSList)):
        if(first_flag == 0):
            first_flag += 1
            AWSList_4.append(pre_AWSList[i])
            continue
        else:

            if( int(pre_AWSList[i][1][11:13]) != hours[(time_index%24)]):
                pre_date = dt.datetime.strptime(pre_AWSList[i - 1][1], '%Y-%m-%d %H:%M')
                i_date = dt.datetime.strptime(pre_AWSList[i][1], '%Y-%m-%d %H:%M')
                date_gap = i_date - pre_date

                loop_index = date_gap.days * 24 + int(date_gap.seconds / 3600) - 1

                for k in range(loop_index):
                    AWSList_4.append(pre_AWSList[i - 1])
                    time_index += 1

        AWSList_4.append(pre_AWSList[i])
        time_index += 1

    AWSList_4.pop(0)

    for i in AWSList_4:
        if (i[1][5:7] == '08'):
            augList_4.append(i)

    '''
    # augList$에 금정 기장 대연 8월 _aws 데이터가 들어가잇음.
    '''
    day_max_thermal = []

    index = 0
    day_max = 0.0
    for i in range(len(augList)):
        if( index >= 24):
            index = 0
            day_max_thermal.append(day_max)
            day_max = 0.0
        if (augList[i][2] == '' ):
            augList[i][2] = augList[i - 1][2]

        elif( float(augList[i][2]) > day_max ):
            day_max = float(augList[i][2])
        index += 1

    for i in range(len(augList_1)):
        if (augList_1[i][2] == '' ):
            augList_1[i][2] = augList_1[i - 1][2]

    for i in range(len(augList_2)):
        if (augList_2[i][2] == ''):
            augList_2[i][2] = augList_2[i - 1][2]

    for i in range(len(augList_3)):
        if (augList_3[i][2] == ''):
            augList_3[i][2] = augList_3[i - 1][2]

    for i in range(len(augList_4)):
        if (augList_4[i][2] == ''):
            augList_4[i][2] = augList_4[i - 1][2]

    #데이터 생성
    train_list = []

    for i in range(len(day_max_thermal) - 45):
        train_item = []
        for j in range(360):
            train_item.append(float(augList[i * 24 + j][2]))
            train_item.append(float(augList_1[i*24 + j][2]))
            train_item.append(float(augList_2[i*24 + j][2]))
            train_item.append(float(augList_3[i*24 + j][2]))
            train_item.append(float(augList_4[i*24 + j][2]))

        train_item.append(float(day_max_thermal[i + 15]))

        train_list.append(train_item)

    #테스팅 데이터 생성
    test_list = []

    for i in range(len(day_max_thermal) - 45, len(day_max_thermal) - 30):
        test_item = []
        for j in range(360):
            test_item.append(float(augList[i*24 + j][2]))
            test_item.append(float(augList_1[i*24 + j][2]))
            test_item.append(float(augList_2[i*24 + j][2]))
            test_item.append(float(augList_3[i*24 + j][2]))
            test_item.append(float(augList_4[i*24 + j][2]))

        test_item.append(float(day_max_thermal[i + 15]))

        test_list.append(test_item)
    '''

    dirCheck("./data/refined_data/")
    writePath = './data/refined_data/training.csv'
    f = open(writePath, 'w', newline='')
    wr = csv.writer(f)
    for row in train_list:
        wr.writerow(row)
    f.close()


    writePath = './data/refined_data/testing.csv'
    f = open(writePath, 'w', newline='')
    wr = csv.writer(f)
    for row in test_list:
        wr.writerow(row)
    f.close()