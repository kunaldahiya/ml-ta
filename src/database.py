from record import Record
import numpy as np
import threading
from operator import itemgetter
import pickle


class rankRecord(object):
    def __init__(self, entry_number, score, rank):
        self.entry_number = entry_number
        self.score = score
        self.rank = rank

    def __repr__(self):
        return "Entry number: {}, Score: {}, Rank: {}\n".format(self.entry_number, self.score, self.rank)


class dbRecord(object):
    def __init__(self, record, pos):
        self.record = record
        self.position = pos

    def __repr__(self):
        return "Entry number: {}, Score: {}, Position: {}".format(self.record.entry_number, self.record.best_score, self.position)


class dataBase(object):
    def __init__(self):
        self.ranks = []
        self.records = dict()
        self.lock = threading.Lock()

    def add_user(self, entry_number):
        rec = Record(entry_number)
        user_rank = -1
        if not self.ranks:
            user_rank = 0
        self.lock.acquire()
        self.ranks.append(rankRecord(entry_number, 0.0, user_rank))
        self.records[entry_number] = dbRecord(rec, len(self.ranks) - 1)
        self.lock.release()

    def _search(self, entry_number, current_pos):
        # Search new position of the user
        new_pos = current_pos
        user_score = self.records[entry_number].record.best_score
        for idx in range(current_pos - 1, -1, -1):
            if user_score <= self.ranks[idx].score:
                new_pos = idx + 1
                break
        else:
            new_pos = 0
        return new_pos

    def _need_to_adjust(self, pos):
        if self.ranks[pos - 1].score == self.ranks[pos].score:
            return False
        else:
            return True

    def _adjust_rank(self, entry_number, old_pos, new_pos):
        # Adjust rank of the users after the current user
        temp = self.ranks.pop(old_pos)
        self.ranks = self.ranks[:new_pos] + [temp] + self.ranks[new_pos:]
        user_rank = self.ranks[new_pos - 1].rank
        if self._need_to_adjust(new_pos) or new_pos == 0:
            user_rank = self.ranks[new_pos - 1].rank + 1
            if new_pos == 0:
                user_rank = 0
            for item in self.ranks[new_pos + 1:]:
                item.rank += 1
                self.records[item.entry_number].position += 1
        self.ranks[new_pos].rank = user_rank
        return user_rank

    def update_score(self, entry_number, score):
        # Check if user exist in database
        if entry_number not in self.records:
            self.add_user(entry_number)
        rec = self.records[entry_number].record
        changed, user_score = rec.update(score)
        user_pos = self.records[entry_number].position
        user_rank = self.ranks[user_pos].rank
        if changed:
            self.ranks[user_pos].score = user_score
            user_rank = self.update_rank(entry_number, user_pos)
        return user_score, user_rank

    def update_rank(self, entry_number, user_pos):
        user_rank = 0
        self.lock.acquire()
        if len(self.ranks) > 1:
            new_pos = self._search(entry_number, user_pos)
            self.records[entry_number].position = new_pos
            user_rank = self._adjust_rank(entry_number, user_pos, new_pos)
        self.lock.release()
        return user_rank

    def save(self, fname):
        data = {'ranks': self.ranks, 'records': self.records}
        with open(fname, 'wb') as fp:
            pickle.dump(data, fp, pickle.HIGHEST_PROTOCOL)
    
    def load(self, fname):
        with open(fname, 'rb') as fp:
            data = pickle.load(fp)
        self.ranks = data['ranks']
        self.records = data['records']

    def __repr__(self):
        return "".join([str(item) for item in self.records])
