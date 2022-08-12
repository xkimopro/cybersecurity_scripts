import csv,json,ipaddress

infile = 'new_networks.csv'
net_file = 'network_hiearchy_export.json'
outfile = 'updated_network_hierarchy.json'

composite_key_separator = '____'


ids = []
network_ids = []
network_names_to_ids = {}
cidrs_of_networks = {}
groups = []

def ipRangeToCidrNotation(ip_range):
    startip = ipaddress.IPv4Address(ip_range[0])
    endip = ipaddress.IPv4Address(ip_range[1])
    return [str(ipaddr) for ipaddr in ipaddress.summarize_address_range(startip, endip)]

with open(net_file, 'r') as network_file:
    net_hierarchy = json.loads(network_file.read()) 
    for network in net_hierarchy:
        groups.append(network['group'])
        ids.append(int(network['id']))
        network_ids.append(int(network['network_id']))
        composite_key = network['group'] + composite_key_separator + network['name']
        network_names_to_ids[composite_key] = network['network_id']
        if composite_key not in cidrs_of_networks: cidrs_of_networks[composite_key] = [network['cidr']]
        else: cidrs_of_networks[composite_key].append(network['cidr'])


ids = sorted(ids)
network_ids = sorted(list(set(network_ids)))
groups = sorted(list(groups))

duplicate_inserts = []
invalid_inserts = []
new_inserts = []
new_net_hierarchy = net_hierarchy.copy()


with open(infile, 'r', encoding='utf-8-sig') as csvfile:
    dict_reader = csv.DictReader(csvfile)
    for row in dict_reader:
        
        group = row['group']
        # cidr = ipRangeToCidrNotation(row['ip_range'].split(' - '))[0]
        cidr = row['cidr']
        name = row['name']
        country_code= row['country_code']
        description = row['description']
        domain_id = int(row['domain_id'])
        # Search for the combination of group and network name to see if it already exists
        composite_key = group + composite_key_separator + name

        # If it exists fetch its network_id and check if the cidr is already in the list for that specific id
        if (composite_key in network_names_to_ids):
            new_network_id = network_names_to_ids[composite_key]
            # Then create the new id for that specific cidr as the max(past_ids)
            new_id = max(ids) + 1
        # Else create a new network_id and the new cidr_id becomes equal to that
        else:
            new_network_id = max(ids) + 1
            new_id = new_network_id
        
        # Create the entry
        entry = {
            "country_code": country_code,
            "name":  name ,
            "description": description,
            "network_id": new_network_id,
            "cidr": cidr,
            "id": new_id,
            "domain_id": domain_id,
            "group": group
        }
        
        # Check if cidr already exists inside the group-network combination
        if composite_key in network_names_to_ids and cidr in cidrs_of_networks[composite_key]:
                duplicate_inserts.append(entry)
                continue

        # Check for nonexistent groups
        if group not in groups:
            invalid_inserts.append(entry)
            continue
        
        new_inserts.append(entry)
        new_net_hierarchy.append(entry)
        ids.append(new_id)
        network_ids.append(new_network_id)
        if composite_key in cidrs_of_networks: cidrs_of_networks[composite_key].append(cidr)
        else: cidrs_of_networks[composite_key] = [cidr]
        network_names_to_ids[composite_key] = new_network_id

        ids = list(set(ids))
        network_ids = list(set(network_ids))

# Comment out for debugging
# print(invalid_inserts)
# print(duplicate_inserts)


jbytes = json.dumps(new_net_hierarchy).encode()
with open(outfile, "wb") as binary_file: binary_file.write(jbytes)