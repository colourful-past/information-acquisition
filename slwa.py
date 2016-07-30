import sys
import json
from itertools import islice, groupby
from operator import itemgetter
from os.path import exists, basename, splitext

import requests
import pandas as pd
from fuzzywuzzy.fuzz import ratio

URL = (
    'http://catalogue.beta.data.wa.gov.au/dataset/7faa2336-7601-447c-91b0-'
    '4b771ee26b6f/resource/9117bf08-bd54-4b19-89f8-ca86ae799875/download/'
    'slwapictorial.csv'
)
FILENAME = basename(URL)

if not exists(FILENAME):
    with open(FILENAME, 'wb') as fh:
        fh.write(requests.get(URL).content)


def get_image(images):
    key = lambda filename: splitext(filename)[1]

    for image in images:
        if key(image) == '.jpg':
            return image


def main(query=sys.argv[1]):
    df = pd.read_csv(FILENAME, encoding='latin1')

    df['URLS for images'] = df['URLS for images'].str.split(';')

    rows = map(itemgetter(1), df.iterrows())  # get rows
    rows = sorted(rows, key=lambda row: ratio(row.Title, query))  # rank rows
    rows = islice(rows, 100)  # limit rows

    for row in rows:
        image = get_image(row["URLS for images"])

        description = (
            row.Summary or
            row["Description of original object"] or
            ''
        )

        sys.stdout.write(
            '{}\n'.format(json.dumps({
                'title': row.Title,
                'description': description,
                'source': 'SLWA Pictorial',
                'original': image,
                'colourised': None
            }))
        )

if __name__ == '__main__':
    main()