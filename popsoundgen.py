import numpy as np
from scipy.io import wavfile

# Sound parameters
sample_rate = 44100  # CD quality audio (44.1 kHz)
duration = 0.2       # Short sound duration in seconds

# Create time array
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Generate the pop sound
# This combines a short attack, brief sustain, and quick decay
# with some frequency modulation to create a "pop" effect

# Start with quick rise (attack)
attack = 0.01  # 10 milliseconds
attack_samples = int(attack * sample_rate)
attack_env = np.linspace(0, 1, attack_samples)

# Followed by a brief sustain and quick decay
decay = duration - attack
decay_samples = int(decay * sample_rate)
decay_env = np.linspace(1, 0, decay_samples) ** 2  # Square for faster decay

# Combine envelopes
envelope = np.concatenate([attack_env, decay_env])
if len(envelope) < len(t):  # Ensure same length
    envelope = np.pad(envelope, (0, len(t) - len(envelope)))
elif len(envelope) > len(t):
    envelope = envelope[:len(t)]

# Create frequency modulation for the pop effect
frequency = 400  # Base frequency in Hz
freq_mod = np.linspace(1.5, 0.7, len(t))  # Frequency drops during sound
phase = 2 * np.pi * frequency * freq_mod * t

# Generate waveform with envelope
signal = envelope * np.sin(phase)

# Add a bit of noise for texture
noise = np.random.normal(0, 0.1, len(t)) * envelope
signal = signal + noise

# Normalize to prevent clipping
signal = signal / np.max(np.abs(signal))

# Convert to 16-bit PCM
signal_16bit = (signal * 32767).astype(np.int16)

# Write to WAV file
wavfile.write('pop.wav', sample_rate, signal_16bit)

print("Successfully created pop.wav!")