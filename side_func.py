import re

import requests


# Special hidden command for cute dog
def get_image_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url