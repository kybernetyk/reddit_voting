#!/bin/sh
# this script will solve a captcha by using the decaptcher service 
# more info: http://decaptcher.com/
#
# for this to work you have to create a file named '.decaptcher.
# in the current directory and fill it with your decaptcher.com
# username and password. seperate user and pass byt a whitespace
# example:
#   jack mypass\n

if [ ! -e ".decaptcher" ]
then
	echo ".decaptcher file does not exist! create one containing 'username password'"
	exit
fi

if [ $# -ne 1 ]
then
  echo "Usage: `basename $0` captchaurl"
  exit $E_BADARGS
fi


# decaptcher.com credentials
_user=`awk <.decaptcher '{print $1}'`
_pass=`awk <.decaptcher '{print $2}'` 

curl -o captcha.png $1  
curl -F "function=picture2" -F "username=$_user" -F "password=$_pass" -F "pict=@captcha.png" -F "pict_to=0" -F "pict_type=0" http://poster.de-captcher.com/ |awk 'BEGIN {FS="|"}; {print $6}'

