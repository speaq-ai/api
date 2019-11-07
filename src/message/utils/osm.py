import overpy


def capitalize_location(location_name):
    separator = " "
    cap_location = ""
    for word in location_name.split(separator):
        cap_location += word.capitalize() + separator
    return cap_location[:-1]

def get_location_coords(location_name):
    api = overpy.Overpass()
    try:
        result = api.query('node["name"="%s"];out center;' % capitalize_location(location_name))
        max_node = result.nodes[0]
        for node in result.nodes:
            if len(node.tags) > len(max_node.tags):
                max_node = node
        return float(max_node.lat), float(max_node.lon)
    except OverpassTooManyRequests:
        return get_location_coords(location_name)
