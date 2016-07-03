A web interface and HTTP API to talk with a Rotel RSX-1505 via RS-232.

Why did I write this?  I wrote it to run a raspberry Pi and to act as bridge between my home automation system and my reciever. This allows me to control my reciever with wall switches.

 
Depenancy: 

 - python 2.7
  - flask
    

Configuration: 

 - Set serial port in app.py
 - http://supervisord.org/ is a good choice to run app as a service on your rPi


References:

http://www.fullstacksystems.com

http://www.rotel.com/sites/default/files/product/rs232/RSX1550%20Protocol.pdf
http://bwgroupsupport.com/downloads/rs232/rotel/RJ45connection.pdf
https://cnet4.cbsistatic.com/hub/i/r/2009/03/27/58e1868d-cc2e-11e2-9a4a-0291187b029a/thumbnail/770x433/d093c2fd3b147e441f1287a5d8fd7442/rotel_rsx1550_2.jpg