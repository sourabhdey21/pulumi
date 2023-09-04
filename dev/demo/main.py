import pulumi
import pulumi_openstack as openstack
from pulumi_openstack import compute


# Define the OpenStack provider configuration

provider = openstack.Provider("openstack",

    user_name="admin",

    password="7dH59ip8eJsOQFSfM2zIgnLSqHINRYRwJaJI778m",

    tenant_name="game_net2",

    auth_url="http://192.168.2.22:5000",

    allow_reauth="true",

)

 

def create_network(Network_Name: str):

    network = openstack.networking.Network(Network_Name,

    name=Network_Name,

    admin_state_up="true",

    #mtu="1450",

    #shared="true",

    #port_security_enabled="false",

    )

    pulumi.export("Network Name: ",network.name)

    pulumi.export("Network ID: ",network.id)

    return network

 

def create_subnet(network: openstack.networking.Network, Subnet_Name: str, Cidr: str, Gateway: str):

    subnet = openstack.networking.Subnet(Subnet_Name,

    name=Subnet_Name,

    network_id=network.id,

    cidr=Cidr,

    #allocation_pools=[{"start": "10.0.0.10", "end": "10.0.0.20"}],

    gateway_ip=Gateway,

    )

    pulumi.export("SUBNET Name: ",subnet.name)

    pulumi.export("SUBNET ID: ",subnet.id)

    pulumi.export("SUBNET Gateway: ",subnet.gateway_ip)

    pulumi.export("SUBNET CIDR: ",subnet.cidr)

 

    return subnet

 
 
 # Define OpenStack compute instance
instance = compute.Instance("vyos-router",
    name="vyos-router",
    image_id="227fc037-dd3d-4758-9d6b-d27aa0f5d444",      # Replace with your Image ID
    flavor_name="m1.small", # Replace with your instance Flavor
    networks=[{"uuid": "212a8327-9dde-4444-bef6-dc94d538f5da"}])  # Replace with your Network ID
pulumi.export('instance_id', instance.id)


# Define several OpenStack compute instances
num_instances = 3  # Specify the number of instances you want to create
instances = {}

for i in range(num_instances):
    instances[i] = compute.Instance(f"my-instance-{i}",
        name=f"my-instance-{i}",
        image_id="227fc037-dd3d-4758-9d6b-d27aa0f5d444",      # Replace with your Image ID
        flavor_name="m1.small", # Replace with your instance Flavor
        networks=[{"uuid": "212a8327-9dde-4444-bef6-dc94d538f5da"}])  # Replace with your Network ID

# Export instance IDs
for i in range(num_instances):
    pulumi.export(f'instance_id_{i}', instances[i].id)


# def create_router(name: str, flavor: str,image: str, Network: list):

#     router = openstack.compute.Instance(name,

#         flavor_name=flavor,

#         image_name=image,

#         #networks=[EX_GF.name],

#         networks=Network,

#     )

#     pulumi.export("Router Name: ",router.name)

#     pulumi.export("Router ID: ",router.id)

#     pulumi.export("Router Interfaces: ",router.networks)

#     return router

 

# def create_firewall(name: str, flavor: str,image: str, Network: list):

#     firewall = openstack.compute.Instance(name,

#         flavor_name=flavor,

#         image_name=image,

#         #networks=[EX_GF.name],

#         networks=Network,

#     )

#     pulumi.export("Firewall Name: ",firewall.name)

#     pulumi.export("Firewall ID: ",firewall.id)

#     pulumi.export("Firewall Interfaces: ",firewall.networks)

#     return firewall

 

# def create_instance(name: str, flavor: str,image: str, Network: list,Block_device: list,):

 

#     instance = openstack.compute.Instance(name,

 

#         flavor_name=flavor,

 

#         image_name=image,

 

#         #networks=[EX_GF.name],

 

#         networks=Network,

 

#         block_devices=Block_device,

 

#     )

 

#     pulumi.export("Instance Name: ",instance.name)

 

#     pulumi.export("Instance ID: ",instance.id)

 

#     pulumi.export("Instance Interfaces: ",instance.networks)

 

#     return instance

# GR_interface = []

 

# block = [{"source_type":"snapshot",

# "uuid":"9a600d3a-8013-4fd3-933d-632f440f11e5"}]

 

 

# GR = create_instance("Gr","m1.small","vyos-img",GR_interface,block)

 

from utils import network_list,subnet_list,gateway_list

 

data_list = {'network':network_list,'subnet':subnet_list,'gateway':gateway_list}

for i in range(len(data_list['network'])):

    network = create_network(data_list['network'][i])

    network_subnet = create_subnet(network,f"{data_list['network'][i]}_subnet",data_list['subnet'][i],data_list['gateway'][i])

 
