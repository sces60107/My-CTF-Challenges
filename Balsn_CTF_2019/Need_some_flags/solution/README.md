# Preface

At the beginning, I wanted to create some reverse challenges. And my targets are python bytecode and wasm. 

So I went to mess around with python bytecode. A couple of hours later, I created two misc challenges.

# Need_some_flags

## Intended Solution 1
In this challenge, you can do these things:

* [0] Write a flag
* [1] Edit a flag
* [2] push your flag
* [3] Secret flag
* [4] Bye bye

And the flag is in `secretflag` function. But it is deleted. And there is no way to print it out.

```python
def secretflag():
  # I know you want this secret flag
  flag="Balsn{this_flag_is_on_the_server}"
  # But I can't give it to you
  del flag
  # How about a non-secret flag
  reload(nonsecret)
  nonsecret.printflag()
```
Also, `nonsecret.printflag` only give you a fake flag

```python
def printflag():
  flag="balsn{Absolutely_not_the_flag_you_want}"
  print flag
```

However, `reload(nonsecret)` seems really weird. That actually points out that you should do something with `nonsecret.py`

Now let's take a look at the other functions:

`writeflag` is useless in this chal. And `pushflag` is disabled.

But in `editflag`, you can edit a file with six bytes. But here are some constraints.

* The file should be in current diretory
* The file should exist
* Can't edit server.py and nonsecret.py

At this moment, you should know that the only file I want you to edit is `nonsecret.pyc`.

My intended solution is modifying bytecode in `nonsecret.pyc`

Here is the bytecode in `nonsecret.printflag`

```python
  2           0 LOAD_CONST               1 ('balsn{Absolutely_not_the_flag_you_want}')
              3 STORE_FAST               0 (flag)

  3           6 LOAD_FAST                0 (flag)
              9 PRINT_ITEM          
             10 PRINT_NEWLINE       
             11 LOAD_CONST               0 (None)
             14 RETURN_VALUE        
             
```
Use `gdb` on `/usr/bin/python2.7` And try to mess up with `nonsecret.pyc`

```gdb
Welcome to BalsnCTF. We are so glad to see you guys here.

To host a CTF, we need tons of flags. Then I thought maybe you can help us.
We would appreciate it if you can provide us some flags.


[0] Write a flag
[1] Edit a flag
[2] push your flag
[3] Secret flag
[4] Bye bye

What's your choice? 1
Why do you want to edit the flag? You should be more careful! I can only let you edit 6 bytes and only edit once
Please give me the flag's name :nonsecret.pyc
Please input the edited content (in hex)ffff
Please input the offset71

[0] Write a flag
[1] Edit a flag
[2] push your flag
[3] Secret flag
[4] Bye bye

What's your choice? 3
Program received signal SIGSEGV, Segmentation fault.

[----------------------------------registers-----------------------------------]
RAX: 0x0 
RBX: 0x3 
RCX: 0xffff 
RDX: 0xff00 
RSI: 0x0 
RDI: 0x555555754460 --> 0xffef4eeaffe5e29c 
RBP: 0xffff 
RSP: 0x7fffffffd5a0 --> 0x555555af12f0 --> 0x0 
RIP: 0x55555564dbf9 (<PyEval_EvalFrameEx+19049>:	add    QWORD PTR [r12],0x1)
R8 : 0x7ffff7e481c8 --> 0x0 
R9 : 0x7ffff7e3e40f --> 0x484700007c00007d ('}')
R10: 0x64 ('d')
R11: 0x7ffff7e481d0 --> 0x7ffff7e9c1b0 --> 0x1 
R12: 0x0 
R13: 0x7ffff7e48050 --> 0x1 
R14: 0x7ffff7e481d8 --> 0x0 
R15: 0x0
EFLAGS: 0x10206 (carry PARITY adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x55555564dbeb <PyEval_EvalFrameEx+19035>:	sub    rbx,QWORD PTR [rsp+0x10]
   0x55555564dbf0 <PyEval_EvalFrameEx+19040>:	
    mov    r12,QWORD PTR [r14+rbp*8+0x18]
   0x55555564dbf5 <PyEval_EvalFrameEx+19045>:	lea    r14,[r11+0x8]
=> 0x55555564dbf9 <PyEval_EvalFrameEx+19049>:	add    QWORD PTR [r12],0x1
   0x55555564dbfe <PyEval_EvalFrameEx+19054>:	mov    QWORD PTR [r11],r12
   0x55555564dc01 <PyEval_EvalFrameEx+19057>:	
    mov    eax,DWORD PTR [rip+0x49d351]        # 0x555555aeaf58
   0x55555564dc07 <PyEval_EvalFrameEx+19063>:	test   eax,eax
   0x55555564dc09 <PyEval_EvalFrameEx+19065>:	mov    esi,eax
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffd5a0 --> 0x555555af12f0 --> 0x0 
0008| 0x7fffffffd5a8 --> 0x0 
0016| 0x7fffffffd5b0 --> 0x7ffff7e3e40c --> 0x7c00007dffff64 
0024| 0x7fffffffd5b8 --> 0x0 
0032| 0x7fffffffd5c0 --> 0x7ffff7e481c8 --> 0x0 
0040| 0x7fffffffd5c8 --> 0x7ffff7f939d0 --> 0x24 ('$')
0048| 0x7fffffffd5d0 --> 0x7ffff7f93050 --> 0x529 
0056| 0x7fffffffd5d8 --> 0x7ffff7f793c0 --> 0x2 
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x000055555564dbf9 in PyEval_EvalFrameEx ()
gdb-peda$

```

What I did is modifying the offset argument of `LOAD_CONST` . The new offset is `0xffff`. You can find out `rbp` is the offset.

`[r14+rbp*8+0x18]` should point to a `PyObject *` pointer. Otherwise it will trigger Segmentation fault.

So the intended solution is finding the pointer which points to the flag. And calculate the offset.

However, you may find out you need a negative offset. You can leverage `EXTENDED_ARG` to create a negative offset. That's why I give you six byte to solve this challenge.

You can find the exploit script [here](Need_some_flags_exp.py)

## Intended Solution 2

There is actually one more intended solution. It's found by @how2hack.

He just tried all the possible offsets of `LOAD_CONST`. And he find out that we can use 2 bytes to beat this challenge.

However, this brute-force technique make him learn nothing in this chal. So he is not able to solve Need_some_flags_2.

By the way, this is why I put a pow in the task. I don't want players to solve this challenge using a brute-force method. That's not cool. But you can still use brute-force method locally after I provide the docker file.

You can find the exploit script [here](Need_some_flags_exp2.py)

# Need_some_flags_2

Once you know the trick of Need_some_flags.

It should be pretty easy for you to solve this challenge.

## Intended Solution

In this chal, I modified the `secretflag` function and `nonsecret.py`.

Let's take a glance.

`secretflag`:

```python
def secretflag():
  # No secret flag this time.
  # But I can do os.listdir() for you
  path=raw_input("Give me the directory path")
  reload(nonsecret)
  nonsecret.printlist(path)
```

`nonsecret.py`:

```python
import os
def printlist(path):
  print os.listdir(path)
```

Again, we should compromise `nonsecret.pyc`. 

`nonsecret.printlist`'s bytecode:

```python
  3           0 LOAD_GLOBAL              0 (os)
              3 LOAD_ATTR                1 (listdir)
              6 LOAD_FAST                0 (path)
              9 CALL_FUNCTION            1
             12 PRINT_ITEM          
             13 PRINT_NEWLINE       
             14 LOAD_CONST               0 (None)
             17 RETURN_VALUE        
```

This time our target is `LOAD_ATTR`. `LOAD_ATTR` practically loads a python string. It indicates that you need to find a `PyObject *` pointer that points to `system`.

Nonetheless you can't get a `system` string object in all possible offsets.

But you can create a `system` string yourself!!

Go to `writeflag` and input `system`. After that you can find a offset that points to your `system` string,

These are all the secrets in this challenge.

You can find the exploit script [here](Need_some_flags_2_exp.py)
