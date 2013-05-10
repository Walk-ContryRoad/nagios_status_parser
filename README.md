nagios_status_parser
====================

A simple status.dat parser for Nagios

* Author: Charles Hamilton
* E-mail: musashi@nefaria.com
* Website: http://www.nefaria.com
* Additional Credits: http://www.decalage.info/fr/python/configparser
    
status_parser.py 
----------------

This file contains two classes:

* SimpleConfigParser
* NagiosStatusParser

SimpleConfigParser is exactly what the name implies. It can be used for 
general purpose configuration file processing. It has the ability to parse
configuration files that contain multiple "keys" or configuration options that
have the same name (nagios.cfg, for example.)

NagiosStatusParser is also exactly what the name implies. It is used solely
for parsing Nagios' status.dat file and returning Nagios status data in json
format.

See doctests for examples.
