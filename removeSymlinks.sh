#! /bin/sh

x=`find $1/ -type l`

for a in $x; do
    FROM=`readlink -f -- $a`
    cp --remove-destination $FROM $a
done
