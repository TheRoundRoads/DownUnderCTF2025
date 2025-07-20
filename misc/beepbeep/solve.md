# misc/beepbeep
> Dear player,
> 
> We were able to pull some audio from the answering machine service, which is hooked straight up to the mainframe. This doesn't sound like anything we've heard before though it may give some clues to how the planet ended up this way. Are you able to work what this is?
> 
> Regards,
> 
> Nosurf

We are given a wav file `beepbeep.wav`.
Listening to it it starts with a increasing beeps, then a lot of various beeps.
We can pipe it to a spectrogram, but not very useful as it is very long.

Looking at the first 10 seconds, using 
```
sox beepbeep.wav trimmed.wav trim 0 10  # First 10 seconds
sox trimmed.wav -n spectrogram -o zoomed.png
```
Looking at zoomed.png, we see that there are an increasing number of beeps at the start. This is likely the reference beeps.
Counting it manually there are 26 which matches the number of alphabets.

Extracting the beep values and playing around with the WINDOW_SIZE, we can extract the beeps.
Then convert to ascii we get a very long string of text in `extracted.txt`.

We can see the flag embedded in: `ductfopenbracketiforonewelcomeouraioverlordsclosebracket`

Hence the flag: `ductf{iforonewelcomeouraioverlords}`