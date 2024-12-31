#
██╗░░██╗██╗░░░██╗██╗░░░██╗░█████╗░
██║░██╔╝██║░░░██║██║░░░██║██╔══██╗
█████═╝░██║░░░██║╚██╗░██╔╝██║░░██║
██╔═██╗░██║░░░██║░╚████╔╝░██║░░██║
██║░╚██╗╚██████╔╝░░╚██╔╝░░╚█████╔╝
╚═╝░░╚═╝░╚═════╝░░░░╚═╝░░░░╚════╝░

![Logo](https://raw.githubusercontent.com/elmanci2/kuvo-cli/dev/logo.txt)

Kuvo CLI is a powerful command-line interface tool designed to streamline your development workflow, particularly for bundle generation and project creation.

## Installation Instructions

### Prerequisites

Before installing kuvo-cli, ensure you have the following installed on your system:

- Python 3.x
- pip3
- curl

### Installation

To install kuvo-cli, run the following command in your terminal:

```sh
curl -O https://raw.githubusercontent.com/elmanci2/kuvo-cli/dev/install.sh && chmod +x install.sh && ./install.sh && rm install.sh
```


Uso
Después de la instalación, puedes usar el comando kuvo en tu terminal.

Comandos
kuvo bundle
Genera bundles para las plataformas especificadas.


kuvo bundle --platform [android|ios]
--platform: Plataforma para generar el bundle. Opciones: android, ios.
kuvo generate
Genera un nuevo ABB (Android App Bundle) o APK (Android Package).


kuvo generate
Selecciona una opción interactiva para generar un nuevo ABB, un nuevo APK o salir.
kuvo create
Crea una nueva plantilla de aplicación clonando un repositorio.


kuvo create --repository [URL] --name [NAME]
--repository: URL del repositorio a clonar.
--name: Nombre de la nueva aplicación.
Ejemplo de Uso

kuvo --version

