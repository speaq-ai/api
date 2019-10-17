import overpy


def capitalize_location(location_name):
    separator = " "
    cap_location = ""
    for word in location_name.split(separator):
        cap_location += word.capitalize() + separator
    return cap_location[:-1]

def get_location_coords(location_name):
    api = overpy.Overpass()
    result = api.query('relation["name"="%s"];out center;' % capitalize_location(location_name))
    max_rel = result.relations[0]
    for rel in result.relations:
        if len(rel.members) + len(rel.tags) > len(max_rel.members) + len(max_rel.tags):
            max_rel = rel

    return float(max_rel.center_lat), float(max_rel.center_lon)
