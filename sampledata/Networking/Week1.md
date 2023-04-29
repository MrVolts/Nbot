# Week 1

## Chapter 1: Introduction

- Goal: Get a feel for terminology and concepts
- Use the Internet as an example
- Topics:
    - What's the Internet?
    - What's a protocol?
    - Network edge: hosts, access networks, physical media
    - Network core: packet/circuit switching, Internet structure
    - Performance: loss, delay, throughput
    - Security
    - Protocol layers, service models
    - History

## Chapter 1: Roadmap

1. What is the Internet?
2. Network edge
    - End systems, access networks, links
3. Network core
    - Packet switching, circuit switching, network structure
4. Delay, loss, throughput in networks
5. Protocol layers, service models
6. Networks under attack: security
7. History

## What's the Internet: "nuts and bolts" view

- Millions of connected computing devices
- Communication links (fiber, copper, radio, satellite)
- Transmission rate: bandwidth
- Packet switches: forward packets (chunks of data)
- Internet: "network of networks" interconnected ISPs
- Protocols: e.g., TCP, IP, HTTP, Skype, 802.11
- Internet standards: RFC, IETF

![Screenshot 2023-04-18 143231.png](Week%201%20078d31cb4c9544039ba649efc461fed0/Screenshot_2023-04-18_143231.png)

## What's the Internet: a service view

- Infrastructure providing services to applications
- Provides programming interface to apps
    - Service options, analogous to postal service
    - hooks allow sending and receiving app programs

## What's a Protocol?

- Human protocols: e.g., asking the time, introductions
- Network protocols: machines instead of humans
    - All communication activity in Internet governed by protocols
- Protocols define format, order of messages, and actions taken on msg transmission, receipt

## Network Structure

- Network edge
    - Hosts: clients and servers
    - Access networks: mobile network, home network, institutional network
    - Physical media: wired, wireless communication links
- Network core
    - Interconnected routers
    - Network of networks

## The Network Edge

- End systems (hosts)
    - Run application programs (e.g., Web, email)
    - Located at the edge of the network
- Client/server model
    - Client requests and receives service from always-on server
- Peer-to-peer model
    - Minimal (or no) use of dedicated servers

![Untitled](Week%201%20078d31cb4c9544039ba649efc461fed0/Untitled.png)

## Access Networks and Physical Media

- Residential access networks
- Institutional access networks (school, company)
- Mobile access networks
- Considerations:
    - Bandwidth (bits per second) of access network
    - Shared or dedicated?

## Access Net: Digital Subscriber Line (DSL)

- Uses existing telephone line to central office DSLAM
- Data over DSL phone line goes to the Internet
- Voice over DSL phone line goes to telephone net
- Upstream transmission rate: < 2.5 Mbps (typically < 1 Mbps)
- Downstream transmission rate: < 24 Mbps (typically < 10 Mbps)

![Untitled](Week%201%20078d31cb4c9544039ba649efc461fed0/Untitled%201.png)

## Access Net: Cable Network

- Data and TV transmitted at different frequencies over shared cable distribution network
- HFC: hybrid fiber coax
    - Asymmetric: up to 30 Mbps downstream transmission rate, 2 Mbps upstream transmission rate
- Network of cable, fiber attaches homes to ISP router
- Homes share access network to cable headend (unlike DSL)

![Untitled](Week%201%20078d31cb4c9544039ba649efc461fed0/Untitled%202.png)

![Untitled](Week%201%20078d31cb4c9544039ba649efc461fed0/Untitled%203.png)

## Access Net: Home Network

- Cable or DSL modem connects to/from headend or central office
- Router, firewall, NAT
- Wired Ethernet (100 Mbps) and wireless access point (54 Mbps)
- Wireless devices

![Untitled](Week%201%20078d31cb4c9544039ba649efc461fed0/Untitled%204.png)

## Enterprise Access Networks (Ethernet)

- Typically used in companies, universities, etc.
- 10 Mbps, 100 Mbps, 1 Gbps, 10 Gbps transmission rates
- End systems typically connect into Ethernet switch, institutional mail, web servers, institutional router, institutional link to ISP (Internet)

![Untitled](Week%201%20078d31cb4c9544039ba649efc461fed0/Untitled%205.png)

## **Wireless Access Networks**

- A shared wireless access network connects end systems to a router via a base station (access point).
- Wireless LANs are used within a building with a range of up to 100ft, and have transmission rates of 11Mbps, 54Mbps, 800Mbps, and 1733Mbps (802.11b/g/n/ac, WiFi).
- Wide-area wireless access is provided by telco (cellular) operators over distances of tens of kilometers, and has transmission rates of 10Mbps, 100Mbps, and 10Gbps (3G, 4G, 5G).

## **Host Sending Function**

- A host sends packets of data.
- The host sending function takes an application message and breaks it into smaller chunks known as packets, with a length of L bits.
- The packet is transmitted into the access network at a transmission rate of R (link transmission rate, link capacity, or link bandwidth).
- Packet transmission delay = time needed to transmit L-bit packet into link = L (bits) / R (bits/sec)

## **Physical Media**

- A bit propagates between transmitter/receiver pairs.
- Physical links are what lie between transmitters and receivers.
- Guided media signals propagate in solid media, such as copper, fiber, and coax.
- Unguided media signals propagate freely, such as radio.

## **Guided Media: Twisted Pair**

- A twisted pair is two insulated copper wires.
- Category 5 twisted pairs provide 100Mbps and 1Gbps Ethernet, while Category 6 twisted pairs provide 10Gbps Ethernet.

## **Guided Media: Coax and Fiber**

- Coaxial cable consists of two concentric copper conductors, is bidirectional, and is used for broadband transmission (e.g., HFC).
- Fiber optic cable consists of glass fiber carrying light pulses, with each pulse representing a bit. It provides high-speed point-to-point transmission rates of up to 10Gbps, has a low error rate, and is immune to electromagnetic noise.

## **Unguided Media: Radio**

- Signals are carried in the electromagnetic spectrum without a physical wire.
- Propagation environment effects include reflection, obstruction by objects, and interference.
- Radio link types include terrestrial microwave (up to 45Mbps), LAN (e.g., WiFi, 11Mbps, 54Mbps), wide-area (e.g., cellular, few Mbps), and satellite (Kbps to 45Mbps channels with a 270msec end-end delay, geosynchronous vs. low altitude).

# **Network CORE**

## **Introduction**

- Mesh of interconnected routers
- Packet-switching: hosts break application-layer messages into packets
- Forward packets from one router to the next, across links on path from source to destination
- Each packet transmitted at full link capacity

## **The network core**

### **Packet-switching: store-and-forward**

- Takes L/R seconds to transmit (push out) L-bit packet into link at R bps
- Store and forward: entire packet must arrive at router before it can be transmitted on the next link
- One-hop numerical example:
    - L = 7.5 Mbits
    - R = 1.5 Mbps
    - One-hop transmission delay = 5 sec
- End-end delay = 2L/R (assuming zero propagation delay)

![Untitled](Week%201%20078d31cb4c9544039ba649efc461fed0/Untitled%206.png)

### **Packet Switching: queueing delay, loss**

- Queuing and loss:
    - If arrival rate (in bits) to link exceeds transmission rate of link for a period of time:
    - Packets will queue, wait to be transmitted on the link
    - Packets can be dropped (lost) if memory (buffer) fills up

![Untitled](Week%201%20078d31cb4c9544039ba649efc461fed0/Untitled%207.png)

## **Network Layer**

### **Two key network-core functions**

- Forwarding: move packets from router’s input to appropriate router output
- Routing: determines source-destination route taken by packets
- Routing algorithms
- Local forwarding table
- Header value output link
- Dest address in arriving packet’s header

![Untitled](Week%201%20078d31cb4c9544039ba649efc461fed0/Untitled%208.png)

### **Alternative core: circuit switching**

- End-end resources allocated to, reserved for “call” between source & dest
- Dedicated resources: no sharing
- Circuit-like (guaranteed) performance
- Circuit segment idle if not used by call (no sharing)
- Commonly used in traditional telephone networks
- In diagram each link has four circuits

[https://www.notion.so](https://www.notion.so)

![Untitled](Week%201%20078d31cb4c9544039ba649efc461fed0/Untitled%209.png)

### **Circuit switching: FDM versus TDM**

![Untitled](Week%201%20078d31cb4c9544039ba649efc461fed0/Untitled%2010.png)

### **Packet switching versus circuit switching**

- Example:
    - 1 Mb/s link
    - Each user:
        - 100 kb/s when “active”
        - Active 10% of time
- Circuit-switching:
    - 10 users
- Packet switching:
    - With 35 users, probability > 10 active at same time is less than .0004
- Packet switching allows more users to use the network!

### **Is packet switching a “slam dunk winner?”**

- Great for bursty data
    - Resource sharing
    - Simpler, no call setup
- Excessive congestion possible: packet delay and loss
    - Protocols needed for reliable data transfer, congestion control
- How to provide circuit-like behavior?
    - Bandwidth guarantees needed for audio/video apps
    - Still an unsolved problem (chapter 7)
- Human analogies of reserved resources (circuit switching) versus on-demand allocation (packet-switching)?

## **Internet structure: network of networks**

- End systems connect to the Internet via access ISPs (Internet Service Providers)
    - Residential, company and university ISPs
- Access ISPs in turn must be interconnected
- So that any two hosts can send packets to each other
- Resulting network of networks is very complex
- Evolution was driven by economics and national policies
- Let’s take a stepwise approach to describe the current Internet structure.

![Untitled](Week%201%20078d31cb4c9544039ba649efc461fed0/Untitled%2011.png)

- The internet is a network of networks. At the center of the internet are a small number of well-connected large networks, known as "tier-1" commercial ISPs. These ISPs, such as Level 3, Sprint, AT&T, and NTT, provide national and international coverage. In addition to tier-1 commercial ISPs, there are regional ISPs that provide access to the internet for end-users. Content provider networks, like Google, have private networks that connect their data centers to the internet, often bypassing tier-1 and regional ISPs. Internet eXchange Points (IXPs) connect different networks together.

## **How do loss and delay occur?**

Packets queue in router buffers when the packet arrival rate to the link exceeds the output link capacity temporarily. Packets then wait for their turn to be transmitted, which causes delay. If no free buffers are available, arriving packets are dropped, resulting in loss.

## **Four sources of packet delay**

- **`dproc`**: nodal processing - check bit errors, determine output link. Typically less than a millisecond.
- **`dqueue`**: queueing delay - time waiting at output link for transmission. Depends on congestion level of the router.
- **`dtrans`**: transmission delay - time to transmit packet into link. Depends on the packet length and the link bandwidth.
- **`dprop`**: propagation delay - time for a bit to propagate from one router to the next. Depends on the length of the physical link and the propagation speed in the medium.

**`dnodal = dproc + dqueue + dtrans + dprop`**

![Untitled](Week%201%20078d31cb4c9544039ba649efc461fed0/Untitled%2012.png)

### Nodal Processing (dproc)

- Check bit errors
- Determine output link
- Typically < 1 msec

### Queueing Delay (dqueue)

- Time waiting at output link for transmission
- Depends on congestion level of router

### Transmission Delay (dtrans)

- L: packet length (bits)
- R: link bandwidth (bps)
- Formula: `dtrans = L/R`

### Propagation Delay (dprop)

- d: length of physical link
- s: propagation speed in medium (~2x10^8 m/sec)
- Formula: `dprop = d/s`

### Transmission vs Propagation Delay

- Transmission and propagation delay are very different
- Check out the Java applet for an interactive animation on trans vs. prop delay

## Queueing Delay (revisited)

- R: link bandwidth (bps)
- L: packet length (bits)
- a: average packet arrival rate

Traffic intensity: `La/R`

- La/R ~ 0: avg. queueing delay small
- La/R -> 1: avg. queueing delay large
- La/R > 1: more “work” arriving than can be serviced, average delay infinite!

### 

![Untitled](Week%201%20078d31cb4c9544039ba649efc461fed0/Untitled%2013.png)

## **"Real" Internet delays and routes**

The traceroute program provides delay measurements from the source to the router along the end-to-end internet path towards the destination. For all **`i`**:

- Sends three packets that will reach router **`i`** on the path towards the destination.
- Router **`i`** returns packets to the sender.
- The sender times the interval between transmission and reply.

Traceroute helps determine what "real" internet delay and loss look like.

![Untitled](Week%201%20078d31cb4c9544039ba649efc461fed0/Untitled%2014.png)

## **Packet Loss**

- Queue (or buffer) preceding link in buffer has finite capacity
- Packet arriving to full queue is dropped (or lost)
- Lost packet may be retransmitted by previous node, by source end system, or not at all

![Untitled](Week%201%20078d31cb4c9544039ba649efc461fed0/Untitled%2015.png)

## **Throughput**

- Throughput is the rate (bits/time unit) at which bits transferred between sender/receiver
- Instantaneous throughput is the rate at a given point in time
- Average throughput is the rate over a longer period of time

### **Throughput Calculation**

- Server with a file of F bits to send to client
- Link capacity Rs bits/sec (server sends bits into pipe that can carry fluid at rate Rs bits/sec)
- Link capacity Rc bits/sec (pipe can carry fluid at rate Rc bits/sec)
    
    ![Untitled](Week%201%20078d31cb4c9544039ba649efc461fed0/Untitled%2016.png)
    

### **End-to-End Throughput**

- If Rs < Rc, average end-to-end throughput is Rs
- If Rs > Rc, average end-to-end throughput is Rc
- The link on end-to-end path that constrains end-to-end throughput is called bottleneck link

## **Protocol "Layers"**

- Networks are complex, with many pieces: hosts, routers, links of various media, applications, protocols, hardware, software
- Protocol "layers" provide a way to organize the structure of the network
- The layers can be thought of as a series of steps, like air travel:
    - Ticket (purchase)
    - Baggage (check)
    - Gates (load)
    - Runway takeoff
    - Airplane routing
    - Ticket (complain)
    - Baggage (claim)
    - Gates (unload)
    - Runway landing
    - Airplane routing

## **Layering in Networking**

Layering is used in dealing with complex systems by providing an explicit structure that allows identification and relationship of the system's pieces. It also eases maintenance and updating of the system by making the change of implementation of a layer's service transparent to the rest of the system. The layering approach is not harmful, as it promotes modularity.

## **Internet Protocol Stack**

The Internet protocol stack has five layers:

1. **Application Layer**: supports network applications like FTP, SMTP, and HTTP.
2. **Transport Layer**: facilitates process-process data transfer using TCP and UDP.
3. **Network Layer**: routes datagrams from source to destination using IP and routing protocols.
4. **Link Layer**: facilitates data transfer between neighboring network elements using Ethernet, 802.111 (WiFi), and PPP.
5. **Physical Layer**: deals with bits "on the wire."

## **ISO/OSI Reference Model**

The ISO/OSI reference model has seven layers:

1. **Application Layer**: allows applications to interpret the meaning of data. It covers encryption, compression, and machine-specific conventions.
2. **Presentation Layer**: handles synchronization, checkpointing, and recovery of data exchange.
3. **Session Layer**: deals with the establishment, management, and termination of a connection between applications.
4. **Transport Layer**: facilitates process-process data transfer using TCP and UDP.
5. **Network Layer**: routes datagrams from source to destination using IP and routing protocols.
6. **Link Layer**: facilitates data transfer between neighboring network elements using Ethernet, 802.111 (WiFi), and PPP.
7. **Physical Layer**: deals with bits "on the wire."

### **Encapsulation**

- Encapsulation is a process in computer networking where data is divided into segments and wrapped with headers from different layers of the OSI model.
- The OSI model has 7 layers: Application, Presentation, Session, Transport, Network, Data Link, and Physical.
- When sending data, it is passed down from the source Application layer through the other layers, with each layer adding a header (or sometimes, a trailer) before passing it to the next layer.
- Headers contain control information, such as source and destination addresses, that is used by each layer to process the data correctly.

### Data Units at Each Layer

- Application Layer: Message (M)
- Transport Layer: Segment (Ht M)
- Network Layer: Datagram (Hn Ht M)
- Data Link Layer: Frame (Hl Hn Ht M)

### Key Devices

- Router: Operates at the Network layer, forwarding data based on IP addresses.
- Switch: Operates at the Data Link layer, forwarding data based on MAC addresses.

During the encapsulation process, the data is transformed from a message into a segment, then a datagram, and finally a frame. The reverse process, called de-encapsulation, happens at the destination, where each layer removes the headers added by the corresponding layer at the source.

![Untitled](Week%201%20078d31cb4c9544039ba649efc461fed0/Untitled%2017.png)

## **Network Security**

The field of network security concerns itself with the following:

1. How bad guys can attack computer networks.
2. How to defend networks against attacks.
3. How to design architectures that are immune to attacks.

The Internet was not originally designed with security in mind. Security considerations are present in all layers of the Internet protocol stack.

## **Bad Guys and Network Security**

### **Malware**

Malware can enter a host through viruses or worms. Spyware malware can record keystrokes, web sites visited, and upload information to a collection site. An infected host can be enrolled in a botnet and used for spam or distributed denial of service (DDoS) attacks.

### **Denial of Service (DoS) Attacks**

Attackers make resources (server, bandwidth) unavailable to legitimate traffic by overwhelming resources with bogus traffic.

### **Sniffing Packets**

Packet "sniffing" occurs in broadcast media (shared ethernet, wireless), where a promiscuous network interface reads/records all packets, including passwords, that pass by.

### **IP Spoofing**

IP spoofing involves sending a packet with a false source address.

# Internet History

## 1961-1972: Early Packet-switching Principles

- 1961: Kleinrock - Queueing theory shows effectiveness of packet-switching
- 1964: Baran - Packet-switching in military nets
- 1967: ARPAnet conceived by Advanced Research Projects Agency
- 1969: First ARPAnet node operational
- 1972:
    - ARPAnet public demo
    - NCP (Network Control Protocol) first host-host protocol
    - First e-mail program
    - ARPAnet has 15 nodes

## 1970: ALOHAnet Satellite Network in Hawaii

## 1974-1980: Internetworking, New and Proprietary Nets

- 1974: Cerf and Kahn - Architecture for interconnecting networks
- 1979: ARPAnet has 200 nodes

### Cerf and Kahn's Internetworking Principles

- Minimalism, autonomy - No internal changes required to interconnect networks
- Best effort service model
- Stateless routers
- Decentralized control

These principles define today's Internet architecture.

## 1980-1990: New Protocols, A Proliferation of Networks

- 1983: Deployment of TCP/IP
- 1982: SMTP e-mail protocol defined
- 1983: DNS defined for name-to-IP-address translation
- 1985: FTP protocol defined
- 1988: TCP congestion control
- New national networks: Csnet, BITnet, NSFnet, Minitel
- 100,000 hosts connected to confederation of networks

## 1990-2000: Commercialization, The Web, New Apps

- Early 1990s: ARPAnet decommissioned
- 1991: NSF lifts restrictions on commercial use of NSFnet (decommissioned, 1995)
- Early 1990s: Web
    - Hypertext [Bush 1945, Nelson 1960’s]
    - HTML, HTTP: Berners-Lee
    - 1994: Mosaic, later Netscape
    - Late 1990s: Commercialization of the Web
- Late 1990s-2000s:
    - More killer apps: Instant messaging, P2P file sharing
    - Network security to forefront
    - Est. 50 million host, 100 million+ users
    - Backbone links running at Gbps

## 2005-Present

- ~750 million hosts
    - Smartphones and tablets
- Aggressive deployment of broadband access
- Increasing ubiquity of high-speed wireless access
- Emergence of online social networks:
    - Facebook: Soon one billion users
- Service providers (Google, Microsoft) create their own networks
    - Bypass Internet, providing “instantaneous” access to search, email, etc.
- E-commerce, universities, enterprises running their services in “cloud” (e.g., Amazon EC2)

# Introduction: Summary

- Summary of material covered:
- Internet overview
- What's a protocol?
- Network edge, core, access network
- Packet-switching vs. circuit-switching
- Internet structure
- Performance: loss, delay, throughput
- Layering, service models
- Security
- History

## Three Big Questions

### 1. Who am I?

- Host name

### 2. Why am I here?

- IP address:
    - IPv4: 32-bit
    - IPv6: 128-bit
    - ICANN
- Subnet mask
- Default gateway

### 3. Where am I going?

- Multiple hops with varying delay
- Internal address vs. external address
- Example: [www.reading.ac.uk](http://www.reading.ac.uk/)
    - 134.225.0.151 (internal)
- Three delays: 291ms, 225ms, 213ms

## IP Address and Subnets

- IP address:
    - Subnet part - high order bits
    - Host part - low order bits
- What's a subnet?
    - Device interfaces with the same subnet part of IP address
    - Can physically reach each other without an intervening router
- Subnet mask: /24, 255.255.255.0
- Example:
    - 223.1.1.0/24
    - 223.1.2.0/24