"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""


import numpy as np
import time
from threading import Timer
from gnuradio import gr
import pmt

flag = 0;
class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
	"""Embedded Python Block example - a simple multiply const"""

	def __init__(self, start_sampling=1.0):  # only default arguments here
		"""arguments to this function show up as parameters in GRC"""
		gr.sync_block.__init__(
		    self,
		    name='Write to file',   # will show up in GRC
		    in_sig=[np.complex64],
		    out_sig=[np.complex64]
		)
		global flag
		self.freqs = [5e9,5.05e9,5.1e9,5.15e9,5.2e9,5.25e9,5.3e9,5.35e9,5.4e9,5.45e9,5.5e9,5.55e9,5.6e9,5.65e9,5.7e9,5.75e9]
		self.nfreqs = 16
		print('global flag', flag);
		if (flag == 0):
			self.cnt = 0

		self.boolTakeSample = False;
		self.boolTookSample = False;
		# if an attribute with the same name as a parameter is found,
		# a callback is registered (properties work, too).
		self.start_sampling = start_sampling
		self.message_port_register_out(pmt.intern('msg out'))
		def doTimer():
			if self.boolTakeSample == True:
				Timer(0.5, doTimer, ()).start();
				return;	
			if self.boolTookSample == False:
				self.boolTookSample = True;
				self.boolTakeSample = True;
				Timer(1, doTimer, ()).start();
				return;
			else:
				self.boolTookSample = False;
				self.boolTakeSample = False;			

			if self.cnt == self.nfreqs - 1:
				print("Press QT Button to Continute!");
				while (self.start_sampling == 0):
					continue
				self.cnt = 0;
			
			self.cnt += 1;
			print(self.cnt)
			d_ChgFreq = pmt.make_dict()
			d_ChgFreq = pmt.dict_add(d_ChgFreq, pmt.intern('freq'),pmt.from_double(self.freqs[self.cnt]) )
			self.message_port_pub(pmt.intern("msg out"), d_ChgFreq)
			Timer(2, doTimer, ()).start();
			return;

		if (flag == 0):
			Timer(1, doTimer, ()).start();
		flag = 1;

                
	def work(self, input_items, output_items):	

	        def get_result():
			if self.boolTakeSample == True:
				f = open(r'/home/lte/output2.csv', 'a+');
				f.write('{0},'.format(input_items[0][0]));
				print('{0},'.format(input_items[0][0]))
				f.close()
				self.boolTakeSample = False;
		get_result();
		output_items[0][:] = input_items[0];
		"""example: multiply with constant"""
		return len(output_items[0])

    
