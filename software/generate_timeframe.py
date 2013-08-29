import numpy as np
import scipy
import scipy.optimize
import pll


def generate_timeframe(signal, angular_frecuency, sampling_rate):
  """ Generate a vector with the times of the samples in signal.
  
  Signal must be composed of a number of pulses and noise.
  
  The estimatiom of the starting point is done by detecting the phase of the
  signal, and then finding the root using newton's method using the first
  sample over a threshold as a starting guess."""
  
  threshold = 5000
  start = 0
  for i in range(signal.size):
    if abs(signal[i]) > threshold:
      start = i*1.0/sampling_rate
      break
  phase = pll.pll(signal, angular_frecuency, sampling_rate)
  
  def f(x):
    return scipy.sin(angular_frecuency*x+phase)
  def fprime(x):
    return angular_frecuency*scipy.cos(angular_frecuency*x+phase)
    
  start = scipy.optimize.newton(f, start, fprime=fprime)
  
  return np.arange(-start, -start+1.0*signal.size/sampling_rate, 1.0/sampling_rate)
