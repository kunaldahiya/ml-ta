class Record(object):
    def __init__(self, entry_number):
        self.entry_number = entry_number
        self.best_score = 0.0
        self.scores = []

    def update(self, new_score):
        self.scores.append(new_score)
        changed = False
        if new_score > self.best_score:
            self.best_score = new_score
            changed = True
        return changed, self.best_score

    def __repr__(self):
        return "Entry number: {}, Best score: {}".format(self.entry_number, self.best_score)