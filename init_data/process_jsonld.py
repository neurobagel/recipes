import os
import json
from pathlib import Path
import logging
import argparse
import shutil
from pydantic import ValidationError, TypeAdapter, HttpUrl
from init_data.utils import models, dataset_description_model
from collections import defaultdict
import isodate

NB_CATALOG_MODE = os.environ.get("NB_CATALOG_MODE", "false").lower() == "true"
DATA_DICTIONARY_SUFFIX = "_annotated.json"
DATASET_DESCRIPTION_SUFFIX = "_dataset_description.json"

AGE_FORMATS = {
    "float": "nb:FromFloat",
    "int": "nb:FromInt",
    "euro": "nb:FromEuro",
    "bounded": "nb:FromBounded",
    "iso8601": "nb:FromISO8601",
    "range": "nb:FromRange",
}

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


def get_all_column_annotations(data_dict: dict) -> list[dict]:
    return [
        column_content["Annotations"]
        for column_content in data_dict.values()
        if "Annotations" in column_content
    ]


def get_column_annotations_about(data_dict: dict, std_var: str) -> list[dict]:
    return [
        column_annotations for column_annotations in get_all_column_annotations(data_dict)
        if column_annotations["IsAbout"]["TermURL"] == std_var
    ]


def get_categorical_annotations_levels(column_annotations: dict) -> list[str]:
    levels_std_terms = []
    for level in column_annotations["Levels"].values():
        levels_std_terms.append(level["TermURL"])
    return levels_std_terms


def get_is_part_of_assessment(column_annotations: dict) -> str:
    return column_annotations["IsPartOf"]["TermURL"]


def transform_age(value: str, value_format: str) -> float | None:
    try:
        if value_format in [
            AGE_FORMATS["float"],
            AGE_FORMATS["int"],
        ]:
            return float(value)
        if value_format == AGE_FORMATS["euro"]:
            return float(value.replace(",", "."))
        if value_format == AGE_FORMATS["bounded"]:
            return float(value.strip("+"))
        if value_format == AGE_FORMATS["iso8601"]:
            if not value.startswith("P"):
                pvalue = "P" + value
            else:
                pvalue = value
            duration = isodate.parse_duration(pvalue)
            return float(duration.years + duration.months / 12)
        if value_format == AGE_FORMATS["range"]:
            a_min, a_max = value.split("-")
            return sum(map(float, [a_min, a_max])) / 2
        logger.error(
            f"The data dictionary contains an unrecognized age format: {value_format}. "
            f"Ensure that the format TermURL is one of {list(AGE_FORMATS.values())}.",
        )
    except (ValueError, isodate.isoerror.ISO8601Error) as e:
        logger.error(
            f"Error applying the format {value_format} to the age value: {value}. Error: {e}\n"
            f"Check your data dictionary to ensure that the annotated age format matches the age values in your phenotypic table, "
            "and that any missing values in your age column have been correctly annotated. "
            "For examples of acceptable values for specific age formats, see https://neurobagel.org/data_models/dictionaries/#age.",
        )
    return None


def get_summary_pheno_attributes(data_dict: dict, dataset_name: str) -> dict | None:
    summary_pheno_attributes = {}

    sex_column_annotations = get_column_annotations_about(data_dict, "nb:Sex")
    # Keep handling of >1 sex columns consistent with the CLI
    if len(sex_column_annotations) > 1:
        logger.warning(
            f"Dataset '{dataset_name}': The data dictionary indicates more than one column about participant sex, "
            "which is not currently supported in Neurobagel. "
            "Only the first of these columns will be used to determine available participant sex."
        )
    summary_pheno_attributes["available_sex"] = get_categorical_annotations_levels(
        sex_column_annotations[0]
    ) if sex_column_annotations else []

    available_diagnoses = []
    for diagnosis_column in get_column_annotations_about(data_dict, "nb:Diagnosis"):
        available_diagnoses.extend(
            get_categorical_annotations_levels(diagnosis_column)
        )
    summary_pheno_attributes["available_diagnoses"] = available_diagnoses

    available_assessments = []
    for assessment_column in get_column_annotations_about(data_dict, "nb:Assessment"):
        available_assessments.append(get_is_part_of_assessment(assessment_column))
    summary_pheno_attributes["available_assessments"] = available_assessments

    summary_pheno_attributes = {
        variable: list(dict.fromkeys(terms)) for variable, terms in summary_pheno_attributes.items()
    }
    
    # TODO: Handle age
    age_column_annotations = get_column_annotations_about(data_dict, "nb:Age")
    if len(age_column_annotations) > 1:
        logger.warning(
            f"Dataset '{dataset_name}': The data dictionary indicates more than one column about age, "
            "which is not currently supported in Neurobagel. "
            "Only the first of these columns will be used to determine the age range for the dataset."
        )
    if age_column_annotations:
        age_range = age_column_annotations[0]["ValueRange"]
        age_format = age_column_annotations[0]["Format"]["TermURL"]
        transformed_min = transform_age(age_range["Minimum"], age_format)
        transformed_max = transform_age(age_range["Maximum"], age_format)
        if transformed_min is None or transformed_max is None:
            logger.error(
                f"Dataset '{dataset_name}': Unable to transform the minimum and/or maximum age values to floats. "
            )
            return None

        summary_pheno_attributes["age_range"] = {
            "minimum": transformed_min,
            "maximum": transformed_max,
        }
    else:
        summary_pheno_attributes["age_range"] = None

    return summary_pheno_attributes


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
                logger.error(
                    f"{file}' is missing a corresponding {missing_file}. Skipping dataset."
                )
                continue

            # TODO: Validate the data dict
            data_dict = load_json(dataset_files["dictionary"])
            dataset_desc = load_json(dataset_files["description"])
            # TODO: Generate a UUID programmatically

            try:
                validated_dataset_desc = dataset_description_model.DatasetDescription.model_validate(dataset_desc)
            except ValidationError as err:
                logger.error(
                    f"{dataset_files['description']} is not a invalid Neurobagel dataset description. "
                    "Skipping dataset."
                    f"\nValidation details:\n"
                    f"{err}",
                )
                continue

            # dump back to dict
            validated_dataset_desc = validated_dataset_desc.model_dump()
            dataset_name = validated_dataset_desc["dataset_name"]

            if homepage_url := get_homepage_url(validated_dataset_desc["references_and_links"]):
                dataset_attributes["homepage"] = homepage_url
            
            dataset_summary_pheno_attributes = get_summary_pheno_attributes(data_dict, dataset_name)
            if dataset_summary_pheno_attributes is None:
                logger.error(
                    f"Dataset '{dataset_name}': Unable to extract summary phenotypic attributes from the data dictionary. Skipping dataset."
                )
                continue
            dataset_attributes = {**validated_dataset_desc, **dataset_summary_pheno_attributes}

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
