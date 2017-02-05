import time

from azure.storage import AccessPolicy
from azure.storage.blob import AppendBlobService, ContentSettings, ContainerPermissions

from datetime import datetime, timedelta

# The name of the new Shared Access policy
policy_name = 'uploadpolicy'
# The Storage Account Name
storage_account_name = 'asq'
storage_account_key = 'FB9fAfnEv1uokM0KZmEbC38EFpxBESFCJKboqQaxSysTudNsRsHTB0HHDv4eSqUV2RUUK7RR9WiplPn0C07LZw=='
storage_container_name = 'media-file'

# Create the blob service, using the name and key for your Azure Storage account
append_service = AppendBlobService(account_name='asqdata', account_key='FB9fAfnEv1uokM0KZmEbC38EFpxBESFCJKboqQaxSysTudNsRsHTB0HHDv4eSqUV2RUUK7RR9WiplPn0C07LZw==')

# Create a new policy that expires after a week
access_policy = AccessPolicy(permission=ContainerPermissions.READ + ContainerPermissions.LIST + ContainerPermissions.WRITE, expiry=datetime.utcnow() + timedelta(hours=24))

# Get the existing identifiers (policies) for the container
identifiers = append_service.get_container_acl(storage_container_name)
# And add the new one ot the list
identifiers[policy_name] = access_policy

# Set the container to the updated list of identifiers (policies)
append_service.set_container_acl(
	storage_container_name,
	identifiers,
)

# Wait 30 seconds for acl to propagate
time.sleep(30)

# Generate a new Shared Access Signature token using the policy (by name)
sas_token = append_service.generate_container_shared_access_signature(
	storage_container_name,
	id=policy_name,
)

print('https://asqdata.blob.core.windows.net/media-file?' + sas_token)

f = open('containerSASToken.txt', 'wb')
f.write('https://asqdata.blob.core.windows.net/media-file?' + sas_token)
f.close()
