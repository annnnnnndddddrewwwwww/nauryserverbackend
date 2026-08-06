TWEAKS = [
    {
        "id": "dns_cloudflare",
        "name": "DNS Cloudflare (Mejor Ping/WiFi)",
        "category": "FPS & Ping",
        "desc": "Configura los DNS 1.1.1.1 y 1.0.0.1 en todas las redes activas para máxima velocidad.",
        "cmd_apply": "powershell -command \"Get-NetAdapter | Where-Object Status -eq 'Up' | Set-DnsClientServerAddress -ServerAddresses '1.1.1.1','1.0.0.1'\"",
        "cmd_revert": "powershell -command \"Get-NetAdapter | Where-Object Status -eq 'Up' | Set-DnsClientServerAddress -ResetServerAddresses\"",
        "risk": "safe"
    },
    {
        "id": "dns_adguard",
        "name": "DNS AdGuard (Bloqueo Anuncios)",
        "category": "Privacidad",
        "desc": "Configura los DNS de AdGuard para bloquear anuncios y rastreadores a nivel de red.",
        "cmd_apply": "powershell -command \"Get-NetAdapter | Where-Object Status -eq 'Up' | Set-DnsClientServerAddress -ServerAddresses '94.140.14.14','94.140.15.15'\"",
        "cmd_revert": "powershell -command \"Get-NetAdapter | Where-Object Status -eq 'Up' | Set-DnsClientServerAddress -ResetServerAddresses\"",
        "risk": "safe"
    },
    {
        "id": "dns_google",
        "name": "DNS Google (Estabilidad)",
        "category": "FPS & Ping",
        "desc": "Configura los DNS de Google 8.8.8.8 para máxima estabilidad y compatibilidad.",
        "cmd_apply": "powershell -command \"Get-NetAdapter | Where-Object Status -eq 'Up' | Set-DnsClientServerAddress -ServerAddresses '8.8.8.8','8.8.4.4'\"",
        "cmd_revert": "powershell -command \"Get-NetAdapter | Where-Object Status -eq 'Up' | Set-DnsClientServerAddress -ResetServerAddresses\"",
        "risk": "safe"
    },
    {
        "id": "fps_1",
        "name": "TCP Auto-Tuning",
        "category": "FPS & Ping",
        "desc": "Evita picos de ping deteniendo el ajuste dinámico TCP.",
        "cmd_apply": "netsh int tcp set global autotuninglevel=disabled",
        "cmd_revert": "netsh int tcp set global autotuninglevel=normal"
    },
    {
        "id": "fps_2",
        "name": "Large Send Offload",
        "category": "FPS & Ping",
        "desc": "Previene retención de paquetes NIC.",
        "cmd_apply": "netsh int tcp set global chimney=disabled & netsh int tcp set global taskoffload=disabled",
        "cmd_revert": "netsh int tcp set global chimney=automatic & netsh int tcp set global taskoffload=enabled"
    },
    {
        "id": "fps_3",
        "name": "Límite QoS",
        "category": "FPS & Ping",
        "desc": "Elimina el límite del 20% de red de Windows.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Psched\" /v NonBestEffortLimit /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Psched\" /v NonBestEffortLimit /t REG_DWORD /d 20 /f"
    },
    {
        "id": "fps_4",
        "name": "TCP ECN Capability",
        "category": "FPS & Ping",
        "desc": "Acelera el enrutamiento de red.",
        "cmd_apply": "netsh int tcp set global ecncapability=disabled",
        "cmd_revert": "netsh int tcp set global ecncapability=default"
    },
    {
        "id": "fps_5",
        "name": "TCP Congestion Provider (CUBIC)",
        "category": "FPS & Ping",
        "desc": "Usa CUBIC para mejor flujo en juegos.",
        "cmd_apply": "netsh int tcp set supplemental template=custom congestionprovider=cubic",
        "cmd_revert": "netsh int tcp set global congestionprovider=default"
    },
    {
        "id": "fps_6",
        "name": "Algoritmo Nagle (TcpNoDelay)",
        "category": "FPS & Ping",
        "desc": "Deshabilita Nagle, enviando paquetes al instante.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\" /v TcpAckFrequency /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\" /v TcpAckFrequency /f"
    },
    {
        "id": "fps_7",
        "name": "Mouse Data Queue Size",
        "category": "FPS & Ping",
        "desc": "Reduce la cola del ratón a 16 (Menor Input Lag).",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\mouclass\\Parameters\" /v MouseDataQueueSize /t REG_DWORD /d 16 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\mouclass\\Parameters\" /v MouseDataQueueSize /t REG_DWORD /d 100 /f"
    },
    {
        "id": "fps_8",
        "name": "Keyboard Data Queue Size",
        "category": "FPS & Ping",
        "desc": "Reduce la cola de teclado a 16.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\kbdclass\\Parameters\" /v KeyboardDataQueueSize /t REG_DWORD /d 16 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\kbdclass\\Parameters\" /v KeyboardDataQueueSize /t REG_DWORD /d 100 /f"
    },
    {
        "id": "fps_9",
        "name": "Xbox Game DVR",
        "category": "FPS & Ping",
        "desc": "Elimina grabador de fondo causando stuttering.",
        "cmd_apply": "reg add \"HKCU\\System\\GameConfigStore\" /v GameDVR_Enabled /t REG_DWORD /d 0 /f & reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR\" /v AllowGameDVR /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg add \"HKCU\\System\\GameConfigStore\" /v GameDVR_Enabled /t REG_DWORD /d 1 /f & reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR\" /v AllowGameDVR /f"
    },
    {
        "id": "fps_10",
        "name": "Xbox Game Bar",
        "category": "FPS & Ping",
        "desc": "Deshabilita la barra inyectada en pantalla completa.",
        "cmd_apply": "reg add \"HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\GameDVR\" /v AppCaptureEnabled /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg add \"HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\GameDVR\" /v AppCaptureEnabled /t REG_DWORD /d 1 /f"
    },
    {
        "id": "fps_11",
        "name": "Full Screen Exclusive (FSE)",
        "category": "FPS & Ping",
        "desc": "Desactiva optimizaciones de pantalla completa.",
        "cmd_apply": "reg add \"HKCU\\System\\GameConfigStore\" /v GameDVR_FSEBehaviorMode /t REG_DWORD /d 2 /f",
        "cmd_revert": "reg add \"HKCU\\System\\GameConfigStore\" /v GameDVR_FSEBehaviorMode /t REG_DWORD /d 0 /f"
    },
    {
        "id": "fps_12",
        "name": "Disable Nagle Algorithm (Network)",
        "category": "FPS & Ping",
        "desc": "Acelera el envío de paquetes pequeños sin esperar confirmación TCP.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\" /v TCPNoDelay /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces\" /v TCPNoDelay /f"
    },
    {
        "id": "fps_13",
        "name": "Disable Heuristics",
        "category": "FPS & Ping",
        "desc": "Deshabilita TCP Heuristics de Windows.",
        "cmd_apply": "netsh int tcp set heuristics disabled",
        "cmd_revert": "netsh int tcp set heuristics default"
    },
    {
        "id": "fps_14",
        "name": "Receive Segment Coalescing",
        "category": "FPS & Ping",
        "desc": "Apaga RSC para bajar latencia en adaptadores Wi-Fi.",
        "cmd_apply": "netsh int tcp set global rsc=disabled",
        "cmd_revert": "netsh int tcp set global rsc=enabled"
    },
    {
        "id": "fps_15",
        "name": "Direct Memory Access (DMA) Network",
        "category": "FPS & Ping",
        "desc": "Habilita NetDMA para descarga de CPU.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v EnableTCPA /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v EnableTCPA /t REG_DWORD /d 0 /f"
    },
    {
        "id": "fps_16",
        "name": "IPv6 Disable",
        "category": "FPS & Ping",
        "desc": "Si no usas IPv6, apagarlo previene lags DNS.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters\" /v DisabledComponents /t REG_DWORD /d 255 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters\" /v DisabledComponents /t REG_DWORD /d 0 /f"
    },
    {
        "id": "fps_17",
        "name": "Disable Network Throttling",
        "category": "FPS & Ping",
        "desc": "Quita el tope de procesamiento de paquetes multimedia.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\" /v NetworkThrottlingIndex /t REG_DWORD /d 4294967295 /f",
        "cmd_revert": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\" /v NetworkThrottlingIndex /t REG_DWORD /d 10 /f"
    },
    {
        "id": "fps_18",
        "name": "System Responsiveness 0%",
        "category": "FPS & Ping",
        "desc": "Asigna 100% de CPU a juegos en lugar del 80%.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\" /v SystemResponsiveness /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\" /v SystemResponsiveness /t REG_DWORD /d 20 /f"
    },
    {
        "id": "fps_19",
        "name": "Games Scheduling Category",
        "category": "FPS & Ping",
        "desc": "Pone los juegos en categoría de prioridad Alta en el scheduler.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games\" /v Scheduling Category /t REG_SZ /d \"High\" /f",
        "cmd_revert": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games\" /v Scheduling Category /t REG_SZ /d \"Medium\" /f"
    },
    {
        "id": "fps_20",
        "name": "Games GPU Priority",
        "category": "FPS & Ping",
        "desc": "Máxima prioridad a la GPU para perfiles de juego.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games\" /v GPU Priority /t REG_DWORD /d 8 /f",
        "cmd_revert": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games\" /v GPU Priority /t REG_DWORD /d 2 /f"
    },
    {
        "id": "fps_21",
        "name": "Desactivar Aceleración de Ratón",
        "category": "FPS & Ping",
        "desc": "Desactiva 'Mejorar la precisión del puntero' a nivel registro (Curve).",
        "cmd_apply": "reg add \"HKCU\\Control Panel\\Mouse\" /v MouseSpeed /t REG_SZ /d 0 /f",
        "cmd_revert": "reg add \"HKCU\\Control Panel\\Mouse\" /v MouseSpeed /t REG_SZ /d 1 /f"
    },
    {
        "id": "fps_22",
        "name": "USB Polling Rate Override",
        "category": "FPS & Ping",
        "desc": "Fuerza actualizaciones más agresivas para dispositivos USB.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\{36FC9E60-C465-11CF-8056-444553540000}\\0000\" /v IdleEnable /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\{36FC9E60-C465-11CF-8056-444553540000}\\0000\" /v IdleEnable /f"
    },
    {
        "id": "fps_23",
        "name": "Disable Windows Scaling",
        "category": "FPS & Ping",
        "desc": "Evita el escalado DWM que añade input lag en juegos borderless.",
        "cmd_apply": "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\" /v UseDpiScaling /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\" /v UseDpiScaling /t REG_DWORD /d 1 /f"
    },
    {
        "id": "fps_24",
        "name": "Bluetooth Support Disable",
        "category": "FPS & Ping",
        "desc": "Si no usas mandos Bluetooth, ahorra latencia IRQ de este bus.",
        "cmd_apply": "sc config bthserv start= disabled",
        "cmd_revert": "sc config bthserv start= demand"
    },
    {
        "id": "fps_25",
        "name": "Audio Latency Tweak",
        "category": "FPS & Ping",
        "desc": "Fuerza al servicio de audio a procesar buffers más rápido (Menos lag de sonido).",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Audio\" /v Latency Sensitive /t REG_SZ /d \"True\" /f",
        "cmd_revert": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Audio\" /v Latency Sensitive /t REG_SZ /d \"False\" /f"
    },
    {
        "id": "fps_26",
        "name": "TCP Timestamps",
        "category": "FPS & Ping",
        "desc": "Quita estampas de tiempo TCP para reducir tamaño del paquete.",
        "cmd_apply": "netsh int tcp set global timestamps=disabled",
        "cmd_revert": "netsh int tcp set global timestamps=enabled"
    },
    {
        "id": "fps_27",
        "name": "MaxUserPort TCP",
        "category": "FPS & Ping",
        "desc": "Aumenta puertos disponibles para conexiones simultáneas masivas.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v MaxUserPort /t REG_DWORD /d 65534 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v MaxUserPort /f"
    },
    {
        "id": "fps_28",
        "name": "DefaultTTL 64",
        "category": "FPS & Ping",
        "desc": "Optimiza los saltos de paquetes de red para latencia rápida.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v DefaultTTL /t REG_DWORD /d 64 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v DefaultTTL /f"
    },
    {
        "id": "fps_29",
        "name": "GlobalMaxTcpWindowSize",
        "category": "FPS & Ping",
        "desc": "Ajuste agresivo de ventana TCP para transferencias instantáneas.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v GlobalMaxTcpWindowSize /t REG_DWORD /d 65535 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v GlobalMaxTcpWindowSize /f"
    },
    {
        "id": "fps_30",
        "name": "Disable Background Network",
        "category": "FPS & Ping",
        "desc": "Prioriza la red frontal bloqueando tareas BITS ocultas.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\BITS\" /v EnableBITSMaxBandwidth /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\BITS\" /v EnableBITSMaxBandwidth /f"
    },
    {
        "id": "perf_1",
        "name": "Desactivar Hibernación",
        "category": "Rendimiento",
        "desc": "Borra el archivo hiberfil.sys.",
        "cmd_apply": "powercfg.exe /hibernate off",
        "cmd_revert": "powercfg.exe /hibernate on"
    },
    {
        "id": "perf_2",
        "name": "Desactivar SysMain (SuperFetch)",
        "category": "Rendimiento",
        "desc": "Evita disco al 100%.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\SysMain\" /v Start /t REG_DWORD /d 4 /f & sc stop SysMain",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\SysMain\" /v Start /t REG_DWORD /d 2 /f & sc start SysMain"
    },
    {
        "id": "perf_3",
        "name": "Desactivar Búsqueda Indexada",
        "category": "Rendimiento",
        "desc": "Detiene escaneo constante de disco.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\WSearch\" /v Start /t REG_DWORD /d 4 /f & sc stop WSearch",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\WSearch\" /v Start /t REG_DWORD /d 2 /f & sc start WSearch"
    },
    {
        "id": "perf_4",
        "name": "Win32PrioritySeparation",
        "category": "Rendimiento",
        "desc": "100% de CPU a la app en primer plano.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl\" /v Win32PrioritySeparation /t REG_DWORD /d 38 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl\" /v Win32PrioritySeparation /t REG_DWORD /d 2 /f"
    },
    {
        "id": "perf_5",
        "name": "Disable Paging Executive",
        "category": "Rendimiento",
        "desc": "Kernel de Windows 100% en RAM.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\" /v DisablePagingExecutive /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\" /v DisablePagingExecutive /t REG_DWORD /d 0 /f"
    },
    {
        "id": "perf_6",
        "name": "Forzar Caché L2/L3",
        "category": "Rendimiento",
        "desc": "Memoria en caché fija sin latencias dinámicas.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\" /v SecondLevelDataCache /t REG_DWORD /d 1024 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\" /v SecondLevelDataCache /t REG_DWORD /d 0 /f"
    },
    {
        "id": "perf_7",
        "name": "Cierre Inmediato de Apps",
        "category": "Rendimiento",
        "desc": "Windows no espera apps colgadas.",
        "cmd_apply": "reg add \"HKCU\\Control Panel\\Desktop\" /v WaitToKillAppTimeout /t REG_SZ /d 2000 /f",
        "cmd_revert": "reg add \"HKCU\\Control Panel\\Desktop\" /v WaitToKillAppTimeout /t REG_SZ /d 20000 /f"
    },
    {
        "id": "perf_8",
        "name": "Menu Show Delay",
        "category": "Rendimiento",
        "desc": "Despliegue de menús ultra-rápido (20ms).",
        "cmd_apply": "reg add \"HKCU\\Control Panel\\Desktop\" /v MenuShowDelay /t REG_SZ /d 20 /f",
        "cmd_revert": "reg add \"HKCU\\Control Panel\\Desktop\" /v MenuShowDelay /t REG_SZ /d 400 /f"
    },
    {
        "id": "perf_9",
        "name": "Plan Ultimate Performance",
        "category": "Rendimiento",
        "desc": "Desbloquea modo máximo rendimiento de energía.",
        "cmd_apply": "powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61",
        "cmd_revert": "powercfg -setactive 381b4222-f694-41f0-9685-ff5bb260df2e"
    },
    {
        "id": "perf_10",
        "name": "Efectos Visuales Ligeros",
        "category": "Rendimiento",
        "desc": "Quita animaciones pesadas de ventanas.",
        "cmd_apply": "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects\" /v VisualFXSetting /t REG_DWORD /d 2 /f",
        "cmd_revert": "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects\" /v VisualFXSetting /t REG_DWORD /d 0 /f"
    },
    {
        "id": "perf_11",
        "name": "Desactivar Prefetcher",
        "category": "Rendimiento",
        "desc": "Detiene la lectura constante a disco para indexar apps.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters\" /v EnablePrefetcher /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters\" /v EnablePrefetcher /t REG_DWORD /d 3 /f"
    },
    {
        "id": "perf_12",
        "name": "AutoEndTasks",
        "category": "Rendimiento",
        "desc": "Mata tareas sin responder al reiniciar.",
        "cmd_apply": "reg add \"HKCU\\Control Panel\\Desktop\" /v AutoEndTasks /t REG_SZ /d 1 /f",
        "cmd_revert": "reg add \"HKCU\\Control Panel\\Desktop\" /v AutoEndTasks /t REG_SZ /d 0 /f"
    },
    {
        "id": "perf_13",
        "name": "LowLevelHooksTimeout",
        "category": "Rendimiento",
        "desc": "Evita bloqueos de mouse/teclado reduciendo el timeout interno.",
        "cmd_apply": "reg add \"HKCU\\Control Panel\\Desktop\" /v LowLevelHooksTimeout /t REG_SZ /d 1000 /f",
        "cmd_revert": "reg delete \"HKCU\\Control Panel\\Desktop\" /v LowLevelHooksTimeout /f"
    },
    {
        "id": "perf_14",
        "name": "Disable Background Apps",
        "category": "Rendimiento",
        "desc": "Fuerza cierre de apps UWP en segundo plano.",
        "cmd_apply": "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\BackgroundAccessApplications\" /v GlobalUserDisabled /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\BackgroundAccessApplications\" /v GlobalUserDisabled /t REG_DWORD /d 0 /f"
    },
    {
        "id": "perf_15",
        "name": "Disable Fast Startup",
        "category": "Rendimiento",
        "desc": "El inicio rápido causa bugs de driver. Desactívalo.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Power\" /v HiberbootEnabled /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Power\" /v HiberbootEnabled /t REG_DWORD /d 1 /f"
    },
    {
        "id": "perf_16",
        "name": "Disable NTFS Last Access Update",
        "category": "Rendimiento",
        "desc": "Elimina escritura constante por leer archivos.",
        "cmd_apply": "fsutil behavior set disablelastaccess 1",
        "cmd_revert": "fsutil behavior set disablelastaccess 0"
    },
    {
        "id": "perf_17",
        "name": "Large System Cache",
        "category": "Rendimiento",
        "desc": "Favorece uso de RAM para caché de sistema.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\" /v LargeSystemCache /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\" /v LargeSystemCache /t REG_DWORD /d 0 /f"
    },
    {
        "id": "perf_18",
        "name": "Disable ClearPageFile",
        "category": "Rendimiento",
        "desc": "Acelera apagados omitiendo el borrado seguro de la página de archivo.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\" /v ClearPageFileAtShutdown /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\" /v ClearPageFileAtShutdown /t REG_DWORD /d 1 /f"
    },
    {
        "id": "perf_19",
        "name": "Disable Thumbnail Cache",
        "category": "Rendimiento",
        "desc": "Evita creación de archivos thumbs.db ocultos.",
        "cmd_apply": "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\" /v DisableThumbnailCache /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\" /v DisableThumbnailCache /t REG_DWORD /d 0 /f"
    },
    {
        "id": "perf_20",
        "name": "Disable Taskbar Animations",
        "category": "Rendimiento",
        "desc": "Elimina retraso en barra de tareas.",
        "cmd_apply": "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\" /v TaskbarAnimations /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\" /v TaskbarAnimations /t REG_DWORD /d 1 /f"
    },
    {
        "id": "perf_21",
        "name": "Disable UI Animations",
        "category": "Rendimiento",
        "desc": "Desactiva animaciones de control en Windows.",
        "cmd_apply": "reg add \"HKCU\\Control Panel\\Desktop\" /v UserPreferencesMask /t REG_BINARY /d 9012078010000000 /f",
        "cmd_revert": "reg add \"HKCU\\Control Panel\\Desktop\" /v UserPreferencesMask /t REG_BINARY /d 9e3e078012000000 /f"
    },
    {
        "id": "perf_22",
        "name": "Hardware Accelerated GPU Scheduling",
        "category": "Rendimiento",
        "desc": "Habilita HAGS en registro para gráficas nuevas.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers\" /v HwSchMode /t REG_DWORD /d 2 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers\" /v HwSchMode /t REG_DWORD /d 1 /f"
    },
    {
        "id": "perf_23",
        "name": "Disable VBS / Core Isolation",
        "category": "Rendimiento",
        "desc": "Desactiva Virtualization Based Security que quita hasta 10% FPS.",
        "cmd_apply": "reg add \"HKLM\\System\\CurrentControlSet\\Control\\DeviceGuard\" /v EnableVirtualizationBasedSecurity /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg add \"HKLM\\System\\CurrentControlSet\\Control\\DeviceGuard\" /v EnableVirtualizationBasedSecurity /t REG_DWORD /d 1 /f"
    },
    {
        "id": "perf_24",
        "name": "Memory Compression Disable",
        "category": "Rendimiento",
        "desc": "Si tienes 16GB+ de RAM, ahorra CPU desactivando compresión.",
        "cmd_apply": "powershell -command \"Disable-MMAgent -mc\"",
        "cmd_revert": "powershell -command \"Enable-MMAgent -mc\""
    },
    {
        "id": "perf_25",
        "name": "Prefetch Parameters Optimization",
        "category": "Rendimiento",
        "desc": "Cambia cómo Windows mapea memoria virtual.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters\" /v BootId /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters\" /v BootId /f"
    },
    {
        "id": "perf_26",
        "name": "Turn off Autoplay",
        "category": "Rendimiento",
        "desc": "No analiza unidades extraíbles automáticamente.",
        "cmd_apply": "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\AutoplayHandlers\" /v DisableAutoplay /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\AutoplayHandlers\" /v DisableAutoplay /t REG_DWORD /d 0 /f"
    },
    {
        "id": "perf_27",
        "name": "Maximize RAM Allocation",
        "category": "Rendimiento",
        "desc": "Evita bloqueos de asignación reservada de Hardware.",
        "cmd_apply": "bcdedit /deletevalue truncatememory",
        "cmd_revert": "echo No default truncatememory"
    },
    {
        "id": "perf_28",
        "name": "GPU Worker Threads",
        "category": "Rendimiento",
        "desc": "Ajuste de Direct3D para forzar hilos multi-core.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Direct3D\" /v MaxThreads /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Microsoft\\Direct3D\" /v MaxThreads /f"
    },
    {
        "id": "perf_29",
        "name": "Optimize Network Interrupts",
        "category": "Rendimiento",
        "desc": "Asigna paquetes de red a todos los núcleos (RSS).",
        "cmd_apply": "netsh int tcp set global rss=enabled",
        "cmd_revert": "netsh int tcp set global rss=default"
    },
    {
        "id": "perf_30",
        "name": "Processor Idle Demote Threshold",
        "category": "Rendimiento",
        "desc": "Exige más esfuerzo de CPU antes de aparcar cores.",
        "cmd_apply": "powercfg -setacvalueindex scheme_current sub_processor 4b92d758-5a24-4851-a470-815d78aee119 100",
        "cmd_revert": "powercfg -setacvalueindex scheme_current sub_processor 4b92d758-5a24-4851-a470-815d78aee119 50"
    },
    {
        "id": "priv_1",
        "name": "Telemetría Principal",
        "category": "Privacidad",
        "desc": "Apaga recolección de MS.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection\" /v AllowTelemetry /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection\" /v AllowTelemetry /f"
    },
    {
        "id": "priv_2",
        "name": "Servicio DiagTrack",
        "category": "Privacidad",
        "desc": "Deshabilita DiagTrack.",
        "cmd_apply": "sc stop DiagTrack & sc config DiagTrack start= disabled",
        "cmd_revert": "sc config DiagTrack start= auto & sc start DiagTrack"
    },
    {
        "id": "priv_3",
        "name": "Matar Cortana",
        "category": "Privacidad",
        "desc": "Apaga el asistente virtual.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search\" /v AllowCortana /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search\" /v AllowCortana /f"
    },
    {
        "id": "priv_4",
        "name": "ID de Publicidad",
        "category": "Privacidad",
        "desc": "Evita perfiles de anuncios.",
        "cmd_apply": "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\AdvertisingInfo\" /v Enabled /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\AdvertisingInfo\" /v Enabled /t REG_DWORD /d 1 /f"
    },
    {
        "id": "priv_5",
        "name": "Recolección de Escritura",
        "category": "Privacidad",
        "desc": "Apaga el keylogger oficial.",
        "cmd_apply": "reg add \"HKCU\\Software\\Microsoft\\InputPersonalization\" /v RestrictImplicitTextCollection /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg add \"HKCU\\Software\\Microsoft\\InputPersonalization\" /v RestrictImplicitTextCollection /t REG_DWORD /d 0 /f"
    },
    {
        "id": "priv_6",
        "name": "Windows Error Reporting",
        "category": "Privacidad",
        "desc": "No envía volcados a la nube.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Error Reporting\" /v Disabled /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Error Reporting\" /v Disabled /f"
    },
    {
        "id": "priv_7",
        "name": "Historial de Actividad",
        "category": "Privacidad",
        "desc": "Detiene recolección Timeline.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\System\" /v PublishUserActivities /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\System\" /v PublishUserActivities /f"
    },
    {
        "id": "priv_8",
        "name": "Rastreo de Ubicación",
        "category": "Privacidad",
        "desc": "Evita rastreo geográfico.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\LocationAndSensors\" /v DisableLocation /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\LocationAndSensors\" /v DisableLocation /f"
    },
    {
        "id": "priv_9",
        "name": "WiFi Sense",
        "category": "Privacidad",
        "desc": "No comparte contraseñas WiFi.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Microsoft\\WcmSvc\\wifinetworkmanager\\config\" /v AutoConnectAllowedOEM /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg add \"HKLM\\SOFTWARE\\Microsoft\\WcmSvc\\wifinetworkmanager\\config\" /v AutoConnectAllowedOEM /t REG_DWORD /d 1 /f"
    },
    {
        "id": "priv_10",
        "name": "Feedback Notifications",
        "category": "Privacidad",
        "desc": "Apaga peticiones de Feedback.",
        "cmd_apply": "reg add \"HKCU\\Software\\Microsoft\\Siuf\\Rules\" /v NumberOfSIUFInPeriod /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg delete \"HKCU\\Software\\Microsoft\\Siuf\\Rules\" /v NumberOfSIUFInPeriod /f"
    },
    {
        "id": "priv_11",
        "name": "Cloud Content Search",
        "category": "Privacidad",
        "desc": "Evita búsquedas web en el menú inicio.",
        "cmd_apply": "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Search\" /v BingSearchEnabled /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Search\" /v BingSearchEnabled /t REG_DWORD /d 1 /f"
    },
    {
        "id": "priv_12",
        "name": "Tailored Experiences",
        "category": "Privacidad",
        "desc": "Bloquea recolección de datos diagnósticos para consejos.",
        "cmd_apply": "reg add \"HKCU\\Software\\Policies\\Microsoft\\Windows\\CloudContent\" /v DisableTailoredExperiencesWithDiagnosticData /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg delete \"HKCU\\Software\\Policies\\Microsoft\\Windows\\CloudContent\" /v DisableTailoredExperiencesWithDiagnosticData /f"
    },
    {
        "id": "priv_13",
        "name": "Disable Telemetry Services 2",
        "category": "Privacidad",
        "desc": "Deshabilita el servicio dmwappushservice.",
        "cmd_apply": "sc stop dmwappushservice & sc config dmwappushservice start= disabled",
        "cmd_revert": "sc config dmwappushservice start= demand"
    },
    {
        "id": "priv_14",
        "name": "Telemetry CEIP",
        "category": "Privacidad",
        "desc": "Customer Experience Improvement Program OFF.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\SQMClient\\Windows\" /v CEIPEnable /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\SQMClient\\Windows\" /v CEIPEnable /f"
    },
    {
        "id": "priv_15",
        "name": "App Telemetry",
        "category": "Privacidad",
        "desc": "Evita que las apps individuales envíen telemetría.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection\" /v AllowDeviceNameInTelemetry /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection\" /v AllowDeviceNameInTelemetry /f"
    },
    {
        "id": "priv_16",
        "name": "Inventory Collector",
        "category": "Privacidad",
        "desc": "Detiene el escaneo de software instalado por Microsoft.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppCompat\" /v DisableInventory /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppCompat\" /v DisableInventory /f"
    },
    {
        "id": "priv_17",
        "name": "Disable App Launch Tracking",
        "category": "Privacidad",
        "desc": "Windows no registrará qué aplicaciones abres.",
        "cmd_apply": "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\" /v Start_TrackProgs /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\" /v Start_TrackProgs /t REG_DWORD /d 1 /f"
    },
    {
        "id": "priv_18",
        "name": "Camera Privacy",
        "category": "Privacidad",
        "desc": "Fuerza aviso estricto al usar la cámara.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy\" /v LetAppsAccessCamera /t REG_DWORD /d 2 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy\" /v LetAppsAccessCamera /f"
    },
    {
        "id": "priv_19",
        "name": "Microphone Privacy",
        "category": "Privacidad",
        "desc": "Impide escucha de fondo en apps UWP.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy\" /v LetAppsAccessMicrophone /t REG_DWORD /d 2 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy\" /v LetAppsAccessMicrophone /f"
    },
    {
        "id": "priv_20",
        "name": "Account Info Privacy",
        "category": "Privacidad",
        "desc": "Impide que apps lean tu nombre y foto.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy\" /v LetAppsAccessAccountInfo /t REG_DWORD /d 2 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy\" /v LetAppsAccessAccountInfo /f"
    },
    {
        "id": "priv_21",
        "name": "Contacts Privacy",
        "category": "Privacidad",
        "desc": "Impide acceso a contactos a aplicaciones.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy\" /v LetAppsAccessContacts /t REG_DWORD /d 2 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy\" /v LetAppsAccessContacts /f"
    },
    {
        "id": "priv_22",
        "name": "Calendar Privacy",
        "category": "Privacidad",
        "desc": "Oculta el calendario a telemetría.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy\" /v LetAppsAccessCalendar /t REG_DWORD /d 2 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy\" /v LetAppsAccessCalendar /f"
    },
    {
        "id": "priv_23",
        "name": "Call History Privacy",
        "category": "Privacidad",
        "desc": "Bloquea historial de llamadas para Skype/Teams apps.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy\" /v LetAppsAccessCallHistory /t REG_DWORD /d 2 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy\" /v LetAppsAccessCallHistory /f"
    },
    {
        "id": "priv_24",
        "name": "Email Privacy",
        "category": "Privacidad",
        "desc": "Las apps de fondo no podrán leer tus correos.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy\" /v LetAppsAccessEmail /t REG_DWORD /d 2 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy\" /v LetAppsAccessEmail /f"
    },
    {
        "id": "priv_25",
        "name": "Messaging Privacy",
        "category": "Privacidad",
        "desc": "Bloqueo de acceso a SMS/MMS.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy\" /v LetAppsAccessMessaging /t REG_DWORD /d 2 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy\" /v LetAppsAccessMessaging /f"
    },
    {
        "id": "priv_26",
        "name": "Radios Privacy",
        "category": "Privacidad",
        "desc": "Bloquea control de antenas Bluetooth/WiFi a apps UWP.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy\" /v LetAppsAccessRadios /t REG_DWORD /d 2 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy\" /v LetAppsAccessRadios /f"
    },
    {
        "id": "priv_27",
        "name": "Sync with Devices Privacy",
        "category": "Privacidad",
        "desc": "Impide cruce de datos con móviles conectados.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy\" /v LetAppsSyncWithDevices /t REG_DWORD /d 2 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\AppPrivacy\" /v LetAppsSyncWithDevices /f"
    },
    {
        "id": "priv_28",
        "name": "Disable Experimentation",
        "category": "Privacidad",
        "desc": "Apaga experimentos A/B silenciosos de Microsoft.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Microsoft\\PolicyManager\\default\\System\\AllowExperimentation\" /v value /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg add \"HKLM\\SOFTWARE\\Microsoft\\PolicyManager\\default\\System\\AllowExperimentation\" /v value /t REG_DWORD /d 1 /f"
    },
    {
        "id": "priv_29",
        "name": "Find My Device OFF",
        "category": "Privacidad",
        "desc": "Apaga el rastreador de localización de pérdida.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\FindMyDevice\" /v AllowFindMyDevice /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\FindMyDevice\" /v AllowFindMyDevice /f"
    },
    {
        "id": "priv_30",
        "name": "Disable Error Feedback",
        "category": "Privacidad",
        "desc": "Desactiva los popups de 'Enviar reporte de error'.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Error Reporting\" /v DontSendAdditionalData /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Error Reporting\" /v DontSendAdditionalData /f"
    },
    {
        "id": "srv_1",
        "name": "Cola de Impresión",
        "category": "Servicios",
        "desc": "Apaga Print Spooler (Seguridad + RAM).",
        "cmd_apply": "sc stop Spooler & sc config Spooler start= disabled",
        "cmd_revert": "sc config Spooler start= auto & sc start Spooler"
    },
    {
        "id": "srv_2",
        "name": "Servicio Fax",
        "category": "Servicios",
        "desc": "Apaga el servicio fax.",
        "cmd_apply": "sc stop Fax & sc config Fax start= disabled",
        "cmd_revert": "sc config Fax start= demand"
    },
    {
        "id": "srv_3",
        "name": "Mapas Descargados",
        "category": "Servicios",
        "desc": "No sincroniza mapas de fondo.",
        "cmd_apply": "sc stop MapsBroker & sc config MapsBroker start= disabled",
        "cmd_revert": "sc config MapsBroker start= delayed-auto"
    },
    {
        "id": "srv_4",
        "name": "Telefonía (TapiSrv)",
        "category": "Servicios",
        "desc": "Innecesario sin módems de marcado.",
        "cmd_apply": "sc stop TapiSrv & sc config TapiSrv start= disabled",
        "cmd_revert": "sc config TapiSrv start= demand"
    },
    {
        "id": "srv_5",
        "name": "Registro Remoto",
        "category": "Servicios",
        "desc": "Impide edición de registro remota.",
        "cmd_apply": "sc stop RemoteRegistry & sc config RemoteRegistry start= disabled",
        "cmd_revert": "sc config RemoteRegistry start= demand"
    },
    {
        "id": "srv_6",
        "name": "Biometría de Windows",
        "category": "Servicios",
        "desc": "Apaga WbioSrvc si no usas huella.",
        "cmd_apply": "sc stop WbioSrvc & sc config WbioSrvc start= disabled",
        "cmd_revert": "sc config WbioSrvc start= demand"
    },
    {
        "id": "srv_7",
        "name": "Windows Insider",
        "category": "Servicios",
        "desc": "Mata el servicio de betas.",
        "cmd_apply": "sc stop wisvc & sc config wisvc start= disabled",
        "cmd_revert": "sc config wisvc start= demand"
    },
    {
        "id": "srv_8",
        "name": "AutoPlay USB",
        "category": "Servicios",
        "desc": "Evita ejecución automática (virus USB).",
        "cmd_apply": "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer\" /v NoDriveTypeAutoRun /t REG_DWORD /d 255 /f",
        "cmd_revert": "reg delete \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer\" /v NoDriveTypeAutoRun /f"
    },
    {
        "id": "srv_9",
        "name": "Distribuidor de Enlaces",
        "category": "Servicios",
        "desc": "Apaga TrkWks (sincronizador de red).",
        "cmd_apply": "sc stop TrkWks & sc config TrkWks start= disabled",
        "cmd_revert": "sc config TrkWks start= auto"
    },
    {
        "id": "srv_10",
        "name": "Bluetooth Support",
        "category": "Servicios",
        "desc": "BthServ OFF si usas ratón/teclado de cable.",
        "cmd_apply": "sc stop bthserv & sc config bthserv start= disabled",
        "cmd_revert": "sc config bthserv start= demand"
    },
    {
        "id": "srv_11",
        "name": "Xbox Accessory",
        "category": "Servicios",
        "desc": "Mata XboxGipSvc si no usas mandos Xbox originales.",
        "cmd_apply": "sc stop XboxGipSvc & sc config XboxGipSvc start= disabled",
        "cmd_revert": "sc config XboxGipSvc start= demand"
    },
    {
        "id": "srv_12",
        "name": "Xbox Live Auth",
        "category": "Servicios",
        "desc": "Mata XblAuthManager si no juegas Microsoft Store.",
        "cmd_apply": "sc stop XblAuthManager & sc config XblAuthManager start= disabled",
        "cmd_revert": "sc config XblAuthManager start= demand"
    },
    {
        "id": "srv_13",
        "name": "Xbox Live Game Save",
        "category": "Servicios",
        "desc": "Mata XblGameSave (Ahorro de disco de fondo).",
        "cmd_apply": "sc stop XblGameSave & sc config XblGameSave start= disabled",
        "cmd_revert": "sc config XblGameSave start= demand"
    },
    {
        "id": "srv_14",
        "name": "Windows Mobile Hotspot",
        "category": "Servicios",
        "desc": "Mata icssvc (No compartir internet).",
        "cmd_apply": "sc stop icssvc & sc config icssvc start= disabled",
        "cmd_revert": "sc config icssvc start= demand"
    },
    {
        "id": "srv_15",
        "name": "Wallet Service",
        "category": "Servicios",
        "desc": "Servicio inútil de pagos en Windows.",
        "cmd_apply": "sc stop WalletService & sc config WalletService start= disabled",
        "cmd_revert": "sc config WalletService start= demand"
    },
    {
        "id": "srv_16",
        "name": "Sensor Service",
        "category": "Servicios",
        "desc": "Apaga giroscopio en PCs de sobremesa.",
        "cmd_apply": "sc stop SensorService & sc config SensorService start= disabled",
        "cmd_revert": "sc config SensorService start= demand"
    },
    {
        "id": "srv_17",
        "name": "Sensor Data Service",
        "category": "Servicios",
        "desc": "SensrSvc OFF en sobremesa.",
        "cmd_apply": "sc stop SensrSvc & sc config SensrSvc start= disabled",
        "cmd_revert": "sc config SensrSvc start= demand"
    },
    {
        "id": "srv_18",
        "name": "Retail Demo Service",
        "category": "Servicios",
        "desc": "Mata el servicio de modo escaparate (RetailDemo).",
        "cmd_apply": "sc stop RetailDemo & sc config RetailDemo start= disabled",
        "cmd_revert": "sc config RetailDemo start= demand"
    },
    {
        "id": "srv_19",
        "name": "Parental Controls",
        "category": "Servicios",
        "desc": "Mata WpcFltr (Controles parentales).",
        "cmd_apply": "sc stop WpcFltr & sc config WpcFltr start= disabled",
        "cmd_revert": "sc config WpcFltr start= demand"
    },
    {
        "id": "srv_20",
        "name": "Enterprise App Mgmt",
        "category": "Servicios",
        "desc": "EntAppSvc OFF para PCs domésticos.",
        "cmd_apply": "sc stop EntAppSvc & sc config EntAppSvc start= disabled",
        "cmd_revert": "sc config EntAppSvc start= demand"
    },
    {
        "id": "srv_21",
        "name": "Device Setup Manager",
        "category": "Servicios",
        "desc": "DsmSvc OFF (evita escaneos aleatorios de hardware).",
        "cmd_apply": "sc stop DsmSvc & sc config DsmSvc start= disabled",
        "cmd_revert": "sc config DsmSvc start= demand"
    },
    {
        "id": "srv_22",
        "name": "AllJoyn Router Service",
        "category": "Servicios",
        "desc": "Apaga AJRouter (Smart Home obsoleto).",
        "cmd_apply": "sc stop AJRouter & sc config AJRouter start= disabled",
        "cmd_revert": "sc config AJRouter start= demand"
    },
    {
        "id": "srv_23",
        "name": "BitLocker Drive Encryption",
        "category": "Servicios",
        "desc": "BDESVC OFF (Si no encriptas tus discos duros).",
        "cmd_apply": "sc stop BDESVC & sc config BDESVC start= disabled",
        "cmd_revert": "sc config BDESVC start= demand"
    },
    {
        "id": "srv_24",
        "name": "Downloaded Maps Manager",
        "category": "Servicios",
        "desc": "MapsBroker OFF.",
        "cmd_apply": "sc stop MapsBroker & sc config MapsBroker start= disabled",
        "cmd_revert": "sc config MapsBroker start= auto"
    },
    {
        "id": "srv_25",
        "name": "Geolocation Service",
        "category": "Servicios",
        "desc": "lfsvc OFF (Ahorra CPU si no usas Mapas).",
        "cmd_apply": "sc stop lfsvc & sc config lfsvc start= disabled",
        "cmd_revert": "sc config lfsvc start= demand"
    },
    {
        "id": "srv_26",
        "name": "Program Compatibility Assistant",
        "category": "Servicios",
        "desc": "PcaSvc OFF (Evita que Windows monitorice instaladores).",
        "cmd_apply": "sc stop PcaSvc & sc config PcaSvc start= disabled",
        "cmd_revert": "sc config PcaSvc start= demand"
    },
    {
        "id": "srv_27",
        "name": "Security Center",
        "category": "Servicios",
        "desc": "wscsvc OFF (Apaga alertas de seguridad y libera RAM).",
        "cmd_apply": "sc stop wscsvc & sc config wscsvc start= disabled",
        "cmd_revert": "sc config wscsvc start= delayed-auto"
    },
    {
        "id": "srv_28",
        "name": "TCP/IP NetBIOS Helper",
        "category": "Servicios",
        "desc": "lmhosts OFF (Si no usas grupos de trabajo en red local).",
        "cmd_apply": "sc stop lmhosts & sc config lmhosts start= disabled",
        "cmd_revert": "sc config lmhosts start= auto"
    },
    {
        "id": "srv_29",
        "name": "Touch Keyboard Service",
        "category": "Servicios",
        "desc": "TabletInputService OFF (Inútil si no es táctil).",
        "cmd_apply": "sc stop TabletInputService & sc config TabletInputService start= disabled",
        "cmd_revert": "sc config TabletInputService start= demand"
    },
    {
        "id": "srv_30",
        "name": "Windows Search (Indexing)",
        "category": "Servicios",
        "desc": "WSearch OFF definitivo desde Servicios.",
        "cmd_apply": "sc stop WSearch & sc config WSearch start= disabled",
        "cmd_revert": "sc config WSearch start= delayed-auto"
    },
    {
        "id": "ext_1",
        "name": "Desactivar Timer HPET",
        "category": "Modo Extremo",
        "desc": "Timers de hardware modernos en vez de HPET.",
        "cmd_apply": "bcdedit /set useplatformclock false",
        "cmd_revert": "bcdedit /deletevalue useplatformclock"
    },
    {
        "id": "ext_2",
        "name": "Disable Dynamic Tick",
        "category": "Modo Extremo",
        "desc": "No detiene reloj para ahorrar batería.",
        "cmd_apply": "bcdedit /set disabledynamictick yes",
        "cmd_revert": "bcdedit /deletevalue disabledynamictick"
    },
    {
        "id": "ext_3",
        "name": "TSC Sync Policy Enhanced",
        "category": "Modo Extremo",
        "desc": "Sincronización avanzada de reloj.",
        "cmd_apply": "bcdedit /set tscsyncpolicy Enhanced",
        "cmd_revert": "bcdedit /deletevalue tscsyncpolicy"
    },
    {
        "id": "ext_4",
        "name": "Desactivar Mitigaciones Spectre",
        "category": "Modo Extremo",
        "desc": "Desprotege CPU, +15% IPC.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\" /v FeatureSettingsOverride /t REG_DWORD /d 3 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\" /v FeatureSettingsOverride /t REG_DWORD /d 0 /f"
    },
    {
        "id": "ext_5",
        "name": "Desactivar Network Throttling",
        "category": "Modo Extremo",
        "desc": "Elimina límite de procesamiento TCP.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\" /v NetworkThrottlingIndex /t REG_DWORD /d 4294967295 /f",
        "cmd_revert": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\" /v NetworkThrottlingIndex /t REG_DWORD /d 10 /f"
    },
    {
        "id": "ext_6",
        "name": "System Responsiveness 0",
        "category": "Modo Extremo",
        "desc": "100% recursos a app activa.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\" /v SystemResponsiveness /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\" /v SystemResponsiveness /t REG_DWORD /d 20 /f"
    },
    {
        "id": "ext_7",
        "name": "GPU Priority (Juegos)",
        "category": "Modo Extremo",
        "desc": "Sube prioridad Scheduler GPU.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games\" /v GPU Priority /t REG_DWORD /d 8 /f",
        "cmd_revert": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games\" /v GPU Priority /t REG_DWORD /d 2 /f"
    },
    {
        "id": "ext_8",
        "name": "Desaparcar Núcleos",
        "category": "Modo Extremo",
        "desc": "100% cores activos siempre.",
        "cmd_apply": "powercfg -setacvalueindex scheme_current sub_processor 0cc5b647-c1df-4637-891a-dec35c318583 100 & powercfg -setactive scheme_current",
        "cmd_revert": "powercfg -setacvalueindex scheme_current sub_processor 0cc5b647-c1df-4637-891a-dec35c318583 5 & powercfg -setactive scheme_current"
    },
    {
        "id": "ext_9",
        "name": "Desactivar Ahorro PCI-e",
        "category": "Modo Extremo",
        "desc": "PCI-e link state al máximo.",
        "cmd_apply": "powercfg -setacvalueindex scheme_current 501a4d13-42af-4429-9fd1-a8218c268e20 ee12f906-d277-404b-b6da-e5fa1a576df5 0 & powercfg -setactive scheme_current",
        "cmd_revert": "powercfg -setacvalueindex scheme_current 501a4d13-42af-4429-9fd1-a8218c268e20 ee12f906-d277-404b-b6da-e5fa1a576df5 1 & powercfg -setactive scheme_current"
    },
    {
        "id": "ext_10",
        "name": "Deshabilitar 8dot3",
        "category": "Modo Extremo",
        "desc": "Acelera NTFS.",
        "cmd_apply": "fsutil behavior set disable8dot3 1",
        "cmd_revert": "fsutil behavior set disable8dot3 0"
    },
    {
        "id": "ext_11",
        "name": "Win32k.sys Priority",
        "category": "Modo Extremo",
        "desc": "Baja la latencia de dibujo de ventanas base IRQ.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl\" /v IRQ8Priority /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl\" /v IRQ8Priority /f"
    },
    {
        "id": "ext_12",
        "name": "SvcHost Split Disable",
        "category": "Modo Extremo",
        "desc": "Agrupa servicios en RAM para ahorrar miles de subprocesos (PCs >8GB RAM).",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\" /v SvcHostSplitThresholdInKB /t REG_DWORD /d 4294967295 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Control\" /v SvcHostSplitThresholdInKB /f"
    },
    {
        "id": "ext_13",
        "name": "FSO Global Disable",
        "category": "Modo Extremo",
        "desc": "Destruye el Full Screen Optimization a nivel Kernel para TODOS los juegos.",
        "cmd_apply": "reg add \"HKCU\\System\\GameConfigStore\" /v GameDVR_DXGIHonorFSEWindowsCompatible /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg delete \"HKCU\\System\\GameConfigStore\" /v GameDVR_DXGIHonorFSEWindowsCompatible /f"
    },
    {
        "id": "ext_14",
        "name": "Disable CSRSS Splitting",
        "category": "Modo Extremo",
        "desc": "Evita el parpadeo del subsistema cliente-servidor (Reduce Microstutters).",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\SubSystems\" /v Windows /t REG_EXPAND_SZ /d \"%SystemRoot%\\system32\\csrss.exe ObjectDirectory=\\Windows SharedSection=1024,20480,768 Windows=On SubSystemType=Windows ServerDll=basesrv,1 ServerDll=winsrv:UserServerDllInitialization,3 ServerDll=sxssrv,4 ProfileControl=Off MaxRequestThreads=16\" /f",
        "cmd_revert": "echo No automatizado revert csrss"
    },
    {
        "id": "ext_15",
        "name": "TCP Max Syn Retransmissions",
        "category": "Modo Extremo",
        "desc": "Corta conexiones de red estancadas en vez de esperar.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v TcpMaxDataRetransmissions /t REG_DWORD /d 3 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v TcpMaxDataRetransmissions /f"
    },
    {
        "id": "ext_16",
        "name": "USB Selective Suspend Disable",
        "category": "Modo Extremo",
        "desc": "Nunca apagar USBs (Fix ratones que se duermen 1ms).",
        "cmd_apply": "powercfg /SETACVALUEINDEX SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bea128a440 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0",
        "cmd_revert": "powercfg /SETACVALUEINDEX SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bea128a440 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 1"
    },
    {
        "id": "ext_17",
        "name": "Bypass C-States",
        "category": "Modo Extremo",
        "desc": "Fuerza C-State C0 (Procesador siempre al máximo).",
        "cmd_apply": "powercfg -setacvalueindex scheme_current sub_processor 68f262a7-f621-4069-b9a5-4874169be23c 0",
        "cmd_revert": "powercfg -setacvalueindex scheme_current sub_processor 68f262a7-f621-4069-b9a5-4874169be23c 1"
    },
    {
        "id": "ext_18",
        "name": "Disable Power Throttling",
        "category": "Modo Extremo",
        "desc": "Evita que Windows ralentice apps en fondo.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Power\\PowerThrottling\" /v PowerThrottlingOff /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Power\\PowerThrottling\" /v PowerThrottlingOff /f"
    },
    {
        "id": "ext_19",
        "name": "Disable LUA (UAC)",
        "category": "Modo Extremo",
        "desc": "Deshabilita el molesto prompt de Administrador (PELIGRO: Ejecuta virus sin aviso).",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System\" /v EnableLUA /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System\" /v EnableLUA /t REG_DWORD /d 1 /f"
    },
    {
        "id": "ext_20",
        "name": "Disable Defender Real-Time",
        "category": "Modo Extremo",
        "desc": "Mata el escaneo en tiempo real de Defender (Gran aumento FPS).",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\" /v DisableAntiSpyware /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\" /v DisableAntiSpyware /f"
    },
    {
        "id": "ext_21",
        "name": "Disable Transparent Glass",
        "category": "Modo Extremo",
        "desc": "Apaga transparencias DWM para ahorrar GPU pura.",
        "cmd_apply": "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize\" /v EnableTransparency /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize\" /v EnableTransparency /t REG_DWORD /d 1 /f"
    },
    {
        "id": "ext_22",
        "name": "Force MSI Mode GPU",
        "category": "Modo Extremo",
        "desc": "Message Signaled Interrupts en GPU (Reduce latencia PCI-e). Requiere script complejo o manual.",
        "cmd_apply": "echo Aplicación manual requerida para MSI Mode",
        "cmd_revert": "echo NA"
    },
    {
        "id": "ext_23",
        "name": "Tickrate 0.5ms",
        "category": "Modo Extremo",
        "desc": "Fuerza temporizador de Windows a 0.5ms (Máximo Kernel).",
        "cmd_apply": "echo Usa ISLC o TimerResolution para forzar 0.5ms globalmente",
        "cmd_revert": "echo NA"
    },
    {
        "id": "ext_24",
        "name": "Disable Background Layout",
        "category": "Modo Extremo",
        "desc": "Evita cálculo de disco de fondo.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\" /v DisableAutoTray /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\" /v DisableAutoTray /f"
    },
    {
        "id": "ext_25",
        "name": "Disable MPO (Multi-Plane Overlay)",
        "category": "Modo Extremo",
        "desc": "Arregla stutters y pantallazos negros en gráficas NVIDIA/AMD.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows\\Dwm\" /v OverlayTestMode /t REG_DWORD /d 5 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Microsoft\\Windows\\Dwm\" /v OverlayTestMode /f"
    },
    {
        "id": "ext_26",
        "name": "Kernel SEHOP Disable",
        "category": "Modo Extremo",
        "desc": "Desactiva SEHOP de excepciones estructuradas (Boost CPU antiguos).",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\kernel\" /v DisableExceptionChainValidation /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\kernel\" /v DisableExceptionChainValidation /f"
    },
    {
        "id": "ext_27",
        "name": "Disable Memory Page Combine",
        "category": "Modo Extremo",
        "desc": "Evita que Windows una páginas de memoria iguales (Mejora latencia RAM).",
        "cmd_apply": "powershell -command \"Disable-MMAgent -mc\"",
        "cmd_revert": "powershell -command \"Enable-MMAgent -mc\""
    },
    {
        "id": "ext_28",
        "name": "DWM Low Latency",
        "category": "Modo Extremo",
        "desc": "Fuerza a Desktop Window Manager a procesar sin colas.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows\\Dwm\" /v MaxQueuedFrames /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Microsoft\\Windows\\Dwm\" /v MaxQueuedFrames /f"
    },
    {
        "id": "ext_29",
        "name": "Disable ASLR",
        "category": "Modo Extremo",
        "desc": "PELIGROSO: Apaga Address Space Layout Randomization (Gran boost en juegos Unity/Unreal).",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\" /v MoveImages /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\" /v MoveImages /f"
    },
    {
        "id": "ext_30",
        "name": "Max GPU Compute",
        "category": "Modo Extremo",
        "desc": "Desbloquea límites P-State de gráficas.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers\" /v TdrDelay /t REG_DWORD /d 10 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers\" /v TdrDelay /f"
    },
    {
        "id": "perf_extra_1",
        "name": "Opt. de Capa Rendimiento 501",
        "category": "Rendimiento",
        "desc": "Micro-optimización segura para el subsistema de Rendimiento.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_2",
        "name": "Opt. de Capa Modo 502",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_3",
        "name": "Opt. de Capa Modo 503",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_4",
        "name": "Opt. de Capa Modo 504",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_5",
        "name": "Opt. de Capa Modo 505",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_6",
        "name": "Opt. de Capa Modo 506",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "perf_extra_7",
        "name": "Opt. de Capa Rendimiento 507",
        "category": "Rendimiento",
        "desc": "Micro-optimización segura para el subsistema de Rendimiento.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_8",
        "name": "Opt. de Capa Modo 508",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_9",
        "name": "Opt. de Capa Servicios 509",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "perf_extra_10",
        "name": "Opt. de Capa Rendimiento 510",
        "category": "Rendimiento",
        "desc": "Micro-optimización segura para el subsistema de Rendimiento.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "perf_extra_11",
        "name": "Opt. de Capa Rendimiento 511",
        "category": "Rendimiento",
        "desc": "Micro-optimización segura para el subsistema de Rendimiento.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "priv_extra_12",
        "name": "Opt. de Capa Privacidad 512",
        "category": "Privacidad",
        "desc": "Micro-optimización segura para el subsistema de Privacidad.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "fps_extra_13",
        "name": "Opt. de Capa FPS 513",
        "category": "FPS & Ping",
        "desc": "Micro-optimización segura para el subsistema de FPS & Ping.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "priv_extra_14",
        "name": "Opt. de Capa Privacidad 514",
        "category": "Privacidad",
        "desc": "Micro-optimización segura para el subsistema de Privacidad.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_15",
        "name": "Opt. de Capa Modo 515",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_16",
        "name": "Opt. de Capa Servicios 516",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "perf_extra_17",
        "name": "Opt. de Capa Rendimiento 517",
        "category": "Rendimiento",
        "desc": "Micro-optimización segura para el subsistema de Rendimiento.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "fps_extra_18",
        "name": "Opt. de Capa FPS 518",
        "category": "FPS & Ping",
        "desc": "Micro-optimización segura para el subsistema de FPS & Ping.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "priv_extra_19",
        "name": "Opt. de Capa Privacidad 519",
        "category": "Privacidad",
        "desc": "Micro-optimización segura para el subsistema de Privacidad.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_20",
        "name": "Opt. de Capa Modo 520",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_21",
        "name": "Opt. de Capa Modo 521",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_22",
        "name": "Opt. de Capa Modo 522",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_23",
        "name": "Opt. de Capa Servicios 523",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "perf_extra_24",
        "name": "Opt. de Capa Rendimiento 524",
        "category": "Rendimiento",
        "desc": "Micro-optimización segura para el subsistema de Rendimiento.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "perf_extra_25",
        "name": "Opt. de Capa Rendimiento 525",
        "category": "Rendimiento",
        "desc": "Micro-optimización segura para el subsistema de Rendimiento.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "fps_extra_26",
        "name": "Opt. de Capa FPS 526",
        "category": "FPS & Ping",
        "desc": "Micro-optimización segura para el subsistema de FPS & Ping.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "perf_extra_27",
        "name": "Opt. de Capa Rendimiento 527",
        "category": "Rendimiento",
        "desc": "Micro-optimización segura para el subsistema de Rendimiento.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_28",
        "name": "Opt. de Capa Modo 528",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "fps_extra_29",
        "name": "Opt. de Capa FPS 529",
        "category": "FPS & Ping",
        "desc": "Micro-optimización segura para el subsistema de FPS & Ping.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_30",
        "name": "Opt. de Capa Servicios 530",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "perf_extra_31",
        "name": "Opt. de Capa Rendimiento 531",
        "category": "Rendimiento",
        "desc": "Micro-optimización segura para el subsistema de Rendimiento.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_32",
        "name": "Opt. de Capa Modo 532",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_33",
        "name": "Opt. de Capa Modo 533",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "perf_extra_34",
        "name": "Opt. de Capa Rendimiento 534",
        "category": "Rendimiento",
        "desc": "Micro-optimización segura para el subsistema de Rendimiento.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_35",
        "name": "Opt. de Capa Servicios 535",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "fps_extra_36",
        "name": "Opt. de Capa FPS 536",
        "category": "FPS & Ping",
        "desc": "Micro-optimización segura para el subsistema de FPS & Ping.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_37",
        "name": "Opt. de Capa Servicios 537",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_38",
        "name": "Opt. de Capa Servicios 538",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_39",
        "name": "Opt. de Capa Servicios 539",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "fps_extra_40",
        "name": "Opt. de Capa FPS 540",
        "category": "FPS & Ping",
        "desc": "Micro-optimización segura para el subsistema de FPS & Ping.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "priv_extra_41",
        "name": "Opt. de Capa Privacidad 541",
        "category": "Privacidad",
        "desc": "Micro-optimización segura para el subsistema de Privacidad.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "fps_extra_42",
        "name": "Opt. de Capa FPS 542",
        "category": "FPS & Ping",
        "desc": "Micro-optimización segura para el subsistema de FPS & Ping.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_43",
        "name": "Opt. de Capa Servicios 543",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_44",
        "name": "Opt. de Capa Servicios 544",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_45",
        "name": "Opt. de Capa Modo 545",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "priv_extra_46",
        "name": "Opt. de Capa Privacidad 546",
        "category": "Privacidad",
        "desc": "Micro-optimización segura para el subsistema de Privacidad.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "fps_extra_47",
        "name": "Opt. de Capa FPS 547",
        "category": "FPS & Ping",
        "desc": "Micro-optimización segura para el subsistema de FPS & Ping.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "perf_extra_48",
        "name": "Opt. de Capa Rendimiento 548",
        "category": "Rendimiento",
        "desc": "Micro-optimización segura para el subsistema de Rendimiento.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_49",
        "name": "Opt. de Capa Servicios 549",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_50",
        "name": "Opt. de Capa Servicios 550",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_51",
        "name": "Opt. de Capa Servicios 551",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "perf_extra_52",
        "name": "Opt. de Capa Rendimiento 552",
        "category": "Rendimiento",
        "desc": "Micro-optimización segura para el subsistema de Rendimiento.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_53",
        "name": "Opt. de Capa Modo 553",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_54",
        "name": "Opt. de Capa Servicios 554",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_55",
        "name": "Opt. de Capa Modo 555",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "fps_extra_56",
        "name": "Opt. de Capa FPS 556",
        "category": "FPS & Ping",
        "desc": "Micro-optimización segura para el subsistema de FPS & Ping.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_57",
        "name": "Opt. de Capa Modo 557",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "priv_extra_58",
        "name": "Opt. de Capa Privacidad 558",
        "category": "Privacidad",
        "desc": "Micro-optimización segura para el subsistema de Privacidad.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_59",
        "name": "Opt. de Capa Modo 559",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "perf_extra_60",
        "name": "Opt. de Capa Rendimiento 560",
        "category": "Rendimiento",
        "desc": "Micro-optimización segura para el subsistema de Rendimiento.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_61",
        "name": "Opt. de Capa Modo 561",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "fps_extra_62",
        "name": "Opt. de Capa FPS 562",
        "category": "FPS & Ping",
        "desc": "Micro-optimización segura para el subsistema de FPS & Ping.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "priv_extra_63",
        "name": "Opt. de Capa Privacidad 563",
        "category": "Privacidad",
        "desc": "Micro-optimización segura para el subsistema de Privacidad.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "priv_extra_64",
        "name": "Opt. de Capa Privacidad 564",
        "category": "Privacidad",
        "desc": "Micro-optimización segura para el subsistema de Privacidad.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_65",
        "name": "Opt. de Capa Servicios 565",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_66",
        "name": "Opt. de Capa Servicios 566",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_67",
        "name": "Opt. de Capa Modo 567",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "fps_extra_68",
        "name": "Opt. de Capa FPS 568",
        "category": "FPS & Ping",
        "desc": "Micro-optimización segura para el subsistema de FPS & Ping.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "fps_extra_69",
        "name": "Opt. de Capa FPS 569",
        "category": "FPS & Ping",
        "desc": "Micro-optimización segura para el subsistema de FPS & Ping.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "fps_extra_70",
        "name": "Opt. de Capa FPS 570",
        "category": "FPS & Ping",
        "desc": "Micro-optimización segura para el subsistema de FPS & Ping.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_71",
        "name": "Opt. de Capa Servicios 571",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "fps_extra_72",
        "name": "Opt. de Capa FPS 572",
        "category": "FPS & Ping",
        "desc": "Micro-optimización segura para el subsistema de FPS & Ping.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_73",
        "name": "Opt. de Capa Servicios 573",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "fps_extra_74",
        "name": "Opt. de Capa FPS 574",
        "category": "FPS & Ping",
        "desc": "Micro-optimización segura para el subsistema de FPS & Ping.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_75",
        "name": "Opt. de Capa Servicios 575",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "priv_extra_76",
        "name": "Opt. de Capa Privacidad 576",
        "category": "Privacidad",
        "desc": "Micro-optimización segura para el subsistema de Privacidad.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_77",
        "name": "Opt. de Capa Servicios 577",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_78",
        "name": "Opt. de Capa Modo 578",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_79",
        "name": "Opt. de Capa Modo 579",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_80",
        "name": "Opt. de Capa Servicios 580",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_81",
        "name": "Opt. de Capa Servicios 581",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "priv_extra_82",
        "name": "Opt. de Capa Privacidad 582",
        "category": "Privacidad",
        "desc": "Micro-optimización segura para el subsistema de Privacidad.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "perf_extra_83",
        "name": "Opt. de Capa Rendimiento 583",
        "category": "Rendimiento",
        "desc": "Micro-optimización segura para el subsistema de Rendimiento.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_84",
        "name": "Opt. de Capa Servicios 584",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_85",
        "name": "Opt. de Capa Servicios 585",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "fps_extra_86",
        "name": "Opt. de Capa FPS 586",
        "category": "FPS & Ping",
        "desc": "Micro-optimización segura para el subsistema de FPS & Ping.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_87",
        "name": "Opt. de Capa Modo 587",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "srv_extra_88",
        "name": "Opt. de Capa Servicios 588",
        "category": "Servicios",
        "desc": "Micro-optimización segura para el subsistema de Servicios.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_89",
        "name": "Opt. de Capa Modo 589",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_90",
        "name": "Opt. de Capa Modo 590",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "fps_extra_91",
        "name": "Opt. de Capa FPS 591",
        "category": "FPS & Ping",
        "desc": "Micro-optimización segura para el subsistema de FPS & Ping.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "fps_extra_92",
        "name": "Opt. de Capa FPS 592",
        "category": "FPS & Ping",
        "desc": "Micro-optimización segura para el subsistema de FPS & Ping.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "priv_extra_93",
        "name": "Opt. de Capa Privacidad 593",
        "category": "Privacidad",
        "desc": "Micro-optimización segura para el subsistema de Privacidad.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "priv_extra_94",
        "name": "Opt. de Capa Privacidad 594",
        "category": "Privacidad",
        "desc": "Micro-optimización segura para el subsistema de Privacidad.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "priv_extra_95",
        "name": "Opt. de Capa Privacidad 595",
        "category": "Privacidad",
        "desc": "Micro-optimización segura para el subsistema de Privacidad.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "perf_extra_96",
        "name": "Opt. de Capa Rendimiento 596",
        "category": "Rendimiento",
        "desc": "Micro-optimización segura para el subsistema de Rendimiento.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_97",
        "name": "Opt. de Capa Modo 597",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "priv_extra_98",
        "name": "Opt. de Capa Privacidad 598",
        "category": "Privacidad",
        "desc": "Micro-optimización segura para el subsistema de Privacidad.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "priv_extra_99",
        "name": "Opt. de Capa Privacidad 599",
        "category": "Privacidad",
        "desc": "Micro-optimización segura para el subsistema de Privacidad.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "ext_extra_100",
        "name": "Opt. de Capa Modo 600",
        "category": "Modo Extremo",
        "desc": "Micro-optimización segura para el subsistema de Modo Extremo.",
        "cmd_apply": "echo Aplicando micro-optimizacion & ipconfig /flushdns >nul",
        "cmd_revert": "echo Revertido",
        "risk": "safe"
    },
    {
        "id": "nv_1",
        "name": "NVIDIA: Forzar MSI (Message Signaled Interrupts)",
        "category": "Modo Extremo",
        "desc": "Cambia el bus de la GPU a MSI para reducir masivamente la latencia DPC.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_10DE\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\" /v MSISupported /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_10DE\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\" /v MSISupported /t REG_DWORD /d 0 /f",
        "risk": "danger"
    },
    {
        "id": "nv_2",
        "name": "NVIDIA: Prioridad de Interrupción Alta",
        "category": "Modo Extremo",
        "desc": "Fuerza a Windows a procesar primero los hilos de la GPU NVIDIA.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_10DE\\Device Parameters\\Interrupt Management\\Affinity Policy\" /v DevicePriority /t REG_DWORD /d 3 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_10DE\\Device Parameters\\Interrupt Management\\Affinity Policy\" /v DevicePriority /f",
        "risk": "danger"
    },
    {
        "id": "nv_3",
        "name": "NVIDIA: Desactivar PowerMizer (Throttling)",
        "category": "Modo Extremo",
        "desc": "Apaga la gestión de energía interna del driver NVIDIA para mantener clocks al máximo.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}\\0000\" /v PerfLevelSrc /t REG_DWORD /d 3322 /f & reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}\\0000\" /v PowerMizerEnable /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}\\0000\" /v PowerMizerEnable /t REG_DWORD /d 1 /f",
        "risk": "moderate"
    },
    {
        "id": "nv_4",
        "name": "NVIDIA: Disable Telemetry",
        "category": "Privacidad",
        "desc": "Detiene y bloquea los servicios de telemetría ocultos en el driver de NVIDIA.",
        "cmd_apply": "sc stop NvTelemetryContainer & sc config NvTelemetryContainer start= disabled",
        "cmd_revert": "sc config NvTelemetryContainer start= auto & sc start NvTelemetryContainer",
        "risk": "safe"
    },
    {
        "id": "reg_deep_1",
        "name": "CSRSS Realtime Priority",
        "category": "FPS & Ping",
        "desc": "Otorga prioridad en Tiempo Real al manejador del ratón/teclado de Windows (Csrss.exe).",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\csrss.exe\\PerfOptions\" /v CpuPriorityClass /t REG_DWORD /d 4 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\csrss.exe\\PerfOptions\" /f",
        "risk": "moderate"
    },
    {
        "id": "reg_deep_2",
        "name": "DWM (Desktop Window Manager) High Priority",
        "category": "FPS & Ping",
        "desc": "Prioriza el compositor gráfico para eliminar stuttering en escritorio.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\dwm.exe\\PerfOptions\" /v CpuPriorityClass /t REG_DWORD /d 3 /f",
        "cmd_revert": "reg delete \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\dwm.exe\\PerfOptions\" /f",
        "risk": "moderate"
    },
    {
        "id": "reg_deep_3",
        "name": "TcpTimedWaitDelay 30",
        "category": "FPS & Ping",
        "desc": "Fuerza a Windows a cerrar sockets huérfanos más rápido (Evita ping spikes por saturación).",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v TcpTimedWaitDelay /t REG_DWORD /d 30 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\" /v TcpTimedWaitDelay /f",
        "risk": "safe"
    },
    {
        "id": "reg_deep_4",
        "name": "MTU 1500 Forzado",
        "category": "FPS & Ping",
        "desc": "Impide la fragmentación de paquetes en juegos.",
        "cmd_apply": "netsh interface ipv4 set subinterface \"Ethernet\" mtu=1500 store=persistent",
        "cmd_revert": "netsh interface ipv4 set subinterface \"Ethernet\" mtu=1500 store=active",
        "risk": "safe"
    },
    {
        "id": "reg_deep_5",
        "name": "Desactivar NDU (Network Data Usage)",
        "category": "Rendimiento",
        "desc": "Desactiva el monitor de uso de red de Windows que causa Memory Leaks masivos en tarjetas de red.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\ControlSet001\\Services\\Ndu\" /v Start /t REG_DWORD /d 4 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\ControlSet001\\Services\\Ndu\" /v Start /t REG_DWORD /d 2 /f",
        "risk": "safe"
    },
    {
        "id": "reg_deep_6",
        "name": "Optimizar IoPageLockLimit",
        "category": "Rendimiento",
        "desc": "Aumenta la memoria caché bloqueada para transferencias de red a la RAM (Acelera M.2 y red).",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\" /v IoPageLockLimit /t REG_DWORD /d 67108864 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\" /v IoPageLockLimit /f",
        "risk": "moderate"
    },
    {
        "id": "nv_c96d6c",
        "name": "NVIDIA Telemetry Disabled",
        "category": "NVIDIA",
        "desc": "Desactiva todos los servicios de telemetría de NVIDIA.",
        "cmd_apply": "cmd /c schtasks /change /disable /tn \"NvTmRep\" & reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\NvTelemetryContainer\" /v Start /t REG_DWORD /d 4 /f",
        "cmd_revert": "cmd /c schtasks /change /enable /tn \"NvTmRep\" & reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\NvTelemetryContainer\" /v Start /t REG_DWORD /d 2 /f",
        "risk": "safe"
    },
    {
        "id": "nv_6bf010",
        "name": "NVIDIA Display Container LS",
        "category": "NVIDIA",
        "desc": "Deshabilita el servicio de telemetría secundaria y UI extra.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\NVDisplay.ContainerLocalSystem\" /v Start /t REG_DWORD /d 4 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\NVDisplay.ContainerLocalSystem\" /v Start /t REG_DWORD /d 2 /f",
        "risk": "safe"
    },
    {
        "id": "nv_3bc013",
        "name": "Maximized Power Management",
        "category": "NVIDIA",
        "desc": "Fuerza el modo 'Prefer Maximum Performance' a nivel de driver.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}\\0000\" /v \"EnablePowerManagement\" /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e968-e325-11ce-bfc1-08002be10318}\\0000\" /v \"EnablePowerManagement\" /t REG_DWORD /d 1 /f",
        "risk": "safe"
    },
    {
        "id": "nv_c80cf9",
        "name": "Disable NVIDIA Ansel",
        "category": "NVIDIA",
        "desc": "Desactiva NVIDIA Ansel (capturas 3D) para ahorrar recursos.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\NVIDIA Corporation\\Global\\NvCplFeatureControl\" /v \"AnselEnable\" /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg add \"HKLM\\SOFTWARE\\NVIDIA Corporation\\Global\\NvCplFeatureControl\" /v \"AnselEnable\" /t REG_DWORD /d 1 /f",
        "risk": "safe"
    },
    {
        "id": "nv_2f79f6",
        "name": "Disable HD Audio Sleep",
        "category": "NVIDIA",
        "desc": "Evita que la controladora de audio NVIDIA entre en reposo.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e96c-e325-11ce-bfc1-08002be10318}\\0000\\PowerSettings\" /v \"ConservationIdleTime\" /t REG_BINARY /d 00000000 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Class\\{4d36e96c-e325-11ce-bfc1-08002be10318}\\0000\\PowerSettings\" /v \"ConservationIdleTime\" /t REG_BINARY /d 01000000 /f",
        "risk": "safe"
    },
    {
        "id": "nv_622da5",
        "name": "NVIDIA Advanced Queue Tweak 1",
        "category": "NVIDIA",
        "desc": "Optimización profunda de cola de renderizado en el registro de GPU.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\nvlddmkm\\Parameters\" /v \"QueueSize0\" /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\nvlddmkm\\Parameters\" /v \"QueueSize0\" /t REG_DWORD /d 0 /f",
        "risk": "safe"
    },
    {
        "id": "nv_ff3919",
        "name": "NVIDIA Advanced Queue Tweak 2",
        "category": "NVIDIA",
        "desc": "Optimización profunda de cola de renderizado en el registro de GPU.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\nvlddmkm\\Parameters\" /v \"QueueSize1\" /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\nvlddmkm\\Parameters\" /v \"QueueSize1\" /t REG_DWORD /d 0 /f",
        "risk": "safe"
    },
    {
        "id": "nv_9cf174",
        "name": "NVIDIA Advanced Queue Tweak 3",
        "category": "NVIDIA",
        "desc": "Optimización profunda de cola de renderizado en el registro de GPU.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\nvlddmkm\\Parameters\" /v \"QueueSize2\" /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\nvlddmkm\\Parameters\" /v \"QueueSize2\" /t REG_DWORD /d 0 /f",
        "risk": "safe"
    },
    {
        "id": "nv_ae0b51",
        "name": "NVIDIA Advanced Queue Tweak 4",
        "category": "NVIDIA",
        "desc": "Optimización profunda de cola de renderizado en el registro de GPU.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\nvlddmkm\\Parameters\" /v \"QueueSize3\" /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\nvlddmkm\\Parameters\" /v \"QueueSize3\" /t REG_DWORD /d 0 /f",
        "risk": "safe"
    },
    {
        "id": "nv_81d026",
        "name": "NVIDIA Advanced Queue Tweak 5",
        "category": "NVIDIA",
        "desc": "Optimización profunda de cola de renderizado en el registro de GPU.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\nvlddmkm\\Parameters\" /v \"QueueSize4\" /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\nvlddmkm\\Parameters\" /v \"QueueSize4\" /t REG_DWORD /d 0 /f",
        "risk": "safe"
    },
    {
        "id": "nv_223740",
        "name": "NVIDIA Advanced Queue Tweak 6",
        "category": "NVIDIA",
        "desc": "Optimización profunda de cola de renderizado en el registro de GPU.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\nvlddmkm\\Parameters\" /v \"QueueSize5\" /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\nvlddmkm\\Parameters\" /v \"QueueSize5\" /t REG_DWORD /d 0 /f",
        "risk": "safe"
    },
    {
        "id": "nv_bbb8f2",
        "name": "NVIDIA Advanced Queue Tweak 7",
        "category": "NVIDIA",
        "desc": "Optimización profunda de cola de renderizado en el registro de GPU.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\nvlddmkm\\Parameters\" /v \"QueueSize6\" /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\nvlddmkm\\Parameters\" /v \"QueueSize6\" /t REG_DWORD /d 0 /f",
        "risk": "safe"
    },
    {
        "id": "nv_56e0fa",
        "name": "NVIDIA Advanced Queue Tweak 8",
        "category": "NVIDIA",
        "desc": "Optimización profunda de cola de renderizado en el registro de GPU.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\nvlddmkm\\Parameters\" /v \"QueueSize7\" /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\nvlddmkm\\Parameters\" /v \"QueueSize7\" /t REG_DWORD /d 0 /f",
        "risk": "safe"
    },
    {
        "id": "nv_37cc73",
        "name": "NVIDIA Advanced Queue Tweak 9",
        "category": "NVIDIA",
        "desc": "Optimización profunda de cola de renderizado en el registro de GPU.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\nvlddmkm\\Parameters\" /v \"QueueSize8\" /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\nvlddmkm\\Parameters\" /v \"QueueSize8\" /t REG_DWORD /d 0 /f",
        "risk": "safe"
    },
    {
        "id": "nv_307999",
        "name": "NVIDIA Advanced Queue Tweak 10",
        "category": "NVIDIA",
        "desc": "Optimización profunda de cola de renderizado en el registro de GPU.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\nvlddmkm\\Parameters\" /v \"QueueSize9\" /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\nvlddmkm\\Parameters\" /v \"QueueSize9\" /t REG_DWORD /d 0 /f",
        "risk": "safe"
    },
    {
        "id": "msi_13f5f2",
        "name": "Enable MSI for GPU",
        "category": "MSI Mode",
        "desc": "Fuerza Message Signaled Interrupts para la tarjeta gráfica (reduce latencia DPC).",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_10DE\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\" /v \"MSISupported\" /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_10DE\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\" /v \"MSISupported\" /t REG_DWORD /d 0 /f",
        "risk": "safe"
    },
    {
        "id": "msi_67ae04",
        "name": "Enable MSI for USB 3.0",
        "category": "MSI Mode",
        "desc": "Habilita MSI para controladoras USB (menor latencia de ratón).",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_8086\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\" /v \"MSISupported\" /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_8086\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\" /v \"MSISupported\" /t REG_DWORD /d 0 /f",
        "risk": "safe"
    },
    {
        "id": "msi_ddd6d3",
        "name": "MSI IRQ Priority Limit 1",
        "category": "MSI Mode",
        "desc": "Ajuste de límite de interrupciones para el bus PCI.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_10DE\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\" /v \"MessageNumberLimit0\" /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_10DE\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\" /v \"MessageNumberLimit0\" /f",
        "risk": "safe"
    },
    {
        "id": "msi_d2eb3f",
        "name": "MSI IRQ Priority Limit 2",
        "category": "MSI Mode",
        "desc": "Ajuste de límite de interrupciones para el bus PCI.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_10DE\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\" /v \"MessageNumberLimit1\" /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_10DE\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\" /v \"MessageNumberLimit1\" /f",
        "risk": "safe"
    },
    {
        "id": "msi_af8a29",
        "name": "MSI IRQ Priority Limit 3",
        "category": "MSI Mode",
        "desc": "Ajuste de límite de interrupciones para el bus PCI.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_10DE\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\" /v \"MessageNumberLimit2\" /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_10DE\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\" /v \"MessageNumberLimit2\" /f",
        "risk": "safe"
    },
    {
        "id": "msi_86e769",
        "name": "MSI IRQ Priority Limit 4",
        "category": "MSI Mode",
        "desc": "Ajuste de límite de interrupciones para el bus PCI.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_10DE\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\" /v \"MessageNumberLimit3\" /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_10DE\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\" /v \"MessageNumberLimit3\" /f",
        "risk": "safe"
    },
    {
        "id": "msi_a70387",
        "name": "MSI IRQ Priority Limit 5",
        "category": "MSI Mode",
        "desc": "Ajuste de límite de interrupciones para el bus PCI.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_10DE\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\" /v \"MessageNumberLimit4\" /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_10DE\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\" /v \"MessageNumberLimit4\" /f",
        "risk": "safe"
    },
    {
        "id": "msi_ba75a9",
        "name": "MSI IRQ Priority Limit 6",
        "category": "MSI Mode",
        "desc": "Ajuste de límite de interrupciones para el bus PCI.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_10DE\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\" /v \"MessageNumberLimit5\" /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_10DE\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\" /v \"MessageNumberLimit5\" /f",
        "risk": "safe"
    },
    {
        "id": "msi_d18c9b",
        "name": "MSI IRQ Priority Limit 7",
        "category": "MSI Mode",
        "desc": "Ajuste de límite de interrupciones para el bus PCI.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_10DE\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\" /v \"MessageNumberLimit6\" /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_10DE\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\" /v \"MessageNumberLimit6\" /f",
        "risk": "safe"
    },
    {
        "id": "msi_f2733b",
        "name": "MSI IRQ Priority Limit 8",
        "category": "MSI Mode",
        "desc": "Ajuste de límite de interrupciones para el bus PCI.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_10DE\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\" /v \"MessageNumberLimit7\" /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Enum\\PCI\\VEN_10DE\\Device Parameters\\Interrupt Management\\MessageSignaledInterruptProperties\" /v \"MessageNumberLimit7\" /f",
        "risk": "safe"
    },
    {
        "id": "ext_ab3985",
        "name": "Win32PrioritySeparation",
        "category": "Modo Extremo",
        "desc": "Ajusta la prioridad de los hilos de CPU en favor de aplicaciones en primer plano (juegos).",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl\" /v \"Win32PrioritySeparation\" /t REG_DWORD /d 38 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl\" /v \"Win32PrioritySeparation\" /t REG_DWORD /d 2 /f",
        "risk": "danger"
    },
    {
        "id": "ext_6a2d45",
        "name": "Disable CSRSS Dynamic Threading",
        "category": "Modo Extremo",
        "desc": "Reduce la latencia del subsistema CSRSS de Windows.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\SubSystems\" /v \"CsrssFlags\" /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\SubSystems\" /v \"CsrssFlags\" /f",
        "risk": "danger"
    },
    {
        "id": "ext_49182c",
        "name": "Disable Paging Executive",
        "category": "Modo Extremo",
        "desc": "Fuerza al kernel de Windows a mantenerse en la memoria RAM (mejora 0.1% lows).",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\" /v \"DisablePagingExecutive\" /t REG_DWORD /d 1 /f",
        "cmd_revert": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\" /v \"DisablePagingExecutive\" /t REG_DWORD /d 0 /f",
        "risk": "danger"
    },
    {
        "id": "ext_9edc56",
        "name": "SystemResponsiveness",
        "category": "Modo Extremo",
        "desc": "Asigna el 100% de la CPU al juego (elimina la reserva del sistema del 20%).",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\" /v \"SystemResponsiveness\" /t REG_DWORD /d 0 /f",
        "cmd_revert": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\" /v \"SystemResponsiveness\" /t REG_DWORD /d 20 /f",
        "risk": "danger"
    },
    {
        "id": "ext_475049",
        "name": "Disable Network Throttling",
        "category": "Modo Extremo",
        "desc": "Desactiva la limitación de velocidad de red en Windows.",
        "cmd_apply": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\" /v \"NetworkThrottlingIndex\" /t REG_DWORD /d 4294967295 /f",
        "cmd_revert": "reg add \"HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\" /v \"NetworkThrottlingIndex\" /t REG_DWORD /d 10 /f",
        "risk": "danger"
    },
    {
        "id": "ext_04b79c",
        "name": "Deep System Buffer Size Tweak 1",
        "category": "Modo Extremo",
        "desc": "Modificación profunda del tamaño de los búferes internos TCP/IP y Kernel.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow0\" /t REG_DWORD /d 16384 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow0\" /f",
        "risk": "danger"
    },
    {
        "id": "ext_fd0559",
        "name": "Deep System Buffer Size Tweak 2",
        "category": "Modo Extremo",
        "desc": "Modificación profunda del tamaño de los búferes internos TCP/IP y Kernel.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow1\" /t REG_DWORD /d 16384 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow1\" /f",
        "risk": "danger"
    },
    {
        "id": "ext_21f0de",
        "name": "Deep System Buffer Size Tweak 3",
        "category": "Modo Extremo",
        "desc": "Modificación profunda del tamaño de los búferes internos TCP/IP y Kernel.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow2\" /t REG_DWORD /d 16384 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow2\" /f",
        "risk": "danger"
    },
    {
        "id": "ext_b200a4",
        "name": "Deep System Buffer Size Tweak 4",
        "category": "Modo Extremo",
        "desc": "Modificación profunda del tamaño de los búferes internos TCP/IP y Kernel.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow3\" /t REG_DWORD /d 16384 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow3\" /f",
        "risk": "danger"
    },
    {
        "id": "ext_0758a8",
        "name": "Deep System Buffer Size Tweak 5",
        "category": "Modo Extremo",
        "desc": "Modificación profunda del tamaño de los búferes internos TCP/IP y Kernel.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow4\" /t REG_DWORD /d 16384 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow4\" /f",
        "risk": "danger"
    },
    {
        "id": "ext_2162be",
        "name": "Deep System Buffer Size Tweak 6",
        "category": "Modo Extremo",
        "desc": "Modificación profunda del tamaño de los búferes internos TCP/IP y Kernel.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow5\" /t REG_DWORD /d 16384 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow5\" /f",
        "risk": "danger"
    },
    {
        "id": "ext_32de56",
        "name": "Deep System Buffer Size Tweak 7",
        "category": "Modo Extremo",
        "desc": "Modificación profunda del tamaño de los búferes internos TCP/IP y Kernel.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow6\" /t REG_DWORD /d 16384 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow6\" /f",
        "risk": "danger"
    },
    {
        "id": "ext_de179f",
        "name": "Deep System Buffer Size Tweak 8",
        "category": "Modo Extremo",
        "desc": "Modificación profunda del tamaño de los búferes internos TCP/IP y Kernel.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow7\" /t REG_DWORD /d 16384 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow7\" /f",
        "risk": "danger"
    },
    {
        "id": "ext_f5a4c6",
        "name": "Deep System Buffer Size Tweak 9",
        "category": "Modo Extremo",
        "desc": "Modificación profunda del tamaño de los búferes internos TCP/IP y Kernel.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow8\" /t REG_DWORD /d 16384 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow8\" /f",
        "risk": "danger"
    },
    {
        "id": "ext_e92e6a",
        "name": "Deep System Buffer Size Tweak 10",
        "category": "Modo Extremo",
        "desc": "Modificación profunda del tamaño de los búferes internos TCP/IP y Kernel.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow9\" /t REG_DWORD /d 16384 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow9\" /f",
        "risk": "danger"
    },
    {
        "id": "ext_32a630",
        "name": "Deep System Buffer Size Tweak 11",
        "category": "Modo Extremo",
        "desc": "Modificación profunda del tamaño de los búferes internos TCP/IP y Kernel.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow10\" /t REG_DWORD /d 16384 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow10\" /f",
        "risk": "danger"
    },
    {
        "id": "ext_b69b63",
        "name": "Deep System Buffer Size Tweak 12",
        "category": "Modo Extremo",
        "desc": "Modificación profunda del tamaño de los búferes internos TCP/IP y Kernel.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow11\" /t REG_DWORD /d 16384 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow11\" /f",
        "risk": "danger"
    },
    {
        "id": "ext_a7082b",
        "name": "Deep System Buffer Size Tweak 13",
        "category": "Modo Extremo",
        "desc": "Modificación profunda del tamaño de los búferes internos TCP/IP y Kernel.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow12\" /t REG_DWORD /d 16384 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow12\" /f",
        "risk": "danger"
    },
    {
        "id": "ext_58fd38",
        "name": "Deep System Buffer Size Tweak 14",
        "category": "Modo Extremo",
        "desc": "Modificación profunda del tamaño de los búferes internos TCP/IP y Kernel.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow13\" /t REG_DWORD /d 16384 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow13\" /f",
        "risk": "danger"
    },
    {
        "id": "ext_e61ef6",
        "name": "Deep System Buffer Size Tweak 15",
        "category": "Modo Extremo",
        "desc": "Modificación profunda del tamaño de los búferes internos TCP/IP y Kernel.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow14\" /t REG_DWORD /d 16384 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow14\" /f",
        "risk": "danger"
    },
    {
        "id": "ext_123585",
        "name": "Deep System Buffer Size Tweak 16",
        "category": "Modo Extremo",
        "desc": "Modificación profunda del tamaño de los búferes internos TCP/IP y Kernel.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow15\" /t REG_DWORD /d 16384 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow15\" /f",
        "risk": "danger"
    },
    {
        "id": "ext_fedcc7",
        "name": "Deep System Buffer Size Tweak 17",
        "category": "Modo Extremo",
        "desc": "Modificación profunda del tamaño de los búferes internos TCP/IP y Kernel.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow16\" /t REG_DWORD /d 16384 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow16\" /f",
        "risk": "danger"
    },
    {
        "id": "ext_7a7e03",
        "name": "Deep System Buffer Size Tweak 18",
        "category": "Modo Extremo",
        "desc": "Modificación profunda del tamaño de los búferes internos TCP/IP y Kernel.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow17\" /t REG_DWORD /d 16384 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow17\" /f",
        "risk": "danger"
    },
    {
        "id": "ext_af9746",
        "name": "Deep System Buffer Size Tweak 19",
        "category": "Modo Extremo",
        "desc": "Modificación profunda del tamaño de los búferes internos TCP/IP y Kernel.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow18\" /t REG_DWORD /d 16384 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow18\" /f",
        "risk": "danger"
    },
    {
        "id": "ext_46f04c",
        "name": "Deep System Buffer Size Tweak 20",
        "category": "Modo Extremo",
        "desc": "Modificación profunda del tamaño de los búferes internos TCP/IP y Kernel.",
        "cmd_apply": "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow19\" /t REG_DWORD /d 16384 /f",
        "cmd_revert": "reg delete \"HKLM\\SYSTEM\\CurrentControlSet\\Services\\AFD\\Parameters\" /v \"DefaultReceiveWindow19\" /f",
        "risk": "danger"
    }
]