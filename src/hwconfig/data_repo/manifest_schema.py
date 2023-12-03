import json

from hwconfig import REPO_DIR
from hwconfig.models import RepoManifestModel


def generate_repo_manifest_schema() -> None:
    """Generate a schema for the repo manifest model in the base directory of this repo."""
    model = RepoManifestModel()
    data = model.model_json_schema()
    schema_file = REPO_DIR / "repo_manifest.schema.json"

    schema_file.touch()
    schema_file.write_text(data=json.dumps(data, indent=2))


if __name__ == "__main__":
    generate_repo_manifest_schema()
