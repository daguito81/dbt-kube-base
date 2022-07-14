from azure.storage.filedatalake import DataLakeServiceClient, ContentSettings
import logging
import os
import json
import sys

logging.basicConfig(level=logging.WARNING, stream=sys.stdout)

logging.warning("Starting Script")
DATALAKE_KEY = os.getenv("DAGOLAKE_KEY")
PROJECT_NAME = os.getenv("PROJECT_NAME")

storage_account_name = "dagolake"
storage_account_key = DATALAKE_KEY
container_name = "dbt-data"

search_str = 'o=[i("manifest","manifest.json"+t),i("catalog","catalog.json"+t)]'


def create_file_system_client(storage_account_name, storage_account_key, container_name, directory_name):
    """
    Creates a file system client for the specified storage account
    """
    logging.warning("Starting to create file system client")

    service_client = DataLakeServiceClient(
        account_url="https://{}.dfs.core.windows.net".format(storage_account_name),
        credential=storage_account_key
    )
    dfs_system_client = service_client.get_file_system_client(container_name)
    directory_client = dfs_system_client.get_directory_client(directory_name)
    logging.warning("Finished creating datalake client")
    return directory_client


def upload_html_file_adls2(path, file_system_client, file_name, html_file=False):
    """
    Uploads a file as text/html to azure data lake store gen 2
    to the $web container
    """
    logging.warning(f"Uploading file {file_name} to ADLS2. HTML: {html_file}")
    # index.html
    if html_file:
        index_file_client = file_system_client.create_file(file_name, content_settings=ContentSettings(content_type='text/html'))
    else:
        index_file_client = file_system_client.create_file(file_name)
    local_file = open(path, 'r')

    index_contents = local_file.read()

    index_file_client.append_data(data=index_contents, offset=0, length=len(index_contents))
    index_file_client.flush_data(len(index_contents))
    logging.warning(f"Finished file {file_name} to ADLS2")


def consolidate_documentation():
    logging.warning("Consolidating Documentation into index2.html")
    with open('/src/dbt/project/target/index.html', 'r') as f:
        content_index = f.read()

    with open('/src/dbt/project/target/manifest.json', 'r') as f:
        json_manifest = json.loads(f.read())

    with open('/src/dbt/project/target/catalog.json', 'r') as f:
        json_catalog = json.loads(f.read())

    with open('/src/dbt/project/target/index2.html', 'w') as f:
        new_str = "o=[{label: 'manifest', data: " + json.dumps(json_manifest) + "},{label: 'catalog', data: " + json.dumps(json_catalog) + "}]"
        new_content = content_index.replace(search_str, new_str)
        f.write(new_content)


consolidate_documentation()

file_system_client = create_file_system_client(storage_account_name, storage_account_key, container_name, PROJECT_NAME)
# index.html
upload_html_file_adls2("/src/dbt/project/target/index.html", file_system_client, "index.html", True)
# catalog.json
upload_html_file_adls2("/src/dbt/project/target/catalog.json", file_system_client, "catalog.json")
# manifest.json
upload_html_file_adls2("/src/dbt/project/target/manifest.json", file_system_client, "manifest.json")
# run_results.json
upload_html_file_adls2("/src/dbt/project/target/run_results.json", file_system_client, "run_results.json")
# Index2.html
upload_html_file_adls2("/src/dbt/project/target/index2.html", file_system_client, "index2.html")
