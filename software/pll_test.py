import pll

from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import unittest


class TestPll(unittest.TestCase):
  def setUp(self):
    self.frecuency = 25500
    self.w = 2*np.pi*self.frecuency
    (self.sample_rate, self.audio_data) = wavfile.read("test_data.wav")
    self.zoom = 10000

  def test_pll(self):
    x = np.arange(0, self.audio_data.shape[0])/(1.0*self.sample_rate)
    phi = pll.pll(self.audio_data[:,0], self.w, self.sample_rate)
    print phi
    plt.plot(x, self.audio_data[:,0])
    plt.plot(x, self.zoom*np.sin(self.w*x+phi))
    plt.show()


if __name__ == '__main__':
  unittest.main()
