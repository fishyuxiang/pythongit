import numpy as np

class Tree:
    def __init__(self, value=None, trueBranch=None, falseBranch=None, results=None, col=-1, summary=None, data=None):
        self.value = value
        self.trueBranch = trueBranch
        self.falseBranch = falseBranch
        self.results = results
        self.col = col
        self.summary = summary
        self.data = data

    def __str__(self):
        print(self.col, self.value)
        print(self.results)
        print(self.summary)
        return ""


def calculateDiffCount(datas):
    # œ«ÊäÈëµÄÊýŸÝ»ã×Ü(input, dataSet)
    # return results Set{type1:type1Count, type2:type2Count .... typeN:typeNCount}
    """
    žÃº¯ÊýÊÇŒÆËãginiÖµµÄžšÖúº¯Êý£¬ŒÙÉèÊäÈëµÄdataSetÎªÎª['A', 'B', 'C', 'A', 'A', 'D']£¬
    ÔòÊä³öÎª['A':3,' B':1, 'C':1, 'D':1]£¬ÕâÑù·ÖÀàÍ³ŒÆdataSetÖÐÃ¿žöÀà±ðµÄÊýÁ¿
    """
    results = {}
    for data in datas:
        # data[-1] means dataType
        if data[-1] not in results:
            results.setdefault(data[-1], 1)
        else:
            results[data[-1]] += 1
    return results


# gini()
def gini(rows):
    # ŒÆËãginiµÄÖµ(Calculate GINI)

    length = len(rows)
    results = calculateDiffCount(rows)
    imp = 0.0
    for i in results:
        imp += results[i] / length * results[i] / length
    return 1 - imp

def splitDatas(rows, value, column):
    # žùŸÝÌõŒþ·ÖÀëÊýŸÝŒ¯(splitDatas by value, column)
    # return 2 part£šlist1, list2£©

    list1 = []
    list2 = []

    if isinstance(value, int) or isinstance(value, float):
        for row in rows:
            if row[column] >= value:
                list1.append(row)
            else:
                list2.append(row)
    else:
        for row in rows:
            if row[column] == value:
                list1.append(row)
            else:
                list2.append(row)
    return list1, list2

def buildDecisionTree(rows, evaluationFunction=gini):
    # µÝ¹éœšÁ¢Ÿö²ßÊ÷£¬ µ±gain=0£¬Ê±Í£Ö¹»Ø¹é
    # build decision tree bu recursive function
    # stop recursive function when gain = 0
    # return tree
    currentGain = evaluationFunction(rows)
    column_lenght = len(rows[0])
    rows_length = len(rows)

    best_gain = 0.0
    best_value = None
    best_set = None

    # choose the best gain
    for col in range(column_lenght - 1):
        col_value_set = set([x[col] for x in rows])
        for value in col_value_set:
            list1, list2 = splitDatas(rows, value, col)
            p = len(list1) / rows_length
            gain = currentGain - p * evaluationFunction(list1) - (1 - p) * evaluationFunction(list2)
            if gain > best_gain:
                best_gain = gain
                best_value = (col, value)
                best_set = (list1, list2)
    dcY = {'impurity': '%.3f' % currentGain, 'sample': '%d' % rows_length}
    #
    # stop or not stop

    if best_gain > 0:
        trueBranch = buildDecisionTree(best_set[0], evaluationFunction)
        falseBranch = buildDecisionTree(best_set[1], evaluationFunction)
        return Tree(col=best_value[0], value = best_value[1], trueBranch = trueBranch, falseBranch=falseBranch, summary=dcY)
    else:
        return Tree(results=calculateDiffCount(rows), summary=dcY, data=rows)


def prune(tree, miniGain, evaluationFunction=gini):
    # ŒôÖŠ when gain < mini Gain, ºÏ²¢£šmerge the trueBranch and falseBranch£©
    if tree.trueBranch.results == None:
        prune(tree.trueBranch, miniGain, evaluationFunction)
    if tree.falseBranch.results == None:
        prune(tree.falseBranch, miniGain, evaluationFunction)

    if tree.trueBranch.results != None and tree.falseBranch.results != None:
        len1 = len(tree.trueBranch.data)
        len2 = len(tree.falseBranch.data)
        len3 = len(tree.trueBranch.data + tree.falseBranch.data)

        p = float(len1) / (len1 + len2)

        gain = evaluationFunction(tree.trueBranch.data + tree.falseBranch.data) - p * evaluationFunction(tree.trueBranch.data) - (1 - p) * evaluationFunction(tree.falseBranch.data)

        if gain < miniGain:
            tree.data = tree.trueBranch.data + tree.falseBranch.data
            tree.results = calculateDiffCount(tree.data)
            tree.trueBranch = None
            tree.falseBranch = None

def classify(data, tree):
    if tree.results != None:
        return tree.results
    else:
        branch = None
        v = data[tree.col]
        if isinstance(v, int) or isinstance(v, float):
            if v >= tree.value:
                branch = tree.trueBranch
            else:
                branch = tree.falseBranch
        else:
            if v == tree.value:
                branch = tree.trueBranch
            else:
                branch = tree.falseBranch
        return classify(data, branch)


def loadCSV():
    def convertTypes(s):
        s = s.strip()
        try:
            return float(s) if '.' in s else int(s)
        except ValueError:
            return s
    data = np.loadtxt("datas.txt", dtype='str', delimiter=',')
    data = data[1:, :]
    dataSet =([[convertTypes(item) for item in row] for row in data])
    return dataSet

# »­Ê÷

if __name__ == '__main__':
    dataSet = loadCSV()
    decisionTree = buildDecisionTree(dataSet, evaluationFunction=gini)
    prune(decisionTree, 0.4)
    test_data = [5.9,3,4.2,1.5]
    r = classify(test_data, decisionTree)
    print(r)