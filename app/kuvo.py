import click  # type: ignore
from app.util import generate_bundles, new_generate
import questionary  # type: ignore
from app.git import create_template
from app.config import config
import os
import shutil


@click.group()
def cli():
    """CLI principal para la generación de bundles."""
    pass


@cli.command()
@click.option(
    '--platform',
    default=None,
    help='Plataforma para generar el bundle.',
    type=click.Choice(['android', 'ios'], case_sensitive=False)
)
def bundle(platform):
    output_dir = "./dist"
    click.echo(f"Generando bundles en {output_dir}...")
    generate_bundles(output_dir=output_dir, platform=platform)


@cli.command()
def generate():
    choice = questionary.select(
        "what do you want to do?",
        choices=[
            "generate a new abb",
            "generate a new apk",
            "exit"
        ]
    ).ask()
    if choice == "generate a new abb":
        new_generate(bundle=True)
    elif choice == "generate a new apk":
        new_generate(bundle=False)
    elif choice == "exit":
        print("Bye!")
        exit(0)

################ template ################


@cli.command()
@click.option("--repository", help="URL of the repository to clone")
@click.option("--name", help="Name of the new app", required=True)
def create(repository, name):
    # Usar la URL del repositorio proporcionada o una predeterminada
    repo = repository or config["git"]["repos"]

    # Verificar si la carpeta ya existe
    if os.path.exists(name):
        # Preguntar si el usuario quiere sobrescribir
        overwrite = questionary.confirm(
            f"The folder '{name}' already exists. Do you want to overwrite it?").ask()

        # Si no quiere sobrescribir, salir
        if not overwrite:
            return

        # Eliminar la carpeta existente
        shutil.rmtree(name)  # Elimina todo el contenido del directorio

    # Crear la plantilla
    create_template(project_name=name, repo_url=repo)

#### main ####


def main():
    cli()


if __name__ == "__main__":
    main()
