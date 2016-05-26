# Learning diary

## day 3 - test python package version

Testing python package versions is possible using the standard python package [distutils](https://docs.python.org/2.7/library/distutils.html):

	from distutils.version import StrictVersion
	import numpy as np
	import sys

	if not (np.version.version>=StrictVersion('1.8.0')):
		sys.exit("Update numpy to at least version 1.8.0")

If you have a module with a __init__.py file, stick something like the above in that file and on import, if the version available is incorrect, you'll get an error e.g.

	An exception has occurred, use %tb to see the full traceback.

	SystemExit: Update numpy to at least version 1.8.0

## day 2 - numpy fft

I spent ages trying to understand moving from real space to k space, developing numerous functions along the way - there are loads of functions and useful documentation available here:

[http://docs.scipy.org/doc/numpy-1.10.1/reference/routines.fft.html](http://docs.scipy.org/doc/numpy-1.10.1/reference/routines.fft.html)

## day 1 - matplotlib

I use matplotlib every day and still find out new bits and pieces as I go along - basic usage is documented here: [http://matplotlib.org/faq/usage_faq.html](http://matplotlib.org/faq/usage_faq.html)
