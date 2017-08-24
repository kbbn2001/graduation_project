from pandas import read_csv
from sklearn import tree
from os import system
from sklearn.tree import _tree
import numpy as np


#main
predicts = []
paths = ["부산_금정구_장전2동", "부산_금정구_청룡동", "부산_해운대구_중1동", "부산_영도구_동삼2동", "부산_사상구_감전동", "부산_동래구_복산동"]
for path in paths:
    predict = []
    data = read_csv(path + '_label_aws.csv')
    Y = data.gap
    #print(Y)

    X = data[['location', 'date', 'thermal', 'wind_direction', 'wind_power', 'rain']]
    #print(X)

    decision_tree = tree.DecisionTreeClassifier(criterion='entropy') #, min_samples_leaf=10)
    decision_tree = decision_tree.fit(X,Y)


    dot_file = open(path + '_decision_tree.dot' , 'w')
    tree.export_graphviz(decision_tree, out_file=dot_file, feature_names=X.columns, class_names=['0','1'])
    dot_file.close()
    system("dot -Tpng /home/kbbn2001/바탕화면/forecast/" + path + "_test.dot -o /home/kbbn2001/바탕화면/forecast/" + path + "_decisionTree.png")

    for i in range(len(paths)):
        test_data = read_csv(paths[i] + '_label_aws.csv')
        test_y = test_data.gap
        test_x = test_data[['location', 'date', 'thermal', 'wind_direction', 'wind_power', 'rain']]

        count = 0
        result = decision_tree.predict(test_x)
        for i in range(len(result)):
            if(result[i] == test_y[i]):
                count += 1
        predict.append(count / len(result))
    predicts.append(predict)
for x in predicts:
    print(x)
