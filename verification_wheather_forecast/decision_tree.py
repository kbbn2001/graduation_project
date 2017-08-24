
import DecisionTree as DT
import csv

paths = ["부산_금정구_청룡동", "부산_금정구_장전2동", "부산_해운대구_중1동", "부산_영도구_동삼2동", "부산_사상구_감전동", "부산_동래구_복산동"]
result = []

for path in paths:
       training_datafile = './' + path + '_test.csv'
       dt = DT.DecisionTree(
              training_datafile = training_datafile,
              csv_class_column_index = 7,
              csv_columns_for_features = [1,2,3,4,5,6],
              entropy_threshold = 0.001,
              max_depth_desired = 10,
              symbolic_to_numeric_cardinality_threshold = 0,
              csv_cleanup_needed = 1,
       )

       dt.get_training_data()
       dt.calculate_first_order_probabilities()
       dt.calculate_class_priors()
       dt.show_training_data()
       root_node = dt.construct_decision_tree_classifier()
       #root_node.display_decision_tree("   ")

       sub_result = []
       for test in paths:
              testFilePath = './' + test +'_test.csv'
              testFile = open(testFilePath, 'r')
              testCSVReader = csv.reader(testFile)
              testList = []
              for row in testCSVReader:
                     testList.append(row)
              label = testList.pop(0)

              true_count = 0
              false_count = 0
              for row in testList:
                     test_sample = [str(label[1]) + ' = ' + str(row[1]),
                                    str(label[2]) + ' = ' + str(row[2]),
                                    str(label[3]) + ' = ' + str(row[3]),
                                    str(label[4]) + ' = ' + str(row[4]),
                                    str(label[5]) + ' = ' + str(row[5]),
                                    str(label[6]) + ' = ' + str(row[6])
                                    ]
                     #print(test_sample)
                     classification = dt.classify(root_node, test_sample)
                     #print("Classification: ", classification)
                     predict_classification = -1
                     if( float(classification['gap=0']) > float(classification['gap=1'])):
                            predict_classification = 0
                     else:
                            predict_classification = 1
                     if(int(row[7]) == predict_classification):
                            true_count += 1
                     else:
                            false_count += 1

              #print(test, true_count, false_count, (true_count/(true_count + false_count)))
              sub_result.append((true_count/(true_count + false_count)))
       result.append(sub_result)

for a in result:
       print(a)

'''
test_sample  = ['location = 940', 'date = 3', 'thermal = 28', 'wind_direction = 27.5', 'wind_power = .7', 'rain = 0']
classification = dt.classify(root_node, test_sample)

print("Classification: ", classification)
print(classification['gap=0'])
'''