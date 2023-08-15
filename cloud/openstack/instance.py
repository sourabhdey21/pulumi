"""An OpenStack Python Pulumi program"""

import pulumi
import pulumi_openstack as openstack
from pulumi_openstack import compute


# Substitute these values with appropriate parameters.
# Resource properties can be found in the official 
# OpenStack Pulumi provider documentation
image_name = "ubuntu"
flavor_name = "small"
network_id = "dd2fcdc9-1bc1-4cf7-95de-6f80d82c457c"
keypair_name = "keypair"

# Create an instance
instance = compute.Instance("ubuntu",
                            name="ubuntu-pulumi",
                            image_name=image_name,
                            flavor_name=flavor_name,
                            networks=[{"uuid": network_id}],  # Assumes only one network
                            key_pair=keypair_name)


# Export the instance Id
pulumi.export("instance_id", instance.id)
