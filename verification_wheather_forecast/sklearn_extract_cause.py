from pandas import read_csv
from sklearn import tree
from os import system
from sklearn.tree import _tree
import numpy as np


def tree_to_code(tree, feature_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    print("def tree({}):".format(", ".join(feature_names)))
    stack = []
    def recurse(node, depth):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            #print("{}if {} <= {}:".format(indent, name, threshold))
            string = "{}if {} <= {}:".format(indent, name, threshold)
            stack.append(string)
            recurse(tree_.children_left[node], depth + 1)
            stack.pop(len(stack) - 1)

            #print("{}else:  # if {} > {}".format(indent, name, threshold))
            #string = "{}else:  # if {} > {}".format(indent, name, threshold)
            string = "{}if {} > {}".format(indent, name, threshold)
            stack.append(string)
            recurse(tree_.children_right[node], depth + 1)
            stack.pop(len(stack)-1)
        else:
            for x in stack:
                print(x)
            #print("{}return {}".format(indent, tree_.value[node]))

            if(tree_.value[node][0][0] > tree_.value[node][0][1]):
                string = '{}오차가 작을것으로 판단'.format(indent)
            else:
                string = '{}오차가 클것으로 판단'.format(indent)
            print(string)

    recurse(0, 1)




#main
path = '부산_금정구_장전2동'
data = read_csv(path + '_test.csv')
Y = data.gap
#print(Y)

X = data[['location', 'date', 'thermal', 'wind_direction', 'wind_power', 'rain']]
#print(X)

decision_tree = tree.DecisionTreeClassifier(criterion='entropy') #, min_samples_leaf=10)
decision_tree = decision_tree.fit(X,Y)


dot_file = open(path + '_test.dot' , 'w')
tree.export_graphviz(decision_tree, out_file=dot_file, feature_names=X.columns, class_names=['0','1'])
dot_file.close()
system("dot -Tpng /home/kbbn2001/바탕화면/forecast/" + path + "_test.dot -o /home/kbbn2001/바탕화면/forecast/" + path + "_test.png")

tree_to_code(decision_tree, X.columns)