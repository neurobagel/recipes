import json
from pathlib import Path
import logging
import argparse
import shutil
from pydantic import ValidationError, TypeAdapter, HttpUrl
from data_init.utils import models

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

jsonld_key_to_dataset_attribute_mapping = {
    "hasLabel": "dataset_name",
    "hasAuthors": "authors",
    "hasReferencesAndLinks": "references_and_links",
    "hasKeywords": "keywords",
    "hasRepositoryURL": "repository_url",
    "hasAccessInstructions": "access_instructions",
    "hasAccessType": "access_type",
    "hasAccessEmail": "access_email",
    "hasAccessLink": "access_link",
    "hasPortalURI": "access_link",  # Map legacy hasPortalURI to access_link
}


def load_jsonld(path: Path) -> dict:
    """Load a JSONLD file and return its content as a dictionary."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_and_validate_jsonld_dataset(file_path: Path) -> dict | None:
    """
    Strip the @context from the contents of a JSONLD file and validate it against the Neurobagel Dataset model.
    """
    jsonld = load_jsonld(file_path)
    jsonld.pop("@context")
    try:
        models.Dataset.model_validate(jsonld)
    except ValidationError as err:
        logger.warning(
            f"{file_path.name} is not a valid Neurobagel dataset JSONLD. Skipping file.\n"
            f"Validation errors: {str(err)}"
        )
        return None
    logger.info(f"File validated: {file_path.name}")
    return jsonld


def is_valid_http_url(value: str) -> bool:
    """Check if the given string is a valid HTTP URL."""
    try:
        TypeAdapter(HttpUrl).validate_python(value)
        return True
    except ValidationError:
        return False


def get_homepage_url(references_and_links: list[str]) -> str | None:
    """Return the first valid HTTP URL from the references and links list, or None if none found."""
    return next(
        (link for link in references_and_links if is_valid_http_url(link)),
        None
    )


def extract_dataset_metadata_to_dict(jsonld_dir: Path, output_dir: Path) -> dict:
    """
    Validate and extract dataset-level metadata from all Neurobagel dataset JSONLD files in a directory.
    
    Validated JSONLD files are copied to the output directory,
    and a dictionary mapping dataset UUIDs to their metadata is returned.
    """    
    dataset_metadata_lookup = {}

    num_input_jsonlds = len(list(jsonld_dir.glob("*.jsonld")))
    for idx, jsonld_path in enumerate(jsonld_dir.glob("*.jsonld"), start=1):
        logger.info(f"({idx}/{num_input_jsonlds}) Processing file: {jsonld_path.name}")
        dataset = load_and_validate_jsonld_dataset(jsonld_path)
        if dataset is None:
            continue

        dataset_uuid = dataset["identifier"]
        dataset_attributes = {}
        for jsonld_key, attribute_name in jsonld_key_to_dataset_attribute_mapping.items():
            if jsonld_key in dataset:
                if jsonld_key == "hasReferencesAndLinks":
                    if homepage_url := get_homepage_url(dataset[jsonld_key]):
                        dataset_attributes["homepage"] = homepage_url
                elif jsonld_key == "hasPortalURI":
                    logger.warning(
                        f"{jsonld_path.name} uses a deprecated dataset-level 'hasPortalURI' key. "
                        "This URL will be stored as the access link for the dataset instead. "
                        "We recommend updating your JSONLD using the latest version of the Neurobagel CLI."
                    )
                dataset_attributes[attribute_name] = dataset[jsonld_key]
        dataset_metadata_lookup[dataset_uuid] = dataset_attributes

        shutil.copy2(jsonld_path, output_dir)

    logger.info(
        f"Dataset metadata successfully extracted from {len(dataset_metadata_lookup)}/{num_input_jsonlds} JSONLD files; "
        "uploading these JSONLD files to the graph store."
    )
    return dataset_metadata_lookup


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate and extract dataset-level metadata from Neurobagel dataset JSONLD files."
    )
    parser.add_argument(
        "input_dir",
        type=lambda p: Path(p).resolve(),
        help="Directory containing Neurobagel dataset JSONLD files."
    )
    parser.add_argument(
        "output_dir",
        type=lambda p: Path(p).resolve(),
        help="Directory to save validated JSONLD files and dataset metadata JSON file."
    )
    return parser.parse_args()
    

if __name__ == "__main__":
    args = parse_arguments()

    dataset_metadata_lookup = extract_dataset_metadata_to_dict(args.input_dir, args.output_dir)

    with open(args.output_dir / "dataset_metadata.json", "w", encoding="utf-8") as f:
        json.dump(dataset_metadata_lookup, f, indent=4)
