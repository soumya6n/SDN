from ryu.lib.packet import packet
from ryu.lib.packet import ipv4
from . import ids_utils
from . import BoyerMooreStringSearch
import MySQLdb as mdb

class udp(object):
    
    def __init__(self,packet_data):
        self.packet_data =  packet.Packet(packet_data.data)  
        self.dst_ip = ids_utils.get_packet_dst_ip_address(self.packet_data)
        self.src_ip = ids_utils.get_packet_src_ip_address(self.packet_data)
        self.dst_port = ids_utils.get_packet_dst_port(self.packet_data)
        self.src_port = ids_utils.get_packet_src_port(self.packet_data)
        self.length_data = ids_utils.get_packet_length(self.packet_data)      

    def check_packet(self,mode,src_ip, src_port, dst_ip, dst_port,rule_type,pattern,depth,offset,flags,rule_msg): 
	global good_pkt  
	good_pkt = 'True'   
	#print "In udp.py "
        alertmsg = 'NONE' 
        for p in self.packet_data:
            if hasattr(p, 'protocol_name') is True:
                #print p.protocol_name
                if p.protocol_name == 'udp':
                     match = self.check_udp_ip_port_match(src_ip, src_port, dst_ip, dst_port)
                     match_content = True
                     pkt_contents = ""  
                     if match == True:
                         length = ids_utils.get_packet_length(self.packet_data)
			 #print 'Length= ', length
                         for p in self.packet_data.protocols:
                             if hasattr(p, 'protocol_name') is False:
                                 print 'Value of P in udp.py ', p
                                 #ids_utils.print_packet_data(p, length)
                                 contents=ids_utils.get_packet_data(p,length)
                                 pkt_contents = str(contents)
				 #print 'pkt_contents before Depth and Offset:',pkt_contents
				 if offset is not None:
				    pkt_contents = pkt_contents[offset:]
				 #print 'pkt_contents after offset:',pkt_contents
				 if depth is not None:
				    pkt_contents = pkt_contents[:depth]	
                                 #print 'pkt_contents after depth:', pkt_contents
                                 #print pattern
                             if pattern is not None:
				 for p in pattern:
                                 #match_content = BoyerMooreStringSearch.BMSearch(pkt_contents,pattern)
                                 	match_content =  pkt_contents.find(p)
					#print 'Pattern in UDP:',p
					if match_content == -1:
					   good_pkt= 'True' #--sow
	 	                           # Writing good pkt val every time to file
                                 	   f = open('/home/rashmi/RYU295/ryu/lib/ids/pkt_value.txt', 'a')
                                 	   f.write("\n")
                                 	   f.write(good_pkt)
                                 	   f.close()
					   break
			     else:
				  match_content = 1	
                             #if match_content == True:
                             if match_content != -1:
				 good_pkt = 'False' #--sow
   				 
				 # Writing good pkt val every time to file
                                 f = open('/home/rashmi/RYU295/ryu/lib/ids/pkt_value.txt', 'a')
                                 f.write("\n")
                                 f.write(good_pkt)
                                 f.close()

                                 f = open('/home/rashmi/RYU295/ryu/lib/ids/log.txt', 'a')
                                 f.write("\n")
                                 f.write(rule_msg)
                                 f.close()
                                 self.writeToDB('UDP Attack Packet', 'udp',rule_msg, 
                                                self.src_ip, self.dst_ip, self.src_port, self.dst_port)
                                 #print 'After Call to Print Packet Data in TCP'
                             #if mode == 'alert' and match_content == True:
			     
                             if mode == 'alert' and match_content != -1:
                                 #print 'UDP Attack Packet'
                                 alertmsg = rule_msg
                                 #return alertmsg --sow	
				 #good_pkt= 'False' #--sow
   				 #print "In udp.py mode=alert, match content!=-1, bfr returngood_pkt=", good_pkt #--sow	
			     	 return alertmsg #--sow
        #print "out of udp check packet function"
  	
     
                                
    def check_udp_ip_port_match(self,src_ip, src_port, dst_ip, dst_port):

        #print 'Print message from tcp.py'
        #print 'packet source', self.src_ip
        #print 'packet dst', self.dst_ip
        #print 'rule source', src_ip
        #print 'rule dst', dst_ip
        #print 'Print Message from tcp.py Ends'
        if (('any' in src_ip) or (self.src_ip in src_ip)):
            if (('any' in dst_ip) or (self.dst_ip in dst_ip)):
                if ((src_port == 'any') or (int(src_port) == int(self.src_port))):
                    if ((dst_port == 'any') or (int(dst_port) == int(self.dst_port))):
                        return True
    
    def writeToDB(self,name, protocol, msg, srcip, dstip, srcport, dstport): 
        dbcon = mdb.connect("localhost","testuser","test123","attackdb" )
        cursor = dbcon.cursor()
        try:
            cursor.execute("INSERT INTO attacks(name,protocol, message, sourceip, destip, sourceport, destport)VALUES (%s, %s,%s, %s, %s,%s,%s)",(name, protocol, msg, srcip, dstip, srcport, dstport))
            dbcon.commit()
        except:
            dbcon.rollback()

      
