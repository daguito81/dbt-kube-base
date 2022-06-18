echo "Starting Init"
echo "COPYING KEYS"
cp /root/ssh-keys/ssh-privatekey /root/.ssh/id_rsa
cp /root/ssh-keys/ssh-publickey /root/.ssh/id_rsa.pub
echo "CLONING REPO"
git clone $(cat /root/dbt-config/$PROJECT_NAME) /src/dbt
echo "RUNNING DBT"
dbt run -t dev-password --project-dir /src/dbt/$PROJECT_NAME/ --profiles-dir /src/dbt/dbt_profiles/
echo "DONE HERE"