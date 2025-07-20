# rev/bilingual

> Dear player,
> 
> Two languages are better than one!
> 
> Regards,
> 
> FozzieBear (cybears)

This was probably the most interesting challenge that I managed to solve.

The challenge presents us with a single file `bilingual.py`. It expected a single command line argument, which is the password.

It writes some contents into a file `hello.bin`. From the code we can guess that it is a DLL. 

Running the script, it creates the `hello.bin` file, which we can decompile. For some reason, it makes IDA crash, so I did this challenge using ghidra.

Essentially the DLL has 4 main check functions: `Check[1-4]`.

`Check1` and `Check2` are relatively straightforward to reverse.

`Check3` and `Check4` are quite a bit harder.

The interesting part of this challenge is that the DLL creates strings, and passes it into python's `eval` function. So you can't reverse everything within the DLL, it uses python as well.

## Check1
The python portion checks that the length of the password is 12.

The DLL portion checks that `password[0] == "H"`. It also sets a global variable `DAT_180009000 = 0x7a`, which will be used later on in `Check4`.

## Check2
The python portion passes this function as a parameter to the DLL `Check2` function:
```python
def callback(i):return ord(password[i-3])+3
```

We can easily reverse it to find that it checks for:
`password[5] == "p"` and `password[6] == "h"`

It also sets `DAT_180009001 = 0x6d`, which is used later on in `Check4`.

## Check3
For both `Check3` and `Check4`, python's `eval` function is being passed as the parameter to the DLL function.

We can see that in `Check3`, the DLL stores some wide strings in memory, including `ord(%s[%d])`. It is likely that these will be passed into the python's `eval` function.

To make things easier to myself, I added a line within the callback function, to print whatever string is being passed into it. This can be found in `bilingual_patched.py`:
```python
def eval_int(v): print(v); return int(eval(v))
```

This made it much easier to reverse, and we can actually see what functions the DLL is calling.

We can also see that in the DLL, the following string is used: `" %d > 48 and %d < 57"`, which corresponds to the ascii codes of `0` and `9` respectively. Likely some portion of our input should be digits.

Currently we know the password is of the form:
`H????ph?????`

So to test this part, I filled them all with digits, so if they appear, we know exactly which digit is being accessed.

So I tried for the input: H1234ph56789

The output gotten is, the code attempts to call `ord(PASSWORD[i])` for all i = 0...11.

Next, it evaluates the following expression:
`54 + 2 == 57 and 53 == 54 and (57 - 4) == 57  and 53 > 48 and 53 < 57 and 54 > 48 and 54 < 57 and 57 > 48 and 57 < 57`

We can tell that there are 4 of our input chaarcters being checked here from the values 54, 57, 53, and 4.

These correspond to our input values 6, 9, 5, and 4.

So the indexes being checked are: 4, 7, 8, 11.

Now we know that: `password[4] == "0"`, `password[7] == password[8]` and `password[8] + 2 == password[11]`.

Also for indexes 7, 8, and 11, they must be digits of values from 1...8. So that means indexes 7 and 8 must be from 1...6.

For the easiest case I just tried `password[7] == password[8] == "1"` and `password[11] == "3"`, which turns out to actually be the answer in the end. But this part can be easily brute forced later on.

So now we know the password is in the form:
`H???0ph<x><x>??<x+2>`

## Check 4
This is definitely the hardest function.
At the start we see some wide strings being stored:
`L"ord(PASSWORD[i])"`, where i = 1, 2, 3.
This shows that the program is now checking indexes 1 to 3. They are then stored in some variables.

Next there is the function at address 0x180002060 being called. Reversing it, it calls 2 subroutines --> an RC4 decryption algorithm, and a djb2 hash variant checker.

Turns out that the global variable `DAT_180009000` will be used as the key for the decryption.

Using our printing python script again, we can see that the program attempts to evaluate `int(KEY[1:4])`, then stops.

This is because after that, it makes use of chracters from password indexes 1 to 3 to populate a new 8 byte key for RC4 decryption, then checks against the existing djb2 hash. Since the key is wrong, the hash doesn't match, and the program doesn't execute anymore.

For this part, I just tried to brute force the 3 characters, and see which output gives a different value (i.e. it executes something else after `int(KEY[0:4])`).

Using `check_output.py` to identify which output is different, the 3 characters are: `ydr`.

So now our new password is: 
`Hydr0ph<x><x>??<x+2>`, which is promising because it looks like a word. There are 2 characters left, which I also just used brute force to get, and treating `x = 1`.

In the end we can get the password to be `Hydr0ph11na3`, and the flag `DUCTF{the_problem_with_dynamic_languages_is_you_cant_c_types}`.

One mistake I made was I was so hung up on brute forcing the key and checking the hash, but that search space is much larger, because we don't know the initialised values of `DAT_180009002` and `DAT_180009007`. I guess you can connect a remote debugger somehow and access the values, but I wasn't sure how to do that.