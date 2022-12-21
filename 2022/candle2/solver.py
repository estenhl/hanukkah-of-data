import argparse
import os

import pandas as pd

def generate_initials(name: str):
    initials = ''.join([token[0] for token in name.split(' ')])

    return initials.upper()


def solve(data: str):
    orders = pd.read_csv(os.path.join(data, 'noahs-orders.csv'))
    orders['year'] = orders['ordered'].apply(lambda x: int(x.split('-')[0]))
    orders = orders[orders['year'] == 2017]

    customers = pd.read_csv(os.path.join(data, 'noahs-customers.csv'))
    customers['initials'] = customers['name'].apply(generate_initials)
    customers = customers[customers['initials'] == 'JD']

    order_items = pd.read_csv(os.path.join(data, 'noahs-orders_items.csv'))
    products = pd.read_csv(os.path.join(data, 'noahs-products.csv'))

    for key in ['coffee', 'bagel']:
        print(products[products['desc'].apply(lambda x: key in x.lower())])

    coffee = 'DLI1464'
    bagel = ['BKY4234', 'BKY5887']

    coffee_orders = order_items[order_items['sku'] == coffee]
    bagel_orders = order_items[order_items['sku'].isin(bagel)]
    order_ids = set(coffee_orders['orderid'].values) & \
                set(bagel_orders['orderid'].values)

    customer = orders.loc[orders['orderid'].isin(order_ids), \
                          'customerid'].values[0]
    phone = customers.loc[customers['customerid'] == customer, \
                          'phone'].values[0]

    print(f'Customer: {customer}')
    print(f'Phone: {phone}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Solves HoD 2022 candle 2')

    parser.add_argument('-d', '--data', required=False,
                        default=os.path.join(os.pardir, 'data'),
                        help='Path to data folder')

    args = parser.parse_args()

    solve(args.data)
