#please pip install pexpect first

import pexpect

child = pexpect.spawn('passwd root')
child.delaybeforesend = 2
child.sendline("banana")
child.sendline("banana")