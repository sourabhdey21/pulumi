"""An OpenStack Python Pulumi program"""

import pulumi
import pulumi_openstack as openstack
from pulumi_openstack import compute

# import pulumi 
# from pulumi_openstack import compute, network


secgroup1 = openstack.compute.SecGroup("secgroup1",
    description="a security group",
    rules=[openstack.compute.SecGroupRuleArgs(
        from_port=22,
        to_port=22,
        ip_protocol="tcp",
        cidr="0.0.0.0/0",
    )])


network1 = openstack.networking.Network("network2", admin_state_up=True)
subnet1 = openstack.networking.Subnet("subnet2",
    network_id=network1.id,
    cidr="192.168.200.0/24",
    ip_version=4)


port1 = openstack.networking.Port("port1",
    network_id=network1.id,
    admin_state_up=True,
    security_group_ids=[secgroup1.id],
    fixed_ips=[openstack.networking.PortFixedIpArgs(
        subnet_id=subnet1.id,
        ip_address="192.168.200.10",
    )])


#Attach interface







# Create Project resources

project2 = openstack.identity.Project("project2", description="project create by pulumi")

# Export the pulumi  project id 
pulumi.export("project_id",project2.id)



project3 = openstack.identity.Project("project3")
flavor2 = openstack.compute.Flavor("flavor2",
    name="t2-pulumi",
    ram=8096,
    vcpus=2,
    disk=20,
    is_public=False)
access1 = openstack.compute.FlavorAccess("access1",
    tenant_id=project3.id,
    flavor_id=flavor2.id)




pulumi_keypair = openstack.compute.Keypair("test-keypair",
                                         name="pulumi-keypair")


#Securiy block start # 

secgroup1 = openstack.compute.SecGroup("pulumi-sec1",
    description="my security group",
    name="pulumi-securitygroup",
    rules=[
        openstack.compute.SecGroupRuleArgs(
            cidr="0.0.0.0/0",
            from_port=22,
            ip_protocol="tcp",
            to_port=22,
        ),
        openstack.compute.SecGroupRuleArgs(
            cidr="0.0.0.0/0",
            from_port=80,
            ip_protocol="tcp",
            to_port=80,
        ),
    ])

# Security group block end #



# # Create a server (VM)
# server = compute.Instance(
#     "ubuntu",
#     flavor_name="small",
#     image_name="ubuntu",
#     network_id="dd2fcdc9-1bc1-4cf7-95de-6f80d82c457c",
# )


# # Create a new network
# openstack_network = network.Network(
#     "my-network",
#     admin_state_up=True,
#     external=False,
# )

# # Create a subnet within the network
# subnet = network.Subnet(
#     "my-subnet",
#     network_id=openstack_network.id,
#     cidr="10.0.1.0/24",
#     ip_version=4,
# )

# # Create a subnet within the network
# subnet = network.Subnet(
#     "my-subnet",
#     network_id=openstack_network.id,
#     cidr="10.0.1.0/24",
#     ip_version=4,
# )


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
                            config_drive= True,
                            user_data=f"""#!/bin/bash
                            # Set a password for the 'cirros' user
    `                       echo 'ubuntu:C1sc0123!' | chpasswd
                            """, 
                            key_pair=keypair_name)
                            


# Export the instance Id
pulumi.export("instance_id", instance.id)


#Register glance image using url #

# # Register a new image
# custom_image = compute.Image(
#     "custom-image",
#     name="ubuntu-20",
#     min_disk=10,  # Minimum disk size in GB
#     min_ram=1024,  # Minimum RAM in MB
#     file="/home/pulumi/focal-server-cloudimg-amd64.img",  # Path to your image file
#     disk_format="qcow2",  # Disk format of the image
#     container_format="bare",  # Container format of the image
# )

ubuntu20 = openstack.images.Image("ubuntu20",
    container_format="bare",
    name="ubuntu20",
    disk_format="qcow2",
    local_file_path="/home/pulumi/focal-server-cloudimg-amd64.img",
    properties={
        "key": "value",
    })



# Export the image ID
pulumi.export("image_id", ubuntu20.id)



