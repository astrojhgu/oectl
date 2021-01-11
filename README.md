# oectrl

## Set gain of a single port
```bash
/usr/bin/python3 ./set_gain.py /dev/ttyUSB0 <port num> <gain>
```

e.g., 
```bash
/usr/bin/python3 ./set_gain.py /dev/ttyUSB0 12 25 # set 12th port to have a gain of 25
```

## Query gain of a single port
```bash
/usr/bin/python3 query_status.py /dev/ttyUSB0 <port num>
```

## Run a fake oe to reply the command for debug purpose
```bash
/usr/bin/python3 ./dummy_oe.py /dev/ttyUSB1
```
