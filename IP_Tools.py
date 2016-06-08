#!/usr/bin/env python
from IPy import IP

ip_s = raw_input('Please input an IP or net-range: ')
ips = IP(ip_s)
if len(ips) > 1:
    print('net: %s' % ips.net())
    print('mask: %s' % ips.netmask())
    print('broadcast: %s' % ips.broadcast())
    print('reverse address: %s' %ips.reverseName())
