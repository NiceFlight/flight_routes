import json
import os
import pandas as pd
from geographiclib.geodesic import Geodesic

url = r"D:/NiceFlight/Airline_Manager/flight_plan.xlsx"

airportsDF = pd.read_excel(url, sheet_name="airportsData")


def separate_routes(opType: str):

    df = pd.read_excel(url, sheet_name=opType)
    Routes = df["Route"].tolist()

    end_list = []
    for data in Routes:
        start_point = data[:3]
        end_point = data[-3:]

        end_list.append(end_point)

        start_lat = airportsDF[airportsDF["IATA Code"].str.strip() == start_point]["Lat"].values[0]
        start_lng = airportsDF[airportsDF["IATA Code"].str.strip() == start_point]["Lng"].values[0]

        end_lat = airportsDF[airportsDF["IATA Code"].str.strip() == end_point]["Lat"].values[0]
        end_lng = airportsDF[airportsDF["IATA Code"].str.strip() == end_point]["Lng"].values[0]
        print(f"{start_point}-{end_point}: ({start_lat}, {start_lng}), ({end_lat}, {end_lng})")

        # model: sphere
        geod = Geodesic(6371000, 0)  # type: ignore
        line = geod.InverseLine(start_lat, start_lng, end_lat, end_lng)

        points1 = []
        points2 = []
        n = 100  # Number of points to generate

        if abs(start_lng - end_lng) > 180:
            # If the line crosses the 180-degree meridian, we need to split it into two lines
            print(f"{start_point}-{end_point}: 跨越 180 度經線")

            for i in range(n + 1):
                # point 各數值解說：起始經緯度(lat1, lon1), 終點經緯度(lat2, lon2), 大圓距離(s12), 起始方位角：azi1, 終點方位角：azi2, 起點到終點的大圓角距(a12)
                point = line.Position(i * line.s13 / n)

                if point["lon2"] > 0 and point["lon2"] < 180:

                    # If the longitude is between 0 and 180, add it to points1
                    points1.append((point["lon2"], point["lat2"]))

                elif point["lon2"] < 0 and point["lon2"] > -180:

                    # If the longitude is between -180 and 0, add it to points2
                    points2.append((point["lon2"], point["lat2"]))

                else:
                    points1.append((point["lon2"], point["lat2"]))

        else:
            print(f"{start_point}-{end_point}: 沒有跨越 180 度經線")

            for i in range(n + 1):
                point = line.Position(i * line.s13 / n)
                points1.append((point["lon2"], point["lat2"]))

        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": ("MultiLineString" if points2 else "LineString"),
                        "coordinates": ([points1, points2] if points2 else points1),
                    },
                    "properties": {"start": start_point, "end": end_point, "distance": f"{line.s13/1000:.0f}"},
                }
            ],
        }

        # format_geojson = json.dumps(geojson, indent=4, ensure_ascii=True)
        # print(format_geojson)

        dirfile = f"D:/Python_Project/AS_P/AxSx/geojson/{opType}/"
        if not os.path.exists(dirfile):
            os.makedirs(dirfile)

        if not os.path.exists(f"{dirfile}/{start_point}-{end_point}.geojson"):
            with open(f"{dirfile}/{start_point}-{end_point}.geojson", "w") as f:
                json.dump(geojson, f, indent=4)
    print(end_list)


def pre_routes_all_geo(planeType: str):

    df = pd.read_excel(url, sheet_name=planeType)
    Routes = df["Route"].tolist()
    """All geojson"""
    featuresList = []
    for data in Routes:
        start_point = data[:3]
        end_point = data[-3:]
        # start_point = "AUH"
        # end_point = "IPC"
        start_lat = airportsDF[airportsDF["IATA Code"].str.strip() == start_point]["Lat"].values[0]
        start_lng = airportsDF[airportsDF["IATA Code"].str.strip() == start_point]["Lng"].values[0]

        end_lat = airportsDF[airportsDF["IATA Code"].str.strip() == end_point]["Lat"].values[0]
        end_lng = airportsDF[airportsDF["IATA Code"].str.strip() == end_point]["Lng"].values[0]
        print(f"{start_point}-{end_point}: ({start_lat}, {start_lng}), ({end_lat}, {end_lng})")

        # model: sphere
        geod = Geodesic(6371000, 0)
        line = geod.InverseLine(start_lat, start_lng, end_lat, end_lng)
        # print(f"{start_point}-{end_point}: {line.s13}")  # s13: distance in meters

        points1 = []
        points2 = []
        n = 100  # Number of points to generate

        if abs(start_lng - end_lng) > 180:
            # If the line crosses the 180-degree meridian, we need to split it into two lines
            print(f"{start_point}-{end_point}: 跨越 180 度經線")

            for i in range(n + 1):
                # point 各數值解說：起始經緯度(lat1, lon1), 終點經緯度(lat2, lon2), 大圓距離(s12), 起始方位角：azi1, 終點方位角：azi2, 起點到終點的大圓角距(a12)
                point = line.Position(i * line.s13 / n)

                if point["lon2"] > 0 and point["lon2"] < 180:

                    # If the longitude is between 0 and 180, add it to points1
                    points1.append((point["lon2"], point["lat2"]))

                elif point["lon2"] < 0 and point["lon2"] > -180:

                    # If the longitude is between -180 and 0, add it to points2
                    points2.append((point["lon2"], point["lat2"]))

                else:
                    points1.append((point["lon2"], point["lat2"]))

        else:
            print(f"{start_point}-{end_point}: 沒有跨越 180 度經線")

            for i in range(n + 1):
                point = line.Position(i * line.s13 / n)
                points1.append((point["lon2"], point["lat2"]))

        feature = {
            "type": "Feature",
            "geometry": {"type": "MultiLineString" if points2 else "LineString", "coordinates": [points1, points2] if points2 else points1},
            "properties": {"start": start_point, "end": end_point, "distance": round(line.s13 / 1000)},
        }

        featuresList.append(feature)

    geojson = {"type": "FeatureCollection", "features": featuresList}
    with open(os.path.join("D:\\", "Python_Project", "AS_P", "AxSx", "geojson", f"{planeType}.geojson"), "w") as f:
        json.dump(geojson, f, indent=4)


if __name__ == "__main__":
    # separate_routes("cargo")
    separate_routes("commercial")
    # pre_routes_all_geo("A380_14500")
    # pre_routes_all_geo("A380_29000")
