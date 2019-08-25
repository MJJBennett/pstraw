import requests, re, json
from . import literals as lit

class Poll:
    def __init__(self, data):
        self.data = data
    def results(self):
        return list(zip(self.data['options'], self.data['votes'])) if 'options' in self.data else None
    def id(self):
        return self.data['id']
    def title(self):
        return self.title['title']

def safe_poll(data):
    try:
        return Poll(json.loads(data.text))
    except Exception as e:
        if is_404(data.text):
            raise requests.HTTPError("HTTP error 404")
        if is_cloudflare(data.text):
            raise requests.ConnectionError("This page is protected by Cloudflare.")
        else:
            raise e

def polls_url():
    return lit._strawpoll_url + lit._strawpoll_api_ext + lit._strawpoll_poll_ext 

def id_from_url(url):
    mo = re.match(lit._url_regex, url)
    return mo.group(lit._url_regex_id_group) if mo is not None else None

def api_url_from_id(id):
    return polls_url() + '/' + str(id)

def is_404(page):
    return re.search(lit._re_404, page) is not None

def is_cloudflare(page):
    return re.search(lit._re_cf, page) is not None

def get(id=None, url=None):
    if url is not None:
        id = id_from_url(url)
    if id is not None:
        url = api_url_from_id(id)
    else:
        return None
    resp = requests.get(url)
    if resp.status_code != 200:
        raise requests.HTTPError("HTTP error " + str(resp.status_code))
    return safe_poll(resp)

def post(title, options, multi=False, dupcheck='normal', captcha=False):
    if len(options) > 2 or len(options) > 30:
        raise ValueError("Value for options must be a list with between 2 and 30 options.")
    data = {"title": title, "options": options, "multi": multi, "dupcheck": dupcheck, "captcha": captcha}
    data = {'title': title, 'options': options}
    print(data)
    headers = {'Content-Type': 'application/json'}
    # Note: To successfully POST, the url must be exactly:
    # https://www.strawpoll.me/api/v2/polls
    # And the Content-Type header above must be included.
    resp = requests.post(polls_url(), json=data, headers=headers)
    return safe_poll(resp)
