import envelope_detector

from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import unittest


class TestEnvelopeDetector(unittest.TestCase):
  def setUp(self):
    self.frecuency = 25500
    self.w = 2*np.pi*self.frecuency
    (self.sample_rate, self.audio_data) = wavfile.read("test_data.wav")

  def test_envelope_detector(self):
    x = np.arange(0, self.audio_data.shape[0])/(1.0*self.sample_rate)
    envelope = envelope_detector.envelope_detector(
                 self.audio_data[:,0], self.frecuency, self.sample_rate)
    plt.plot(x, self.audio_data[:,0])
    plt.plot(x, envelope)
    plt.show()


if __name__ == '__main__':
  unittest.main()
