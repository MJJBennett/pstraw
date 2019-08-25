import re

_strawpoll_url = 'https://www.strawpoll.me'
_strawpoll_api_ext = '/api/v2/'
_strawpoll_poll_ext = 'polls'

_url_regex = re.compile(r'(https?://)?strawpoll\.me/([0-9]+)')
_url_regex_id_group = 2

_re_404 = re.compile(r'<title>Not found - Straw Poll *</title>')
_re_cf = re.compile(r'Checking your browser')
