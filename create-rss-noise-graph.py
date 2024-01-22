from scapy.all import *
import matplotlib.pyplot as plt

def extract_signal_noise_snr(pcap_file):
    signal_strength_list = []
    noise_level_list = []

    # Read the pcap file
    packets = rdpcap(pcap_file)

    # Extract signal strength and noise level from RadioTap headers for probe requests
    for packet in packets:
        if RadioTap in packet and Dot11ProbeReq in packet:
            # Check if the fields exist before adding to the lists
            if hasattr(packet[RadioTap], 'dBm_AntSignal') and hasattr(packet[RadioTap], 'dBm_AntNoise'):
                signal_strength = packet[RadioTap].dBm_AntSignal
                noise_level = packet[RadioTap].dBm_AntNoise

                signal_strength_list.append(signal_strength)
                noise_level_list.append(noise_level)

    # Calculate SNR only for packets with both signal strength and noise level
    snr_list = [signal - noise for signal, noise in zip(signal_strength_list, noise_level_list)
                if signal is not None and noise is not None]

    return signal_strength_list, noise_level_list, snr_list

def plot_signal_noise_snr(signal_strength, noise_level, snr):
    # Plotting
    plt.plot(signal_strength, label='Signal Strength (dBm)', color='blue')
    plt.plot(noise_level, label='Noise Level (dBm)', color='red')
    plt.plot(snr, label='SNR (dB)', color='green')

    plt.xlabel('Packet Number')
    plt.ylabel('Amplitude (dBm)')
    plt.title('Signal Strength, Noise Level, and SNR Over Probe Requests')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    # Specify the path to your pcap file
    pcap_file_path = 'data/<name-of-the-pcap-file>.pcap'


    # Extract and plot signal strength, noise level, and SNR for probe requests
    signal_strength, noise_level, snr = extract_signal_noise_snr(pcap_file_path)
    plot_signal_noise_snr(signal_strength, noise_level, snr)
