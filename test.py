import os, sys, select, json
# setup up mavlink 
os.environ['MAVLINK20'] = '1' # force MAVLink v2 for the moment
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mavlink'))
from pymavlink import mavutil
import MAVLink_binder


def msg_str(self):
    ret = '%s {' % self._type
    for a in list(self._fieldnames):
        v = self.format_attr(a)
        ret += '%s : %s, ' % (a, v)
    ret = ret[0:-2] + '}'
    return ret


def format_attr(self, field):
    '''override field getter'''
    raw_attr = getattr(self, field)
    if isinstance(raw_attr, bytes):
        raw_attr = raw_attr.decode("utf-8").rstrip("\00")
    return raw_attr


def to_json(self):
    return json.dumps(self.to_dict())

# MAVLink_binder.MAVLink_message.__str__ = msg_str
# MAVLink_binder.MAVLink_message.format_attr = format_attr


mavmap = mavutil.mavlink.mavlink_map
#print(mavmap['1'])
print(mavmap[1].fieldnames)
constr = 'tcp:162.243.255.160:5780'
con = mavutil.mavlink_connection(constr)
connection = mavutil.mavlink.MAVLink(con)
parser = MAVLink_binder.MAVLink_parser()
mavutil.mavlink.MAVLink.parse_char = parser.parse_char  # replace the python parser with the c++ version

# print(connection)
while True:
    inputready,outputready,exceptready = select.select([con.port],[],[])#,0) # timeout  = 0 will cause non-blocking behaviour
    for s in inputready:
        msg = con.recv_msg()
        if msg is not None:
            pass
#             msg_id = msg.get_msgId()
            msg_type = msg.get_type()
            msg_dict = msg.to_dict()
#             if msg_type == 'HEARTBEAT':
            if msg_type == 'PARAM_VALUE':

                print(msg_dict)
    #             print(msg.to_json())
    #             print(msg._fieldnames)
                print(msg)
    #             msg_sys = msg.get_srcSystem()
    #             msg_comp = msg.get_srcComponent()

