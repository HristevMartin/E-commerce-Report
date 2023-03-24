Project Title
Brief description of the project.

### Running locally

#### Pre requisites

1.
    1. Install Python  version `3` and above
    2. Install MYSQL Workbench/Docker image for mysql
    3. Locate the Dump files in one location
    4. Install the package requirements - go in the root directory of the project and run pip install -r requirements.txt

2. Add environment variables
    1. It can be added as a shell script or via the interpreter
        1. IE_DB_HOST=localhost;
        2. DB_PORT=3306;
        3. IE_DB_USERNAME=root;
        4. IE_DB_PASSWORD=pass;
        5. IE_DB_NAME=simulation_cache_ie;
        6. DEPLOYMENT_PROJECT=local;

IMPORTANT NOTE: In order to create the tables and ingest the data we need to add environment variable.
    1. `DUMPS_PATH=PATH_OF_DUMPS_FOLDER` should be updated with the path of the downloaded csv files.

## Testing

### Run tests

Run all tests: `pytest`

Run a specific test file: `pytest dtwin-api/tests/unit/filename.py`

Run a specific test case: `pytest dtwin-api/tests/unit/filename.py::function_name`