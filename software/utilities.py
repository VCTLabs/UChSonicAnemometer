#
# Copyright (C) 2013  UNIVERSIDAD DE CHILE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors: Luis Alberto Herrera <herrera.luis.alberto@gmail.com>

import nonuniform_sampled_signal
import uniform_sampled_signal
from scipy import signal as scipysignal
import numpy as np

MEASURING_DIRECTIONS = ["NORTH", ]
SAMPLES_PER_DIRECTION = 3000
EXCITATION_SAMPLES = 300


def split_signal(signal):
  """ Splits a signal into all measuring direccions and aligns the zero
      timestamp to the  rising edge of the exitation of the transducer. """
  responses = dict()
  for i in range(len(MEASURING_DIRECTIONS)):
    frame = uniform_sampled_signal.UniformSampledSignal(
        signal.values[i*SAMPLES_PER_DIRECTION:(i+1)*SAMPLES_PER_DIRECTION-1],
        signal.sampling_rate)
    threshold = 1500
    start_of_response = 0
    for j in range(frame.values.size):
      if abs(frame.values[j]) > threshold:
        start_of_response = j+EXCITATION_SAMPLES
        frame.values = frame.values[start_of_response:].astype(np.float32)
        frame.values.resize((SAMPLES_PER_DIRECTION, ))
        frame.values *= 1.0/frame.values.max()
        frame.start_timestamp = (EXCITATION_SAMPLES+2.0)/frame.sampling_rate
        break
    responses[MEASURING_DIRECTIONS[i]] = frame
  return responses


def get_signal_envelope(signal):
  envelope = np.abs(scipysignal.hilbert(signal.values))
  result = uniform_sampled_signal.UniformSampledSignal(
      envelope, signal.sampling_rate)
  result.start_timestamp = signal.start_timestamp
  return result


def plot_signal_list(signals, axes, string_format):
  for signal in signals:
    plot_signal(signal, axes, string_format)

def plot_signal(signal, axes, string_format):
  axes.plot(signal.get_timestamp_array(), signal.values, string_format)
