import overpy

def get_location_coords(location_name):
    api = overpy.Overpass()
    result = api.query("relation[name=%s];out center;" % location_name)
    max_rel = result.relations[0]
    for rel in result.relations:
        if len(rel.members) > len(max_rel.members):
            max_rel = rel

    return max_rel.center_lat, max_rel.center_lon
