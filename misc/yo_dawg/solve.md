# misc/YoDawg

> Dear player,
> 
> We found this file on a USB drive, it seems to be some sort of gamified cyber skilled based learning system thingy?
> 
> Maybe if all of the challenges are sold we will get some answers, or maybe it is just the friends we make along the way.
> 
> Note - This may produce false positives with your virus scanner.
> 
> Regards,
> 
> Nosurf

This was quite an interesting and creepy challenge.

For this challenge, we are given a zip file containing an executable and a dll. Usually for this case, it is more useful to analyze the dll.

Running the executable, we get a sort of mini CTF challenge, with multiple easy challenges. There are also jumpscares and like eerie things involved.

For example, the `Even Deeper` challenge requires you to submit your username in the flag. After you submit it, it then says "Shouldn't it be {your windows username}", which kind of seems like it hacked your computer.

Because I wasn't sure how to solve the `Hidden` challenge, I opted for the rev route for this challenge. 

## rev
I used the errors that appear when you make a wrong submission to gauge where the encrypted flags are. Amongst the error messages, there are some plaintext flags, and some base64 strings. These are likely the encrypted flags.

Looking at cross references to the strings, I found that they are decrypted using AES. We can then recover the AES key and IV (although they are a lot of fakes, but it is quite easy to tell using cross references).

I then wrote a script `aes.py` to decrypt the flags using AES.

There are 2 parts to the mini CTF. After solving all the challenges, they provide the DES-encoded flag, which I wrote another script `des.py` to decode. We can get the flag: `DUCTF{1995_to_2025}`