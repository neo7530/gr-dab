#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 Moritz Luca Schmid, Communications Engineering Lab (CEL) / Karlsruhe Institute of Technology (KIT).
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

"""
receive DAB with USRP (for DAB+ reception see usrp_dabplus_rx.py)
"""

from gnuradio import gr, uhd, blocks
from gnuradio import audio, digital
from gnuradio import qtgui
from gnuradio import fft
import dab
import time, math


class usrp_dab_rx(gr.top_block):
    def __init__(self, dab_mode, frequency, bit_rate, address, size, protection, use_usrp, src_path, record_audio = False, sink_path = "None"):
        gr.top_block.__init__(self)

        self.dab_mode = dab_mode
        self.verbose = False
        self.sample_rate = 2e6
        self.use_usrp = use_usrp
        self.src_path = src_path
        self.record_audio = record_audio
        self.sink_path = sink_path

        ########################
        # source
        ########################
        if self.use_usrp:
            self.src = uhd.usrp_source("", uhd.io_type.COMPLEX_FLOAT32, 1)
            self.src.set_samp_rate(self.sample_rate)
            self.src.set_antenna("TX/RX")
        else:
            print "using file source"
            self.src = blocks.file_source_make(gr.sizeof_gr_complex, self.src_path, True)

        # set paramters to default mode
        self.softbits = True
        self.filter_input = True
        self.autocorrect_sample_rate = False
        self.resample_fixed = 1
        self.correct_ffe = True
        self.equalize_magnitude = True
        self.frequency = frequency
        self.dab_params = dab.parameters.dab_parameters(self.dab_mode, self.sample_rate, self.verbose)
        self.rx_params = dab.parameters.receiver_parameters(self.dab_mode, self.softbits,
                                                            self.filter_input,
                                                            self.autocorrect_sample_rate,
                                                            self.resample_fixed,
                                                            self.verbose, self.correct_ffe,
                                                            self.equalize_magnitude)
        ########################
        # FFT and waterfall plot
        ########################
        self.fft_plot = qtgui.freq_sink_c_make(1024, fft.window.WIN_BLACKMAN_HARRIS, self.frequency, 2e6, "FFT")
        self.waterfall_plot = qtgui.waterfall_sink_c_make(1024, fft.window.WIN_BLACKMAN_HARRIS, self.frequency, 2e6, "Waterfall")
        #self.time_plot = qtgui.time_sink_c_make(1024, 2e6, "Time")

        ########################
        # OFDM demod
        ########################
        self.demod = dab.ofdm_demod(self.dab_params, self.rx_params, self.verbose)

        ########################
        # SNR measurement
        ########################
        self.v2s_snr = blocks.vector_to_stream_make(gr.sizeof_gr_complex, self.dab_params.num_carriers)
        self.snr_measurement = digital.mpsk_snr_est_cc_make(digital.SNR_EST_SIMPLE, 10000)
        self.constellation_plot = qtgui.const_sink_c_make(1024, "", 1)

        ########################
        # FIC decoder
        ########################
        self.fic_dec = dab.fic_decode(self.dab_params)

        ########################
        # MSC decoder and audio sink
        ########################
        self.msc_dec = dab.msc_decode(self.dab_params, address, size, protection)
        self.mp2 = dab.mp2_decode_bs_make(bit_rate / 8)
        self.s2f_left = blocks.short_to_float_make(1, 32767)
        self.s2f_right = blocks.short_to_float_make(1, 32767)
        self.gain_left = blocks.multiply_const_ff(1, 1)
        self.gain_right = blocks.multiply_const_ff(1, 1)
        self.audio = audio.sink_make(32000)

        ########################
        # Connections
        ########################
        self.connect(self.src, self.fft_plot)
        self.connect(self.src, self.waterfall_plot)
        #self.connect(self.src, self.time_plot)
        self.connect(self.src, self.demod, (self.fic_dec, 0))
        self.connect((self.demod, 1), (self.fic_dec, 1))
        self.connect((self.demod, 0), (self.msc_dec, 0))
        self.connect((self.demod, 1), (self.msc_dec, 1))
        self.connect(self.msc_dec, (self.mp2, 0), self.s2f_left, self.gain_left, (self.audio, 0))
        self.connect((self.mp2, 1), self.s2f_right, self.gain_right, (self.audio, 1))
        self.connect((self.demod, 0), self.v2s_snr, self.snr_measurement, self.constellation_plot)
        # connect file sink if recording is selected
        if self.record_audio:
            self.sink = blocks.wavfile_sink_make("dab_audio.wav", 2, 32000)
            self.connect(self.gain_left, (self.sink, 0))
            self.connect(self.gain_right, (self.sink, 1))

        # tune USRP frequency
        if self.use_usrp:
            self.set_freq(self.frequency)
            # set gain
            # if no gain was specified, use the mid-point in dB
            g = self.src.get_gain_range()
            self.rx_gain = float(g.start() + g.stop()) / 2
            self.src.set_gain(self.rx_gain)

########################
# getter methods
########################
    def get_ensemble_info(self):
        return self.fic_dec.get_ensemble_info()

    def get_service_info(self):
        return self.fic_dec.get_service_info()

    def get_service_labels(self):
        return self.fic_dec.get_service_labels()

    def get_subch_info(self):
        return self.fic_dec.get_subch_info()

    def get_programme_type(self):
        return self.fic_dec.get_programme_type()

    def get_sample_rate(self):
        return self.mp2.get_sample_rate()

    def get_snr(self):
        return self.snr_measurement.snr()

########################
# setter methods
########################
    def set_volume(self, volume):
        self.dabplus.set_volume(volume)

    def set_freq(self, freq):
        if self.src.set_center_freq(freq):
            if self.verbose:
                print "--> retuned to " + str(freq) + " Hz"
            return True
        else:
            print "-> error - cannot tune to " + str(freq) + " Hz"
            return False

    def receive(self):
        rx = usrp_dab_rx()
        rx.run()

