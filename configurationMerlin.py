#!/usr/bin/env python3
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
from ipmininet.iptopo import IPTopo
from ipmininet.router.config import RouterConfig,AF_INET, AF_INET6 #for router configuration
from ipmininet.router.config import OSPF, OSPF6 # for OSPF configuration
from ipmininet.router.config import BGP, bgp_fullmesh, set_rr, ebgp_session, SHARE, CLIENT_PROVIDER, bgp_peering # for BGP configuration

from ipmininet.router.config.bgp import bgp_anycast # for anycast configuration
"""     
PORT     STATE SERVICE
2601/tcp open  zebra   --> controls the RIB of each daemon
        show ip route
        show ipv6 route
        show ip bgp
        
2605/tcp open  bgpd    --> show information related to the configuration of BGP
        show bgp route (IPv4)
        show bgp (IPv6)

2606/tcp open  ospf6d  --> same but for OSPFv3 (OSPF for IPv6)
        show ip ospf route 

zebrasrv        2600/tcp             # zebra service
zebra           2601/tcp              # zebra vty
ripd            2602/tcp              # RIPd vty
ripngd          2603/tcp              # RIPngd vty
ospfd           2604/tcp              # OSPFd vty
bgpd            2605/tcp             # BGPd vty
ospf6d          2606/tcp              # OSPF6d vty

INTERESTING COMMANDS
mininet> router ping -R ipaddress
mininet> router traceroute -w 10 -z 100 -I ipaddress
"""   
class OVHTopology(IPTopo):

    def build(self, *args, **kwargs):
        # --- Metrics ---
        small = 1
        medium = 3
        large = 8
        extra_large = 13

        # IPv4 range 198.27.92.0/24
        # IPv6 range 2604:2dc0::/32
            # lan USA : 2604:2dc0:0000::/34
            # OTHER : 2604:2dc0:2000::/34
            # lan APAC : 2604:2dc0:4000::/34
            # lan EU : 2604:2dc0:8000::/34
            
        #OVH = \32
        #OVH+continent = \34
        #OVH+continent+type = \36
        
        
        # ===================== OVH Router configurations ==================
        # 16 routers identified by a single IPv4, IPv6 address
        # ==================================================================        
        # --- Routers configuration ---
        sin = self.addRouter("sin", config=RouterConfig,lo_addresses=["2604:2dc0:4000::0/36","198.27.92.0/24"] );
        syd = self.addRouter("syd", config=RouterConfig,lo_addresses=["2604:2dc0:4000::1/36","198.27.92.1/24"]);

        pao = self.addRouter("pao", config=RouterConfig,lo_addresses=["2604:2dc0::0/36","198.27.92.2/24"]);
        sjo = self.addRouter("sjo", config=RouterConfig,lo_addresses=["2604:2dc0::1/36","198.27.92.3/24"]);
        lax1 = self.addRouter("lax1", config=RouterConfig,lo_addresses=["2604:2dc0::2/36","198.27.92.4/24"]);

        chi1 = self.addRouter("chi1", config=RouterConfig,lo_addresses=["2604:2dc0::3/36","198.27.92.5/24"]);
        chi5 = self.addRouter("chi5", config=RouterConfig,lo_addresses=["2604:2dc0::4/36","198.27.92.6/24"]);

        bhs1 = self.addRouter("bhs1", config=RouterConfig,lo_addresses=["2604:2dc0::5/36","198.27.92.7/24"]);
        bhs2 = self.addRouter("bhs2", config=RouterConfig,lo_addresses=["2604:2dc0::6/36","198.27.92.8/24"]);

        ash1 = self.addRouter("ash1", config=RouterConfig,lo_addresses=["2604:2dc0::7/36","198.27.92.9/24"]);
        ash5 = self.addRouter("ash5", config=RouterConfig,lo_addresses=["2604:2dc0::8/36","198.27.92.10/24"]);

        nwk1 = self.addRouter("nwk1", config=RouterConfig,lo_addresses=["2604:2dc0::9/36","198.27.92.11/24"]);
        nwk5 = self.addRouter("nwk5", config=RouterConfig,lo_addresses=["2604:2dc0::a/36","198.27.92.12/24"]);
        nyc = self.addRouter("nyc", config=RouterConfig,lo_addresses=["2604:2dc0::b/36","198.27.92.13/24"]);

        lon_thw = self.addRouter("lon_thw", config=RouterConfig,lo_addresses=["2604:2dc0:8000::0/36","198.27.92.14/24"]);
        lon_drch = self.addRouter("lon_drch", config=RouterConfig,lo_addresses=["2604:2dc0:8000::1/36","198.27.92.15/24"]);
        
        anycast1 = self.addRouter("anycast1",config = RouterConfig, lo_addresses = ["2604:2dc1::0/128","192.27.92.255/32",] );   
        anycast2 = self.addRouter("anycast2",config = RouterConfig, lo_addresses = ["2604:2dc1::0/128","192.27.92.255/32",] );   
        anycast3 = self.addRouter("anycast3",config = RouterConfig, lo_addresses = ["2604:2dc1::0/128","192.27.92.255/32",] );   
        anycastServers = [anycast1,anycast2,anycast3];

        OVHRouters = [sin, syd, pao, sjo, lax1, chi1, chi5, bhs1, bhs2, ash1, ash5, nwk1, nwk5, nyc, lon_thw, lon_drch, anycast1,anycast2,anycast3];
        self.addAS(16276, OVHRouters);
        
        # --- Subnets of each router ---
        #       IPv6
        subnetSin6 = "2604:2dc0:4800::0/40";
        subnetSyd6 = "2604:2dc0:4900::0/40";
        
        subnetPao6 = "2604:2dc0:0800::0/40";
        subnetSjo6 = "2604:2dc0:0900::0/40";
        subnetLax16 = "2604:2dc0:0a00::0/40";
        
        subnetChi16 = "2604:2dc0:0b00::0/40";
        subnetChi56 = "2604:2dc0:0c00::0/40";

        subnetBhs16 = "2604:2dc0:0d00::0/40";
        subnetBhs26 = "2604:2dc0:0e00::0/40";
        
        subnetAsh16 = "2604:2dc0:0f00::0/40";
        subnetAsh56 = "2604:2dc0:1000::0/40";
        
        subnetNwk16 = "2604:2dc0:1100::0/40";
        subnetNwk56 = "2604:2dc0:1200::0/40";
        subnetNyc6 = "2604:2dc0:1300::0/40";
        
        subnetLon_thw6 = "2604:2dc0:8800::0/40";
        subnetLon_drch6 = "2604:2dc0:8900::0/40";
        
        #       IPv4
        subnetSin = "198.27.92.16/28";
        subnetSyd = "198.27.92.32/28";
        
        subnetPao = "198.27.92.48/28";
        subnetSjo = "198.27.92.64/28";
        subnetLax1 = "198.27.92.80/28";
        
        subnetChi1 = "198.27.92.96/28";
        subnetChi5 = "198.27.92.112/28";
        
        subnetBhs1 = "198.27.92.128/28";
        subnetBhs2 = "198.27.92.144/28";
        
        subnetAsh1 = "198.27.92.160/28";
        subnetAsh5 = "198.27.92.176/28";
        
        subnetNwk1 = "198.27.92.192/28";
        subnetNwk5 = "198.27.92.208/28";
        subnetNyc = "198.27.92.224/28";
        
        subnetLon_thw = "198.27.92.240/29";
        subnetLon_drch = "198.27.92.248/29";


        OVHSubsnets4 = [subnetSin, subnetSyd,subnetPao,subnetSjo,subnetLax1,subnetChi1,subnetChi5,subnetBhs1,subnetBhs2,subnetAsh1,subnetAsh5,subnetNwk1,subnetNwk5,subnetNyc,subnetLon_thw,subnetLon_drch];
        OVHSubsnets6 = [subnetSin6, subnetSyd6,subnetPao6,subnetSjo6,subnetLax16,subnetChi16,subnetChi56,subnetBhs16,subnetBhs26,subnetAsh16,subnetAsh56,subnetNwk16,subnetNwk56,subnetNyc6,subnetLon_thw6,subnetLon_drch6];


        # ====== Host configuration ========================================
        #  
        # ==================================================================
        h1 = self.addHost("h1");
        self.addLink(h1,chi1);

        h2 = self.addHost("h2");
        self.addLink(h2,"lax1");     
        
        self.addSubnet(nodes = [sin], subnets = [subnetSin6, subnetSin]); 
        self.addSubnet(nodes = [syd], subnets = [subnetSyd6,subnetSyd]); 
        
        self.addSubnet(nodes = [pao], subnets = [subnetPao6,subnetPao]); 
        self.addSubnet(nodes = [sjo], subnets = [subnetSjo6,subnetSjo]);
        self.addSubnet(nodes = [lax1,h2], subnets = [subnetLax16,subnetLax1]);
        
        self.addSubnet(nodes = [chi1,h1], subnets = [subnetChi16,subnetChi1]);
        self.addSubnet(nodes = [chi5], subnets = [subnetChi56,subnetChi5]);
        
        self.addSubnet(nodes = [bhs1], subnets = [subnetBhs16,subnetBhs1]);
        self.addSubnet(nodes = [bhs2], subnets = [subnetBhs26,subnetBhs2]);
        
        self.addSubnet(nodes = [ash1], subnets = [subnetAsh16,subnetAsh1]);
        self.addSubnet(nodes = [ash5], subnets = [subnetAsh56,subnetAsh5]);

        self.addSubnet(nodes = [nwk1], subnets = [subnetNwk16,subnetNwk1]);
        self.addSubnet(nodes = [nwk5], subnets = [subnetNwk56,subnetNwk5]);
        self.addSubnet(nodes = [nyc], subnets = [subnetNyc6,subnetNyc]);
        
        self.addSubnet(nodes = [lon_thw], subnets = [subnetLon_thw6,subnetLon_thw]);
        self.addSubnet(nodes = [lon_drch], subnets = [subnetLon_drch6,subnetLon_drch]);
        
        
        # --- Physical links between routers ---
        self.addLink(sin, sjo,igp_metric=extra_large); 
        self.addLink(syd,lax1,igp_metric=extra_large);

        self.addLink(syd,sin,igp_metric=large);
        self.addLink(syd,lon_thw,igp_metric=extra_large);
        self.addLink(syd,lon_drch,igp_metric=extra_large);
        self.addLink(sin,lon_thw,igp_metric=extra_large);
        self.addLink(sin,lon_drch,igp_metric=extra_large);
        self.addLink(lon_thw,lon_drch,igp_metric=small);

        self.addLink(pao,sjo,igp_metric=medium);
        self.addLink(sjo,lax1,igp_metric=medium);

        self.addLink(pao,chi1,igp_metric=medium);
        self.addLink(pao,chi5,igp_metric=medium);
        self.addLink(chi1,chi5,igp_metric=small);

        self.addLink(lax1,ash1,igp_metric=large);
        self.addLink(lax1,ash5,igp_metric=large);
        self.addLink(ash1,ash5,igp_metric=small);

        self.addLink(chi1,bhs1,igp_metric=medium);
        self.addLink(chi5,bhs2,igp_metric=medium);
        self.addLink(bhs1,bhs2,igp_metric=small);

        self.addLink(bhs1,nwk1,igp_metric=medium);
        self.addLink(bhs2,nwk5,igp_metric=medium);

        self.addLink(ash1,nwk1,igp_metric=large);
        self.addLink(ash5,nwk5,igp_metric=large);

        self.addLink(ash1,chi1,igp_metric=large);
        self.addLink(ash5,chi5,igp_metric=large);

        self.addLink(nwk1,nwk5,igp_metric=small);
        self.addLink(nwk1,nyc,igp_metric=small);
        self.addLink(nwk5,nyc,igp_metric=small);

        self.addLink(nwk1,lon_thw,igp_metric=extra_large);
        self.addLink(nwk5,lon_drch,igp_metric=extra_large);

        self.addLink(anycast1,sin);     
        self.addLink(anycast2,ash1);     
        self.addLink(anycast3,lon_thw);     
        
        # ========================= OSPF configuration ==================
        #
        # ===============================================================
        # --- Add a OSPF daemon on each router of OVH
        for r in OVHRouters:
            if(r not in anycastServers):
                r.addDaemon(OSPF)
                r.addDaemon(OSPF6)
        
        # ========================= BGP configuration ==================
        #   - 3 route reflectors at level 1 (highest in hierarchy)
        #   - 3 route reflectors at level 0 
        # ==============================================================
        # --- Add a BGP daemon on each router ---
        for i in range(len(OVHRouters)-len(anycastServers)):
            OVHRouters[i].addDaemon(BGP,debug = ("neighbor",),address_families=(AF_INET(networks=(OVHSubsnets4[i],)),AF_INET6(networks=(OVHSubsnets6[i],))));
        
        anycast1.addDaemon(BGP,RouterConfig,address_families = ( AF_INET6( networks=("2604:2dc0::0/128",) ), AF_INET( networks=("192.27.92.255/32",))));  
        anycast2.addDaemon(BGP,RouterConfig,address_families = ( AF_INET6( networks=("2604:2dc0::0/128",) ), AF_INET( networks=("192.27.92.255/32",))));  
        anycast3.addDaemon(BGP,RouterConfig,address_families = ( AF_INET6( networks=("2604:2dc0::0/128",) ), AF_INET( networks=("192.27.92.255/32",))));  

        bgp_anycast(self,sin,anycast1);
        bgp_anycast(self,ash1,anycast2);
        bgp_anycast(self,lon_thw,anycast3);

        # --- Configure the router reflectors ---
        #       Lower hierarchy route reflectors
        
        # --- Configure the router reflectors ---
        set_rr(self, rr= bhs1, peers=[chi1,pao,nwk1,nyc]);
        set_rr(self, rr= bhs2, peers=[nwk5,pao,sjo,chi5]);
        set_rr(self, rr= ash5, peers=[nyc,chi5,nwk5,lax1]);

        bgp_peering(self, bhs1, bhs2);
        bgp_peering(self, bhs1, ash5);
        bgp_peering(self, bhs2, ash5);

        #       higher hierarchy route reflectors 
        set_rr(self, rr = sin, peers=[syd,anycast1]);                                    # This one is a super RR
        set_rr(self, rr= ash1, peers=[bhs1,bhs2,ash5,chi1,sjo,lax1,nwk1,anycast2]);      # This one is a super RR
        set_rr(self, rr = lon_thw, peers=[lon_drch,anycast3]);                           # This one is a super RR
        

        bgp_peering(self, ash1, lon_thw)
        bgp_peering(self, ash1, sin)
        bgp_peering(self, sin, lon_thw)
        

        
        # ====== Router configurations of transit/stub providers ===========
        # - 1 stub provider : Google (ggl)
        # - 3 transit providers : 
        #       - Cogent (cgt)
        #       - Level3 (lvl3) 
        #       - Telia (tel) 
        # ==================================================================
        # --- Google (AS=2)  
        ggl = self.addRouter("ggl", config=RouterConfig);
        self.addLinks( (ggl,ash1), (ggl,ash5) );
        self.addAS(2,(ggl , ));
        
        lan_ggl = '1.3.1.0/24'
        lan_ggl_v6 = 'cafe:babe:dead:beaf::/64'            
        ggl.addDaemon(BGP, address_families=(AF_INET(networks=(lan_ggl,)),AF_INET6(networks=(lan_ggl_v6,))));
        
        h_ggl = self.addHost("h_ggl");
        self.addSubnet(nodes = [ggl, h_ggl], subnets=(lan_ggl,lan_ggl_v6));
        self.addLink(h_ggl,ggl,igp_metric=1);
        
        ebgp_session(self, ggl, ash1, link_type=SHARE);
        ebgp_session(self, ggl, ash5, link_type=SHARE);
        
        # --- Cogent (AS=3) 
        cgt = self.addRouter("cgt", config=RouterConfig);
        self.addLinks( (cgt,nwk1), (cgt,nwk5), (cgt,ash1), (cgt,ash5), (cgt,chi1), (cgt,sjo) );
        self.addAS(3,(cgt , ));
        
        lan_cgt = '1.4.2.0/24'
        lan_cgt_v6 = 'c1a4:4ad:c0ff:ee::/64'
        cgt.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_cgt_v6,)),AF_INET(networks=(lan_cgt,)),));
        
        h_cgt = self.addHost("h_cgt");
        self.addSubnet(nodes = [cgt, h_cgt], subnets=(lan_cgt,lan_cgt_v6));
        self.addLink(h_cgt,cgt,igp_metric=1);
        
        ebgp_session(self, cgt, nwk1, link_type=SHARE);
        ebgp_session(self, cgt, nwk5, link_type=SHARE);
        ebgp_session(self, cgt, ash1, link_type=SHARE);
        ebgp_session(self, cgt, ash5, link_type=SHARE);
        ebgp_session(self, cgt, chi1, link_type=SHARE);
        ebgp_session(self, cgt, sjo, link_type=SHARE);
        
        # --- Level 3 (AS=4) 
        lvl3 = self.addRouter("lvl3", config=RouterConfig);
        self.addLinks( (lvl3,nwk1), (lvl3,nwk5), (lvl3,chi1), (lvl3,chi5), (lvl3,sjo) );
        self.addAS(4,(lvl3, ));
        
        lan_lvl3 = '1.5.3.0/24'
        lan_lvl3_v6 = 'cafe:d0d0:e5:dead::/64'
        lvl3.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_lvl3_v6,)),AF_INET(networks=(lan_lvl3,)),));

        h_lvl3 = self.addHost("h_lvl3");
        self.addSubnet(nodes = [lvl3, h_lvl3], subnets=(lan_lvl3,lan_lvl3_v6));
        self.addLink(h_lvl3,lvl3,igp_metric=1);
        
        ebgp_session(self, lvl3, nwk1, link_type=SHARE);# regarde si on change 
        ebgp_session(self, lvl3, nwk5, link_type=SHARE);
        ebgp_session(self, lvl3, chi1, link_type=SHARE);
        ebgp_session(self, lvl3, chi5, link_type=SHARE);
        ebgp_session(self, lvl3, sjo, link_type=SHARE);
        
        # --- Telia (AS=5) 
        tel = self.addRouter("tel", config=RouterConfig);
        self.addLinks( (tel,nwk1), (tel,nwk5), (tel,ash5), (tel,chi5), (tel,pao) );
        self.addAS(5,(tel, ));
        
        lan_tel = '1.6.4.0/24'
        lan_tel_v6 = 'aaaa:aaaa:aaaa:aaaa::/64'        
        tel.addDaemon(BGP, address_families=(AF_INET6(networks=(lan_tel_v6,)),AF_INET(networks=(lan_tel,)),));
        
        h_tel = self.addHost("h_tel");
        self.addSubnet(nodes = [tel, h_tel], subnets=(lan_tel,lan_tel_v6));
        self.addLink(h_tel,tel,igp_metric=1);
        
        ebgp_session(self, tel, nwk1, link_type=SHARE);
        ebgp_session(self, tel, nwk5, link_type=SHARE);
        ebgp_session(self, tel, ash5, link_type=SHARE);
        ebgp_session(self, tel, chi5, link_type=SHARE);
        ebgp_session(self, tel, pao, link_type=SHARE);
        
        
        externalRouters = [ggl, cgt, lvl3, tel];
        
        for eR in externalRouters:  
            eR.addDaemon(OSPF6);
            eR.addDaemon(OSPF);
        
        super().build(*args, **kwargs)


        
# Press the green button to run the script.
if __name__ == '__main__':
    net = IPNet(topo=OVHTopology())#,allocate_IPs=False)
    try:
        net.start()
        IPCLI(net)
    finally:
        net.stop()
