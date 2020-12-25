import sys
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
import numpy as np


with open(sys.argv[1], "r") as f:
    gold = f.readlines()
    gold = [int(float(each.strip())) for each in gold]

status = False
with open(sys.argv[2], "r") as f:
    pred = f.readlines()
    try:
        pred = [int(float(each.strip())) for each in pred]
        status = True
    except Exception as e:
        print("Error in reading prediction file: ", e)

with open(sys.argv[3], 'w') as fp:
    if status:
        try:
            acc = 100*accuracy_score(gold, pred)
            fscore = 100*f1_score(gold, pred, average='macro')
            print(f"Accuracy (%): {acc}")
        except Exception as e:
            print("Error in calculating accuracy: ", e)
            acc = 0.0
            fscore = 0.0
    else:
        acc = 0.0
        fscore = 0.0
        print(f"Accuracy (%): {acc}")
    acc = "{:02f},{:02f}".format(acc, fscore)
    fp.write(acc)
