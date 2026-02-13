import pexpect
import sys

child = pexpect.spawn('python manage.py makemigrations rango')
child.expect('Select an option:')
child.sendline('1')
child.expect('>>>')
child.sendline("''")
child.interact()