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

    def add(self, rank:int, cash:int):
        level_csv = pd.read_csv(f'{path}level.csv')
        cash_csv = pd.read_csv(f'{path}cash.csv')
        name_csv = pd.read_csv(f'{path}name.csv')
        display_csv = pd.read_csv(f'{path}display.csv')

        ld = [{
            'uid': self.uid,
            'value': rank
        }]
        cd = [{
            'uid': self.uid,
            'value': cash
        }]
        nd = [{
            'uid': self.uid,
            'value': 'new_user_soon'
        }]
        dd = [{
            'uid': self.uid,
            'value': 'new_user_soon'
        }]
        ld, cd, nd, dd = pd.DataFrame(ld), pd.DataFrame(cd), pd.DataFrame(nd), pd.DataFrame(dd)

        level_csv = pd.concat([level_csv, ld], ignore_index=True)
        cash_csv = pd.concat([cash_csv, cd], ignore_index=True)
        name_csv = pd.concat([name_csv, nd], ignore_index=True)
        display_csv = pd.concat([display_csv, dd], ignore_index=True)
        
        level_csv.to_csv(f'{path}level.csv', index=False, header=True)
        cash_csv.to_csv(f'{path}cash.csv', index=False, header=True)
        name_csv.to_csv(f'{path}name.csv', index=False, header=True)
        display_csv.to_csv(f'{path}display.csv', index=False, header=True)
    def edit(self, rank:int, cash:int):
        level_csv = pd.read_csv(f'{path}level.csv')
        cash_csv = pd.read_csv(f'{path}cash.csv')

        lTarget = level_csv.index[level_csv['uid'] == self.uid].to_list()
        cTarget = cash_csv.index[cash_csv['uid'] == self.uid].to_list()

        if not (len(lTarget) and len(cTarget)):
            raise Exception

        ld = [{
            'uid': self.uid,
            'value': rank
        }]
        cd = [{
            'uid': self.uid,
            'value': cash
        }]

        level_csv.iloc[lTarget] = ld
        cash_csv.iloc[cTarget] = cd

        level_csv.to_csv(f'{path}level.csv', index=False, header=True)
        cash_csv.to_csv(f'{path}cash.csv', index=False, header=True)
    def delete(self):
        level_csv = pd.read_csv(f'{path}level.csv')
        cash_csv = pd.read_csv(f'{path}cash.csv')
        name_csv = pd.read_csv(f'{path}name.csv')
        display_csv = pd.read_csv(f'{path}display.csv')

        level_csv = level_csv.loc[level_csv['uid'] != self.uid]
        cash_csv = cash_csv.loc[cash_csv['uid'] != self.uid]
        name_csv = name_csv.loc[name_csv['uid'] != self.uid]
        display_csv = display_csv.loc[display_csv['uid'] != self.uid]

        level_csv.to_csv(f'{path}level.csv', index=False, header=True)
        cash_csv.to_csv(f'{path}cash.csv', index=False, header=True)
        name_csv.to_csv(f'{path}name.csv', index=False, header=True)
        display_csv.to_csv(f'{path}display.csv', index=False, header=True)