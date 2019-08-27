import requests, re, json
from . import literals as lit

class Poll:
    """A thin wrapper around a dict representing Poll data."""
    def __init__(self, data):
        """Create a poll.
        data : Dictionary containing poll data.
        """
        self.data = data
    def results(self):
        """Returns a list of tuples representing poll results."""
        return list(zip(self.data['options'], self.data['votes'])) if 'options' in self.data else None
    def id(self):
        """Returns the ID of the poll."""
        return self.data['id']
    def url(self):
        """Returns the URL of the poll."""
        return lit._strawpoll_url + '/' + self.id()
    def title(self):
        """Returns the title of the poll."""
        return self.title['title']

def is_cloudflare(page):
    return re.search(lit._re_cf, page) is not None

def safe_poll(data):
    """Method to create a poll from a JSON string.

    Checks if the string is in fact JSON or if the API has returned
    something strange, like a 404 error or a Cloudflare check page.
    """
    if data.status_code != 200:
        raise requests.HTTPError("HTTP error " + str(data.status_code))
    try:
        return Poll(json.loads(data.text))
    except Exception as e:
        if is_cloudflare(data.text):
            raise requests.ConnectionError("This page is protected by Cloudflare.")
        else:
            # Unexpected error
            raise e

def polls_url():
    return lit._strawpoll_url + lit._strawpoll_api_ext + lit._strawpoll_poll_ext 

def id_from_url(url):
    mo = re.match(lit._url_regex, url)
    return mo.group(lit._url_regex_id_group) if mo is not None else None

def url_from_id(id):
    return polls_url() + '/' + str(id)

def get(id=None, url=None):
    if url is not None:
        id = id_from_url(url)
    return safe_poll(requests.get(url_from_id(id))) if id is not None else None

def post(title, options, multi=False, dupcheck='normal', captcha=False):
    # API preconditions
    if len(options) < 2 or len(options) > 30:
        raise ValueError("Value for options must be a list with between 2 and 30 options.")
    if title == '':
        raise ValueError("Title cannot be a 0-length string.")

    data = {"title": title, "options": options, "multi": multi, "dupcheck": dupcheck, "captcha": captcha}
    headers = {'Content-Type': 'application/json'}
    # Note: To successfully POST, the url must be exactly:
    # https://www.strawpoll.me/api/v2/polls
    # And the Content-Type header above must be included.
    resp = requests.post(polls_url(), json=data, headers=headers)
    return safe_poll(resp)
