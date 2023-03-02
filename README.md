# Monocular Pi
Monocular Pi is an experimental repo to run vSLAM on a Raspberry Pi 4 using the following sensors:
- Raspberry Pi Camera V2.1
- Adafruit BNO085 IMU

## Installing Dependencies
### On Device
To install all dependencies on the deployed device (on the Raspberry Pi in this case), run the following command in a terminal:
``` bash
poetry install
```

### On Devloper PC
As some dependencies are not able to be installed on any machine, it is recommended to run the following command to install the bare-minimum dependencies for development:
``` bash
poetry install --only main
```

## Convert `.proto` file to python
Run the following command:

``` bash
protoc --python_out=. ./filename.proto
```

Note that the latest version of the `protobuf` module will require you to compile the `.proto` file with a `protoc` version higher than 3.19.

Foxglove Protobuf schemas: <https://foxglove.dev/docs/studio/messages/introduction>

## Scanning Local Netowrk to Find Device
You can use the `arp-scan` terminal utility to find the IP addresses on the local network. Use the command:

``` bash
sudo arp-scan --localnet
```

For more information, consult the [`how_to` guide](https://johnhal.gitlab.io/how_to/apps/network_scan/).
