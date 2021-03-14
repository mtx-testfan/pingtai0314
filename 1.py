{
    "params": {
        "longitude": 121.04925573429551,
        "latitude": 31.315590522490712

    }
}

import hashlib
def test(data):
    longitude = data['params']['longitude']
    latitude=data['params']['latitude']
    text = '{}{}'.format(longitude,latitude)
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    return md5.hexdigest()