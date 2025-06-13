# setup.ps1

# Créer un dossier de flags
New-Item -Path "C:\flags" -ItemType Directory -Force

# Flag visible
Set-Content -Path "C:\flags\flag1.txt" -Value "FLAG{first_flag_found}"

# Flag final caché sur un port
Set-Content -Path "C:\flags\final_flag.txt" -Value "FLAG{hidden_flag_on_port_1337}"

# Écoute sur port 1337 pour flag final
echo "FLAG{hidden_flag_on_port_1337}" | Out-File -Encoding ASCII -FilePath C:\flag_port.txt
Start-Process powershell -ArgumentList "-NoExit", "-Command", "while ($true) { echo 'FLAG{hidden_flag_on_port_1337}' | ncat -lvp 1337 }"
