from prometheus_api_client import PrometheusConnect
from rich.console import Console
import time

# Initialization: set up the console 
console = Console(color_system='standard')
prom = PrometheusConnect(url ="http://localhost:3555", disable_ssl=True)

def cluster_is_active():
    result = prom.custom_query(query="sum(ray_node_cpu_utilization)")
    activity_level = float(result[0]['value'][1])
    if activity_level < 25:
        console.print("[green]Cluster is idle. Nothing is happening.")
        return False
    else:
        console.print("[yellow]Cluster is active.")
        return True
    
def detect_too_many_tasks():
    result = prom.custom_query(query="sum(ray_scheduler_tasks{State='SpilledUnschedulable'})")
    backlog = int(result[0]['value'][1])
    if backlog > 10000:
        console.print("[bold]Issue detected. Too many unscheduled tasks.")
        console.print(f'   You currently have {backlog} tasks waiting to be scheduled. ')
        console.print( '   Consider using ray.wait to manage the backpressure. ')
        console.print( '   For more information, please see https://docs.ray.io/en/master/ray-core/tasks/patterns/limit-tasks.html')
        return True
    return False

while True: 
    console.clear() 
    console.rule("[bold blue]Anyscale Advisor")
    issues_detected = []
    if cluster_is_active():
        issues_detected.append(detect_too_many_tasks())
        
    if all(issues_detected) == False:
        console.print('[green] No issues detected!')
        

    time.sleep(5)

    

    
