"""Rights management system."""
from keycloak import KeycloakAdmin
from django.conf import settings


class RightsManager:

    def __init__(self):
        config = settings.KEYCLOAK_CONFIG

        self.keycloak_admin = KeycloakAdmin(
            server_url=config["SERVER_URL"],
            realm_name=config["REALM_NAME"],
            client_id=config["CLIENT_ID"],
            client_secret_key=config["CLIENT_SECRET_KEY"],
            verify=True
        )

    # Create new group
    #group = keycloak_admin.create_group({"name": "Example Group"})

# except Exception as e:
#     print(e)
