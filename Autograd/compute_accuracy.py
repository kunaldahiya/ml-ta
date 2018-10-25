import sys
from sklearn.metrics import accuracy_score

with open(sys.argv[1], "r") as f:
    gold = f.readlines()
    gold = [int(float(each.strip())) for each in gold]

with open(sys.argv[2], "r") as f:
    pred = f.readlines()
    pred = [int(float(each.strip())) for each in pred]

with open(sys.argv[3], 'w') as fp:
    acc = str(accuracy_score(gold, pred))
    print("Accuracy: %s" % acc)
    fp.write(acc)
