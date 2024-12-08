import asyncio
import shutil
from pathlib import Path
import argparse
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


async def read_folder(source_folder: Path, output_folder: Path):

    try:
        for file in source_folder.rglob('*'):
            if file.is_file():
                await copy_file(file, output_folder)
    except Exception as e:
        logging.error(f"Error reading folder {source_folder}: {e}")


async def copy_file(file_path: Path, output_folder: Path):

    try:
        extension = file_path.suffix.lower() or "_no_extension"
        destination_folder = output_folder / extension.lstrip('.')
        await asyncio.to_thread(destination_folder.mkdir, parents=True, exist_ok=True)
        destination_file = destination_folder / file_path.name
        await asyncio.to_thread(shutil.copy2, file_path, destination_file)
        logging.info(f"Copied {file_path} to {destination_file}")
    except Exception as e:
        logging.error(f"Error copying file {file_path}: {e}")


async def main():

    parser = argparse.ArgumentParser(
        description="Asynchronous file sorter by extension.")
    parser.add_argument('source_folder', type=str,
                        help="Path to the source folder.")
    parser.add_argument('output_folder', type=str,
                        help="Path to the output folder.")

    args = parser.parse_args()

    source_folder = Path(args.source_folder).resolve()
    output_folder = Path(args.output_folder).resolve()

    if not source_folder.exists() or not source_folder.is_dir():
        logging.error("Source folder does not exist or is not a directory.")
        return

    if not output_folder.exists():
        await asyncio.to_thread(output_folder.mkdir, parents=True)

    logging.info(f"Starting to process files from {
                 source_folder} to {output_folder}")

    await read_folder(source_folder, output_folder)

if __name__ == "__main__":
    asyncio.run(main())
