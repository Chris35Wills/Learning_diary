# Learning diary

## day 4 - matplotlib and X11

I ran into issues with a piece of code with matplotlib where one environment did not have access to [DISPLAY](http://superuser.com/questions/368530/understanding-x-windows-display-environment-variable-when-tunnelling). This was because my system uses an x-windows backend with matplotlib's [pyplot](http://matplotlib.org/api/pyplot_api.html). Where this is not the case - say perhaps you ssh in to somewhere without X11 forwarding - pyplot related things will fail. To deal with this, you can change the [matplotlibrc](http://matplotlib.org/users/customizing.html). To do this where DISPLAY isn't set (which I grabbed from [here](http://stackoverflow.com/questions/2801882/generating-a-png-with-matplotlib-when-display-is-undefined)):

	import os
	
	havedisplay = "DISPLAY" in os.environ
	
	try:
		assert havedisplay == True
	except AssertionError:
		print("DISPLAY variable not set (no X11 forwarding) - changing matplotlib backend to Agg")
		matplotlib.use('Agg')

If you have a module where this is required, stick it in [__init__.py](https://docs.python.org/2/tutorial/modules.html), or put it into your testing file so it can at least be flagged. If code is supposed to plot, you will need to catch this so your code doesn't catch (maybe save rather than plot where DISPLAY is not set).

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
