import json

with open('korea_geo.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

min_lon, max_lon = 124.5, 131.5
min_lat, max_lat = 33.0, 39.0

width = 600
height = 800

def project(lon, lat):
    x = ((lon - min_lon) / (max_lon - min_lon)) * width
    y = height - (((lat - min_lat) / (max_lat - min_lat)) * height)
    return x, y

REGION_MAP_LABEL = {
    '서울특별시': '서울', '부산광역시': '부산', '대구광역시': '대구',
    '인천광역시': '인천', '광주광역시': '광주', '대전광역시': '대전',
    '울산광역시': '울산', '경기도': '경기', '강원도': '강원',
    '충청북도': '충북', '충청남도': '충남', '전라북도': '전북',
    '전라남도': '전남', '경상북도': '경북', '경상남도': '경남',
    '제주특별자치도': '제주', '세종특별자치시': '세종'
}

svg_str = '<svg viewBox=\"0 0 600 800\" preserveAspectRatio=\"xMidYMid meet\" class=\"w-full h-full drop-shadow-[0_0_15px_rgba(30,144,255,0.15)]\">\n'

for feature in data['features']:
    raw_name = feature['properties'].get('name_kor', feature['properties'].get('name', feature['properties'].get('CTP_KOR_NM', '')))
    name = REGION_MAP_LABEL.get(raw_name, raw_name)
    geom_type = feature['geometry']['type']
    coords = feature['geometry']['coordinates']

    d = ''
    def render_ring(ring, path_str):
        for i, point in enumerate(ring):
            lon, lat = point[0], point[1]
            x, y = project(lon, lat)
            prefix = 'M' if i == 0 else 'L'
            path_str += f'{prefix}{x:.1f},{y:.1f} '
        path_str += 'Z '
        return path_str

    if geom_type == 'Polygon':
        for ring in coords:
            d = render_ring(ring, d)
    elif geom_type == 'MultiPolygon':
        for poly in coords:
            for ring in poly:
                d = render_ring(ring, d)

    svg_str += f'  <path id=\"map-region-{name}\" d=\"{d.strip()}\" '
    svg_str += f'class=\"region-path transition-colors duration-300 stroke-[#151c24] stroke-[1px] hover:stroke-white hover:stroke-[2.5px] cursor-pointer\" '
    svg_str += f'fill=\"#283039\" '
    svg_str += f'onclick=\"selectMapRegion(\'{name}\')\" '
    svg_str += f'onmousemove=\"showMapTooltip(event, \'{name}\')\" '
    svg_str += f'onmouseout=\"hideMapTooltip()\">\n'
    svg_str += f'    <title>{name}</title>\n  </path>\n'

svg_str += '</svg>'

with open('map_korea.js', 'w', encoding='utf-8') as f:
    f.write('const KOREA_SVG = `\n' + svg_str + '\n`;\n')

print('Successfully generated map_korea.js')
