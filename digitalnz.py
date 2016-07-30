import os
import sys
import json
import requests


def search(query):
    url = 'http://api.digitalnz.org/v3/records.json'

    params = [
        ('text', query),
        ('and[category][]', 'Images'),
        ('api_key', os.environ['DIGITAL_NZ_API_KEY'])
    ]

    for decade in range(1900, 1960, 10):
        params.append(('or[decade]', decade))

    res = requests.get(
        url,
        params=params
    )
    print(res.request.url)
    res = res.json()

    search = res['search']

    results = [
        {
            "title": result['title'],
            "description": result['description'],
            "source": result['collection'][0],
            "originalImageUrl": (
                result.get('large_thumbnail_url') or
                result.get('thumbnail_url')
            )
        }
        for result in search['results']
        if 'All rights reserved' not in result['Usage']
    ]

    print(json.dumps(results))


def main(query=sys.argv[1]):
    search(query)


if __name__ == '__main__':
    main()