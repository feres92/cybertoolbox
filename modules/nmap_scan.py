import nmap

def run_nmap(ip):
    scanner = nmap.PortScanner()
    scanner.scan(ip, arguments='-T4 -F')
    open_ports = []
    for proto in scanner[ip].all_protocols():
        ports = scanner[ip][proto].keys()
        open_ports.extend([str(port) for port in ports])
    return {'ip': ip, 'open_ports': open_ports}
