import msal
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def acquire_token(client_id, tenant_id, scopes):
    """
    Authenticate with Microsoft using MSAL and return an access token.
    """
    authority = f'https://login.microsoftonline.com/{tenant_id}'
    app = msal.PublicClientApplication(client_id, authority=authority)
    accounts = app.get_accounts()

    result = None
    if accounts:
        logger.info("Attempting silent authentication...")
        result = app.acquire_token_silent(scopes, account=accounts[0])

    if not result:
        logger.info("Initiating device code flow...")
        flow = app.initiate_device_flow(scopes=scopes)
        if 'user_code' not in flow:
            logger.error("Failed to initiate device flow.")
            return None

        logger.info(flow['message'])
        result = app.acquire_token_by_device_flow(flow)

    if 'access_token' in result:
        logger.info("Authentication successful.")
        return result['access_token']
    else:
        logger.error(f"Authentication failed: {result}")
        return None