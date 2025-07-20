import numpy as np
from scipy.io import wavfile
from scipy.signal import find_peaks
from scipy.fft import rfft, rfftfreq

# === CONFIG ===
SCALE = 4
WAV_FILE = "beepbeep.wav"  # <-- Replace with your actual WAV path
PREAMBLE_DURATION = 1.92  # seconds
THRESHOLD = 500  # Adjust if needed for peak detection
WINDOW_SIZE = 2048 // SCALE
HOP_SIZE = 1024 // SCALE

# === LOAD AUDIO ===
rate, data = wavfile.read(WAV_FILE)
if data.ndim == 2:
    data = data[:, 0]  # take one channel

# === SPLIT INTO FRAMES ===
def dominant_freq(frame, rate):
    win = np.hanning(len(frame)) * frame
    spectrum = np.abs(rfft(win))
    freq_bins = rfftfreq(len(frame), 1/rate)
    peak = np.argmax(spectrum)
    return freq_bins[peak]

# === EXTRACT DOMINANT FREQUENCIES PER WINDOW ===
positions = []
frequencies = []

for i in range(0, len(data) - WINDOW_SIZE, HOP_SIZE):
    start = i
    end = i + WINDOW_SIZE
    frame = data[start:end]

    energy = np.sum(np.abs(frame))
    if energy > THRESHOLD:
        time_pos = start / rate
        freq = dominant_freq(frame, rate)
        positions.append(time_pos)
        frequencies.append(freq)

# === IDENTIFY REFERENCE FREQUENCIES FROM PREAMBLE ===
preamble_freqs = [
    f for t, f in zip(positions, frequencies) if t < PREAMBLE_DURATION
]

# Remove near-duplicates
def cluster_frequencies(freqs, tolerance=20):
    freqs = sorted(freqs)
    clusters = []
    for f in freqs:
        if not clusters or abs(clusters[-1][-1] - f) > tolerance:
            clusters.append([f])
        else:
            clusters[-1].append(f)
    return [np.mean(cluster) for cluster in clusters]

reference_freqs = cluster_frequencies(preamble_freqs)
reference_freqs = sorted(reference_freqs)
print(f"[+] Detected reference frequencies ({len(reference_freqs)}):")
for i, f in enumerate(reference_freqs):
    print(f"  {i}: {f:.1f} Hz")

# === MAP FREQUENCIES TO SYMBOLS ===
def map_to_symbol(freq):
    return np.argmin([abs(freq - ref) for ref in reference_freqs])

data_symbols = []
for t, f in zip(positions, frequencies):
    if t >= PREAMBLE_DURATION:
        symbol = map_to_symbol(f)
        data_symbols.append(symbol)

# print("\n[+] Extracted symbol sequence:")
# print(data_symbols)

def deduplicate_beeps(symbols):
    deduped = []
    i = 0
    while i < len(symbols):
        count = 1
        while i + count < len(symbols) and symbols[i + count] == symbols[i]:
            count += 1

        if count >= 4:
            # Assume multiple adjacent beeps of same tone
            num_beeps = round(count / 3)  # each beep ~3 entries
            deduped.extend([symbols[i]] * num_beeps)
        else:
            deduped.append(symbols[i])

        i += count
    return deduped

original = deduplicate_beeps(data_symbols)
data = "".join([chr(ord("a")+val) for val in original])
open("extracted.txt", "w").write(data)