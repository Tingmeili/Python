#!/usr/bin/env python
# encoding: utf-8

class ShowProcess_find():
	# the number of the process 
	i = 1 
	#total count
	max_steps = 0
	#the length of the processing bar 
	max_arrow = 50 

	def __init__(self, max_steps):
		self.max_steps = max_steps

	def show_process(self, i=1):
		num_arrow = int(self.i * self.max_arrow / self.max_steps)
		num_line = self.max_arrow - num_arrow
		percent = self.i * 100.0 / self.max_steps
		process_bar = '[' + '>' * num_arrow + '-' * num_line + ']'\
						+ '%.2f' % percent + '%' + '\r'
		sys.stdout.write(process_bar)
		sys.stdout.flush()
		self.i += 1

#how to use
if __name__=='__main__':
	max_number = 100
	process_bar = ShowProcess_find(max_number)
	#function() is the function you write
	function()
	process_bar.show_process()
	time.sleep(0.5)





