#!/bin/bash

echo "Starting Init"
echo "RUNNING DBT"
echo "BUILD"

if [[ "$FULL_REFRESH" = "true" ]]; then
    echo "Running dbt with Full Refresh"
    dbt build -t dev-password --project-dir /src/dbt/project/ --profiles-dir /src/dbt/dbt_profiles/ --full-refresh
else
    echo "Running dbt without Full Refresh"
    dbt build -t dev-password --project-dir /src/dbt/project/ --profiles-dir /src/dbt/dbt_profiles/
fi

# echo "RUN"
# dbt run -t dev-password --project-dir /src/dbt/$PROJECT_NAME/ --profiles-dir /src/dbt/dbt_profiles/
echo "DOCS"
dbt docs generate -t dev-password --project-dir /src/dbt/project/ --profiles-dir /src/dbt/dbt_profiles/ --no-compile
echo "DONE WITH DBT"
echo "POST-RUNNING DBT"

python /src/parser.py

# tail -f /dev/null