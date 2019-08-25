### PStraw

PStraw is a simple Python module wrapping the [Strawpoll](https://www.strawpoll.me) API. Their API reference is [here](https://github.com/strawpoll/strawpoll/wiki/API).

#### Install

`pip install git+https://github.com/MJJBennett/pstraw.git`

#### Usage

```python
>>> import pstraw
>>> poll = pstraw.get(id=1)
>>> poll.results()
[('Sucker punch ', 26963), ('Pirates of carribian ', 56656), ('Prison logic', 13470), ('Witchhunter', 13453)]
>>> newpoll = pstraw.post("What day is it?", ["Monday", "Unknown"])
>>> newpoll.id()
18537745
>>> newpoll.data
{"id":18537745,"title":"What day is it?","options":["Monday", "Unknown"],"votes":[0,0],"multi":false,"dupcheck":"normal","captcha":false}
```
