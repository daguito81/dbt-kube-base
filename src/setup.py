from tokenazad.tokenmagic import AzureADTokenSetter
import os
import logging
import sys

service = sys.argv[1] if len(sys.argv) > 1 else None


logging.info("Starting Token Magic")
client = AzureADTokenSetter(
    tenant=os.getenv("TENANT_ID"),
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    oauth_scope=os.getenv("OAUTH_SCOPE"),
    var_prefix=service,
)

logging.info("Getting Token")
client.do_magic_trick()


class TokenHolder:
    def __init__(self):
        self.token = os.getenv("TOKEN")

    def __repr__(self):
        return "export TOKEN={}".format(self.token)


x = TokenHolder()
logging.info("Persisting Token")
client.persist_token("./tokenazad/")
