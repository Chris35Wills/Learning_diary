# Learning diary

## day 6 - creating parameter files

I often receive numerous files of survey data where the first few lines describe the coordinate system, with the remaining lines denoting position and attribute information e.g. x,y,z - an example of the top of such a file can be seen [here](./files/header_example.txt). The header format is not always that convenient when all I really want is access to a few values. To deal with this, I have a bash script that reads in the file, then using [gawk](https://www.gnu.org/software/gawk/manual/gawk.html) to pull out the information that is required, putting this into a new file which can be more easily handled down the processing chain. 

Using our example file:

```
*** Header info for something cool... ***
Survey ID: jr106_EastGreenlandshelf 
Datum: WGS84 
Half axis: 5432165.0000000 
Flattening: 1/300.43 
Coordinate system: Lat/Long 
Latitude min.:  65.23145 
Longitude min.: -3.543890 
Latitude max.:  69.26 
Longitude max.: 12.526900 
Latitude cell size: 500.00 meter
Longitude cell size: 432.50 meter
Elevation values
```

Let's say I want to have access to the datum info, half axis value, the flattening value in order to create a [proj4 string](https://trac.osgeo.org/proj/) which I can the write out to a new file.

First, in bash, I set my file (if you have many files, then start a loop):

```
f='./header_example.txt'
echo "Working on $f" 
```

In this example, I already know the projection and ellipsoid info, so I can set variables accordingly:

```
proj="longlat"
ellips="WGS84"
```

The datum, flattening and half axis info I can take fro the header_example.txt file, for which I can make ue of [gawk]():

```
datum=`gawk 'NR!=1{if($1 == "Datum") printf("%s\n", $2)}' FS=":" $f`
flattening=`gawk 'NR!=1{if($1 == "Flattening") printf("%s\n", $2)}' FS=":" $f`
half_axis=`gawk 'NR!=1{if($1 == "Half axis") printf("%s\n", $2)}' FS=":" $f`
```

So if you are new to gawk, there is a lot going on here. For the first call to set the `datum` variable, the call starts with a back tick followed by a call to `gawk` itself. The `NR!=1` call skips the first line. Within the curly braces, `if($1 == "Datum") printf("%s\n", $2)` states that if the first column is equal to the string `Datum`, then print the second column as a string followed by a new line. Outside the curly braces, `FS=":"` states that each field is separated by a colon. For example, for a given line such as:

```
Longitude max.: 12.526900 
```

... using  `FS=":"` means that the first column (`$1`) will be `Longitude max.` and the second column (`$2`) will be `12.526900`. The final call in the lines above to `$f` simple tells gawk which file to work on.

To ensure I don't have any white space either side of these variable values, I can do a quick pipe of the variable into [xargs](http://linux.die.net/man/1/xargs) (careful using this pipe in this way for other applications):

datum=`echo $datum | xargs`
flattening=`echo $flattening | xargs`
half_axis=`echo $half_axis | xargs`

I can now set my proj4 string using the variables defined above:

```
proj4="+proj=$proj +ellps=$ellips +datum=$datum +f=$flattening +a=$half_axis"
```

Now, I can write the proj4 string variable to a new file:

```
echo $proj4 > example.hdr
```

This can be repeated for any other variables to, for example to get the longitude cell size:

```
lon_res = `gawk 'NR!=1{if($1 == "Longitude cell size") printf("%.2f \n", $2)}' FS=":" $f`
```

... and then to append this to the same file that we wrote the proj4 variable to:

```
echo $lon_res > example.hdr
```

## day 5 - apply function over Pandas dataframe

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

![Cumulative distance]({{ site.baseurl }}./images/cumulative_distance.png)	

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
