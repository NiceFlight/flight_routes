from geographiclib.geodesic import Geodesic
import json
import os


def cal_dis_from_tpe(desPoint: list):
    with open("airportsData.json", "r", encoding="utf-8") as f:
        ar_data = json.load(f)

    for i in desPoint:
        for j in ar_data:
            if i == j["IATA Code"]:
                start = "TPE"
                startLat = 25.0777
                startLng = 121.233002
                des = i
                desLat = float(j["Lat"])
                desLng = float(j["Lng"])

                # model: WGS84
                geod = Geodesic.WGS84
                line = geod.InverseLine(startLat, startLng, desLat, desLng)
                distance = line.s13 / 1000  # Convert to kilometers

                points1 = []
                points2 = []
                n = 1000  # Number of points to generate

                if abs(startLng - desLng) > 180:
                    print(f"{start}-{des}: 跨越 180 度經線")

                    for i in range(n + 1):
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
                    print(f"{start}-{des}: 沒有跨越 180 度經線")

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
                            "properties": {"Start": start, "Des": des, "Distance": f"{distance:.6f}"},
                        }
                    ],
                }

                dirfile = f"TPE/{start}-{des}.geojson"

                if not os.path.exists(dirfile):
                    with open(dirfile, "w") as f:
                        json.dump(geojson, f, indent=4)


if __name__ == "__main__":
    cal_dis_from_tpe(["JFK", "LHR"])
