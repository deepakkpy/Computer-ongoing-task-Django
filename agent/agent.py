
import psutil, requests, socket, platform, shutil, time, configparser, os, json

def get_config():
    cfg = configparser.ConfigParser()
    cfg.read(os.path.join(os.path.dirname(__file__), 'config.ini'))
    url = os.environ.get('BACKEND_URL', cfg.get('agent', 'backend_url', fallback='http://localhost:8000/api/ingest/'))
    key = os.environ.get('API_KEY', cfg.get('agent', 'api_key', fallback='changeme123'))
    return url, key

def collect_system():
    vm = psutil.virtual_memory()
    total, used, avail = vm.total/(1024**3), (vm.total-vm.available)/(1024**3), vm.available/(1024**3)
    disk = shutil.disk_usage(os.path.abspath(os.sep))
    disk_total, disk_used, disk_free = disk.total/(1024**3), disk.used/(1024**3), disk.free/(1024**3)
    cpu_model = platform.processor() or platform.machine()
    try:
        cores = psutil.cpu_count(logical=False) or 0
        threads = psutil.cpu_count(logical=True) or 0
    except Exception:
        cores = threads = 0
    return {
        "os": f"{platform.system()} {platform.release()} {platform.version()}",
        "cpu_model": cpu_model,
        "cores": cores,
        "threads": threads,
        "ram_total_gb": round(total,2),
        "ram_used_gb": round(used,2),
        "ram_available_gb": round(avail,2),
        "storage_total_gb": round(disk_total,2),
        "storage_used_gb": round(disk_used,2),
        "storage_free_gb": round(disk_free,2),
    }

def collect_processes():
    procs = []
    # First call to cpu_percent to prime
    for p in psutil.process_iter(['pid']): 
        try: p.cpu_percent(None)
        except Exception: pass
    time.sleep(0.3)
    for proc in psutil.process_iter(['pid','ppid','name','memory_info']):
        try:
            procs.append({
                "pid": proc.info['pid'],
                "ppid": proc.info['ppid'],
                "name": proc.info['name'] or 'unknown',
                "cpu": proc.cpu_percent(None),
                "mem_mb": (proc.info['memory_info'].rss/(1024*1024)) if proc.info.get('memory_info') else 0.0
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return procs

def main():
    url, key = get_config()
    payload = {
        "hostname": socket.gethostname(),
        "system": collect_system(),
        "processes": collect_processes()
    }
    headers = {"Authorization": f"Api-Key {key}", "Content-Type":"application/json"}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=15)
        print("Status", r.status_code, r.text[:200])
    except Exception as e:
        print("Failed to send:", e)

if __name__ == "__main__":
    main()
