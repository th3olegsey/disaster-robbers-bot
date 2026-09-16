import pandas as pd
class User():
    def __init__(self, id:int):
        self.id = id

    def get_reputation(self) -> int:
        data = pd.read_csv('Data/Guild/Users/reputation.csv')
        target = data.index[data['id'] == self.id].to_list()[0]
        value = data.iloc[target]
        return value['value']

    def set_reputation(self, value:int):
        data = pd.read_csv('Data/Guild/Users/reputation.csv')
        target = data.index[data['id'] == self.id].to_list()[0]
        d = [{
            'id':self.id,
            'value': value
        }]
        data.iloc[target] = d[0]
        data.to_csv('Data/Guild/users/reputation.csv', index=False, header=True)