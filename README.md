# pymavlink-bindings

git clone https://github.com/APRAND/pymavlink-bindings.git

cd pymavlink-bindings

bash ./setup.sh

pip3 install -r requirements.txt

pip3 install .


```
from pymavlink import mavutil
import MAVLink_binder

parser = MAVLink_binder.MAVLink_parser()
mavutil.mavlink.MAVLink.parse_char = parser.parse_char  # replace the python parser with the c++ version
```
