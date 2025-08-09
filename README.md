# 🔐 Network Security Laboratory

## 📘 Overview
Educational lab for the Master's Degree in Cybersecurity – focusing on three key network attacks:
- **ARP Poisoning**
- **Man-in-the-Middle (MitM)**
- **TCP Session Hijacking**

Hands-on exercises are performed in a safe, containerized Docker environment.

## 🖥 Lab Environment
- **Docker Compose** setup with `client`, `server`, and `attacker` nodes.
- Controlled network for attack demonstrations.
```bash
cd netseclab
sudo docker compose up
sudo docker exec -it [client|server|attacker] bash
```

## 📂 Modules
1. **ARP Poisoning** – Use Ettercap/Scapy to spoof ARP tables and redirect traffic.
2. **Man-in-the-Middle** – Intercept/modify HTTP traffic with mitmproxy or run a fake server.
3. **TCP Session Hijacking** – Inject commands into active sessions using sniffed sequence numbers.

## 🛠 Tools
Docker, Ettercap, Scapy, Wireshark, arpspoof, mitmproxy, tcpdump, hping3.

## 📜 Authors
Matteo Bertoldo, Filippo Basilico, Andrea Pappacoda

## 📄 License
For **educational purposes only**. Do not use on unauthorized systems.
