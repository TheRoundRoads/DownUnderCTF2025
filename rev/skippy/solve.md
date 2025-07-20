# rev/skippy

> Dear player,
> 
> Skippy seems to be in a bit of trouble skipping over some sandwiched functions. Help skippy get across with a hop, skip and a jump!
> 
> Regards,
> 
> jzt

This challenge has 2 approaches, either patching or debugging. I did the debugging method, but now that I think about it probably patching is easier, because you don't have to keep manually changing the values.

There are 2 problematic functions: `stone` and `decryptor`.


## stone
In `stone`, the problem is that the program attempts to write to constant memory, in the line: `aOhNoSkippyIsAb[0] = *a1;`

In assembly, this is the line: `mov [rax], dl`. I found that `rbp-8` seems like a safe place to write memory, so I changed `rax` to `rbp-8`.

## decryptor
In `decryptor`, the program tries to access the memory at 0, which is invalid.
This is in the lines:
```asm
mov     [rbp+var_10], 0
mov     rax, [rbp+var_10]
mov     eax, [rax]
```
Again, before `mov eax, [rax]`, I changed the value of `rax` to `rbp-8`.

Repeating this multiple times, we can get the flag.