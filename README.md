# pymavlink-bindings
**[Work in progress]** 

Reduce CPU useage wherever pymavlink is used. Works with MAVLink / MAVLinkv2 and Python2.7+ / Python3.5+

## Setup

git clone https://github.com/APRAND/pymavlink-bindings.git

cd pymavlink-bindings

pip2/3 install -r requirements.txt

pip2/3 install .

## Usage
```
from pymavlink import mavutil
import MAVLink_binder

parser = MAVLink_binder.MAVLink_parser()
mavutil.mavlink.MAVLink.parse_char = parser.parse_char  # replace the python parser with the c++ version
```
