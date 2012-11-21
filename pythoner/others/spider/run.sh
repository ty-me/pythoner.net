kill -9 `pgrep -f simple_spider.py`
kill -9 `pgrep -f oschina_spider.py`
kill -9 `pgrep -f jobbole_spider.py`
nohup python -u simple_spider.py  >> /tmp/simle.log &
nohup python -u oschina_spider.py >> /tmp/oschina.log &
nohup python -u jobbole_spider.py  >> /tmp/jobbole.log &
