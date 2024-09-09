# hackpi-dash
## Introduction ##
This script is designed to go along with my hackberry pi dashboard which can be found [here](https://github.com/chriswilson2020/hack-environment-monitor)
We can use this to make a live view remote (all be it http not https but I access it over a ssl vpn so doesn't matter much) dashboard for our little environmental monitor

### Background ###
Unfortunately as of September 2024 it is a challenge (pain in the ass) to use flask and plot.ly to make a nice simple webserver to display the output of your measurements on a Raspberry Pi Zero 2W because many of the newer python modules seem to be incompatible with the older Arm v6 architecture of the Pi Zero 2W we end up with rather cryptic Illegal Instruction errors.  This is my incredibly ugly work around to make this whole thing work simply with as lower overhead as possible.

It requrires a whole bunch of very specific versions of libraries for reference I have included the requirements.txt for you.  The easy fix is to make a virtual environment and install the requirements as follows. 


## Installation ##
clone this git hub or just download the requirements.txt and move it into the root of the directory where you want your script to live then create a virtual environment as follows:

`python3 -m venv .plotter`

**IMPORTANT** 
If you do not want to be in a world of pain activate your virtual environment:

`source .plotter/bin/activate`

Install the requirements:

`pip install -r requirements.txt`

If you want to do it manually these are the packages you need and their versions:
`Brotli==1.1.0
click==8.1.7
dash==1.21.0
dash-core-components==1.17.1
dash-html-components==1.1.4
dash-table==4.12.0
Flask==1.1.2
Flask-Compress==1.15
future==1.0.0
itsdangerous==1.1.0
Jinja2==2.11.3
MarkupSafe==1.1.1
numpy==2.1.1
pandas==2.2.2
plotly==4.14.3
python-dateutil==2.9.0.post0
pytz==2024.1
retrying==1.3.4
six==1.16.0
tzdata==2024.1
Werkzeug==2.0.3
zstandard==0.23.0`


Next you will still get a bool8 error if you don't make some changes because of the incompatibilities it is easier to just modify plotly express to remove bool8 than continue to play whack a mole with the deps. 

so use your favourite editor (nano in my case) to modify imshow_utils.py assuming that you used the same location above for the virtual environment you can execute the following:

`nano .plotter/lib/python3.11/site-packages/plotly/express/imshow_utils.py`

You should see the following code and you need to simply comment out `np.bool8: (False, True),` it should be some 23 lines down or so in the definition of `_integer_range`

<img width="985" alt="Screenshot 2024-09-09 at 16 02 39" src="https://github.com/user-attachments/assets/0473ef4a-adc1-44ba-b9a2-f5c82c8bb418">

## Useage ##

With this all done you should be able to now execute the script specifying the location of your csv files as the example below:

`python3 plot.py --csv-dir ~/Development/seeed-air/` replace `~/Development/seeed-air/` with the location of your hackberrypi environment monitor script.

You will see an output something like this 

<img width="724" alt="Screenshot 2024-09-09 at 16 16 54" src="https://github.com/user-attachments/assets/82d4aa29-3c2d-4e0a-8b61-8319761667d6">

In a web-browser you can navigate to the IP of your device something like `http://192.168.1.X:8050` where X is the last digits of your IP address at port 8050 and you should be able to select the csv and load the graphs. It will take some time to render the graphs remember we are using a little Pi Zero 2W so it isn't the fastest horse in the stables. 

You will see something like this in your browser:


![2024-09-09_16-34-37](https://github.com/user-attachments/assets/545f5c88-f40c-4fa1-82f1-50317dcfc75c)


