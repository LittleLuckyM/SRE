#!/usr/bin/env python
#A System Information Gathering Script

import subprocess

#Command 1
uname= "uname"
uname_arg = "-a"
print "Gathering system information with %s command:\n" % uname
subprocess.call([uname,uname_arg])

#Command 2
diskspace = "df"
diskspace_age = "-h"
print "Gathering diskspace imformation %s command:\n" % diskspace
subprocess.call([diskspace,diskspace_age])


