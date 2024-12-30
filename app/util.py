import os
import shutil
import subprocess
import time
from tqdm import tqdm  # type: ignore
import sys

# Validar el directorio del proyecto antes de cada función


def validate_project_root():
    """Valida que el directorio actual sea un proyecto React Native."""
    if not os.path.exists("package.json"):
        print("No se encontró package.json. Asegúrate de estar en el directorio raíz del proyecto React Native.")
        sys.exit(1)
    if not os.path.exists("ios"):
        print(
            "No se encontró la carpeta ios. Este proyecto no parece ser compatible con iOS.")
        sys.exit(1)


def generate_bundles(output_dir, platform=None):
    validate_project_root()

    platforms = ["android", "ios"] if platform is None else [platform]

    # Crear la carpeta de salida principal
    os.makedirs(output_dir, exist_ok=True)

    # Carpeta para almacenar las versiones anteriores
    previous_dir = os.path.join(output_dir, "Previous")
    os.makedirs(previous_dir, exist_ok=True)

    for plat in platforms:
        if plat not in ["android", "ios"]:
            raise ValueError(
                "Plataforma no válida. Usa 'android', 'ios' o deja None para ambas."
            )

        # Define las rutas para el bundle y los assets
        plat_dir = os.path.join(output_dir, plat)
        bundle_file = os.path.join(plat_dir, "index.bundle")
        assets_dest = os.path.join(plat_dir, "assets")

        # Verificar si existe un respaldo previo y eliminarlo si es necesario
        previous_plat_dir = os.path.join(previous_dir, plat)
        previous_bundle = os.path.join(previous_plat_dir, "index.bundle")
        previous_assets = os.path.join(previous_plat_dir, "assets")

        if os.path.exists(previous_bundle) or os.path.exists(previous_assets):
            print(f"\nEliminando respaldo previo de {plat}...")
            # Eliminar los respaldos anteriores
            if os.path.exists(previous_bundle):
                os.remove(previous_bundle)
            if os.path.exists(previous_assets):
                shutil.rmtree(previous_assets)

        # Mover los archivos actuales a la carpeta "Previous" como respaldo
        if os.path.exists(bundle_file):
            print(
                f"Moviendo archivo existente {bundle_file} a la carpeta 'previous'..."
            )
            shutil.move(bundle_file, previous_bundle)

        if os.path.exists(assets_dest):
            print(
                f"Moviendo carpeta de assets {assets_dest} a la carpeta 'previous'..."
            )
            shutil.move(assets_dest, previous_assets)

        # Crear los directorios necesarios para el bundle y los assets
        os.makedirs(plat_dir, exist_ok=True)
        os.makedirs(assets_dest, exist_ok=True)

        # Ejecutar el comando de React Native para generar el bundle y los assets
        command = [
            "npx", "react-native", "bundle",
            "--platform", plat,
            "--dev", "false",
            "--entry-file", "index.js",
            "--bundle-output", bundle_file,
            "--assets-dest", assets_dest
        ]

        print(f"\nGenerando bundle para {plat}...")

        with tqdm(
            total=100,
            desc=f"Creando bundle {plat}",
            bar_format="{l_bar}{bar} | {n_fmt}/{total_fmt}%",
            ncols=70,
            colour="green",
        ) as progress_bar:

            # Ejecutar el proceso en segundo plano
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            while process.poll() is None:
                time.sleep(0.1)  # Simular progreso
                progress_bar.update(5)  # Incrementar el progreso

            # Asegurar que la barra llega al 100% al finalizar
            progress_bar.update(progress_bar.total - progress_bar.n)

            # Capturar salida y errores
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                print(
                    f"\n✔ Bundle para {plat} generado con éxito en {output_dir}\n")
            else:
                print(
                    f"\n✘ Error al generar bundle para {plat}: {stderr.decode('utf-8')}\n")

############################## apk generate ##################################

def new_generate(bundle=None):
    validate_project_root()

    # Verificar si la carpeta android está disponible
    if not os.path.exists("android"):
        print("No se encontró la carpeta android. Este proyecto no parece ser compatible con Android.")
        sys.exit(1)

    # Cambiar al directorio android
    os.chdir("android")

    # Comando para generar el APK o el AAB
    if bundle:
        gradlew_command = "./gradlew bundleRelease" if os.name != "nt" else "gradlew bundleRelease"
        print("Generando bundle...")
    else:
        gradlew_command = "./gradlew assembleRelease" if os.name != "nt" else "gradlew assembleRelease"
        print("Generando APK...")

    try:
        subprocess.run(gradlew_command, shell=True, check=True)

        # Volver al directorio raíz del proyecto
        os.chdir("..")

        # Ruta del directorio donde se genera el APK o el AAB
        if bundle:
            output_dir = os.path.join("android", "app", "build", "outputs", "bundle", "release")
            file_extension = ".aab"
            file_name = "app-release.aab"
        else:
            output_dir = os.path.join("android", "app", "build", "outputs", "apk", "release")
            file_extension = ".apk"
            file_name = "app-release.apk"

        # Buscar el archivo generado
        output_files = [f for f in os.listdir(output_dir) if f.endswith(file_extension)]
        if not output_files:
            print(f"No se encontró ningún archivo {file_extension} en la carpeta de salida.")
            sys.exit(1)

        output_file = os.path.join(output_dir, output_files[0])
        print(f"Archivo generado en: {output_file}")

        # Verificar si el archivo existe
        if not os.path.exists(output_file):
            print(f"No se encontró el archivo {file_extension} en la ruta: {output_file}")
            sys.exit(1)

        # Crear la carpeta build en la raíz del proyecto si no existe
        build_dir = os.path.join("build", "android")
        os.makedirs(build_dir, exist_ok=True)

        # Copiar el archivo a la carpeta build
        shutil.copy(output_file, build_dir)
        print(f"Archivo copiado a: {build_dir}")

    except subprocess.CalledProcessError as e:
        print("Error al generar el archivo:")
        print(e)
        sys.exit(1)
    except FileNotFoundError as e:
        print("Error al encontrar el archivo:")
        print(e)
        sys.exit(1)


############################## adb check ##################################

def validate_adb():
    """Valida que ADB esté instalado y funcionando correctamente."""
    try:
        result = subprocess.run(
            ["adb", "version"], capture_output=True, text=True, check=True)
        print(f"ADB detectado: {result.stdout.splitlines()[0]}")
    except FileNotFoundError:
        print("ADB no está instalado o no se encuentra en el PATH. Instala ADB y asegúrate de que esté configurado correctamente.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error al verificar ADB: {e}")
        sys.exit(1)

############################## ipa generate ##################################


def execute_with_progress(command, description, progress_bar):
    """Ejecuta un comando del sistema mostrando una barra de progreso."""
    try:
        progress_bar.set_description(f"{description}...")
        subprocess.run(command, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        progress_bar.update(1)
    except subprocess.CalledProcessError as e:
        progress_bar.close()
        print(f"\n❌ Error durante '{description}': {e}")
        sys.exit(1)


def generate_ipa(scheme, export_options_plist):
    validate_project_root()

    """Genera el archivo .ipa en un proyecto React Native."""
    ios_path = os.path.join(os.getcwd(), "ios")
    os.chdir(ios_path)

    # Crear barra de progreso
    tasks = ["Limpiar proyecto", "Compilar .xcarchive", "Exportar archivo .ipa"]
    with tqdm(total=len(tasks), bar_format="{l_bar}{bar} [ {n_fmt}/{total_fmt} etapas ]") as progress_bar:
        # Limpiar proyecto
        execute_with_progress(
            ["xcodebuild", "clean"],
            "Limpiar proyecto",
            progress_bar
        )

        # Construir el archivo .xcarchive
        archive_path = os.path.join(
            os.getcwd(), "build", f"{scheme}.xcarchive")
        execute_with_progress(
            [
                "xcodebuild",
                "-scheme", scheme,
                "-workspace", f"{scheme}.xcworkspace",
                "-configuration", "Release",
                "-archivePath", archive_path,
                "archive"
            ],
            "Compilar .xcarchive",
            progress_bar
        )

        # Exportar el archivo .ipa
        export_path = os.path.join(os.getcwd(), "build", "ipa")
        execute_with_progress(
            [
                "xcodebuild",
                "-exportArchive",
                "-archivePath", archive_path,
                "-exportPath", export_path,
                "-exportOptionsPlist", export_options_plist
            ],
            "Exportar archivo .ipa",
            progress_bar
        )

    print(f"\n✅ El archivo .ipa se generó en: {export_path}")
