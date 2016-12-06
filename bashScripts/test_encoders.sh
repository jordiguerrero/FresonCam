#!/bin/bash

./enable_encoder_slots.sh

while :
do
    echo -ne Left: $(cat /sys/devices/ocp.3/48302000.epwmss/48302180.eqep/position)
    echo -ne " Right:" $(cat /sys/devices/ocp.3/48304000.epwmss/48304180.eqep/position)
    
    echo "  -- Press q to quit!"

    read -t 2 -n 1 key

    if [[ $key = q ]]
    then
        break
    fi
done    
