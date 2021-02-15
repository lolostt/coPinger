# coPinger
This script will read HOSTS_FILE and ping machines to them. It will generate a REPORT_FILE.

## Prerequisites
Python3-capable system. Tested on macOS 10.15.

### Installing
1. Place script wherever you want and set execution permission. User executing script must have write permission in working folder.
2. Provide HOSTS_FILE. This is a plaint text file with comma separated entries. Ex:
  ```
  router,192.168.1.1
  machine,192.168.1.2
  ```
Default file name is 'machines.txt'. This can be customized in VARIABLES section inside the script.

## Usage
Execute as any other script.
```
./coPinger.py
```
or 
```
python3 coPinger.py
```
Script will generate a JSON report. Ex:
```
[
  [
    "router",
    true
  ],
  [
    "machine",
    false
  ]
]
```
Default file name is 'copinger_report.json'. This can be customized in VARIABLES section inside the script.

### Script behaviour
You can set some variables to customize script behaviour:
 - DEBUG. Set to '1' to get verbose mode. Default value is 0.
 - SIMULTANEOUS_PINGS. Sets simultaneous pings to launch. Excesive simultaneous pings can be problematic in some systems. Default value is 4.
If set to '1' script runs in sync mode. Any value greater than 1 makes sript run in async mode using multiple threads.
 - SIMULTANEOUS_MAX_PINGS. Sets simultaneous pings limit. This prevents problems if SIMULTANEOUS_PINGS is set too high. Default value is 51.
 - REPORT_INDENT. Set blank space indentation depth in report. Default value is 2.

## Authors
* **lolost** - [sleepingcoconut.com](https://sleepingcoconut.com/)

## License
This project is licensed under the [Zero Clause BSD license](https://opensource.org/licenses/0BSD).