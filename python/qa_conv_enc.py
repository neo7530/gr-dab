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

from gnuradio import gr, gr_unittest, fec, trellis
from gnuradio import blocks
import dab
from math import sqrt


class qa_conv_enc (gr_unittest.TestCase):


# test code only for convolutional encoding, not for puncturing


    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        self.dp = dab.parameters.dab_parameters(1, 2e6, False)
        data = (0x02, 0xBE, 0x3E, 0x8E, 0x16, 0xB9, 0xA5, 0xCD, 0x48, 0xB3, 0x22, 0xB2, 0xAD, 0x76, 0x88, 0x80, 0x42, 0x30, 0x9C, 0xAB, 0x0D, 0xE9, 0xB9, 0x14, 0x2B, 0x4F, 0xD9, 0x25, 0xBF, 0x26, 0xEA, 0xE9, 0x02, 0xBE, 0x3E, 0x8E, 0x16, 0xB9, 0xA5, 0xCD, 0x48, 0xB3, 0x22, 0xB2, 0xAD, 0x76, 0x88, 0x80, 0x42, 0x30, 0x9C, 0xAB, 0x00, 0xE9, 0xB9, 0x14, 0x2B, 0x4F, 0xA9, 0x25, 0xBF, 0x26, 0xEA, 0xE1, 0x02, 0xBE, 0x3E, 0x8E, 0x16, 0xB9, 0xA5, 0xCD, 0x48, 0xB3, 0x23, 0xB2, 0xAD, 0x76, 0x88, 0x80, 0x42, 0x30, 0x9C, 0xAB, 0x0D, 0xE9, 0xB9, 0x14, 0x2B, 0x4F, 0xD9, 0x25, 0xBF, 0x26, 0x9A, 0xE9, 0x02, 0xBE, 0x3E, 0x8E, 0x16, 0xB9, 0xA5, 0xCD, 0x48, 0xB3, 0x22, 0xB2, 0xAD, 0x76, 0x88, 0x80, 0x42, 0x30, 0x9C, 0xAB, 0x0D, 0xE9, 0xB9, 0x14, 0x2B, 0x4F, 0xD9, 0x25, 0xBF, 0x26, 0xEA, 0xE9, 0x02, 0xBE, 0x3E, 0x8E, 0x16, 0xB9, 0xA5, 0xCD, 0x48, 0xB3, 0x22, 0xB2, 0xAD, 0x76, 0x88, 0x80, 0x42, 0x30, 0x9C, 0xAB, 0x00, 0xE9, 0xB9, 0x14, 0x2B, 0x4F, 0xA9, 0x25, 0xBF, 0x26, 0xEA, 0xE1, 0x02, 0xBE, 0x3E, 0x8E, 0x16, 0xB9, 0xA5, 0xCD, 0x48, 0xB3, 0x23, 0xB2, 0xAD, 0x76, 0x88, 0x80, 0x42, 0x30, 0x9C, 0xAB, 0x0D, 0xE9, 0xB9, 0x14, 0x2B, 0x4F, 0xD9, 0x25, 0xBF, 0x26, 0x9A, 0xE9, 0x02, 0xBE, 0x3E, 0x8E, 0x16, 0xB9, 0xA5, 0xCD, 0x48, 0xB3, 0x22, 0xB2, 0xAD, 0x76, 0x88, 0x80, 0x42, 0x30, 0x9C, 0xAB, 0x0D, 0xE9, 0xB9, 0x14, 0x2B, 0x4F, 0xD9, 0x25, 0xBF, 0x26, 0xEA, 0xE9, 0x02, 0xBE, 0x3E, 0x8E, 0x16, 0xB9, 0xA5, 0xCD, 0x48, 0xB3, 0x22, 0xB2, 0xAD, 0x76, 0x88, 0x80, 0x42, 0x30, 0x9C, 0xAB, 0x00, 0xE9, 0xB9, 0x14, 0x2B, 0x4F, 0xA9, 0x25, 0xBF, 0x26, 0xEA, 0xE1, 0x02, 0xBE, 0x3E, 0x8E, 0x16, 0xB9, 0xA5, 0xCD, 0x48, 0xB3, 0x23, 0xB2, 0xAD, 0x76, 0x88, 0x80, 0x42, 0x30, 0x9C, 0xAB, 0x0D, 0xE9, 0xB9, 0x14, 0x2B, 0x4F, 0xD9, 0x25, 0xBF, 0x26, 0x9A, 0xE9, 0x02, 0xBE, 0x3E, 0x8E, 0x16, 0xB9, 0xA5, 0xCD, 0x48, 0xB3, 0x22, 0xB2, 0xAD, 0x76, 0x88, 0x80, 0x42, 0x30, 0x9C, 0xAB, 0x0D, 0xE9, 0xB9, 0x14, 0x2B, 0x4F, 0xD9, 0x25, 0xBF, 0x26, 0xEA, 0xE9, 0x02, 0xBE, 0x3E, 0x8E, 0x16, 0xB9, 0xA5, 0xCD, 0x48, 0xB3, 0x22, 0xB2, 0xAD, 0x76, 0x88, 0x80, 0x42, 0x30, 0x9C, 0xAB, 0x00, 0xE9, 0xB9, 0x14, 0x2B, 0x4F, 0xA9, 0x25, 0xBF, 0x26, 0xEA, 0xE1, 0x02, 0xBE, 0x3E, 0x8E, 0x16, 0xB9, 0xA5, 0xCD, 0x48, 0xB3, 0x23, 0xB2, 0xAD, 0x76, 0x88, 0x80, 0x42, 0x30, 0x9C, 0xAB, 0x0D, 0xE9, 0xB9, 0x14, 0x2B, 0x4F, 0xD9, 0x25, 0xBF, 0x26, 0x9A, 0xE9)
        self.src = blocks.vector_source_b(data)
        self.src2 = blocks.file_source_make(gr.sizeof_float, "debug/fic_unpunctured.dat")
        self.fib_packed_to_unpacked = blocks.packed_to_unpacked_bb(1, gr.GR_MSB_FIRST)
        self.append = dab.append_bb_make(768, 774)
        conv_encoder_config = fec.cc_encoder_make(774, 7, 4, [91, 121, 101, 91], 0, fec.CC_STREAMING)
        conv_encoder = fec.extended_encoder(conv_encoder_config, None, '1111')

        # convolutional coding
        # self.fsm = trellis.fsm(self.dp.conv_code_in_bits, self.dp.conv_code_out_bits, self.dp.conv_code_generator_polynomials)
        self.fsm = trellis.fsm(1, 4, [0133, 0171, 0145, 0133])  # OK (dumped to text and verified partially)
        self.conv_v2s = blocks.vector_to_stream(gr.sizeof_float, self.dp.fic_conv_codeword_length)
        # self.conv_decode = trellis.viterbi_combined_fb(self.fsm, 20, 0, 0, 1, [1./sqrt(2),-1/sqrt(2)] , trellis.TRELLIS_EUCLIDEAN)
        table = [
            0, 0, 0, 0,
            0, 0, 0, 1,
            0, 0, 1, 0,
            0, 0, 1, 1,
            0, 1, 0, 0,
            0, 1, 0, 1,
            0, 1, 1, 0,
            0, 1, 1, 1,
            1, 0, 0, 0,
            1, 0, 0, 1,
            1, 0, 1, 0,
            1, 0, 1, 1,
            1, 1, 0, 0,
            1, 1, 0, 1,
            1, 1, 1, 0,
            1, 1, 1, 1
        ]
        assert (len(table) / 4 == self.fsm.O())
        table = [(1 - 2 * x) / sqrt(2) for x in table]
        self.conv_decode = trellis.viterbi_combined_fb(self.fsm, 774, 0, 0, 4, table, trellis.TRELLIS_EUCLIDEAN)
        self.conv_s2v = blocks.stream_to_vector(gr.sizeof_char, 774)
        self.conv_prune = dab.prune(gr.sizeof_char, self.dp.fic_conv_codeword_length / 4, 0, self.dp.conv_code_add_bits_input)
        self.fib_unpacked_to_packed = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)

        # symbol mapping
        self.mapper = dab.qpsk_mapper_vbc(self.dp.num_carriers)

        dst = blocks.vector_sink_b()
        self.tb.connect(self.src,
                        self.fib_packed_to_unpacked,
                        self.append,
                        conv_encoder,
                        blocks.char_to_float_make(),
                        self.conv_decode,
                        self.conv_prune,
                        self.fib_unpacked_to_packed,
                        dst)

        self.tb.run ()
        result_data = dst.data()
        print result_data
        #self.assertEqual(result_data, data)
        pass

if __name__ == '__main__':
    gr_unittest.run(qa_conv_enc, "qa_conv_enc.xml")