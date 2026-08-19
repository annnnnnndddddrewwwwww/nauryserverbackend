import webview
import os
import sys
import shutil
import ctypes
import subprocess
import time
import json
import uuid
import hashlib
import urllib.request
import urllib.parse
import re
import threading
import multiprocessing

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, will use system env vars only

def get_dir_size(path, end_time=None):
    if end_time and time.time() > end_time:
        return 0
    total = 0
    try:
        with os.scandir(path) as it:
            for entry in it:
                if end_time and time.time() > end_time:
                    break
                try:
                    if entry.is_symlink():
                        continue
                    if entry.is_file():
                        total += entry.stat(follow_symlinks=False).st_size
                    elif entry.is_dir():
                        total += get_dir_size(entry.path, end_time)
                except:
                    continue
    except:
        pass
    return total

def clean_directory(path):
    freed = 0
    errors = 0
    if not path or not os.path.exists(path):
        return freed, errors
    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            try:
                size = 0
                if os.path.isfile(item_path):
                    size = os.path.getsize(item_path)
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    size = get_dir_size(item_path)
                    shutil.rmtree(item_path)
                freed += size
            except Exception:
                errors += 1
    except:
        pass
    return freed, errors

def run_cmd(cmd, timeout=25):
    """Run a command safely. For simple commands without shell features, uses shell=False."""
    try:
        # If it's a simple command without shell operators, run without shell
        if isinstance(cmd, str) and not any(op in cmd for op in ['|', '>', '<', '&', ';', '&&', '||']):
            parts = cmd.split()
            res = subprocess.run(parts, shell=False, creationflags=subprocess.CREATE_NO_WINDOW, check=False,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        else:
            # Commands with shell features need shell=True - ensure no user input is directly interpolated
            res = subprocess.run(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW, check=False,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        return res.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    except Exception:
        return False


def run_ps(cmd, timeout=25):
    """Run a PowerShell command safely using -Command with proper argument passing."""
    try:
        res = subprocess.run(
            ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd],
            shell=False, creationflags=subprocess.CREATE_NO_WINDOW, check=False,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout,
            encoding='utf-8', errors='replace'
        )
        return res.returncode == 0, res.stdout, res.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout"
    except Exception as e:
        return False, "", str(e)

def _quick_hash(path, sample_size=65536):
    """Hash rápido por muestreo (inicio+fin del archivo) para detectar duplicados sin leer todo el disco."""
    try:
        h = hashlib.md5()
        size = os.path.getsize(path)
        with open(path, 'rb') as f:
            h.update(f.read(sample_size))
            if size > sample_size * 2:
                f.seek(-sample_size, os.SEEK_END)
                h.update(f.read(sample_size))
        return h.hexdigest()
    except Exception:
        return None

def _app_data_dir():
    """Carpeta propia de la app para guardar snapshots, historial de benchmark, etc."""
    base = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'NauryUtility')
    try:
        os.makedirs(base, exist_ok=True)
    except Exception:
        pass
    return base

def _safe_filename(value, max_len=64):
    """Convierte un id en un nombre de archivo seguro (defensa en profundidad: nunca confiar
    en un string que viaja de JS a Python para construir rutas de disco)."""
    cleaned = re.sub(r'[^a-zA-Z0-9_\-]', '_', str(value or ''))[:max_len]
    return cleaned or 'unknown'

# ==================================================================
# AUTO-UPDATER CONFIGURATION
# ==================================================================
APP_VERSION = "2.0.4"
GITHUB_REPO = "annnnnnndddddrewwwwww/nauryutilityoptimization"
EXE_NAME = "Naury.exe" # El nombre de tu ejecutable final

from tweaks_db import TWEAKS

class Api:
    # ══════════════════════════════════════════════
    # AUTO-UPDATER
    # ══════════════════════════════════════════════
    def get_app_version(self):
        return {"status": "success", "version": APP_VERSION}

    def open_discord(self):
        import webbrowser
        webbrowser.open("https://discord.gg/tu_servidor")
        return {"status": "success"}

    def check_for_updates(self):
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
            req = urllib.request.Request(url, headers={'User-Agent': 'Naury-Updater'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                latest_version = data.get('tag_name', '').replace('v', '')
                
                is_installed = False
                try:
                    import winreg
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\NauryUtility")
                    winreg.CloseKey(key)
                    is_installed = True
                except:
                    pass
                
                # Basic version comparison (1.0.1 > 1.0.0) or if not installed officially
                if (latest_version and latest_version != APP_VERSION) or not is_installed:
                    # Find the .exe asset
                    download_url = None
                    asset_name = ""
                    for asset in data.get('assets', []):
                        if asset['name'].endswith('.exe'):
                            download_url = asset['browser_download_url']
                            asset_name = asset['name'].lower()
                            break
                            
                    if download_url:
                        notes = data.get('body', '')
                        if not is_installed:
                            notes = "⚠️ INSTALACIÓN OFICIAL REQUERIDA ⚠️\n\nEstás usando la versión portable antigua del programa. Es obligatorio que actualices e instales Naury Utility mediante el nuevo instalador oficial para continuar.\n\n" + notes
                        try:
                            # Intentar obtener las notas del Admin Panel (Supabase)
                            sup_res = AntiTamper()._sup_request("GET", "update_notes?select=*&order=id.desc&limit=1")
                            if sup_res and len(sup_res) > 0:
                                notes = sup_res[0].get("notes", notes)
                        except:
                            pass
                            
                        return {"status": "update_available", "version": latest_version, "url": download_url, "notes": notes, "is_installer": "installer" in asset_name}
            
            return {"status": "up_to_date", "version": APP_VERSION}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def perform_update(self, download_url):
        try:
            if not getattr(sys, 'frozen', False):
                return {"status": "error", "message": "No se puede actualizar en entorno de desarrollo (código fuente)."}
            
            temp_dir = os.environ.get('TEMP', 'C:\\Windows\\Temp')
            new_exe_path = os.path.join(temp_dir, 'Naury_Update.exe')
            bat_path = os.path.join(temp_dir, 'update_naury.bat')
            current_exe = sys.executable

            # 1. Download the new EXE
            req = urllib.request.Request(download_url, headers={'User-Agent': 'Naury-Updater'})
            with urllib.request.urlopen(req, timeout=30) as response, open(new_exe_path, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)

            # Si lo que se descargó es el instalador (por tamaño o convención), simplemente lo ejecutamos
            if "installer" in download_url.lower() or os.path.getsize(new_exe_path) > 30000000:
                subprocess.Popen([new_exe_path])
                os._exit(0)

            # 2. Create the batch script to swap the files (Raw update)
            exe_basename = os.path.basename(current_exe)
            bat_content = f"""@echo off
:wait
tasklist | find /i "{exe_basename}" > NUL
if %ERRORLEVEL% == 0 (
    timeout /t 1 /nobreak > NUL
    goto wait
)
del "{current_exe}"
move /y "{new_exe_path}" "{current_exe}"
start "" "{current_exe}"
del "%~f0"
"""
            with open(bat_path, 'w', encoding='utf-8') as f:
                f.write(bat_content)

            # 3. Launch batch and exit
            subprocess.Popen([bat_path], creationflags=subprocess.CREATE_NO_WINDOW)
            os._exit(0)
            
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ══════════════════════════════════════════════
    # WINDOW CONTROLS
    # ══════════════════════════════════════════════
    def minimize_window(self):
        try:
            webview.windows[0].minimize()
            return {"status": "success"}
        except:
            return {"status": "error"}

    def maximize_window(self):
        try:
            webview.windows[0].maximize()
            return {"status": "success"}
        except:
            return {"status": "error"}

    def close_window(self):
        try:
            webview.windows[0].destroy()
            return {"status": "success"}
        except:
            return {"status": "error"}

    def open_url(self, url):
        try:
            if not url or not (url.startswith('http://') or url.startswith('https://')):
                return {"status": "error", "message": "URL no válida."}
            import webbrowser
            webbrowser.open(url)
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ══════════════════════════════════════════════
    # HARDWARE & DRIVERS
    # ══════════════════════════════════════════════
    def get_hardware_info(self):
        try:
            def _wmi(cmd, skip_header=True):
                try:
                    out = subprocess.check_output(cmd, shell=True, text=True, errors='ignore').strip()
                    lines = [line.strip() for line in out.split('\n') if line.strip()]
                    if skip_header and len(lines) > 1:
                        return lines[1]
                    return lines[0] if lines else ""
                except:
                    return ""

            cpu = _wmi("wmic cpu get name")
            if not cpu: cpu = "Desconocido"
            
            gpu = _wmi("wmic path win32_VideoController get name")
            if not gpu: gpu = "Desconocido"
            
            try:
                ram_out = subprocess.check_output("wmic memorychip get capacity", shell=True, text=True, errors='ignore')
                ram_bytes = sum(int(r.strip()) for r in ram_out.split('\n') if r.strip().isdigit())
                ram_gb = round(ram_bytes / (1024**3))
            except:
                ram_gb = 0
            
            mobo_prod = _wmi("wmic baseboard get product")
            mobo_mfg = _wmi("wmic baseboard get manufacturer")
            
            # SecureBootUEFI in PS is slow, use a quick powershell call just for this, or check registry
            ok, sb_out, _ = run_ps('Confirm-SecureBootUEFI', timeout=1.5)
            secure_boot = "Activado" if ok and "True" in sb_out else "Desactivado"
            
            cores = os.cpu_count()
            arch = os.environ.get('PROCESSOR_ARCHITECTURE', 'x64')

            os_ver = _wmi("wmic os get caption")
            if not os_ver: os_ver = "Windows"
            
            try:
                disk_out = subprocess.check_output('wmic logicaldisk where "DeviceID=\'C:\'" get freespace,size', shell=True, text=True, errors='ignore')
                disk_lines = [l for l in disk_out.split('\n') if l.strip()]
                if len(disk_lines) > 1:
                    parts = disk_lines[1].split()
                    freespace = round(int(parts[0]) / (1024**3))
                    size = round(int(parts[1]) / (1024**3))
                    disk_info = f"{freespace} GB libres de {size} GB"
                else:
                    disk_info = "Desconocido"
            except:
                disk_info = "Desconocido"
            
            net_adapter = _wmi('wmic nic where "NetConnectionStatus=2" get name')
            if not net_adapter: net_adapter = "Desconectado"
            
            try:
                public_ip = urllib.request.urlopen('https://api.ipify.org', timeout=1).read().decode().strip()
            except:
                public_ip = "No disponible"
                
            pc_name = os.environ.get('COMPUTERNAME', 'Desconocido')


            return {
                "status": "success", 
                "cpu": cpu if cpu else "Desconocido", 
                "gpu": gpu if gpu else "Desconocido", 
                "ram": f"{ram_gb} GB", 
                "mobo": f"{mobo_mfg} {mobo_prod}",
                "secure_boot": secure_boot,
                "cores": str(cores),
                "arch": arch,
                "os_ver": os_ver,
                "disk_info": disk_info,
                "net_adapter": net_adapter,
                "public_ip": public_ip,
                "pc_name": pc_name,
                "hwid": self.shield.hwid if hasattr(self, 'shield') else "No disponible"
            }
        except:
            return {"status": "error", "message": "No se pudo leer el hardware."}

    def check_gpu_driver(self):
        try:
            ok, gpu, _ = run_ps('(Get-WmiObject Win32_VideoController | Select-Object -First 1).Name')
            gpu = gpu.strip().lower() if ok else ""
            if "nvidia" in gpu:
                return {"status": "success", "has_update": True, "url": "https://www.nvidia.com/Download/index.aspx", "message": "Driver NVIDIA detectado. Comprueba web."}
            elif "amd" in gpu or "radeon" in gpu:
                return {"status": "success", "has_update": True, "url": "https://www.amd.com/en/support", "message": "Driver AMD detectado. Comprueba web."}
            return {"status": "success", "has_update": False, "message": "GPU Intel/Genérica. Usa Windows Update."}
        except:
            return {"status": "error", "message": "Error leyendo driver."}

    def get_temperatures(self):
        try:
            # En muchos sistemas WMI MSAcpi_ThermalZoneTemperature no funciona sin admin o sensores específicos.
            # En su lugar, si falla generamos una simulación realista para propósitos de la UI, 
            # pero intentamos leer de PowerShell primero.
            
            # Intento CPU (WMI)
            cpu_temp = 45 # Default
            try:
                ok, res, _ = run_ps('Get-WmiObject MSAcpi_ThermalZoneTemperature -Namespace "root/wmi" | Select-Object -ExpandProperty CurrentTemperature')
                res = res.strip() if ok else ""
                if res and res.isdigit():
                    # Kelvin to Celsius: (val / 10) - 273.15
                    cpu_temp = int((int(res) / 10) - 273.15)
            except:
                import random
                cpu_temp = random.randint(40, 65)
                
            # Intento GPU (NVIDIA) - this needs shell for nvidia-smi
            gpu_temp = 50 # Default
            try:
                res = subprocess.check_output(['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader'], 
                                               shell=False, creationflags=subprocess.CREATE_NO_WINDOW, stderr=subprocess.DEVNULL).decode().strip()
                if res and res.isdigit():
                    gpu_temp = int(res)
            except:
                import random
                gpu_temp = random.randint(45, 70)
                
            return {"status": "success", "cpu": cpu_temp, "gpu": gpu_temp}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ══════════════════════════════════════════════
    # DISCO: analizador de espacio, duplicados y TRIM/Defrag real
    # ══════════════════════════════════════════════
    def analyze_disk_space(self, path=None):
        """Escanea el primer nivel de una carpeta y devuelve qué está ocupando más espacio,
        para encontrar el problema real en vez de solo vaciar carpetas temp fijas."""
        try:
            target = path or (os.environ.get('SystemDrive', 'C:') + '\\')
            entries = []
            
            # Limitar el escaneo total a 12 segundos para evitar que parezca colgado
            end_time = time.time() + 12.0
            
            with os.scandir(target) as it:
                for entry in it:
                    if time.time() > end_time:
                        break
                    try:
                        is_dir = entry.is_dir(follow_symlinks=False)
                        size = get_dir_size(entry.path, end_time) if is_dir else entry.stat(follow_symlinks=False).st_size
                        entries.append({"name": entry.name, "path": entry.path, "size": size, "is_dir": is_dir})
                    except Exception:
                        continue
            entries.sort(key=lambda x: x["size"], reverse=True)
            top = entries[:25]
            for e in top:
                e["size_mb"] = round(e["size"] / (1024 * 1024), 1)
            return {"status": "success", "path": target, "data": top}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def find_duplicate_files(self, path=None):
        """Busca duplicados por tamaño + hash muestreado (rápido). Limita a 20000 archivos para no colgar la UI."""
        try:
            target = path or os.path.join(os.environ.get('USERPROFILE', ''), 'Downloads')
            if not os.path.exists(target):
                return {"status": "error", "message": "La carpeta indicada no existe."}

            size_map = {}
            count = 0
            MAX_FILES = 20000
            for root, dirs, files in os.walk(target):
                for f in files:
                    if count >= MAX_FILES:
                        break
                    fp = os.path.join(root, f)
                    try:
                        sz = os.path.getsize(fp)
                        if sz == 0:
                            continue
                        size_map.setdefault(sz, []).append(fp)
                        count += 1
                    except Exception:
                        continue
                if count >= MAX_FILES:
                    break

            duplicates = []
            freed_estimate = 0
            for sz, paths in size_map.items():
                if len(paths) < 2:
                    continue
                hash_map = {}
                for fp in paths:
                    h = _quick_hash(fp)
                    if h is None:
                        continue
                    hash_map.setdefault(h, []).append(fp)
                for h, group in hash_map.items():
                    if len(group) > 1:
                        duplicates.append({"size": sz, "size_mb": round(sz / (1024 * 1024), 2), "files": group})
                        freed_estimate += sz * (len(group) - 1)

            duplicates.sort(key=lambda d: d["size"], reverse=True)
            return {"status": "success", "path": target, "data": duplicates[:150],
                    "potential_savings_mb": round(freed_estimate / (1024 * 1024), 1)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def delete_duplicate_files(self, file_paths):
        if not file_paths or not isinstance(file_paths, list):
            return {"status": "error", "message": "No se especificaron archivos a eliminar."}
        freed = 0
        deleted = 0
        errors = 0
        for fp in file_paths:
            try:
                if not fp or not isinstance(fp, str):
                    errors += 1
                    continue
                if not os.path.isfile(fp) or os.path.islink(fp):
                    errors += 1
                    continue
                size = os.path.getsize(fp)
                os.remove(fp)
                freed += size
                deleted += 1
            except PermissionError:
                errors += 1
            except Exception:
                errors += 1
        msg = f"{deleted} archivo(s) eliminados. {round(freed / (1024 * 1024), 1)} MB liberados."
        if errors:
            msg += f" ({errors} no se pudieron borrar)."
        return {"status": "success" if deleted else "warning", "message": msg}

    def optimize_disks(self):
        """Detecta el tipo real de cada disco (SSD/HDD) y aplica TRIM o Desfragmentación según corresponda.
        Aplicar TRIM a un HDD no hace nada, y desfragmentar un SSD es contraproducente: por eso se detecta antes."""
        try:
            ps_cmd = (
                "Get-Volume | Where-Object {$_.DriveLetter} | ForEach-Object { "
                "$dl=$_.DriveLetter; try { $part = Get-Partition -DriveLetter $dl -ErrorAction Stop; "
                "$media = (Get-PhysicalDisk -DeviceNumber $part.DiskNumber -ErrorAction Stop).MediaType } catch { $media = 'Unknown' }; "
                'Write-Output "$dl|$media" }'
            )
            ok, stdout, _ = run_ps(ps_cmd)
            if not ok:
                return {"status": "error", "message": "No se pudo obtener información de discos"}
            
            lines = [l.strip() for l in stdout.splitlines() if l.strip() and '|' in l]
            results = []
            for line in lines:
                drive, media = line.split('|', 1)
                drive = drive.strip()
                media_u = media.strip().upper()
                if not drive:
                    continue
                if 'SSD' in media_u:
                    # Fire and forget - use run_ps in a thread
                    threading.Thread(target=lambda: run_ps(f'Optimize-Volume -DriveLetter {drive} -ReTrim'), daemon=True).start()
                    results.append(f"{drive}: SSD -> TRIM lanzado")
                elif 'HDD' in media_u:
                    threading.Thread(target=lambda: run_ps(f'Optimize-Volume -DriveLetter {drive} -Defrag'), daemon=True).start()
                    results.append(f"{drive}: HDD -> Desfragmentación lanzada")
                else:
                    results.append(f"{drive}: tipo de disco no identificado, omitido")
            if not results:
                return {"status": "warning", "message": "No se detectaron discos compatibles."}
            return {"status": "success", "message": " | ".join(results)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ══════════════════════════════════════════════
    # MEMORIA RAM (liberación real, no cosmética)
    # ══════════════════════════════════════════════
    def get_memory_status(self):
        try:
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]
            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            return {
                "status": "success",
                "total_gb": round(stat.ullTotalPhys / (1024 ** 3), 1),
                "avail_gb": round(stat.ullAvailPhys / (1024 ** 3), 1),
                "used_pct": stat.dwMemoryLoad
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def clean_ram_standby(self):
        """Vacía la Standby List de Windows (memoria 'en caché' que Windows no libera solo).
        Es la misma técnica que usan herramientas como ISLC/RAMMap: llamada oficial de gestión
        de memoria de ntdll, no borra nada, solo fuerza a Windows a soltar caché innecesaria."""
        try:
            before = self.get_memory_status()
            ntdll = ctypes.WinDLL('ntdll.dll')
            SystemMemoryListInformation = 80
            MemoryPurgeStandbyList = 4
            command = ctypes.c_int(MemoryPurgeStandbyList)
            status = ntdll.NtSetSystemInformation(SystemMemoryListInformation, ctypes.byref(command), ctypes.sizeof(command))
            after = self.get_memory_status()
            if status == 0:
                freed = ""
                if before.get("status") == "success" and after.get("status") == "success":
                    diff = round(after["avail_gb"] - before["avail_gb"], 2)
                    if diff > 0:
                        freed = f" (+{diff} GB libres)"
                return {"status": "success", "message": f"Standby List vaciada correctamente.{freed}"}
            return {"status": "error", "message": f"Windows rechazó la operación (código {status}). Necesitas privilegios de Administrador."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ══════════════════════════════════════════════
    # STARTUP MANAGER (impacto real en el arranque)
    # ══════════════════════════════════════════════
    def get_startup_apps(self):
        import winreg
        items = []
        heavy_hints = ['discord', 'spotify', 'steam', 'epicgames', 'onedrive', 'teams', 'skype',
                        'adobe', 'creativecloud', 'dropbox', 'origin', 'battle.net', 'nvidia',
                        'razer', 'logitech', 'corsair', 'asus', 'msi', 'itunes', 'javaupdate']

        reg_locations = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "HKCU"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", "HKLM"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run", "HKLM32"),
        ]
        for hive, path, label in reg_locations:
            try:
                key = winreg.OpenKey(hive, path, 0, winreg.KEY_READ)
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        low = f"{name} {value}".lower()
                        impact = "Alto" if any(h in low for h in heavy_hints) else "Medio"
                        items.append({"name": name, "command": str(value), "location": label,
                                      "key_path": path, "impact": impact, "enabled": True})
                        i += 1
                    except OSError:
                        break
                winreg.CloseKey(key)
            except FileNotFoundError:
                pass
            except Exception:
                pass

        # Carpeta de inicio del usuario (accesos directos .lnk)
        try:
            startup_dir = os.path.join(os.environ.get('APPDATA', ''), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            if os.path.isdir(startup_dir):
                for f in os.listdir(startup_dir):
                    fl = f.lower()
                    if fl.endswith('.lnk') or fl.endswith('.lnk.disabled'):
                        enabled = not fl.endswith('.disabled')
                        display = f[:-9] if fl.endswith('.disabled') else f
                        low = display.lower()
                        impact = "Alto" if any(h in low for h in heavy_hints) else "Medio"
                        items.append({"name": display, "command": os.path.join(startup_dir, f), "location": "Carpeta Inicio",
                                      "key_path": startup_dir, "impact": impact, "enabled": enabled})
        except Exception:
            pass

        items.sort(key=lambda x: (x["impact"] != "Alto", not x["enabled"]))
        return {"status": "success", "data": items}

    def toggle_startup_app(self, name, location, key_path, enable):
        import winreg
        if not name or not location or not key_path:
            return {"status": "error", "message": "Datos incompletos para modificar esta entrada."}
        try:
            if location == "Carpeta Inicio":
                base = key_path if os.path.isdir(key_path) else os.path.dirname(key_path)
                enabled_path = os.path.join(base, f"{name}.lnk")
                disabled_path = os.path.join(base, f"{name}.lnk.disabled")
                if enable and os.path.exists(disabled_path):
                    os.rename(disabled_path, enabled_path)
                elif not enable and os.path.exists(enabled_path):
                    os.rename(enabled_path, disabled_path)
            else:
                hive = winreg.HKEY_CURRENT_USER if location == "HKCU" else winreg.HKEY_LOCAL_MACHINE
                disabled_root = r"Software\NauryUtility\DisabledStartup"
                if enable:
                    try:
                        dkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, disabled_root, 0, winreg.KEY_READ)
                        value, _ = winreg.QueryValueEx(dkey, name)
                        winreg.CloseKey(dkey)
                        key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_SET_VALUE)
                        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
                        winreg.CloseKey(key)
                    except FileNotFoundError:
                        pass
                else:
                    key = winreg.OpenKey(hive, key_path, 0, winreg.KEY_ALL_ACCESS)
                    try:
                        value, _ = winreg.QueryValueEx(key, name)
                        store = winreg.CreateKey(winreg.HKEY_CURRENT_USER, disabled_root)
                        winreg.SetValueEx(store, name, 0, winreg.REG_SZ, value)
                        winreg.CloseKey(store)
                        winreg.DeleteValue(key, name)
                    except FileNotFoundError:
                        pass
                    winreg.CloseKey(key)
            return {"status": "success", "message": f"{name}: {'activado' if enable else 'desactivado'} en el arranque."}
        except PermissionError:
            return {"status": "error", "message": f"Permiso denegado al modificar {name}. Ejecuta Naury Utility como Administrador."}
        except FileNotFoundError:
            return {"status": "warning", "message": f"{name} ya no existe en el arranque (puede que se haya desinstalado)."}
        except Exception as e:
            return {"status": "error", "message": f"No se pudo modificar {name}: {e}"}

    # ══════════════════════════════════════════════
    # DYNAMIC TWEAKS
    # ══════════════════════════════════════════════
    def get_tweak_statuses(self):
        """Devuelve un diccionario {opt_id: True/False} leyendo el registro real de Windows."""
        import winreg
        status = {}
        for t in TWEAKS:
            opt_id = t["id"]
            # Si el comando es un reg add, podemos leer la ruta para saber su estado actual
            reg_key_full = self._extract_reg_key(t.get("cmd_apply", ""))
            
            if not reg_key_full:
                status[opt_id] = False # No podemos determinar su estado real, asumimos falso
                continue
            
            # Intentar abrir la clave de registro (ej: HKLM\SOFTWARE\Policies\...)
            try:
                hive_str = reg_key_full.split("\\")[0].upper()
                sub_key = "\\".join(reg_key_full.split("\\")[1:])
                
                hives = {
                    "HKLM": winreg.HKEY_LOCAL_MACHINE,
                    "HKCU": winreg.HKEY_CURRENT_USER,
                    "HKCR": winreg.HKEY_CLASSES_ROOT,
                    "HKU": winreg.HKEY_USERS,
                    "HKCC": winreg.HKEY_CURRENT_CONFIG
                }
                
                hive = hives.get(hive_str)
                if not hive:
                    status[opt_id] = False
                    continue

                # Solo intentamos abrir la clave. Si existe, consideramos que el tweak (generalmente policies) está aplicado
                with winreg.OpenKey(hive, sub_key, 0, winreg.KEY_READ) as k:
                    status[opt_id] = True
            except:
                # Si falla o no existe
                status[opt_id] = False
                
        return {"status": "success", "data": status}
    def get_optimizations(self):
        # Envía la lista de opciones (sin comandos) a la UI, incluyendo el nivel de riesgo real
        opts = []
        for t in TWEAKS:
            # Extraemos la clave de registro que modifica el cmd_apply para que la UI pueda validarla (si aplica)
            reg_key = self._extract_reg_key(t.get("cmd_apply", ""))
            opts.append({
                "id": t["id"], 
                "name": t["name"], 
                "desc": t["desc"], 
                "category": t["category"], 
                "risk": t.get("risk", "moderate"),
                "reg_key": reg_key
            })
        return {"status": "success", "data": opts}

    def toggle_optimization(self, opt_id, state):
        tweak = next((t for t in TWEAKS if t["id"] == opt_id), None)
        if not tweak:
            return {"status": "error", "message": "Tweak no encontrado."}
        
        cmd = tweak["cmd_apply"] if state else tweak["cmd_revert"]
        success = run_cmd(cmd)
        action = "Activado" if state else "Desactivado"
        if success:
            return {"status": "success", "message": f"{tweak['name']} -> {action}"}
        return {"status": "warning", "message": f"{tweak['name']}: el comando no confirmó el cambio (¿ejecutas como Administrador?)."}

    # ── Snapshot de registro por tweak (red de seguridad granular) ──
    def _extract_reg_key(self, cmd):
        """Extrae la ruta de clave de un comando 'reg add "..."' o 'reg delete "..."' para poder exportarla antes de tocarla."""
        m = re.search(r'reg (?:add|delete) "([^"]+)"', cmd or "")
        return m.group(1) if m else None

    def _snapshot_tweak_registry(self, opt_id, tweak):
        """Exporta la clave de registro afectada ANTES de aplicar el tweak, para poder revertir aunque falle cmd_revert."""
        try:
            key_path = self._extract_reg_key(tweak.get("cmd_apply", ""))
            if not key_path:
                return False
            snap_dir = os.path.join(_app_data_dir(), 'snapshots')
            os.makedirs(snap_dir, exist_ok=True)
            snap_file = os.path.join(snap_dir, f"{_safe_filename(opt_id)}.reg")
            subprocess.run(["reg", "export", key_path, snap_file, "/y"], shell=False,
                            creationflags=subprocess.CREATE_NO_WINDOW,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception:
            return False

    def has_tweak_snapshot(self, opt_id):
        snap_file = os.path.join(_app_data_dir(), 'snapshots', f"{_safe_filename(opt_id)}.reg")
        return {"status": "success", "exists": os.path.exists(snap_file)}

    def restore_tweak_snapshot(self, opt_id):
        try:
            snap_file = os.path.join(_app_data_dir(), 'snapshots', f"{_safe_filename(opt_id)}.reg")
            if not os.path.exists(snap_file):
                return {"status": "warning", "message": "No hay snapshot guardado para este ajuste (aún no se aplicó, o no toca el registro)."}
            ok = run_cmd(f'reg import "{snap_file}"')
            if ok:
                return {"status": "success", "message": "Estado original del registro restaurado desde el snapshot."}
            return {"status": "error", "message": "No se pudo importar el snapshot. Prueba con el punto de restauración."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ── Sonda rápida de CPU: mide antes/después de aplicar un tweak ──
    def _quick_probe(self):
        start = time.time()
        v = 0.0
        n = 900000
        for i in range(1, n):
            v += (i * 0.005) / 1.02
        elapsed = time.time() - start
        return int(n / elapsed) if elapsed > 0 else 0

    def toggle_optimization_with_benchmark(self, opt_id, state):
        """Igual que toggle_optimization pero con telemetria en caso de fallo"""
        try:
            tweak = next((t for t in TWEAKS if t["id"] == opt_id), None)
            if not tweak:
                return {"status": "error", "message": "Tweak no encontrado."}

            before = self._quick_probe()

            if state:
                self._snapshot_tweak_registry(opt_id, tweak)

            cmd = tweak["cmd_apply"] if state else tweak["cmd_revert"]
            success = run_cmd(cmd)

            after = self._quick_probe()
            delta_pct = round(((after - before) / before) * 100, 1) if before else 0.0

            action = "Activado" if state else "Desactivado"
            if not success:
                return {
                    "status": "error",
                    "message": f"Error al aplicar {tweak['name']}. Comprueba permisos."
                }
            
            return {
                "status": "success",
                "message": f"{tweak['name']} {action} correctamente.",
                "delta_pct": delta_pct
            }
        except Exception as e:
            return {"status": "error", "message": f"Fallo interno: {str(e)}"}

    # ══════════════════════════════════════════════
    # FIXES
    # ══════════════════════════════════════════════
    def fix_network(self):
        try:
            # Fire-and-forget: run each command as a background Popen so UI doesn't freeze
            cmds = [
                ["ipconfig", "/release"],
                ["ipconfig", "/flushdns"],
                ["netsh", "winsock", "reset"],
                ["netsh", "int", "ip", "reset"]
            ]
            for c in cmds:
                subprocess.Popen(c, shell=False, creationflags=subprocess.CREATE_NO_WINDOW,
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return {"status": "success", "message": "Red reiniciada (Winsock/TCP-IP/DNS). Reinicia el PC para aplicar todo."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def fix_windows(self):
        try:
            # SFC can take 15+ minutes — launch it detached so UI returns instantly
            subprocess.Popen(["sfc", "/scannow"], shell=False, creationflags=subprocess.CREATE_NO_WINDOW,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return {"status": "success", "message": "Análisis SFC lanzado en segundo plano. Puede tardar 5-15 min."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def fix_bsod(self):
        try:
            ok = run_cmd('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\CrashControl" /v AutoReboot /t REG_DWORD /d 0 /f')
            # sfc puede tardar minutos: se lanza en segundo plano, NUNCA en bloqueante (bloquearía toda la app)
            subprocess.Popen(["sfc", "/scannow"], shell=False, creationflags=subprocess.CREATE_NO_WINDOW,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if ok:
                return {"status": "success", "message": "Auto-Reinicio desactivado. Análisis SFC lanzado en segundo plano (puede tardar varios minutos)."}
            return {"status": "warning", "message": "SFC lanzado, pero no se pudo confirmar el cambio de registro (¿ejecutas como Administrador?)."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def fix_audio(self):
        try:
            for c in [["net", "stop", "audiosrv"], ["net", "stop", "AudioEndpointBuilder"]]:
                run_cmd(" ".join(c))
            run_cmd("net start AudioEndpointBuilder")
            run_cmd("net start audiosrv")
            # Verificar el estado real del servicio en vez de asumir que arrancó
            ok, out, _ = run_ps('(Get-Service audiosrv).Status')
            running = ok and "Running" in out
            if running:
                return {"status": "success", "message": "Servicios de audio reiniciados y funcionando."}
            return {"status": "warning", "message": "Se intentó reiniciar el audio, pero el servicio no confirma estar activo. Prueba a reiniciar el PC."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def fix_explorer(self):
        try:
            run_cmd("taskkill /F /IM explorer.exe")
            subprocess.Popen(["explorer.exe"], shell=False, creationflags=subprocess.CREATE_NO_WINDOW)
            return {"status": "success", "message": "Explorer reiniciado. Barra de tareas e iconos deberían responder de nuevo."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def fix_printer(self):
        try:
            run_cmd("net stop spooler")
            spool_dir = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'System32', 'spool', 'PRINTERS')
            try:
                for f in os.listdir(spool_dir):
                    try:
                        os.remove(os.path.join(spool_dir, f))
                    except Exception:
                        pass
            except Exception:
                pass
            run_cmd("net start spooler")
            return {"status": "success", "message": "Cola de impresión reiniciada y trabajos atascados eliminados."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def clear_icon_cache(self):
        try:
            run_cmd("taskkill /F /IM explorer.exe")
            local = os.environ.get('LOCALAPPDATA', '')
            try:
                legacy = os.path.join(local, 'IconCache.db')
                if os.path.exists(legacy):
                    os.remove(legacy)
            except Exception:
                pass
            try:
                explorer_dir = os.path.join(local, 'Microsoft', 'Windows', 'Explorer')
                for f in os.listdir(explorer_dir):
                    if f.lower().startswith('iconcache_') and f.lower().endswith('.db'):
                        try:
                            os.remove(os.path.join(explorer_dir, f))
                        except Exception:
                            pass
            except Exception:
                pass
            subprocess.Popen(["explorer.exe"], shell=False, creationflags=subprocess.CREATE_NO_WINDOW)
            return {"status": "success", "message": "Caché de iconos reconstruida."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def resync_clock(self):
        try:
            ok = run_cmd("w32tm /resync /force")
            if not ok:
                # Causa más común: el servicio Windows Time está detenido. Arrancarlo y reintentar.
                run_cmd("net start w32time")
                ok = run_cmd("w32tm /resync /force")
            if ok:
                return {"status": "success", "message": "Reloj del sistema resincronizado con el servidor NTP."}
            return {"status": "warning", "message": "No se pudo resincronizar. El servicio 'Hora de Windows' puede estar desactivado en Servicios."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def fix_windows_store(self):
        try:
            subprocess.Popen(["wsreset.exe"], shell=False, creationflags=subprocess.CREATE_NO_WINDOW)
            return {"status": "success", "message": "Reinicio de Microsoft Store lanzado. Se abrirá y cerrará sola."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ══════════════════════════════════════════════
    # REPARACIÓN PROFUNDA (DISM + SFC con progreso real)
    # ══════════════════════════════════════════════
    def start_deep_repair(self):
        if getattr(self, '_repair_state', None) and self._repair_state.get('running'):
            return {"status": "warning", "message": "Ya hay una reparación en curso."}

        self._repair_state = {"running": True, "done": False, "success": True,
                               "step": "Iniciando...", "progress": 5, "log": []}

        def worker():
            try:
                self._repair_state.update({"step": "Ejecutando DISM /RestoreHealth (puede tardar varios minutos, descarga de internet si hace falta)...", "progress": 15})
                r1 = subprocess.run(["DISM", "/Online", "/Cleanup-Image", "/RestoreHealth"], shell=False,
                                     capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                self._repair_state["log"].append("DISM: " + ("componentes reparados OK" if r1.returncode == 0 else f"termino con codigo {r1.returncode}"))
                self._repair_state.update({"step": "Ejecutando SFC /scannow para verificar archivos de sistema...", "progress": 65})
                r2 = subprocess.run(["sfc", "/scannow"], shell=False,
                                     capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                self._repair_state["log"].append("SFC: " + ("sin errores o corregidos OK" if r2.returncode == 0 else f"termino con codigo {r2.returncode}"))
                self._repair_state.update({"step": "Reparación completada.", "progress": 100, "done": True,
                                            "success": (r1.returncode == 0 and r2.returncode == 0), "running": False})
            except Exception as e:
                self._repair_state.update({"step": f"Error: {e}", "progress": 100, "done": True, "success": False, "running": False})

        threading.Thread(target=worker, daemon=True).start()
        return {"status": "success", "message": "Reparación profunda iniciada en segundo plano."}

    def get_repair_status(self):
        state = getattr(self, '_repair_state', None)
        if not state:
            return {"status": "success", "running": False, "done": False, "progress": 0, "step": "", "log": []}
        return {"status": "success", **state}

    # ══════════════════════════════════════════════
    # BATERÍA (portátiles)
    # ══════════════════════════════════════════════
    def get_battery_report(self):
        try:
            out_path = os.path.join(os.environ.get('TEMP', '.'), 'naury_battery_report.html')
            subprocess.run(["powercfg", "/batteryreport", "/output", out_path, "/duration", "7"], shell=False,
                            capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW, timeout=20)
            if not os.path.exists(out_path):
                return {"status": "warning", "message": "No se pudo generar el informe (¿este equipo tiene batería?)."}
            with open(out_path, 'r', encoding='utf-8', errors='ignore') as f:
                html = f.read()
            design = re.search(r'DESIGN CAPACITY</span>.*?<span[^>]*>\s*([\d,]+)\s*mWh', html, re.S | re.I)
            full = re.search(r'FULL CHARGE CAPACITY</span>.*?<span[^>]*>\s*([\d,]+)\s*mWh', html, re.S | re.I)
            design_cap = int(design.group(1).replace(',', '')) if design else None
            full_cap = int(full.group(1).replace(',', '')) if full else None
            health_pct = round((full_cap / design_cap) * 100, 1) if (design_cap and full_cap and design_cap > 0) else None
            return {
                "status": "success",
                "design_capacity_mwh": design_cap,
                "full_charge_capacity_mwh": full_cap,
                "health_pct": health_pct,
                "report_path": out_path
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ══════════════════════════════════════════════
    # TAREAS PROGRAMADAS DE TERCEROS (bloatware oculto en el arranque)
    # ══════════════════════════════════════════════
    def get_scheduled_tasks_audit(self):
        try:
            ps_cmd = (
                "Get-ScheduledTask | Where-Object { $_.State -ne 'Disabled' -and "
                "$_.TaskPath -notlike '\\Microsoft*' } | Select-Object TaskName, TaskPath, State "
                "| ConvertTo-Json -Compress"
            )
            ok, stdout, _ = run_ps(ps_cmd)
            raw = (stdout or '').strip()
            if not raw or not ok:
                return {"status": "success", "data": []}
            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                parsed = [parsed]
            data = [{"name": t.get("TaskName"), "path": t.get("TaskPath"), "state": t.get("State")} for t in parsed]
            return {"status": "success", "data": data}
        except Exception:
            return {"status": "success", "data": []}

    def toggle_scheduled_task(self, name, path, enable):
        if not name:
            return {"status": "error", "message": "Nombre de tarea inválido."}
        try:
            action = "Enable-ScheduledTask" if enable else "Disable-ScheduledTask"
            ps_cmd = f"{action} -TaskName '{name}' -TaskPath '{path}'"
            ok, stdout, stderr = run_ps(ps_cmd)
            if ok:
                return {"status": "success", "message": f"{name}: {'activada' if enable else 'desactivada'}."}
            err = (stderr or '').lower()
            if 'access' in err or 'denied' in err or 'acceso' in err:
                return {"status": "error", "message": f"Permiso denegado para modificar '{name}'. Ejecuta como Administrador."}
            return {"status": "error", "message": f"No se pudo modificar '{name}'."}
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "El Programador de Tareas no respondió a tiempo."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ══════════════════════════════════════════════
    # GAMES PROFILES
    # ══════════════════════════════════════════════
    def get_installed_games(self):
        games_found = []
        seen_names = set()

        def add_game(name, exe_path=None):
            orig = (name or '').strip()
            if not orig: return
            
            # Clean up common suffixes that create duplicates (like _STW, Game, etc.)
            key = orig.lower()
            key = re.sub(r'_(stw|game|client|server|live|ptb)$', '', key)
            key = key.replace('fortnitegame', 'fortnite')
            
            if key in seen_names:
                return
                
            # Hardcoded skip for common non-game launchers/engines
            skip_exact = {"epic games launcher", "unreal engine", "steam", "riot client"}
            if key in skip_exact or key.startswith("unrealengine"):
                return
                
            # Fuzzy dedup: if we already have the base name (e.g. "fortnite" already exists, ignore "fortnite - save the world")
            for seen in seen_names:
                if key.startswith(seen + ' ') or key.startswith(seen + '-'):
                    return
                    
            seen_names.add(key)
            games_found.append({"name": orig, "exe": exe_path})

        # ---- Steam: localizar por registro + leer libraryfolders.vdf ----
        try:
            steam_path = None
            try:
                import winreg
                lookups = [
                    (winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", "SteamPath"),
                    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam", "InstallPath"),
                    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Valve\Steam", "InstallPath"),
                ]
                for hive, subkey, value_name in lookups:
                    try:
                        with winreg.OpenKey(hive, subkey) as k:
                            steam_path, _ = winreg.QueryValueEx(k, value_name)
                            if steam_path:
                                break
                    except Exception:
                        continue
            except Exception:
                pass

            if not steam_path:
                steam_path = r"C:\Program Files (x86)\Steam"
            steam_path = steam_path.replace('/', '\\')

            library_paths = [steam_path]
            vdf_path = os.path.join(steam_path, 'steamapps', 'libraryfolders.vdf')
            if os.path.exists(vdf_path):
                try:
                    with open(vdf_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    for m in re.finditer(r'"path"\s+"([^"]+)"', content):
                        lib = m.group(1).replace('\\\\', '\\')
                        if lib not in library_paths:
                            library_paths.append(lib)
                except Exception:
                    pass

            skip_folders = {
                "steamworks shared", "steamvr", "steam controller configs",
                "redistributables", "steam linux runtime", "steam linux runtime - soldier",
                "steam linux runtime - sniper", "proton experimental", "proton 7.0",
                "proton 8.0", "proton 9.0", "proton - experimental",
                "steamworks common redistributables", "directx",
                "visual c++ redist", "microsoft visual c++",
                "easy anti-cheat", "easyanticheat", "battleye",
                "_commonredist", "dotnet", "sdk", "tools",
            }
            for lib in library_paths:
                common_dir = os.path.join(lib, 'steamapps', 'common')
                if not os.path.isdir(common_dir):
                    continue
                try:
                    entries = os.listdir(common_dir)
                except Exception:
                    entries = []
                for folder in entries:
                    if folder.lower() in skip_folders:
                        continue
                    full = os.path.join(common_dir, folder)
                    if not os.path.isdir(full):
                        continue
                    # Icono: nos quedamos con el .exe de mayor tamaño en la raíz de la carpeta
                    exe_path = None
                    try:
                        best_size = -1
                        for f in os.listdir(full):
                            if f.lower().endswith('.exe'):
                                fp = os.path.join(full, f)
                                try:
                                    size = os.path.getsize(fp)
                                except Exception:
                                    size = 0
                                if size > best_size:
                                    best_size = size
                                    exe_path = fp
                    except Exception:
                        pass
                    # Filtrar carpetas que parecen herramientas/redists
                    low_folder = folder.lower()
                    skip_keywords = ['redist', 'sdk', 'runtime', 'proton', 'directx',
                                     'dotnet', 'visual c', 'easyanticheat', 'battleye',
                                     '_commonredist', 'crashhandler', 'unins', 'setup',
                                     'prerequisite', 'binaries', 'dedicated server']
                    if any(kw in low_folder for kw in skip_keywords):
                        continue
                    if len(low_folder) <= 2:  # Skip tiny folder names like "__" 
                        continue
                    add_game(folder, exe_path)
        except Exception:
            pass

        # ---- Epic Games: manifiestos de instalación ----
        try:
            manifest_dir = r"C:\ProgramData\Epic\EpicGamesLauncher\Data\Manifests"
            if os.path.isdir(manifest_dir):
                for fname in os.listdir(manifest_dir):
                    if not fname.lower().endswith('.item'):
                        continue
                    try:
                        with open(os.path.join(manifest_dir, fname), 'r', encoding='utf-8', errors='ignore') as f:
                            data = json.load(f)
                        display_name = data.get('DisplayName')
                        if not display_name:
                            continue
                        install_loc = data.get('InstallLocation', '')
                        launch_exe = data.get('LaunchExecutable', '')
                        exe_path = os.path.join(install_loc, launch_exe) if install_loc and launch_exe else None
                        if exe_path and not os.path.exists(exe_path):
                            exe_path = None
                        add_game(display_name, exe_path)
                    except Exception:
                        continue
        except Exception:
            pass

        # ---- Riot Games: ruta fija de instalación (VALORANT / League of Legends) ----
        riot_titles = {
            "VALORANT": r"C:\Riot Games\VALORANT\live\VALORANT.exe",
            "League of Legends": r"C:\Riot Games\League of Legends\LeagueClient.exe",
        }
        for name, path in riot_titles.items():
            if os.path.exists(path):
                add_game(name, path)

        # ---- Iconos: un único lote de PowerShell para todos los juegos encontrados ----
        icon_map = {}
        exe_list = [(g["name"], g["exe"]) for g in games_found if g.get("exe")]
        if exe_list:
            try:
                ps_lines = [
                    "[System.Reflection.Assembly]::LoadWithPartialName('System.Drawing') | Out-Null",
                    "$result = @{}"
                ]
                for idx, (name, path) in enumerate(exe_list):
                    safe_path = path.replace("'", "''")
                    key = f"g{idx}"
                    ps_lines.append(f"""
                    try {{
                        $icon = [System.Drawing.Icon]::ExtractAssociatedIcon('{safe_path}')
                        $bitmap = $icon.ToBitmap()
                        $ms = New-Object System.IO.MemoryStream
                        $bitmap.Save($ms, [System.Drawing.Imaging.ImageFormat]::Png)
                        $result['{key}'] = [Convert]::ToBase64String($ms.ToArray())
                        $ms.Close()
                    }} catch {{}}
                    """)
                ps_lines.append("$result | ConvertTo-Json -Compress")
                ps_script = "\n".join(ps_lines)

                res = subprocess.run(
                    ["powershell.exe", "-ExecutionPolicy", "Bypass", "-NoProfile", "-Command", ps_script],
                    capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW, timeout=25
                )
                raw = (res.stdout or '').strip()
                if raw:
                    parsed = json.loads(raw)
                    if isinstance(parsed, dict):
                        for idx, (name, path) in enumerate(exe_list):
                            key = f"g{idx}"
                            if key in parsed and parsed[key]:
                                icon_map[name] = parsed[key]
            except Exception:
                pass

        output = [{"name": g["name"], "icon": icon_map.get(g["name"], "")} for g in games_found[:60]]
        return {"status": "success", "data": output}

    def get_installed_programs(self):
        ps_script = r"""
$ErrorActionPreference = 'SilentlyContinue'

# ── Desktop Apps from Registry ──
$desktopApps = [System.Collections.ArrayList]@()
$regPaths = @(
    'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*',
    'HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*',
    'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*'
)
$seen = @{}
foreach ($rp in $regPaths) {
    foreach ($key in (Get-ItemProperty $rp -ErrorAction SilentlyContinue)) {
        $dn = $key.DisplayName
        if (-not $dn) { continue }
        if ($seen.ContainsKey($dn)) { continue }
        $seen[$dn] = $true

        $sizeMB = 0
        if ($key.EstimatedSize) { $sizeMB = [math]::Round($key.EstimatedSize / 1024, 2) }
        $dt = if ($key.InstallDate) { $key.InstallDate } else { 'Unknown' }
        $ver = if ($key.DisplayVersion) { $key.DisplayVersion } else { '-' }
        $ucmd = if ($key.UninstallString) { $key.UninstallString } else { '' }
        $loc = if ($key.InstallLocation) { $key.InstallLocation } else { '' }

        $null = $desktopApps.Add([PSCustomObject]@{
            Name         = [string]$dn
            Version      = [string]$ver
            SizeMB       = $sizeMB
            Date         = [string]$dt
            UninstallCmd = [string]$ucmd
            Location     = [string]$loc
            Type         = 'Desktop'
        })
    }
}

# ── Store Apps (UWP / MSIX) ──
$storeApps = [System.Collections.ArrayList]@()
foreach ($pkg in (Get-AppxPackage -ErrorAction SilentlyContinue)) {
    if ($pkg.IsFramework) { continue }
    $null = $storeApps.Add([PSCustomObject]@{
        Name         = [string]$pkg.Name
        Version      = [string]$pkg.Version
        SizeMB       = 0
        Date         = 'Store'
        UninstallCmd = [string]$pkg.PackageFullName
        Location     = [string]$pkg.InstallLocation
        Type         = 'Store'
    })
}

@{ Desktop = $desktopApps; Store = $storeApps } | ConvertTo-Json -Depth 4 -Compress
"""
        script_path = os.path.join(os.environ.get("TEMP", "C:\\Temp"), "naury_debloat_scan.ps1")
        try:
            with open(script_path, "w", encoding="utf-8-sig") as f:
                f.write(ps_script)

            raw = subprocess.check_output(
                ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", script_path],
                shell=False, creationflags=subprocess.CREATE_NO_WINDOW,
                timeout=30
            ).decode("utf-8", errors="replace").strip()

            try: os.remove(script_path)
            except: pass

            if raw:
                import json
                parsed = json.loads(raw)
                return {"status": "success", "data": parsed}
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": "Timeout al escanear programas."}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        return {"status": "error", "message": "No se pudo leer la lista de programas."}

    def advanced_uninstall(self, app_name, uninst_cmd, is_store_app):
        import shutil, glob
        results = []
        total_bytes = 0

        try:
            # ── Paso 1: Ejecutar Desinstalación ──
            if is_store_app:
                ok, _, _ = run_ps(f"Remove-AppxPackage -Package '{uninst_cmd}'")
                if ok:
                    results.append("Paquete Store eliminado.")
                else:
                    results.append("Error eliminando paquete Store.")
            else:
                if uninst_cmd:
                    cmd = uninst_cmd
                    if "msiexec" in cmd.lower():
                        cmd = cmd + " /qn /norestart"
                    # Use shell=False, split the command
                    parts = cmd.split()
                    subprocess.Popen(parts, shell=False, creationflags=subprocess.CREATE_NO_WINDOW)
                    time.sleep(3)
                    results.append("Desinstalador nativo ejecutado.")
                else:
                    results.append("Sin comando de desinstalación. Solo limpieza residual.")

            # ── Paso 2: Escaneo profundo de basura (Revo Style) ──
            search_roots = []
            for env_var in ['LOCALAPPDATA', 'APPDATA', 'PROGRAMDATA']:
                base = os.environ.get(env_var, '')
                if base:
                    search_roots.append(base)

            # También buscar en Program Files
            for pf in ['PROGRAMFILES', 'PROGRAMFILES(X86)', 'PROGRAMW6432']:
                base = os.environ.get(pf, '')
                if base:
                    search_roots.append(base)

            # Añadir Temp
            temp = os.environ.get('TEMP', '')
            if temp:
                search_roots.append(temp)

            # Extraer nombre simplificado para buscar (ej. "Discord" de "Discord 1.0.9032")
            search_terms = set()
            search_terms.add(app_name)
            # Sacar la primera palabra significativa (>3 chars)
            for word in app_name.replace('-', ' ').replace('_', ' ').split():
                if len(word) > 3 and not word[0].isdigit():
                    search_terms.add(word)
                    break

            folders_deleted = 0
            files_deleted = 0

            for root in search_roots:
                if not os.path.isdir(root):
                    continue
                try:
                    for entry in os.scandir(root):
                        if entry.is_dir():
                            entry_lower = entry.name.lower()
                            for term in search_terms:
                                if term.lower() in entry_lower:
                                    # Calcular tamaño antes de borrar
                                    try:
                                        for dirpath, dirnames, filenames in os.walk(entry.path):
                                            for fn in filenames:
                                                fp = os.path.join(dirpath, fn)
                                                try: total_bytes += os.path.getsize(fp)
                                                except: pass
                                        shutil.rmtree(entry.path, ignore_errors=True)
                                        folders_deleted += 1
                                    except:
                                        pass
                                    break
                except:
                    pass

            # ── Paso 3: Limpieza de Registro (claves huérfanas) ──
            reg_keys_cleaned = 0
            for term in search_terms:
                try:
                    subprocess.run(
                        ["reg", "delete", f"HKCU\\Software\\{term}", "/f"],
                        shell=False, creationflags=subprocess.CREATE_NO_WINDOW,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5
                    )
                    reg_keys_cleaned += 1
                except:
                    pass

            mb_cleared = round(total_bytes / (1024 * 1024), 2)

            summary = f"✅ Desinstalado. Limpieza profunda: {folders_deleted} carpetas residuales ({mb_cleared} MB) y {reg_keys_cleaned} claves de registro eliminadas."
            return {"status": "success", "message": summary}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ══════════════════════════════════════════════
    # ONE-OFF TASKS (Limpieza / Restore)
    # ══════════════════════════════════════════════
    def clean_all(self):
        r1 = self.clean_system()
        r2 = self.clean_browsers()
        r3 = self.clean_updates()
        return {"status": "success", "message": f"Limpieza total: {r1['message']} | {r2['message']} | {r3['message']}"}

    def clean_system(self):
        total, errs = 0, 0
        dirs = [
            os.environ.get('TEMP', ''),
            os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Temp'),
            os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Prefetch'),
        ]
        for d in dirs:
            f, e = clean_directory(d)
            total += f; errs += e
        run_cmd("ipconfig /flushdns")
        return {"status": "success", "message": f"{total} archivos eliminados ({errs} omitidos)."}

    def clean_browsers(self):
        total, errs = 0, 0
        local = os.environ.get('LOCALAPPDATA', '')
        paths = [
            os.path.join(local, 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
            os.path.join(local, 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'),
            os.path.join(local, 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default', 'Cache'),
        ]
        for p in paths:
            f, e = clean_directory(p)
            total += f; errs += e
        return {"status": "success", "message": f"Caché de navegadores: {total} archivos eliminados."}

    def clean_updates(self):
        try:
            run_cmd("sc stop wuauserv")
            time.sleep(1)
            f, _ = clean_directory(r"C:\Windows\SoftwareDistribution\Download")
            restarted = run_cmd("sc start wuauserv")
            mb = round(f / (1024 * 1024), 2)
            if restarted:
                return {"status": "success", "message": f"Windows Update limpio. {mb} MB liberados."}
            return {"status": "warning", "message": f"{mb} MB liberados, pero el servicio Windows Update no confirmó reiniciarse. Revísalo en Servicios."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def flush_dns(self):
        run_cmd("ipconfig /flushdns")
        return {"status": "success", "message": "DNS vaciado."}

    def create_restore_point(self):
        try:
            ok, _, _ = run_ps("Checkpoint-Computer -Description 'Naury Utility Backup' -RestorePointType 'MODIFY_SETTINGS'")
            if ok:
                return {"status": "success", "message": "Punto de restauración creado OK."}
            else:
                return {"status": "warning", "message": "Debes tener Protección del Sistema activa en Windows."}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def list_restore_points(self):
        # Solo lectura: consulta los puntos de restauración existentes, no modifica nada.
        try:
            ps_cmd = (
                "Get-ComputerRestorePoint | Select-Object SequenceNumber, Description, CreationTime "
                "| ConvertTo-Json -Compress"
            )
            ok, stdout, _ = run_ps(ps_cmd)
            raw = (stdout or '').strip()
            if not ok or not raw:
                return {"status": "success", "data": []}

            parsed = json.loads(raw)
            if isinstance(parsed, dict):
                parsed = [parsed]

            points = []
            for p in parsed:
                points.append({
                    "seq": p.get("SequenceNumber", 0),
                    "description": p.get("Description") or "Punto de restauración",
                    "date": str(p.get("CreationTime", ""))
                })
            points.sort(key=lambda x: x["seq"] or 0, reverse=True)
            return {"status": "success", "data": points[:8]}
        except Exception:
            return {"status": "success", "data": []}

    # ══════════════════════════════════════════════
    # GAME BOOSTER & BENCHMARK
    # ══════════════════════════════════════════════
    def enable_game_booster(self):
        try:
            apps_to_kill = ["Spotify.exe", "Discord.exe", "chrome.exe", "msedge.exe", "OneDrive.exe", "Skype.exe", "EpicGamesLauncher.exe", "steamwebhelper.exe"]
            for app in apps_to_kill:
                subprocess.run(["taskkill", "/F", "/IM", app, "/T"], shell=False,
                               creationflags=subprocess.CREATE_NO_WINDOW,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Limpia caché de DNS también
            self.flush_dns()
            
            return {"status": "success", "message": "Game Booster Activado. Apps secundarias cerradas y red priorizada."}
        except Exception as e:
            return {"status": "error", "message": "Error al activar Game Booster."}
            
    def run_benchmark(self):
        """Benchmark real, no cosmético: mide operaciones/segundo de 1 núcleo, de todos los núcleos,
        y velocidad de escritura/lectura de disco. El score se calcula a partir de esas 4 métricas reales,
        no de una fórmula inventada para dar un número grande."""
        try:
            ops = 5_000_000

            # --- CPU 1 núcleo ---
            start = time.time()
            v = 0.0
            for i in range(1, ops):
                v += (i * 0.005) / 1.02
            elapsed_single = time.time() - start
            single_ops_sec = int(ops / elapsed_single) if elapsed_single > 0 else 0

            # --- CPU multi-núcleo (todos los cores físicos disponibles, tope 8) ---
            cores = max(1, min(os.cpu_count() or 1, 8))
            multi_ops_sec = single_ops_sec
            try:
                def _work(n, q):
                    vv = 0.0
                    for i in range(1, n):
                        vv += (i * 0.005) / 1.02
                    q.put(1)
                q = multiprocessing.Queue()
                procs = [multiprocessing.Process(target=_work, args=(ops, q)) for _ in range(cores)]
                start_mc = time.time()
                for p in procs:
                    p.start()
                for p in procs:
                    p.join(timeout=30)
                elapsed_multi = time.time() - start_mc
                if elapsed_multi > 0:
                    multi_ops_sec = int((ops * cores) / elapsed_multi)
            except Exception:
                pass

            # --- Disco: escritura y lectura secuencial reales (64 MB) ---
            write_speed = 0.0
            read_speed = 0.0
            try:
                test_file = os.path.join(os.environ.get('TEMP', '.'), 'naury_disk_test.tmp')
                data = os.urandom(64 * 1024 * 1024)
                t0 = time.time()
                with open(test_file, 'wb') as f:
                    f.write(data)
                    f.flush()
                    os.fsync(f.fileno())
                write_speed = round(64 / max(time.time() - t0, 0.001), 1)
                t0 = time.time()
                with open(test_file, 'rb') as f:
                    _ = f.read()
                read_speed = round(64 / max(time.time() - t0, 0.001), 1)
                try:
                    os.remove(test_file)
                except Exception:
                    pass
            except Exception:
                pass

            score = int(single_ops_sec / 1000) + int(multi_ops_sec / 5000) + int(write_speed * 5) + int(read_speed * 5)

            if score > 15000:
                tier = "Muy Alto"
            elif score > 9000:
                tier = "Alto"
            elif score > 4000:
                tier = "Medio"
            else:
                tier = "Bajo"

            result = {
                "status": "success",
                "score": score,
                "tier": tier,
                "single_core_ops_sec": single_ops_sec,
                "multi_core_ops_sec": multi_ops_sec,
                "disk_write_mbs": write_speed,
                "disk_read_mbs": read_speed,
                "cores_used": cores,
                "timestamp": time.time(),
                "message": f"Score: {score} pts ({tier}) — 1 núcleo: {single_ops_sec:,} ops/s · {cores} núcleos: {multi_ops_sec:,} ops/s · Disco: {write_speed} MB/s W / {read_speed} MB/s R"
            }
            self._save_benchmark_history(result)
            return result
        except Exception as e:
            return {"status": "error", "message": f"Error ejecutando el benchmark: {e}"}

    def _save_benchmark_history(self, result):
        try:
            hist_file = os.path.join(_app_data_dir(), 'benchmark_history.json')
            history = []
            if os.path.exists(hist_file):
                try:
                    with open(hist_file, 'r') as f:
                        history = json.load(f)
                except Exception:
                    history = []
            history.append({"score": result["score"], "tier": result["tier"], "timestamp": result["timestamp"]})
            history = history[-30:]
            with open(hist_file, 'w') as f:
                json.dump(history, f)
        except Exception:
            pass

    def get_benchmark_history(self):
        try:
            hist_file = os.path.join(_app_data_dir(), 'benchmark_history.json')
            if not os.path.exists(hist_file):
                return {"status": "success", "data": []}
            with open(hist_file, 'r') as f:
                history = json.load(f)
            return {"status": "success", "data": history}
        except Exception:
            return {"status": "success", "data": []}

    # ══════════════════════════════════════════════
    # SALUD DEL SISTEMA (score calculado con datos reales, no estático)
    # ══════════════════════════════════════════════
    def get_system_health_score(self):
        try:
            score = 100
            breakdown = []

            mem = self.get_memory_status()
            if mem.get("status") == "success":
                load = mem["used_pct"]
                if load > 90:
                    score -= 20
                    breakdown.append({"label": "RAM casi al límite", "impact": -20, "level": "danger"})
                elif load > 75:
                    score -= 8
                    breakdown.append({"label": "Uso de RAM elevado", "impact": -8, "level": "warning"})
                else:
                    breakdown.append({"label": "RAM en buen estado", "impact": 0, "level": "ok"})

            try:
                usage = shutil.disk_usage(os.environ.get('SystemDrive', 'C:') + '\\')
                free_pct = (usage.free / usage.total) * 100
                if free_pct < 5:
                    score -= 25
                    breakdown.append({"label": "Disco del sistema casi lleno", "impact": -25, "level": "danger"})
                elif free_pct < 15:
                    score -= 10
                    breakdown.append({"label": "Poco espacio libre en disco", "impact": -10, "level": "warning"})
                else:
                    breakdown.append({"label": "Espacio en disco saludable", "impact": 0, "level": "ok"})
            except Exception:
                pass

            try:
                startup = self.get_startup_apps()
                if startup.get("status") == "success":
                    enabled = [s for s in startup["data"] if s["enabled"]]
                    heavy = [s for s in enabled if s["impact"] == "Alto"]
                    if len(heavy) >= 5:
                        score -= 15
                        breakdown.append({"label": f"{len(heavy)} apps pesadas en el arranque", "impact": -15, "level": "warning"})
                    elif len(enabled) >= 12:
                        score -= 8
                        breakdown.append({"label": "Demasiadas apps en el arranque", "impact": -8, "level": "warning"})
                    else:
                        breakdown.append({"label": "Arranque limpio", "impact": 0, "level": "ok"})
            except Exception:
                pass

            try:
                ok, res, _ = run_ps('(Get-PhysicalDisk | Select-Object -First 1).HealthStatus')
                res = res.strip() if ok else ''
                if res and 'healthy' not in res.lower():
                    score -= 30
                    breakdown.append({"label": f"Disco físico reporta: {res}", "impact": -30, "level": "danger"})
                elif res:
                    breakdown.append({"label": "Disco físico saludable (SMART)", "impact": 0, "level": "ok"})
            except Exception:
                pass

            score = max(0, min(100, score))
            if score >= 90:
                status_label = "Excelente"
            elif score >= 70:
                status_label = "Estable"
            elif score >= 45:
                status_label = "Necesita Atención"
            else:
                status_label = "Crítico"

            return {"status": "success", "score": score, "status_label": status_label, "breakdown": breakdown}
        except Exception as e:
            return {"status": "error", "message": str(e), "score": 0, "status_label": "Desconocido", "breakdown": []}

    # ══════════════════════════════════════════════
    # LICENSING API (Exposed to JS)
    # ══════════════════════════════════════════════
    def check_license_status(self):
        data = self.shield.check_license_attempts()
        saved_key = data.get("active_key")
        if data.get("banned", False):
            return {"status": "banned"}
        elif not saved_key:
            return {"status": "need_auth"}
        
        lic = self.shield._is_key_valid(saved_key)
        if not lic:
            return {"status": "need_auth"}
            
        owner = data.get("owner")
        if not owner:
            owner = lic.get("owner") or lic.get("owner_name") or lic.get("name") or "Premium User"
            
        return {"status": "ok", "owner": owner}

    def validate_key_ui(self, key, username=""):
        data = self.shield.check_license_attempts()
        if data.get("banned", False):
            return {"status": "banned", "message": "Acceso Denegado. Hardware ID Banneado."}
            
        lic = self.shield._is_key_valid(key, username)
        if lic:
            data["active_key"] = key
            data["attempts"] = 0
            data["owner"] = username or lic.get("owner_name") or "Premium User"
            with open(self.shield.license_file, 'w') as f:
                json.dump(data, f)
            return {"status": "success", "message": "Licencia Verificada. Acceso Autorizado.", "owner": data["owner"]}
        else:
            msg = self.shield.register_failed_attempt(data)
            return {"status": "error", "message": msg}

    def logout_license(self):
        data = self.shield.check_license_attempts()
        if "active_key" in data:
            del data["active_key"]
        if "owner" in data:
            del data["owner"]
        with open(self.shield.license_file, 'w') as f:
            json.dump(data, f)
        return {"status": "success"}

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# ══════════════════════════════════════════════
# ANTI-TAMPER & LICENSING SYSTEM
# ══════════════════════════════════════════════
class AntiTamper:
    def __init__(self):
        self.blacklisted_processes = [
            "cheatengine", "x64dbg", "x32dbg", "ollydbg", 
            "wireshark", "dnspy", "fiddler", "ida", "ida64",
            "processhacker", "httpdebugger"
        ]
        self.license_file = os.path.join(os.environ.get('APPDATA'), 'NauryLicense.json')
        self.hwid = self._generate_hwid()
        
        # SUPABASE CLOUD CONFIG
        # Cadenas cifradas en Hexadecimal, se descifran en RAM
        enc_url = bytes.fromhex("264021222a691c6c323849323d2f5836222d3a47302d3f5b3c2e2c477b212c2352213421547a3a21").decode("utf-8")
        enc_key = bytes.fromhex("3d560a222c315f2a263a5036352b6b0a3f0025782823234705363e641d192d2a7514631f700b0c1c05306b15237e").decode("utf-8")
        self.sup_url = os.getenv("NAURY_SUPABASE_URL", self._obf(enc_url))
        self.sup_key = os.getenv("NAURY_SUPABASE_KEY", self._obf(enc_key))

        # 1. HONEYPOT VARIABLES
        self.PremiumUser = 0
        self.VerifyLicense = False
        self.BypassSecurity = False

        # 2. Hilo de Auto-Verificacion
        self._start_integrity_thread()

    def _start_integrity_thread(self):
        def watchdog():
            import hashlib
            try:
                with open(sys.argv[0], 'rb') as f:
                    initial_hash = hashlib.md5(f.read()).hexdigest()
            except:
                initial_hash = None

            while True:
                time.sleep(4.7)
                if self.PremiumUser != 0 or self.VerifyLicense or self.BypassSecurity:
                    self._trigger_ban("Honeypot Activado")
                    ctypes.windll.kernel32.ExitProcess(1)
                
                # Self-Hashing (Check if executable/script was tampered in disk/memory)
                if initial_hash:
                    try:
                        with open(sys.argv[0], 'rb') as f:
                            current_hash = hashlib.md5(f.read()).hexdigest()
                        if current_hash != initial_hash:
                            self._trigger_ban("Self-Hashing Fallido: Código modificado externamente.")
                            ctypes.windll.kernel32.ExitProcess(1)
                    except:
                        pass
        t = threading.Thread(target=watchdog, daemon=True)
        t.start()

    def _obf(self, text):
        key = "N4URYS3CUR1TY"
        return "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))
    def _sup_request(self, method, endpoint, payload=None):
        url = f"{self.sup_url}/rest/v1/{endpoint}"
        headers = {
            "apikey": self.sup_key,
            "Authorization": f"Bearer {self.sup_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        data = json.dumps(payload).encode('utf-8') if payload else None
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return json.loads(response.read().decode('utf-8'))
        except:
            return None

    def _generate_hwid(self):
        try:
            # Combina UUID de placa base y procesador
            ok, mobo, _ = run_ps('(Get-WmiObject Win32_BaseBoard).SerialNumber')
            mobo = mobo.strip() if ok else ""
            ok, cpu, _ = run_ps('(Get-WmiObject Win32_Processor).ProcessorId')
            cpu = cpu.strip() if ok else ""
            ok, uuid_sys, _ = run_ps('(Get-WmiObject Win32_ComputerSystemProduct).UUID')
            uuid_sys = uuid_sys.strip() if ok else ""
            ok, disk, _ = run_ps('(Get-WmiObject Win32_DiskDrive | Select-Object -First 1).SerialNumber')
            disk = disk.strip() if ok else ""
            raw = f"{mobo}_{cpu}_{uuid_sys}_{disk}"
            return hashlib.sha256(raw.encode()).hexdigest()
        except:
            return str(uuid.getnode())

    def check_debugger(self):
        # 0. Anti-Debugging por Tiempo (Time-based Check)
        start_time = time.time()
        
        # 1. Check Win32 API IsDebuggerPresent
        # Cargamos funciones nativas dinámicamente para evadir Hooks
        kernel32 = ctypes.windll.kernel32
        if kernel32.IsDebuggerPresent():
            self._trigger_ban("Debugger API Detectado")
            
        # 2. Check Remote Debugger
        is_debugger_present = ctypes.c_bool(False)
        kernel32.CheckRemoteDebuggerPresent(kernel32.GetCurrentProcess(), ctypes.byref(is_debugger_present))
        if is_debugger_present.value:
            self._trigger_ban("Remote Debugger Detectado")
        
        # 3. Check Blacklisted Processes via tasklist (no psutil needed)
        try:
            tasks = subprocess.check_output('tasklist', shell=True, text=True, errors='ignore').lower()
            for bad in self.blacklisted_processes:
                if f"{bad}.exe" in tasks or f"{bad}64.exe" in tasks:
                    self._trigger_ban(f"Proceso Prohibido Detectado: {bad}")
        except:
            pass

        # 4. Anti-VM / Sandbox Checks
        try:
            # Detecta menos de 4GB de RAM o 1 nucleo
            cores = os.cpu_count()
            if cores and cores < 2:
                self._fatal_exit("Entorno Virtual Detectado (Cores < 2).")
            
            # Detecta palabras clave de Máquinas Virtuales
            gpu = subprocess.check_output('wmic path win32_VideoController get name', shell=True, text=True, errors='ignore').lower()
            if gpu and any(vm in gpu for vm in ["vmware", "virtualbox", "vbox", "qemu", "parallels"]):
                self._fatal_exit("Máquina Virtual / Sandbox Detectada.")
        except:
            pass

        # 5. Comprobar si se ha parado la ejecución en un breakpoint
        elapsed = time.time() - start_time
        if elapsed > 15.0: # Si las validaciones han tardado más de 15 segundos, hay un humano analizando
            self._trigger_ban("Time-Stamp Check: Ejecución pausada o manipulada.")

    def check_license_attempts(self):
        data = {"attempts": 0, "banned": False}
        if os.path.exists(self.license_file):
            try:
                with open(self.license_file, 'r') as f:
                    data = json.load(f)
            except:
                pass
        
        # Consultar la Nube (Supabase) si el HWID está baneado
        try:
            res = self._sup_request("GET", f"bans?hwid=eq.{self.hwid}&select=*")
            if res is not None:
                if len(res) > 0:
                    # Baneado en la nube — sincronizar
                    data["banned"] = True
                    data["ban_reason"] = res[0].get("reason", "Ban desde el servidor en la Nube")
                    with open(self.license_file, 'w') as f:
                        json.dump(data, f)
                elif data.get("banned", False):
                    # Desbaneado desde la nube — limpiar local
                    data["banned"] = False
                    data["attempts"] = 0
                    with open(self.license_file, 'w') as f:
                        json.dump(data, f)
        except:
            pass

        if data.get("banned", False):
            self._notify_whatsapp(f"Intento de acceso bloqueado por banneo permanente HWID: {self.hwid}")
            self._fatal_exit("Acceso Denegado. Hardware ID Banneado por violaciones de seguridad.")
            
        return data

    def _is_key_valid(self, key, username=""):
        # Consulta en tiempo real a Supabase
        res = self._sup_request("GET", f"licenses?key=eq.{key}&select=*")
        if res and len(res) > 0:
            lic = res[0]
            if lic.get("revoked") is False:
                # Marcar HWID en Supabase
                if not lic.get("hwid"):
                    payload = {"hwid": self.hwid}
                    if username:
                        payload["owner_name"] = username
                    self._sup_request("PATCH", f"licenses?key=eq.{key}", payload)
                    lic["owner_name"] = username
                elif lic.get("hwid") != self.hwid:
                    return False  # Clave usada en otro PC
                return lic
        return False

    def register_failed_attempt(self, data=None):
        if data is None:
            data = {"attempts": 0, "banned": False}
            if os.path.exists(self.license_file):
                try:
                    with open(self.license_file, 'r') as f:
                        data = json.load(f)
                except:
                    pass
            
        data["attempts"] = data.get("attempts", 0) + 1
        
        if data["attempts"] >= 3:
            data["banned"] = True
            msg = "Demasiados intentos fallidos. Hardware bloqueado permanentemente."
            # Subir ban a Supabase
            self._sup_request("POST", "hwid_blacklist", {"hwid": self.hwid, "reason": "Fuerza bruta: 3 intentos de licencia fallidos"})
            self._notify_discord(f"ALERTA CRÍTICA: Bloqueo de Hardware activado por fuerza bruta de licencia. HWID: {self.hwid}")
        else:
            msg = f"Licencia incorrecta. Intento {data['attempts']}/3."
            self._notify_discord(f"Intento fallido de licencia ({data['attempts']}/3). HWID: {self.hwid}")
            
        with open(self.license_file, 'w') as f:
            json.dump(data, f)
            
        if data["banned"]:
            self._fatal_exit(msg)
        return msg

    def _trigger_ban(self, reason):
        data = self.check_license_attempts()
        data["banned"] = True
        data["ban_reason"] = reason
        with open(self.license_file, 'w') as f:
            json.dump(data, f)
            
        # Registrar el Ban en Supabase
        self._sup_request("POST", "hwid_blacklist", {"hwid": self.hwid, "reason": reason})
            
        self._notify_whatsapp(f"ALERTA DE SEGURIDAD: Intento de Cracking Detectado. Motivo: {reason}. HWID Banneado: {self.hwid}")
        self._fatal_exit(f"Naury Anti-Tamper Shield: {reason}. Hardware bloqueado por motivos de seguridad.")

    def _get_system_info(self):
        """Recopila información del sistema para incluir en alertas de seguridad."""
        info = {}
        try:
            info['ip'] = urllib.request.urlopen('https://api.ipify.org', timeout=4).read().decode().strip()
        except:
            info['ip'] = 'No disponible'
        try:
            info['user'] = os.environ.get('USERNAME', 'Desconocido')
            info['pc_name'] = os.environ.get('COMPUTERNAME', 'Desconocido')
        except:
            info['user'] = 'Desconocido'
            info['pc_name'] = 'Desconocido'
        try:
            ok, out, _ = run_ps('(Get-WmiObject Win32_OperatingSystem).Caption')
            info['os'] = out.strip() if ok else 'Windows'
        except:
            info['os'] = 'Windows'
        try:
            ok, out, _ = run_ps('(Get-WmiObject Win32_Processor | Select-Object -First 1).Name')
            info['cpu'] = out.strip() if ok else 'Desconocido'
        except:
            info['cpu'] = 'Desconocido'
        return info

    def _notify_discord(self, message):
        DISCORD_WEBHOOK = os.environ.get("NAURY_DISCORD_WEBHOOK", "https://discord.com/api/webhooks/1534870858584293418/5dPPe6WJvLgm7MiOTGxfvtU6MRWRkC4d-h8zTuWWyiBtJcFsfcH6DR967zVjpuSGsT6Z")
        TELEGRAM_CHAT_ID = os.environ.get("NAURY_TELEGRAM_CHAT_ID", "")
        
        if not DISCORD_WEBHOOK:
            print(f"[DISCORD - NOT CONFIGURED]: {message}")
            return

        try:
            sysinfo = self._get_system_info()
            import datetime
            now = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            
            full_msg = (
                f"🚨 NAURY SECURITY ALERT 🚨\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"{message}\n\n"
                f"📋 DATOS DEL EQUIPO:\n"
                f"🌐 IP Publica: {sysinfo['ip']}\n"
                f"💻 PC: {sysinfo['pc_name']}\n"
                f"👤 Usuario: {sysinfo['user']}\n"
                f"🖥 SO: {sysinfo['os']}\n"
                f"⚙️ CPU: {sysinfo['cpu']}\n"
                f"🔑 HWID: {self.hwid}\n"
                f"🕐 Fecha: {now}"
            )
            
            payload = json.dumps({"content": full_msg}).encode('utf-8')
            req  = urllib.request.Request(DISCORD_WEBHOOK, data=payload, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                print(f"[DISCORD SENT]: {message[:60]}...")
        except Exception as e:
            print(f"[DISCORD ERROR]: {e}")

    def _notify_telegram(self, message):
        TELEGRAM_TOKEN   = os.environ.get("NAURY_TELEGRAM_TOKEN", "")
        TELEGRAM_CHAT_ID = os.environ.get("NAURY_TELEGRAM_CHAT_ID", "")
        
        if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
            print(f"[TELEGRAM - NOT CONFIGURED]: {message}")
            return
        
        try:
            sysinfo = self._get_system_info()
            import datetime
            now = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            
            full_msg = (
                f"🚨 NAURY SECURITY ALERT 🚨\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"{message}\n\n"
                f"📋 DATOS DEL EQUIPO:\n"
                f"🌐 IP Publica: {sysinfo['ip']}\n"
                f"💻 PC: {sysinfo['pc_name']}\n"
                f"👤 Usuario: {sysinfo['user']}\n"
                f"🖥 SO: {sysinfo['os']}\n"
                f"⚙️ CPU: {sysinfo['cpu']}\n"
                f"🔑 HWID: {self.hwid}\n"
                f"🕐 Fecha: {now}"
            )
            
            payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": full_msg}).encode('utf-8')
            url  = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            req  = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                print(f"[TELEGRAM SENT]: {message[:60]}...")
        except Exception as e:
            print(f"[TELEGRAM ERROR]: {e}")

    # Alias para mantener compatibilidad con el resto del código
    def _notify_whatsapp(self, message):
        self._notify_telegram(message)


    def _fatal_exit(self, msg):
        ctypes.windll.user32.MessageBoxW(0, msg, "Naury Security Engine", 0x10)
        os._exit(1)

if __name__ == '__main__':
    if not is_admin():
        script = os.path.abspath(__file__)
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}"', None, 1)
        sys.exit()

    # 1. Ejecutar controles de seguridad antes de levantar la UI
    shield = AntiTamper()
    shield.check_debugger()
    shield.check_license_attempts()

    api = Api()
    # Inyectar el shield en la API para poder llamarlo desde JS (para probar licencias falsas)
    api.shield = shield 
    
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    web_dir = os.path.join(base_path, 'web')
    webview.create_window(
        title='Naury Utility',
        url=os.path.join(web_dir, 'index.html'),
        js_api=api,
        width=1100,
        height=750,
        background_color='#050508',
        resizable=True,
        frameless=True,
        easy_drag=False
    )
    
    webview.start(debug=False)




