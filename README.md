Availability:
=============  
If you're in Ottawa and make use of various bookable equipment, you may
find this program to be handy.  It will take in your barcode, pin, and a
list of resources and find out when they are "bookable".

Example:
========
```
$ python ./availability.py -u barcode -p pin -n "['dev1-code', 'dev2-code']"  
Machine: dev1-code  
Sep 07, 2019  
	10:00am to 3:30pm  
Sep 13, 2019  
	3:00pm to 3:30pm  
Machine: dev2-code  
Sep 07, 2019  
	10:30am to 4:30pm
```