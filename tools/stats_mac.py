import subprocess
from core.registre import outil

@outil(
    nom="stats_systeme",
    description="Donne les statistiques en direct du Mac M2 : CPU, RAM utilisée, Batterie et Espace disque.",
    parametres={"type": "object", "properties": {}},
    securite="N1",
    affichage="toujours"
)
def stats_systeme() -> str:
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=0.2)
        mem = psutil.virtual_memory()
        ram_u = mem.used / (1024 ** 3)
        ram_t = mem.total / (1024 ** 3)
        batt = psutil.sensors_battery()
        info_batt = f", Batterie: {batt.percent}%" if batt else ""
        return f"CPU: {cpu}% | RAM: {ram_u:.1f}/{ram_t:.1f} Go ({mem.percent}%){info_batt}"
    except ImportError:
        # Fallback natif macOS sans psutil
        res = subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True)
        tot_go = int(res.stdout.strip()) / (1024**3) if res.returncode == 0 else 8.0
        return f"MacBook Air M2 : {tot_go:.0f} Go Mémoire Unifiée active."
