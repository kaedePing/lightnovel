import pandas as pd
import requests
import json
import sys


def post_data(path="../reptile/results/novel.csv"):
    df = pd.read_csv(path, encoding='utf-8')
    headers = {
        'Content-Type': 'application/json'
    }
    url = 'http://127.0.0.1:8000/hot_novel'

    columns = ['title', 'classification', 'author', 'status', 'update', 'length', 'cover']
    df.columns = columns
    print(df.shape)

    temp = df['update'].isna()
    df.loc[temp, 'update'] = '2000-1-1'
    temp = df['length'].isna()
    df.loc[temp, 'length'] = 0

    data = df.to_dict(orient='records')

    data = json.dumps(data)

    print('大小为:' + '{}kb!'.format(sys.getsizeof(data) / 1024.))
    res = requests.post(url, data=data, headers=headers)
    print(res.status_code)


if __name__ == '__main__':
    post_data()
