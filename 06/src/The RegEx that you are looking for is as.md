The RegEx that you are looking for is as follows:

```python
(?P<dest>[AMD]{1,3}=)?(?P<comp>[01\-AMD!|+&><]{1,3})(?P<jump>;[JGTEQELNMP]{3})?
```

Let's break it down into parts:

- `(?P<dest>[AMD]{1,3}=)?` - will search for optional `destination` to store the computation result in it. 
- `(?P<comp>[01\-AMD!|+&><]{1,3})` - will search for `computation` instruction.
- `(?P<jump>;[JGTEQELNMP]{3})?` - will search for optional `jump` directive.

Do note, that `dest` and `jump` parts of every `C-Instruction` are optional.  
They only appear  with postfix `=` and prefix `;` respectively.

Hence, you will have to take care of these signs:
```python
if dest is not None:
    dest = dest.rstrip("=")

if jump is not None:
    jump = jump.lstrip(";")
```

Finally, you will get the desired `C-Instrucion` parsing:

For the line `A=A+M;JMP` you will get:
```python
dest = 'A'
comp = 'A+M'
jump = 'JMP'
```
For the line `D;JGT` you will get:
```python
dest = None
comp = 'D'
jump = 'JGT'
```

And for the line `M=D` you will get:
```python
dest = 'M'
comp = 'D'
jump = None
```


|          | `A=A+M;JMP`   |   `D;JGT`     |  `M=D`    |
| -------- | :---------:   | :---------:   | :-----:   |
| **dest** | `'A'`         | `None`        | `'M'`     |
| **comp** | `'A+M'`       | `'D'`         | `'D'`     |
| **jump** | `'JMP'`       | `'JGT'`       | `None`    |
