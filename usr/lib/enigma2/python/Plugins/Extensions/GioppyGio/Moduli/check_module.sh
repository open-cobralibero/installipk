#!/bin/sh
pyv="$(python -V 2>&1)"
echo "$pyv"
echo "Checking dependencie python requests"
echo ""
echo "Updating feeds"
opkg update
echo ""
if [[ $pyv =~ "Python 3" ]]; then
	echo "checking python3-requests"
	if python -c "import requests" &> /dev/null; then
		echo "Requests library already installed"
	else
		opkg install python3-requests
	fi
	echo ""
else
	echo "checking python-requests"
	if python -c "import requests" &> /dev/null; then
		echo "Requests library already installed"
	else
		opkg install python-requests
	fi
fi
exit 0
