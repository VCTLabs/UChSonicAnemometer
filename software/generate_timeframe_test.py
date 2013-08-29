import generate_timeframe

from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import unittest


class TestGenerateTimeframe(unittest.TestCase):
  def setUp(self):
    self.frecuency = 25500
    self.w = 2*np.pi*self.frecuency
    (self.sampling_rate, self.audio_data) = wavfile.read("test_data.wav")

  def test_pll(self):
    x = generate_timeframe.generate_timeframe(self.audio_data[:,1],
                                              self.w,
                                              self.sampling_rate)
    plt.plot(x, self.audio_data[:,1], '*-')
    plt.show()


if __name__ == '__main__':
  unittest.main()
