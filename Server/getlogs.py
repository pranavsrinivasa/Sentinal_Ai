import psutil
import csv
from datetime import datetime
import time

csv_file = 'Data\cybersecurity_logs_structured.csv'

def initialize_csv():
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "CPU Usage (%)", "Memory Usage (%)", "PID", "Process Name", "User", "Local IP", "Local Port", "Remote IP", "Remote Port", "Status"])

def log_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    return cpu_usage, memory_usage

def log_running_processes():
    processes = []
    for process in psutil.process_iter(['pid', 'name', 'username']):
        try:
            processes.append((process.info['pid'], process.info['name'], process.info['username']))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return processes

def log_network_info():
    connections = []
    net_connections = psutil.net_connections(kind='inet')
    for conn in net_connections:
        if conn.status == psutil.CONN_ESTABLISHED:
            connections.append((conn.laddr.ip, conn.laddr.port, conn.raddr.ip, conn.raddr.port, conn.status))
    return connections

def main(max_count = 1,time_interval=60):
    initialize_csv()
    cycle_count = 0
    while cycle_count < max_count:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cpu_usage, memory_usage = log_system_info()
        processes = log_running_processes()
        connections = log_network_info()

        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            for process in processes: 
                pid, name, user = process
                for conn in connections:
                    local_ip, local_port, remote_ip, remote_port, status = conn
                    writer.writerow([timestamp, cpu_usage, memory_usage, pid, name, user, local_ip, local_port, remote_ip, remote_port, status])
        cycle_count+= 1
        if cycle_count < max_count:
            time.sleep(time_interval)
if __name__ == "__main__":
    main()
