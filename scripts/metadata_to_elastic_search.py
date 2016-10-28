import iris

iris.FUTURE.cell_datetime_objects = True
iris.FUTURE.netcdf_promote = True

def create_metadata(cube):
    metadata = {
        'name': cube.name(),
        'source': 's3://mogreps/2b6a/englaa_pd039_engl_um_006_20161001T0000Z',
        'model_run': cube.coord('forecast_reference_time').points[0] * 60 * 60,
        'validity_time': cube.coord('time').points[0] * 60 * 60,
        'coordinates': []}

    for coord in cube.coords():
        metadata['coordinates'].append({
            'name': coord.name(),
            'standard_name': coord.standard_name,
            'long_name': coord.long_name,
            #'points': [float(p) for p in coord.points.tolist()],
            'units': str(coord.units),
            'min': min(coord.points.tolist()),
            'max': min(coord.points.tolist())
        })
    return metadata

def process_file(filepath):
    cubes = iris.load(filepath)
    for cube in cubes:
        print (create_metadata(cube))
    return "processed"