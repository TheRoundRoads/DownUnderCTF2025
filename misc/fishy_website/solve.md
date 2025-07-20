# misc/Fishy Website

> Dear player,
> 
> Found this fishy website URL on my e-mail and it started to do some crazy stuff on my computer. I have captured some network traffic that may help you find out what is happening on my computer. Thanks a lot for the help!
> 
> Regards,
> 
> k3ng

## Analyzing pcap traffic
We are given a single capture file `capture.pcapng`.

Since it involes a website, of course my first guess is to look for any HTTP data. Luckily there is a GET request sent to `/verify/script`.

The response contains an extremely long base64 encoded payload. I used `decrypt_powershell.py` to write it to another file `decoded.ps1`. Need to base64 decode and convert from widestring.

## Analysing powershell script
It is obfuscated with variables named: B8B8... and function names like IIlIlIlIllIIllIl.

But there are 4 main functions used:
1. `decrypt_xor`: This is used to decrypt certain data like website name, IP address
2. `rc4` (encrypt/decrypt): Used to encrypt/decrypt traffic sent to and from the server. The RC4 key used can be found at the top of the script.
3. `create_tls_payload`: Used to encrypt payload before sending to the server
4. `tls_handshake`: Used at the start of the program.

The script attempts to connect to `20.5.48.200:443`. 

Then it calls `tls_handshake`, including informatino like `'verify.duwnonder.com'` and some standard bytes of data.

## Decrypting TLS traffic
The following communication with the server is as follows:
|Offset|Size|Remarks|
|-|-|-|
|0x0|0x3|Standard TLS header `"\x17\x03\x03"`|
|0x3|0x2|`n` = Size of payload in big endian|
|0x5|`n`|RC4 encrypted payload|

Using this information, we can then decrypt the communication using the script found in `decrypt_traffic.py`

We can see that the server invokes a command to encode the bytes of `C:\Users\jdoe\Documents\keys_backup.tar.gz` in base64, which the client sends over.

Saving the bytes to a file and gzip + tar extract, we can get a file `keys.txt` containing the flag: `DUCTF{1_gu355_y0u_c4n_d3cRyPT_TLS_tr4ff1c}`