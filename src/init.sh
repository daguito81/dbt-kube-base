echo "Starting Init"
echo "COPYING KEYS"
cp /root/ssh-keys/ssh-privatekey /root/.ssh/id_ed25519
cp /root/ssh-keys/ssh-publickey /root/.ssh/id_ed25519.pub
echo "CLONING REPO"
git clone $(cat /root/dbt-config/$PROJECT_NAME) /src/dbt
echo "RUNNING DBT"
echo "BUILD"
dbt build -t dev-password --project-dir /src/dbt/$PROJECT_NAME/ --profiles-dir /src/dbt/dbt_profiles/
echo "RUN"
dbt run -t dev-password --project-dir /src/dbt/$PROJECT_NAME/ --profiles-dir /src/dbt/dbt_profiles/
echo "DONE WITH DBT"
echo "POST-RUNNING DBT"

python /src/parser.py
