import pandas as pd

def get_stat(id: int, stat: str) -> int:
    data = pd.read_csv(f'Data/Guild/Users/{stat}.csv')
    target = data.index[data['id'] == id].to_list()[0]
    value = data.iloc[target]
    return value['value']

def set_stat(id:int, stat: str, value: int):
    data = pd.read_csv(f'Data/Guild/Users/{stat}.csv')
    target = data.index[data['id'] == id].to_list()[0]
    d = [{
        'id':id,
        'value': value
    }]
    data.iloc[target] = d[0]
    data.to_csv(f'Data/Guild/users/{stat}.csv', index=False, header=True)

class User():
    def __init__(self, id:int):
        self.id = id

    def get_reputation(self) -> int:
        get_stat(self.id, 'reputation')

    def set_reputation(self, value:int):
        set_stat(self.id, 'reputation', value)