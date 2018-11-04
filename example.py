import os
import sys
import select
import MAVLink_binder

# setup up mavlink
os.environ["MAVLINK20"] = "1"  # force MAVLink v2 for the moment
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mavlink"))
from pymavlink import mavutil  # noqa: E402

# The following is required to activate the C++
# decode bindings
##############################################
parser = MAVLink_binder.MAVLink_parser()
mavutil.mavlink.MAVLink.parse_char = (
    parser.parse_char
)  # replace the python parser with the c++ version
##############################################

constr = "tcp:162.243.255.160:5780"
con = mavutil.mavlink_connection(constr)
connection = mavutil.mavlink.MAVLink(con)

while True:
    inputready, outputready, exceptready = select.select(
        [con.port], [], []
    )  # ,0) # timeout  = 0 will cause non-blocking behaviour
    for s in inputready:
        msg = con.recv_msg()
        if msg is not None:
            pass
            msg_id = msg.get_msgId()
            msg_type = msg.get_type()
            msg_dict = msg.to_dict()
            # if msg_type == 'HEARTBEAT':
            print(msg_dict)
            print(msg.to_json())
            print(msg._fieldnames)
            print(msg)
            msg_sys = msg.get_srcSystem()
            msg_comp = msg.get_srcComponent()
