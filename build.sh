
#sudo pip3 install -r requirements.txt
git submodule update --init --recursive
echo "Generating mavlink headders..."
python3 ./mavlink/pymavlink/tools/mavgen.py --lang C++11 ./mavlink/message_definitions/v1.0/ardupilotmega.xml -o ./generated/mavlink --wire-protocol=2.0

#python3 ./mavlink/pymavlink/tools/mavgen.py --lang Python ./mavlink/message_definitions/v1.0/ardupilotmega.xml -o ./generated/mavlink --wire-protocol=2.0


