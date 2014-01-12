#-----------------------------------------------------------
# Filename      : shuriken.py
# Description   : Dirty script to capture & combine traffic
#                 from both upstream & downstream interfaces
#                 of Great Scott's Throwing Star LAN tap
#                 and push out a single PCAP. Relies on
#                 tcpdump and mergecap
# Created By    : Rich Smith
# Date Created  : 24-Nov-2013 10:17
#
# License       : LGPL
#
# (c) Copyright 2013, Rich Smith all rights reserved.
#-----------------------------------------------------------
__author__ = 'rich.smith'
__version__ = "0.1"

import os
import sys
import time
import tempfile
import subprocess
import multiprocessing

class Shuriken(object):

    def __init__(self, in_if, out_if, pcap_name = ""):

        self.in_if     = in_if
        self.out_if    = out_if
        self.pcap_name = pcap_name


    def __call__(self):
        """
        Listen on both interfaces, capturing to two temp pcaps after complete (ctrl-c) merge the pcaps
        """
        ##Root check
        if os.geteuid() != 0:
            print "[-] Sorry you need to be root in order to be able sniff the interfaces"
            return False

        ##Temp files
        in_fd, in_path   = tempfile.mkstemp(suffix=".pcap")
        out_fd, out_path = tempfile.mkstemp(suffix=".pcap")

        ##Capture
        print "[+] Starting captures...."
        p_in  = multiprocessing.Process(target = self._capture_if, args=(self.in_if, in_path))
        p_out = multiprocessing.Process(target = self._capture_if, args=(self.out_if, out_path))
        p_in.start()
        p_out.start()

        ##Wait for ctrl-c
        try:
            while True:
                time.sleep(1.0)

        except KeyboardInterrupt:
            print "Ctrl-C detected"
            p_in.terminate()
            p_out.terminate()

        except Exception, err:
            print "[-] Unhandled Exception '%s' - exiting"%(err)

        ##Merge
        print "[+] Merging files ..."
        ret = subprocess.call(["mergecap", "-w", self.pcap_name, in_path, out_path])

        ##Cleanup
        print "[+] Cleaning up ..."
        os.unlink(in_path)
        os.unlink(out_path)

        print "[+] Done.\nMerged file can be found at: %s"%(self.pcap_name)

        return True


    def _capture_if(self, iface, path):
        """
        Kick off the tcpdump on the specified interface
        """
        ret = subprocess.call(["tcpdump", "-s","0", "-i", iface,  "-w",  path])


if __name__ == "__main__":

    if len(sys.argv) < 4:
        print "%s <iface_in> <iface_out> <merged_pcap_name>"%(sys.argv[0])
        sys.exit(0)

    S = Shuriken(sys.argv[1], sys.argv[2], sys.argv[3])
    S()