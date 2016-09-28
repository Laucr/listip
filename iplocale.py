# __author__ = lau
# 2016.9.14
import urllib2
import sys
import re


def locale_ip(ip):
    req_url = 'http://ip.cn/index.php?ip='
    response = urllib2.urlopen(req_url + ip)
    html = response.read()
    pattern = re.compile('(<code>)(.)+(</code>)')
    match = pattern.search(html)
    if match:
        locale = match.group().strip('</code>').split('<code>')[-1].split()[0]
    else:
        locale = ''
    return locale


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print locale_ip('').decode('utf8')
    elif len(sys.argv) == 2:
        print locale_ip(sys.argv[1]).decode('utf8')
    else:
        print 'args error.'
