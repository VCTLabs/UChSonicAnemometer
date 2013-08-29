import numpy as np

def pll(signal, angular_frecuency, sample_rate):
  """ Detects the phase of the signal using minimum square error."""
  best_phase = 0
  best_mse = float('inf')
  x = np.arange(0, signal.size)/(1.0*sample_rate)
  for phase in np.arange(0, 2*np.pi, 0.01):
    difference = signal - np.sin(angular_frecuency*x+phase)
    mse = np.sum(np.power(difference, 2))
    if mse < best_mse:
      best_mse = mse
      best_phase = phase
  return best_phase
