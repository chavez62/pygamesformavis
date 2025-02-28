import numpy as np
from scipy.io import wavfile

# Sound parameters
sample_rate = 44100  # CD quality audio (44.1 kHz)
duration = 1.0       # Sound duration in seconds

# Create time array
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Generate a childish laugh sound with multiple "ha" sounds
def generate_laugh():
    # Number of "ha" sounds in the laugh
    num_ha = 4
    
    # Full laugh signal
    laugh_signal = np.zeros_like(t)
    
    # Duration of each "ha" sound
    ha_duration = duration / num_ha
    samples_per_ha = int(sample_rate * ha_duration)
    
    # Base frequencies and modulation
    base_freq = 300  # Base frequency for a child's voice
    
    for i in range(num_ha):
        # Time segment for this "ha"
        start_idx = i * samples_per_ha
        end_idx = min((i + 1) * samples_per_ha, len(t))
        t_segment = t[start_idx:end_idx] - t[start_idx]  # Reset time to start at 0
        
        # Slight variations in pitch for each "ha"
        pitch_variation = 1.0 + 0.05 * np.sin(i * 0.7)
        freq = base_freq * pitch_variation
        
        # Create amplitude envelope for each "ha"
        # Fast attack, slow decay
        attack_time = 0.1 * ha_duration
        decay_time = 0.9 * ha_duration
        
        attack_samples = int(attack_time * sample_rate)
        decay_samples = int(decay_time * sample_rate)
        
        # Create envelope
        envelope = np.zeros_like(t_segment)
        
        # Attack phase (quick rise)
        attack_indices = np.arange(min(attack_samples, len(t_segment)))
        if len(attack_indices) > 0:
            envelope[attack_indices] = np.linspace(0, 1, len(attack_indices))
        
        # Decay phase
        decay_indices = np.arange(min(attack_samples, len(t_segment)), len(t_segment))
        if len(decay_indices) > 0:
            envelope[decay_indices] = np.linspace(1, 0.2, len(decay_indices)) ** 0.7
        
        # Frequency modulation for more natural sound
        vibrato_rate = 8.0  # Hz
        vibrato_depth = 0.03
        freq_mod = 1.0 + vibrato_depth * np.sin(2 * np.pi * vibrato_rate * t_segment)
        
        # Generate harmonic components
        signal = np.zeros_like(t_segment)
        
        # Fundamental
        signal += 1.0 * np.sin(2 * np.pi * freq * freq_mod * t_segment)
        
        # First harmonic (one octave up)
        signal += 0.5 * np.sin(2 * np.pi * freq * 2 * freq_mod * t_segment)
        
        # Second harmonic
        signal += 0.25 * np.sin(2 * np.pi * freq * 3 * freq_mod * t_segment)
        
        # Add a bit of noise for texture
        noise = np.random.normal(0, 0.05, len(t_segment))
        
        # Combine components with envelope
        ha_signal = envelope * (signal + noise)
        
        # Add to full laugh
        laugh_signal[start_idx:end_idx] = ha_signal
    
    return laugh_signal

# Generate laugh
signal = generate_laugh()

# Normalize to prevent clipping
signal = signal / np.max(np.abs(signal)) * 0.9

# Convert to 16-bit PCM
signal_16bit = (signal * 32767).astype(np.int16)

# Write to WAV file
wavfile.write('laugh.wav', sample_rate, signal_16bit)

print("Successfully created laugh.wav!")