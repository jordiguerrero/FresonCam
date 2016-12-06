#!/bin/bash

left_slot="bone_eqep1"
right_slot="bone_eqep2"

if grep -q  bone_eqep1 /sys/devices/bone_capemgr.9/slots; then
    echo "left slot already enabled"
else
    echo bone_eqep1 > /sys/devices/bone_capemgr.9/slots
fi

if grep -q  bone_eqep2 /sys/devices/bone_capemgr.9/slots; then
    echo "right slot already enabled"
else
    echo bone_eqep2 > /sys/devices/bone_capemgr.9/slots
fi

