import json
import math

with open('../tr-cities.json', 'r', encoding='utf-8') as f:
    geojson = json.load(f)

min_lon, max_lon = 25.6651, 44.8338
min_lat, max_lat = 35.8154, 42.1054
mid_lat_rad = math.radians(39.0)
cos_mid = math.cos(mid_lat_rad)

width, height = 1100, 500
padding = 25

proj_w = (max_lon - min_lon) * cos_mid
proj_h = (max_lat - min_lat)

scale_x = (width - 2 * padding) / proj_w
scale_y = (height - 2 * padding) / proj_h
scale = min(scale_x, scale_y)

def project(lon, lat):
    px = padding + (lon - min_lon) * cos_mid * scale
    py = height - (padding + (lat - min_lat) * scale)
    return round(px, 1), round(py, 1)

city_features = []
for feat in geojson['features']:
    props = feat['properties']
    geom = feat['geometry']
    polys = [geom['coordinates']] if geom['type'] == 'Polygon' else geom['coordinates']
    
    path_cmds = []
    total_x, total_y, count = 0, 0, 0
    
    for poly in polys:
        for ring in poly:
            for idx, c in enumerate(ring):
                px, py = project(c[0], c[1])
                total_x += px
                total_y += py
                count += 1
                cmd = "M" if idx == 0 else "L"
                path_cmds.append(f"{cmd}{px},{py}")
            path_cmds.append("Z")
            
    cx = round(total_x / count, 1) if count > 0 else 0
    cy = round(total_y / count, 1) if count > 0 else 0
    plate = props.get('number', 0)
    name = props.get('name', '')
    
    city_features.append({
        'plate': plate,
        'name': name,
        'cx': cx,
        'cy': cy,
        'd': "".join(path_cmds)
    })

city_features.sort(key=lambda x: x['plate'])
print(f"Successfully processed {len(city_features)} provinces.")
for c in city_features:
    if c['plate'] in [1, 6, 34, 35, 7, 50, 61, 36]:
        print(f"Plate {c['plate']:02d} ({c['name']}): ({c['cx']}, {c['cy']})")

with open('turkey_svg_map.json', 'w', encoding='utf-8') as f:
    json.dump(city_features, f, ensure_ascii=False)
