import numpy as np
from matplotlib import pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.signal import welch

def cleanup(file_name):
    with open(file_name, "r+") as f:
            d = f.readlines()
            f.seek(0)
            for i in d:
                if i != "\t\n":
                    f.write(i)
            f.truncate()

def main():
    # cleaning up the data files
    cleanup("adc.txt")
    cleanup("open_light.txt")
    cleanup("half_light.txt")
    cleanup("full_dark.txt")

    files = ["adc.txt", "open_light.txt", "half_light.txt", "full_dark.txt"]

    plt.figure("OSEM Noise")

    # for each file, plotting the noise spectral density v/s frequency
    for name in files:
        file = open(name, "r")
        lines = file.readlines()

        # reading voltage data for each reading
        voltages = []
        for line in lines:
            words = line.split("\t")
            voltages.append(float(words[1].strip("\n")))
        
        sample_rate = 256
        fftlength = 10
        voltages = voltages[10::]
        times = np.arange(len(voltages))/sample_rate
        
        # calculating power spectral density
        ff, psd = welch(voltages, fs=sample_rate, window='hann', nperseg=fftlength * sample_rate, noverlap = fftlength * sample_rate/2, nfft=fftlength * sample_rate)

        # ASD is sqrt of PSD
        plt.loglog(ff, np.sqrt(psd), label=name[:-4])
        plt.grid(True, which="both")
        plt.ylabel(r'Noise Spectral Density (V/$\sqrt{Hz}$')
        plt.xlabel('Frequency (Hz)')
        plt.legend()
        file.close()

    plt.show()

if __name__ == "__main__":
    main()
