import pickle

fname = "../backup.db"
with open(fname, 'rb') as fp:
    data = pickle.load(fp)
    print("++++++ Ranks +++++++")
    for each in data['ranks']:
        print(each, end="")
    print("\n++++++ Records ++++++")
    for key in data['records']:
        print(key + ":", data['records'][key])
