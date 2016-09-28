# __author__ = lau
# 2016.9.28
import os
import re


class DigAnalyzer:
    __version__ = '1.0'
    __author__ = 'Lau'
    _server_list_ = []
    _log_file_ = 'dig.log'
    _domain_ = ' '

    def __init__(self, server_list, domain):
        self._server_list_ = server_list
        self._domain_ += domain

    def _get_dig_response_(self):
        server_list = self._server_list_
        log = open(self._log_file_, 'a')
        for server in server_list:
            print '[-] Dealing with', server[1]
            cmd = 'dig @' + server[1] + self._domain_
            response = os.popen(cmd).read()
            pattern = re.compile('(;; ANSWER SECTION:\\n)([\s\S]*?)(\\n\\n)')
            m = re.search(pattern, response)
            if m is not None:
                log.write(m.group(2).strip())
                log.write('\n')
        log.close()

    def analyze(self):
        try:
            self._get_dig_response_()
            response = open(self._log_file_, 'r')
            lines = response.readlines()
            ip_list = []
            for line in lines:
                if "A" in line.split() and line.split()[4] not in ip_list:
                    ip_list.append(line.split()[4])
            return ip_list
        except IOError:
            print '[!] There is something wrong getting dig response, try plan B like:'
            self.__plan_b__()

    def __plan_b__(self):
        with open('nslist.txt') as nsl:
            for ns in self._server_list_:
                nsl.write(ns[1] + '\n')
