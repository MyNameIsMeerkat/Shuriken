#Shuriken

A little Python script that allows the capture & combination of upstream and downstream traffic from [Great Scott's Throwing Star LAN Tap](http://greatscottgadgets.com/throwingstar/).

As the LAN tap captures the upstream and downstream traffic seperately this is just a convience script that capture data from two network interafces simultaneously and then combines all the captured data into a single PCAP for subsequent analysis.

##Usage

From the command line just call:

```
python shuriken.py <iface_up> <iface_down> <pcap_name>
```

Where `iface_up` is the local NIC that is connected to the LAN taps upstream interface, `iface_down` is the local NIC that is connected to the LAN tap's downstream interface, and `pcap_name` is the name of the combined PCAP file to write out.

To stop an ongoing capture and dump the data to PCAP just press `Ctrl-C`. 

**NOTE**: To successfully run tcpdump you will likely need to be root.

##Requirements

`Shuriken` relies on `tcpdump` and the associated `mergecap` utility to do it's thing, without them it is useless.

##License
`Shuriken` is released under the LGPL.
