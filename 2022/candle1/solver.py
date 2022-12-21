import argparse
import os
import re

import pandas as pd

def extract(name: str):
    pattern = r'([A-Za-z]+ )+([A-Za-z]+)( Jr\.)?( [IV]+)?'
    match = re.fullmatch(pattern, name)

    return match.groups(0)[-3]

def encode(name: str):
    return ''.join([str(((ord(c) - 94) // 3) + 1) for c in name.lower()])

def solve(data: str):
    customers = pd.read_csv(os.path.join(data, 'noahs-customers.csv'))
    customers['lastname'] = customers['name'].apply(extract)
    customers['encoded'] = customers['lastname'].apply(encode)
    customers['clean'] = customers['phone'].apply(lambda x: x.replace('-', ''))
    rows = customers[customers['encoded'] == customers['clean']]
    print(f'Phone: {rows["phone"].values[0]}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves HoD 2022 candle 1')

    parser.add_argument('-d', '--data', required=False,
                        default=os.path.join(os.pardir, 'data'),
                        help='Path to data folder')

    args = parser.parse_args()

    solve(args.data)
