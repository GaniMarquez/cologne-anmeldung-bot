from distutils.util import strtobool

import os
import logging

from dotenv import load_dotenv


load_dotenv(".env")

# General Configs
DEBUG: bool = bool(strtobool(os.getenv("DEBUG", "False")))
TELEGRAM_API_TOKEN: str = os.getenv("TELEGRAM_API_TOKEN")


# DOCUMENT_TYPES: list = [
#     doc_type.strip().lower() for doc_type in os.getenv("DOCUMENT_TYPES").split(",") if doc_type
# ]

# DATASET_BUCKET_NAMES = {
#     "uat": "ids-dataset-uat",
#     "prod": "ids-dataset-prod",
# }

# # Vault Configs
# VAULT_ENABLED: bool = bool(strtobool(os.getenv("VAULT_ENABLED", "True")))
# VAULT_URL: str = os.getenv("VAULT_URL")
# VAULT_ROLE: str = os.getenv("VAULT_ROLE")
# VAULT_VERIFY: str = os.getenv("VAULT_VERIFY", "/tls/vault-tls")
# DATATOOLS_ML_S3_SECRET_KEY: str = os.getenv("DATATOOLS_ML_S3_SECRET_KEY", "kv/ml_pipelines")
# IDS_APPLICATION_S3_SECRET_KEY: str = os.getenv(
#     "IDS_APPLICATION_S3_SECRET_KEY", "kv/regression_storagegrid"
# )

# # S3 Configs
# S3_AUTH_ENABLED: bool = bool(strtobool(os.getenv("S3_AUTH_ENABLED", "True")))
# S3_ENDPOINT_URL: str = os.getenv("S3_ENDPOINT_URL")
# S3_REGION: str = os.getenv("S3_REGION")
# S3_TIMEOUT: int = int(os.getenv("S3_TIMEOUT", 600))
# S3_RETRY_COUNT: int = int(os.getenv("S3_RETRY_COUNT", 5))
# S3_LIST_OBJECT_MAX_KEYS: int = int(os.getenv("S3_LIST_OBJECT_MAX_KEYS", 100))
# S3_CHUNK_SIZE: int = int(os.getenv("S3_CHUNK_SIZE", 100))
# S3_MAX_CONCURRENCY: int = int(os.getenv("S3_MAX_CONCURRENCY", 10))

# Logging Specific Configs
_logging_levels = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}
LOGGING_LEVEL = _logging_levels.get(
    os.getenv("LOGGING_LEVEL", "INFO").upper(),
    logging.INFO,
)
