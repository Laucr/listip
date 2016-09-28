# __author__ = lau
# 2016.9.28
import ns_select
import dig_anlyz
import os
import sys


def clean():
    os.popen('rm *.pyc')
    os.popen('rm *.log')


def executor(_domain_, _db_path_, _f_path_):
    ns_list = ns_select.NsSelector(_db_path_, _f_path_)
    server_list = ns_list.select()
    analyzer = dig_anlyz.DigAnalyzer(server_list, _domain_)
    ip_list = analyzer.analyze()
    print '[*] Total', len(ip_list), 'ip(s).'
    for ip in ip_list:
        print '[+]', ip

    clean()


def show_help():
    print '[*] Usage: python listip.py domain [options]'
    print '    -D, --db     Set database file path.'
    print '    -F, --file   Set server file path.'
    print '    -H, --help   Show help info.'

if len(sys.argv) > 1:
    db_path = 'servers.db'
    f_path = 'servers.txt'
    options = sys.argv[1:]
    if len(options) == 1:
        if '-H' in options or '--help' in options:
            show_help()
        else:
            executor(options[0], db_path, f_path)
    elif len(options) == 3 or len(options) == 5:
        if '-D' in options:
            db_path = options[options.index('-D') + 1]
        elif '--db' in options:
            db_path = options[options.index('--db') + 1]
        elif '-F' in options:
            f_path = options[options.index('-F') + 1]
        elif '--file' in options:
            f_path = options[options.index('--file') + 1]
        executor(options[0], db_path, f_path)
    else:
        print '[!] Error parameters.'
        show_help()
else:
    print '[!] Error parameters.'
    show_help()



