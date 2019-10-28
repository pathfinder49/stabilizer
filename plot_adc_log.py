import numpy as np
from matplotlib import pyplot as plt

if __name__=="__main__":
    plt_every_n = 100

    samples = np.load("adc_log.npy")

    print("np.diff(data).std()/2**.5". np.diff(samples).std()/2**.5)

    plt.figure(figsize=(10,10))
    plt.plot(np.arange(samples.shape[0])[::plt_every_n], samples[::plt_every_n],
             linestyle='', marker='x', markersize=1.5)
    plt.ylabel("LSB")
    plt.xlabel(r"$n^{th}$ sample")
    plt.title(r"stabilizer_current_sense open loop noise")
    # plt.savefig("LSB_log.png", dpi=600)
    plt.savefig("LSB_log.pdf")
    # plt.show()

    # LSB to V
    v_fact = 2 * 4.096 / 2**16
    plt.figure(figsize=(10,10))
    plt.plot(np.arange(samples.shape[0])[::plt_every_n], v_fact * samples[::plt_every_n],
             linestyle='', marker='x', markersize=1.5)
    plt.ylabel("Volt")
    plt.xlabel(r"$n^{th}$ sample")
    plt.title(r"stabilizer_current_sense open loop noise")
    # plt.savefig("V_log.png", dpi=600)
    plt.savefig("V_log.pdf")
    # plt.show()
