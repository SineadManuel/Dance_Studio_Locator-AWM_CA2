import json

from django.contrib.auth.decorators import login_required
from django.contrib.gis.geos import Point, Polygon
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
import overpy


def index(request):
    return render(request, 'ds_locator/index.html')


def register(request):
    if request.method == 'POST':
        regform = UserCreationForm(request.POST)

        if regform.is_valid():
            regform.save()
            return redirect('login')
    else:
        regform = UserCreationForm()
    return render(request, 'ds_locator/register.html', {'form': regform})


def maps(request):
    return render(request, 'ds_locator/map.html')


@login_required
def update_database(request):
    my_location = request.POST.get("point", None)
    if not my_location:
        return JsonResponse({"message": "No location found."}, status=400)

    try:
        my_coords = [float(coord) for coord in my_location.split(", ")]
        my_profile = request.user
        my_profile.last_location = Point(my_coords)
        my_profile.save()

        message = f"Updated {request.user.username} with {f'POINT({my_location})'}"

        return JsonResponse({"message": message}, status=200)
    except:
        return JsonResponse({"message": "No profile found."}, status=400)


@login_required
def find_studio(request):
    print("in find_studio()")
    try:
        # Create overpass API object
        api = overpy.Overpass()

        bbox = request.POST.get("bbox", None)
        print('bbox: ' + bbox)
        if bbox:
            b_box = bbox.split(",")
            shuffled_bbox = [b_box[1], b_box[0], b_box[3], b_box[2]]
            mod_bbox = [float(item) for item in shuffled_bbox]
            print(mod_bbox)

        result = api.query(f'''
            [out:json][timeout:25];
            // gather results
            (
                // query part for: ""dance:style"=*"
                node["dance:style"]({{bbox}});
                way["dance:style"]({{bbox}});
                relation["dance:style"]({{bbox}});
              
                // query part for: “amenity=dancing_school”
                node["amenity"="dancing_school"]({{bbox}});
                way["amenity"="dancing_school"]({{bbox}});
                relation["amenity"="dancing_school"]({{bbox}});
              
                // query part for: “"dance:teaching"=yes”
                node["dance:teaching"="yes"]({{bbox}});
                way["dance:teaching"="yes"]({{bbox}});
                relation["dance:teaching"="yes"]({{bbox}});
              
                // query part for: “leisure=dance”
                node["leisure"="dance"]({{bbox}});
                way["leisure"="dance"]({{bbox}});
                relation["leisure"="dance"]({{bbox}});
            );
            // print results
            out body;
            >;
            out skel qt;
        ''')

        print("nodes: ", len(result.nodes))

        geojson_result = {
            "type": "FeatureCollection",
            "features": [],
        }

        nodes_in_way = []

        for way in result.ways:
            geojson_feature = {
                "type": "Feature",
                "id": "",
                "geometry": "",
                "properties": {}
            }

            poly = []

            for node in way.nodes:
                # Record the nodes and make the polygon
                nodes_in_way.append(node.id)
                poly.append([float(node.lon), float(node.lat)])

            try:
                poly = Polygon(poly)
            except:
                continue

            geojson_feature["id"] = f"way_{way.id}"
            geojson_feature["geometry"] = json.loads(poly.centroid.geojson)
            geojson_feature["properties"] = {}
            for k, v in way.tags.items():
                geojson_feature["properties"][k] = v

            geojson_result["features"].append(geojson_feature)

        for node in result.nodes:
            # Ignore nodes which are also in a 'way' as we will have already processed the 'way'.
            if node.id in nodes_in_way:
                continue

            geojson_feature = {
                "type": "Feature",
                "id": "",
                "geometry": "",
                "properties": {}
            }

            point = Point([float(node.lon), float(node.lat)])
            geojson_feature["id"] = f"node_{node.id}"
            geojson_feature["geometry"] = json.loads(point.geojson)
            geojson_feature["properties"] = {}

            for k, v in node.tags.items():
                geojson_feature["properties"][k] = v

            geojson_result["features"].append(geojson_feature)

        return JsonResponse(geojson_result, status=200)
    except Exception as e:
        return JsonResponse({"message": f"Error: {e}."}, status=400)
