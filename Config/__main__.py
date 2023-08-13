
"""An OpenStack Python Pulumi program"""

import pulumi
from pulumi_openstack import compute
import pulumi_openstack as openstack
import pulumi
from pulumi_openstack import networking



# Register rancheros image #

rancheros = openstack.images.Image("rancheros",
    container_format="bare",
    disk_format="qcow2",
    image_source_url="https://releases.rancher.com/os/latest/rancheros-openstack.img",
    properties={
        "key": "value",
    })

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



# Create network #
network1 = openstack.networking.Network("network1", admin_state_up=True)
subnet1 = openstack.networking.Subnet("subnet1",
    network_id=network1.id,
    cidr="192.168.199.0/24",
    ip_version=4)
secgroup1 = openstack.compute.SecGroup("secgroup1",
    description="a security group",
    rules=[openstack.compute.SecGroupRuleArgs(
        from_port=22,
        to_port=22,
        ip_protocol="tcp",
        cidr="0.0.0.0/0",
    )])
port1 = openstack.networking.Port("port1",
    network_id=network1.id,
    admin_state_up=True,
    security_group_ids=[secgroup1.id],
    fixed_ips=[openstack.networking.PortFixedIpArgs(
        subnet_id=subnet1.id,
        ip_address="192.168.199.10",
    )])



test_flavor = openstack.compute.Flavor("test-flavor",
    disk=20,
    extra_specs={
        "hw:cpu_policy": "CPU-POLICY",
        "hw:cpu_thread_policy": "CPU-THREAD-POLICY",
    },
    ram=8096,
    vcpus=2)



# Create external network #



# Define the external network
external_network = openstack.networking.Network(
    "external-network",
    name="external-network",
    external=True,
    #network_type="flat",
)

# Define the subnet for the external network
subnet = openstack.networking.Subnet(
    "external-subnet",
    name="external-subnet",
    cidr="192.168.202.0/24",
    network_id=external_network.id,
    allocation_pools=[
#        openstack.networking.SubnetAllocationPoolArgs(start="192.168.202.0", end="192.168.202.254")
    ],
    gateway_ip="192.168.202.32",
)

# Export the external network and subnet information
pulumi.export("external_network_id", external_network.id)
pulumi.export("external_subnet_id", subnet.id)

# Define the router
router = openstack.networking.Router(
    "my-router",
    name="my-router",
    #external_network=external_network.id,
)



# Create security group #

network1 = openstack.networking.Network("network1", admin_state_up=True)
subnet1 = openstack.networking.Subnet("subnet1",
    network_id=network1.id,
    cidr="192.168.199.0/24",
    ip_version=4)
secgroup1 = openstack.compute.SecGroup("secgroup1",
    description="a security group",
    rules=[openstack.compute.SecGroupRuleArgs(
        from_port=22,
        to_port=22,
        ip_protocol="tcp",
        cidr="0.0.0.0/0",
    )])
port1 = openstack.networking.Port("port1",
    network_id=network1.id,
    admin_state_up=True,
    security_group_ids=[secgroup1.id],
    fixed_ips=[openstack.networking.PortFixedIpArgs(
        subnet_id=subnet1.id,
        ip_address="192.168.199.10",
    )])
instance1 = openstack.compute.Instance("instance1",
    security_groups=[secgroup1.name],
    networks=[openstack.compute.InstanceNetworkArgs(
        port=port1.id,
    )])




