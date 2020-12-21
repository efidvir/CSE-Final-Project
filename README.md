# WiFi Based Wireless Imaging and Positioning for WSN
## CSE-Final-Project
### Efi Dvir & Oren Zaharia
### Supervisor:  Omer Gurewitz (Prof.)

In the era of IoT, many network devices rely on WiFi to gather data, but without knowing their purpose in the network as a whole. Thus, in order to get more insight about the sensor’s intended usage, more environmental information is needed. By discovering the position of the device in space and obtaining an image of its surroundings, the device is able to infer its purpose in the network and assign itself a proper configuration. 
When the sensor node is idle it can use its radio to initiate an RF scan of its surroundings and generate a reflectivity image of its environment.  Using an SDR (Software Defined Radio) as the sensor node radio which can transmit and receive CW signals at various frequencies in order to measure reflections of its signal (Magnitude and Phase) from objects its vicinity. Then using Range Migration Algorithm to construct a 3D image of the sensor nodes environment from the sampled scene matrix.
When the sensor is active, and its radio is employed in favor of WiFi communication it can use the Beacon and RSSI of the intercepted frames and triangulate its position in space using a propagation model from all APs in range. Using 1 WiFi dongle as the sensor and 4 APs we gather the AP’s Tx power and the RSSI from the sensor.  Using an indoor radio propagation model for estimating the distance from each AP (which have fixed known location) and triangulating the relative sensor position.


![](https://github.com/efidvir/CSE-Final-Project/blob/main/QR.jpg)

> Link to the project's Drive
