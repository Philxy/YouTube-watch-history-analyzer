
from urllib import parse
import requests
import util

def video_id(url):
    url_parsed = parse.urlparse(url)
    qsl = parse.parse_qs(url_parsed.query)
    return url_parsed.query[2:]



# returns list of tags obtained from google api given a video url
def request_tags_via_api(url):

    API_key = ''
    video_id = util.video_id(url)

    r = requests.get('https://www.googleapis.com/youtube/v3/videos?key=' + API_key + ' &fields=items(snippet(title,tags))&part=snippet&id=' + video_id)

    if 'items' not in r.json():
        return []

    if len(r.json()['items']) == 0:
        return []

    if 'tags' in r.json()['items'][0]['snippet']:
        return r.json()['items'][0]['snippet']['tags']

    return []


def main():
    return


if __name__ == "__main__":
    main()