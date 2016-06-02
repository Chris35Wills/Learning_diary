# Learning diary

## day 4 - apply function over Pandas dataframe

The [assign](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.assign.html) function available in [Pandas](http://pandas.pydata.org/) is extremely convenient and allows for quick calculations across a dataframe. I need to make more use of this. You create your dataframe such as:

	import pandas as pd
	import numpy as np

	x=np.arange(0,100,1)
	y=np.arange(0,100,1)

	index=np.arange(0, len(x), 1)
	columns=['x','y']
	df=pd.DataFrame(index=index, columns=columns)

	df['x']=x
	df['y']=y

You can then use the assign function, where here we use it to create a new column calculating distance between successive xy pairs using the function [rolling_apply](http://pandas.pydata.org/pandas-docs/version/0.17.0/generated/pandas.rolling_apply.html), the x and y values being held in separate columns:

	df=df.assign(x_diff=pd.rolling_apply(df['x'], 2, \
	  lambda x : x[1]-x[0])) 

	df=df.assign(y_diff=pd.rolling_apply(df['y'], 2, \
	  lambda y : y[1]-y[0]))

	df['distance']=np.hypot(df['y_diff'], df['x_diff'])

You can then manipulate the result as required:

	np.cumsum(df['distance']).plot()
	plt.title("Cumulative distance")
	plt.show()

![Cumulative distance]({{ site.baseurl }}/images/cumulative_distance.png)	

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
