echo "Starting Init"
echo "COPYING KEYS"
cp /root/ssh-keys/ssh-privatekey /root/.ssh/id_rsa
cp /root/ssh-keys/ssh-publickey /root/.ssh/id_rsa.pub
echo "CLONING REPO"
git clone $(cat /root/dbt-config/$PROJECT_NAME) /src/dbt
echo "DONE HERE"