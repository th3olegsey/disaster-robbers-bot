import pandas as pd
path = 'Data/Guild/Leaderboard/'
def getStat(uid, stat):
    csv = pd.read_csv(f'{path}{stat}.csv')
    target = csv.index[csv['uid'] == uid].to_list()
    if len(target):
        value = csv.iloc[target[0]]['value']
    else:
        d = [{'uid':uid, 'value':0}]
        csv = pd.concat([csv, pd.DataFrame(d)], ignore_index=True)
        csv.to_csv(f'{path}{stat}.csv', index=False, header=True)
        value = 0
    return value

def setStat(uid, stat, value):
    csv = pd.read_csv(f'{path}{stat}.csv')
    target = csv.index[csv['uid'] == uid].to_list()[0]
    d = [{
        'uid': uid,
        'value': value
    }]
    csv.iloc[target] = d[0]
    csv.to_csv(f'{path}{stat}.csv', index=False, header=True)

class Player():
    def __init__(self, uid:int):
        self.uid = uid

    def level(self) -> int:
        return getStat(self.uid, 'level')
    def setLevel(self, value):
        setStat(self.uid, 'level', value)

    def cash(self) -> int:
        return int(getStat(self.uid, 'cash'))
    def setCash(self, value):
        setStat(self.uid, 'cash', value)

    def name(self) -> str:
        return getStat(self.uid, 'name')
    def display(self) -> str:
        return getStat(self.uid, 'display')