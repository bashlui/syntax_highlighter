# Guía de Instalación de Racket

Este documento proporciona instrucciones detalladas para instalar Racket en diferentes sistemas operativos.

## Windows

### Método 1: Instalador Oficial

1. Visita [https://download.racket-lang.org/](https://download.racket-lang.org/)
2. Descarga el instalador para Windows
3. Ejecuta el archivo `.exe` descargado
4. Sigue las instrucciones del instalador
5. Durante la instalación, elige "Añadir programas de Racket a PATH" para poder ejecutar racket desde cualquier ubicación
6. Completa la instalación

### Método 2: Usando winget (Windows 10/11)

1. Abre PowerShell o el Símbolo del sistema
2. Ejecuta el siguiente comando:
   ```
   winget install Racket.Racket
   ```
3. Sigue las instrucciones en pantalla

### Método 3: Chocolatey

1. Si tienes Chocolatey instalado, abre PowerShell como administrador
2. Ejecuta:
   ```
   choco install racket
   ```

## macOS

### Método 1: Instalador Oficial

1. Visita [https://download.racket-lang.org/](https://download.racket-lang.org/)
2. Descarga el instalador para macOS
3. Abre el archivo `.dmg` descargado
4. Arrastra la aplicación Racket a la carpeta Aplicaciones
5. Para configurar el acceso desde la terminal, abre Terminal y ejecuta:
   ```
   echo 'export PATH="/Applications/Racket v8.x/bin:$PATH"' >> ~/.zshrc
   ```
   (Reemplaza "8.x" con la versión que hayas instalado)

### Método 2: Homebrew

1. Si tienes Homebrew instalado, abre Terminal
2. Ejecuta:
   ```
   brew install minimal-racket
   ```
   o para la versión completa:
   ```
   brew install racket
   ```

## Linux

### Método 1: Instalador Oficial

1. Visita [https://download.racket-lang.org/](https://download.racket-lang.org/)
2. Descarga el instalador para Linux (según tu arquitectura)
3. Abre una terminal
4. Navega a donde descargaste el archivo
5. Extrae el archivo:
   ```
   tar -xzf racket-8.x-x86_64-linux-cs.tgz
   ```
   (Reemplaza el nombre del archivo según la versión que hayas descargado)
6. Instala:
   ```
   cd racket-8.x-x86_64-linux-cs
   sudo ./install.sh
   ```

### Método 2: Gestor de paquetes

#### Ubuntu/Debian
```
sudo apt update
sudo apt install racket
```

#### Fedora
```
sudo dnf install racket
```

#### Arch Linux
```
sudo pacman -S racket
```

## Verificación de la Instalación

Para verificar que Racket se ha instalado correctamente:

1. Abre una terminal o símbolo del sistema
2. Ejecuta:
   ```
   racket --version
   ```
3. Deberías ver la versión de Racket instalada

## Entornos en Línea (si no puedes instalar localmente)

Si no puedes instalar Racket en tu máquina, puedes usar estos entornos en línea:

1. [Replit](https://replit.com/) - Permite crear proyectos en Racket
2. [Try Racket](https://try-racket.defn.io/) - Para pruebas pequeñas

## Solución de Problemas

### Racket no se encuentra en el PATH

Si después de instalar Racket, no puedes ejecutarlo desde la línea de comandos:

#### Windows
1. Busca la ubicación de instalación (normalmente `C:\Program Files\Racket`)
2. Añade la carpeta `bin` al PATH del sistema:
   - Abre Panel de Control > Sistema > Configuración avanzada del sistema
   - Haz clic en "Variables de entorno"
   - Edita la variable "Path"
   - Añade la ruta a la carpeta bin de Racket (ej: `C:\Program Files\Racket\bin`)

#### macOS/Linux
Añade la siguiente línea a tu archivo `.bashrc`, `.bash_profile` o `.zshrc`:
```
export PATH="/ruta/a/racket/bin:$PATH"
```
Reemplaza "/ruta/a/racket" con la ubicación real de tu instalación de Racket.

## Recursos Adicionales

- [Documentación oficial de Racket](https://docs.racket-lang.org/)
- [Tutorial de Racket](https://docs.racket-lang.org/quick/)
- [The Racket Guide](https://docs.racket-lang.org/guide/) 