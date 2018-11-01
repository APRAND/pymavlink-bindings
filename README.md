# pymavlink-bindings
pip3 install .


```
from pymavlink import mavutil
import MAVLink_binder

parser = MAVLink_binder.MAVLink_parser()
mavutil.mavlink.MAVLink.parse_char = parser.parse_char  # replace the python parser with the c++ version
```
