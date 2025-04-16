#!/data/data/com.termux/files/usr/bin/bash

# -----------------------
# 🧠 Auto-Ejecuta Scripts
# -----------------------
echo -e "\n🔄 Ejecutando módulos de análisis previos..."

# Asegúrate que estén en el mismo directorio o en $PATH
bash proc-monitor.sh > proc_sus.txt 2>/dev/null
bash net-connections.sh > net_con.txt 2>/dev/null
bash find-hidden-files.sh --fast > hidden_files.log 2>/dev/null

# Variables
fecha=$(date "+%d-%m-%Y %H:%M")
output="report-$(date '+%d%m%Y-%H%M').html"
proc_sus="proc_sus.txt"
net_con="net_con.txt"
hidden_files="hidden_files.log"

# -----------------------
# 📊 Contadores para el resumen
# -----------------------
cant_procs=$(wc -l < "$proc_sus")
cant_conex=$(grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' "$net_con" | sort -u | grep -vE '^(127|10|192\.168|172\.(1[6-9]|2[0-9]|3[01]))' | wc -l)
cant_archivos=$(wc -l < "$hidden_files")
cant_usuarios=$(who | cut -d' ' -f1 | sort | uniq | wc -l)

# -----------------------
# 🧾 Inicia HTML
# -----------------------
cat <<EOF > "$output"
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>📄 Informe Forense - Termux Hackers</title>
  <style>
    body {
      background: #0f0f0f;
      color: #00ffcc;
      font-family: monospace;
      padding: 20px;
    }
    h1, h2 {
      color: #00ffcc;
      border-bottom: 2px solid #00ffcc;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 30px;
    }
    th, td {
      border: 1px solid #444;
      padding: 8px;
      text-align: left;
    }
    th {
      background: #111;
      color: #0ff;
    }
    tr:nth-child(even) {
      background-color: #1c1c1c;
    }
    .alerta { color: #ff4444; font-weight: bold; }
    .ok { color: #44ff44; }
    .neutro { color: #cccccc; }
  </style>
</head>
<body>
  <h1>🧠 Informe Forense de Seguridad</h1>
  <p>📅 Generado: <strong>$fecha</strong></p>

  <h2>📌 Mini-Resumen</h2>
  <ul>
    <li>👥 Usuarios activos detectados: <strong>$cant_usuarios</strong></li>
    <li>🌐 IPs externas conectadas: <strong>$cant_conex</strong></li>
    <li>🔐 Procesos sospechosos: <strong>$cant_procs</strong></li>
    <li>🕵️ Archivos ocultos encontrados: <strong>$cant_archivos</strong></li>
  </ul>
EOF

# -----------------------
# 🧍 Usuarios Activos Sospechosos
# -----------------------
echo "<h2>🧍 Usuarios Activos Sospechosos</h2>" >> "$output"
echo "<table><tr><th>Usuario</th><th>UID</th><th>Shell</th><th>Sesión</th></tr>" >> "$output"

getent passwd | awk -F: '$3 < 1000 && $1 != "root" { print $1,$3,$7 }' | while read user uid shell; do
  sesion=$(who | grep "$user" | wc -l)
  echo "<tr><td>$user</td><td>$uid</td><td>$shell</td><td>$sesion</td></tr>" >> "$output"
done

usuarios=$(who | cut -d' ' -f1 | sort | uniq)
for u in $usuarios; do
  uid=$(id -u "$u")
  shell=$(getent passwd "$u" | cut -d: -f7)
  if [ "$uid" -ge 1000 ]; then
    echo "<tr><td>$u</td><td>$uid</td><td>$shell</td><td>1</td></tr>" >> "$output"
  fi
done
echo "</table>" >> "$output"

# -----------------------
# 🌍 Whois de IPs Extranjeras
# -----------------------
echo "<h2>🌍 Whois de IPs Extranjeras</h2>" >> "$output"
grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' net_con.txt | sort -u | grep -vE '^(127|10|192\.168|172\.(1[6-9]|2[0-9]|3[01]))' > ips_ext.txt

if [ -s ips_ext.txt ]; then
  echo "<table><tr><th>IP</th><th>Organización</th><th>País</th></tr>" >> "$output"
  while read -r ip; do
    info=$(python whois-lookup.py "$ip" | grep -E 'OrgName|Organization|Country' | paste -s -d "|" -)
    org=$(echo "$info" | cut -d"|" -f1 | cut -d: -f2 | xargs)
    pais=$(echo "$info" | grep -oP 'Country:?\s+\K\S+' | head -1)
    echo "<tr><td>$ip</td><td>$org</td><td>$pais</td></tr>" >> "$output"
  done < ips_ext.txt
  echo "</table>" >> "$output"
else
  echo "<p class='neutro'>No se detectaron IPs externas.</p>" >> "$output"
fi

# -----------------------
# 📦 Función tabla
# -----------------------
insertar_tabla() {
  titulo="$1"
  archivo="$2"
  columnas="$3"

  echo "<h2>$titulo</h2>" >> "$output"
  if [ -s "$archivo" ]; then
    echo "<table><tr>" >> "$output"
    for col in $columnas; do
      echo "<th>$col</th>" >> "$output"
    done
    echo "</tr>" >> "$output"

    while IFS= read -r linea; do
      echo "<tr>" >> "$output"
      for campo in $linea; do
        echo "<td>${campo}</td>" >> "$output"
      done
      echo "</tr>" >> "$output"
    done < "$archivo"
    echo "</table>" >> "$output"
  else
    echo "<p class='neutro'>Sin datos disponibles o archivo no encontrado.</p>" >> "$output"
  fi
}

# -----------------------
# 🧩 Secciones del Reporte
# -----------------------
insertar_tabla "🔐 Procesos Sospechosos" "$proc_sus" "PID NOMBRE CMD"
insertar_tabla "🌐 Conexiones Abiertas" "$net_con" "PROTO PUERTO IP_ESTABLECIDA"
insertar_tabla "🕵️‍♂️ Archivos Ocultos / Inusuales" "$hidden_files" "RUTA"

# -----------------------
# 📌 Pie de página
# -----------------------
cat <<EOF >> "$output"
  <hr>
  <p>🧠 <em>Termux Hacker Lab</em> - Powered by shell & style</p>
</body>
</html>
EOF

# -----------------------
# ✅ Resultado Final
# -----------------------
echo -e "\n✅ Informe generado: \033[1;36m$output\033[0m"
termux-open "$output" > /dev/null 2>&1 || echo "Puedes abrirlo manualmente con cualquier navegador."
