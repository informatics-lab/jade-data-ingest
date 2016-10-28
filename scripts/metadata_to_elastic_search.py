import iris

iris.FUTURE.cell_datetime_objects = True
iris.FUTURE.netcdf_promote = True

def create_metadata(cube, bucket, key):
    metadata = {
        'name': cube.name(),
        'bucket': bucket,
        'key': key,
        'model_run': cube.coord('forecast_reference_time').points[0] * 60 * 60,
        'validity_time': cube.coord('time').points[0] * 60 * 60,
        'coordinates': []}

    for coord in cube.coords():
        points = [float(p) for p in coord.points.tolist()]
        metadata['coordinates'].append({
            'name': coord.name(),
            'standard_name': coord.standard_name,
            'long_name': coord.long_name,
            'points': points,
            'units': str(coord.units),
            'min': min(points),
            'max': max(points),
            'num_points': len(points)
        })
    return metadata

def process_file(filepath, bucket, key):
    cubes = iris.load(filepath)
    for cube in cubes:
        print (create_metadata(cube, bucket, key))
    return "processed"