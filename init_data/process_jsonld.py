import os
import json
from pathlib import Path
import logging
import argparse
import shutil
from pydantic import ValidationError, TypeAdapter, HttpUrl
from init_data.utils import models, dataset_description_model
from collections import defaultdict

NB_CATALOG_MODE = os.environ.get("NB_CATALOG_MODE", "false").lower() == "true"
DATA_DICTIONARY_SUFFIX = "_annotated.json"
DATASET_DESCRIPTION_SUFFIX = "_dataset_description.json"

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

json_key_to_dataset_attribute_mapping = {
    "Name": "dataset_name",  # required
    "Authors": "authors",
    "ParticipantCount": "participant_count",  # required
    "ReferencesAndLinks": "references_and_links",
    "Keywords": "keywords",
    "RepositoryURL": "repository_url",
    "AccessInstructions": "access_instructions",
    "AccessType": "access_type",
    "AccessEmail": "access_email",
    "AccessLink": "access_link",
}

# participant_count
# range: minimum, maximum

def load_json(path: Path) -> dict:
    """Load a JSON file and return its content as a dictionary."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_and_validate_jsonld_dataset(file_path: Path) -> dict | None:
    """
    Strip the @context from the contents of a JSONLD file and validate it against the Neurobagel Dataset model.
    """
    jsonld = load_json(file_path)
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

# TODO: Rename jsonld_dir to data_dir to account for fact that it'll have JSONs as well
def extract_datasets_metadata_to_dict(jsonld_dir: Path, output_dir: Path) -> dict:
    """
    Validate and extract dataset-level metadata from all Neurobagel dataset JSONLD files in a directory.
    
    Validated JSONLD files are copied to the output directory,
    and a dictionary mapping dataset UUIDs to their metadata is returned.
    """    
    datasets_metadata_lookup = {}
    excluded_jsonlds = []

    if NB_CATALOG_MODE:
        dataset_file_groups = defaultdict(dict)
        for json_file in jsonld_dir.glob("*.json"):
            if json_file.name.endswith(DATA_DICTIONARY_SUFFIX):
                dataset_id = json_file.name.removesuffix(DATA_DICTIONARY_SUFFIX)
                dataset_file_groups[dataset_id]["dictionary"] = json_file
            elif json_file.name.endswith(DATASET_DESCRIPTION_SUFFIX):
                dataset_id = json_file.name.removesuffix(DATASET_DESCRIPTION_SUFFIX)
                dataset_file_groups[dataset_id]["description"] = json_file
        
        dataset_file_pairs = {}
        for dataset_file_id, dataset_files in dataset_file_groups.items():
            # or, just check based on length
            if "dictionary" not in dataset_files or "description" not in dataset_files:
                file = dataset_files.get("dictionary") or dataset_files.get("description")
                if "dictionary" not in dataset_files:
                    missing_file = f"{dataset_file_id}{DATA_DICTIONARY_SUFFIX}"
                else:
                    missing_file = f"{dataset_file_id}{DATASET_DESCRIPTION_SUFFIX}"
                logger.warning(
                    f"{file}' is missing a corresponding {missing_file}. Skipping dataset."
                )
                continue

            data_dict = load_json(dataset_files["dictionary"])
            dataset_desc = load_json(dataset_files["description"])
            # TODO: Generate a UUID programmatically

            validated_dataset_desc = dataset_description_model.DatasetDescription.model_validate(dataset_desc)

            for dataset_description_key in json_key_to_dataset_attribute_mapping:
                if dataset_description_key in validated_dataset_desc:
                    if dataset_description_key == "ReferencesAndLinks":
                        if homepage_url := get_homepage_url(validated_dataset_desc[dataset_description_key]):
                            dataset_attributes["homepage"] = homepage_url

    else:
        num_input_jsonlds = len(list(jsonld_dir.glob("*.jsonld")))
        for idx, jsonld_path in enumerate(jsonld_dir.glob("*.jsonld"), start=1):
            filename = jsonld_path.name
            logger.info(f"({idx}/{num_input_jsonlds}) Processing file: {filename}")
            jsonld_dataset = load_and_validate_jsonld_dataset(jsonld_path)
            if jsonld_dataset is None:
                excluded_jsonlds.append(filename)
                continue

            dataset_uuid = jsonld_dataset["identifier"]
            dataset_attributes = {}
            for jsonld_key, attribute_name in jsonld_key_to_dataset_attribute_mapping.items():
                if jsonld_key in jsonld_dataset:
                    if jsonld_key == "hasReferencesAndLinks":
                        if homepage_url := get_homepage_url(jsonld_dataset[jsonld_key]):
                            dataset_attributes["homepage"] = homepage_url
                    elif jsonld_key == "hasPortalURI":
                        logger.warning(
                            f"{filename} uses a deprecated dataset-level 'hasPortalURI' key. "
                            "This URL will be stored as the access link for the dataset instead. "
                            "We recommend updating your JSONLD using the latest version of the Neurobagel CLI."
                        )
                    dataset_attributes[attribute_name] = jsonld_dataset[jsonld_key]
            datasets_metadata_lookup[dataset_uuid] = dataset_attributes

        shutil.copy2(jsonld_path, output_dir)

    logger.info(
        f"Dataset metadata successfully extracted from {len(datasets_metadata_lookup)}/{num_input_jsonlds} JSONLD file(s); "
        "will upload the file(s) to the graph store."
    )
    if excluded_jsonlds:
        logger.warning(
            f"The following {len(excluded_jsonlds)} JSONLD file(s) failed validation and will not be uploaded:\n"
            + '\n'.join(excluded_jsonlds)
        )
    return datasets_metadata_lookup


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

    datasets_metadata_lookup = extract_datasets_metadata_to_dict(args.input_dir, args.output_dir)

    with open(args.output_dir / "datasets_metadata.json", "w", encoding="utf-8") as f:
        json.dump(datasets_metadata_lookup, f, indent=2, ensure_ascii=False)
