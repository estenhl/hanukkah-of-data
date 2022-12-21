import argparse
import os
import pandas as pd

from datetime import datetime


def generate_birthday(birthdate: str):
    _, m, d = birthdate.split('-')

    return datetime.strptime(f'{d}/{m}/2020', '%d/%m/%Y')

def is_dog(birthdate: str):
    y = int(birthdate.split('-')[0])

    return (y - 1910) % 12 == 0

def solve(data: str):
    customers = pd.read_csv(os.path.join(data, 'noahs-customers.csv'))
    area = customers.loc[customers['customerid'] == 4164, \
                         'citystatezip'].values[0]
    aries_start = datetime.strptime('20/03/2020', '%d/%m/%Y')
    aries_end = datetime.strptime('20/04/2020', '%d/%m/%Y')
    customers['birthday'] = customers['birthdate'].apply(generate_birthday)
    customers = customers[(customers['birthday'] >= aries_start) & \
                          (customers['birthday'] <= aries_end)]
    customers = customers[customers['birthdate'].apply(is_dog)]
    customers = customers[customers['citystatezip'] == area]
    phone = customers['phone'].values[0]

    print(f'Phone: {phone}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves HoD 2022 candle 3')

    parser.add_argument('-d', '--data', required=False,
                        default=os.path.join(os.pardir, 'data'),
                        help='Path to data folder')

    args = parser.parse_args()

    solve(args.data)
