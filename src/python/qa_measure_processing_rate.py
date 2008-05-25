#!/usr/bin/env python

from gnuradio import gr, gr_unittest
import dab_swig

class qa_measure_processing_rate(gr_unittest.TestCase):
	"""
	@brief QA for Null symbol insertion.

	This class implements a test bench to verify the corresponding C++ class.
	"""

	def setUp(self):
		self.tb = gr.top_block()

	def tearDown(self):
		self.tb = None

	def test_001_measure_processing_rate(self):
		src = gr.null_source(gr.sizeof_gr_complex)
		throttle = gr.throttle(gr.sizeof_gr_complex, 1000000)
		head = gr.head(gr.sizeof_gr_complex, 200000)
		sink = dab_swig.measure_processing_rate(gr.sizeof_gr_complex,100000)
		
		self.tb.connect(src, throttle, head, sink)
		self.tb.run()

		rate = sink.processing_rate()
		assert(rate > 900000 and rate < 1100000)

if __name__ == '__main__':
	gr_unittest.main()

