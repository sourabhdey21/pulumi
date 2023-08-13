
"""An OpenStack Python Pulumi program"""

import pulumi
from pulumi_openstack import compute
import pulumi_openstack as openstack
import pulumi
from pulumi_openstack import networking





flavors_data = [
    {"name": "t2-small", "vcpus": 1, "ram": 1024, "disk": 10},
    {"name": "t4-medium", "vcpus": 2, "ram": 2048, "disk": 10},
    {"name": "t5-large", "vcpus": 4, "ram": 4096, "disk": 10},
    {"name": "t2-mini", "vcpus": 2, "ram": 4096, "disk": 10},
    {"name": "t2-micro", "vcpus": 2, "ram": 4096, "disk": 10},
    {"name": "t2-large", "vcpus": 2, "ram": 8192, "disk": 10},
    {"name": "t1-small", "vcpus": 2, "ram": 8192, "disk": 10},
    {"name": "t1-medium", "vcpus": 4, "ram": 8192, "disk": 10},
    {"name": "t1-large", "vcpus": 6, "ram": 8192, "disk": 10},

]

flavors = []

for flavor_data in flavors_data:
    flavor = openstack.compute.Flavor(
        flavor_data["name"],
        name=flavor_data["name"],
        vcpus=flavor_data["vcpus"],
        ram=flavor_data["ram"],
        disk=flavor_data["disk"],
    )
    flavors.append(flavor)

pulumi.export("flavors", [flavor.name for flavor in flavors])



project = openstack.identity.Project("my_project",
    description="Pulumi-Project",
    domain_id="default",
    enabled=True,
    is_domain=False,
    name="my_project"
)




# Create a new OpenStack flavor
flavor = openstack.compute.Flavor(
    "my-flavor",
    name="pulumi",
    ram=2048,
    vcpus=1,
    disk=20,
)



instance = openstack.compute.Instance(
    "pulumi-instance",
    name="pulumi",
    flavor_name="small",
    image_name="ubuntu",
    # network_interfaces=[
    #     {
    #         "network": "net1",
    #     }
    # ],
    # user_data="#cloud-config\nruncmd:\n - echo 'Hello, Pulumi!' > /tmp/greeting.txt",
    
       user_data=f"""#cloud-config
password: C1sc0123!
chpasswd: {{ expire: False }}
ssh_pwauth: True
""",

)
# Export the instance IP address
pulumi.export("instance_ip", instance.access_ip_v4)


# Create an OpenStack instance with cloud-init user data
instance = openstack.compute.Instance(
    "my-instance",
    name="my-instance",
    flavor_name="small",
    image_name="ubuntu",
    # network_interfaces=[
    #     {
    #         "network": "net1",
    #     }
    # ],
    user_data=f"""#cloud-config
password: 123
chpasswd: {{ expire: False }}
ssh_pwauth: True
""",
)

# Export the instance IP address
pulumi.export("instance_ip", instance.access_ip_v4)


# Create a key pair
keypair = openstack.compute.Keypair(
    "pulumi-keypair",
    name="pulumi-keypair",
)

pulumi.export("public_key", keypair.public_key)

# Create a security group
security_group = openstack.networking.SecGroup(
    "my-security-group",
    name="my-security-group",
    description="My Pulumi Security Group",
)

pulumi.export("security_group_id", security_group.id)




## Additional Resources ##

# Create a keypair
keypair = openstack.compute.Keypair(
    "my-keypair",
    name="my-keypair",
)


# Create an OpenStack instance with keypair
instance = openstack.compute.Instance(
    "keypair",
    name="keypair",
    flavor_name="small",
    image_name="ubuntu",
    # network_interfaces=[
    #     {
    #         "network": "YOUR_NETWORK_NAME",
    #     }
    # ],
    key_pair=keypair.name,
)

pulumi.export("instance_ip", instance.access_ip_v4)


# Define the network and subnet
network = openstack.networking.Network("my-network")
subnet = openstack.networking.Subnet(
    "my-subnet",
    network_id=network.id,
    cidr="192.168.0.0/24",
)

# Create an OpenStack port
port = openstack.networking.Port(
    "my-port",
    network_id=network.id,
    fixed_ips=[{"subnet_id": subnet.id,
                "ip_address": "192.168.0.10",
                }
               ],
)

pulumi.export("port_id", port.id)


# # Create an OpenStack instance with attached port
# instance = openstack.compute.Instance(
#     "port-instance",
#     name="port-instance",
#     flavor_name="small",
#     image_name="ubuntu",
#     # network_interfaces=[
#     #     {
#     #         "port": port.id,
#     #     }
#     # ],
# )

# pulumi.export("instance_ip", instance.access_ip_v4)

# Create an OpenStack volume
volume = openstack.blockstorage.Volume(
    "my-volume",
    size=15,  # Size in GB
)

pulumi.export("volume_id", volume.id)




## Attach volume in  vm using  ##

# Attach the volume to the instance
volume_attachment = openstack.compute.VolumeAttachment(
    "my-volume-attachment",
    instance_uuid=instance.id,
    volume_id=volume.id,
    device="/dev/vdb",  # Choose a device name
)







