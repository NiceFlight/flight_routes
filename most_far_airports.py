import json
import pandas as pd
from geographiclib.geodesic import Geodesic


"""Most far of two airports for A380"""


def MFOTAs(runway: int):
    url = r"D:/NiceFlight/Airline_Manager/flight_plan.xlsx"
    df = pd.read_excel(url, header=0, sheet_name="airportsData")
    # print(airports)

    selectAirports = []
    for airport in df.iloc:
        if int(airport["Max Runway(ft)"]) >= runway:
            selectAirports.append(airport.tolist())
    # print(len(selectAirports))

    _startAirport = ""
    _endAirport = ""
    dis = 0
    output_list = []

    for i_index, i in enumerate(selectAirports):
        for j_index, j in enumerate(selectAirports):
            if j_index <= i_index:
                continue
            startAirport = i[1].strip()
            startIATA = i[5].strip()
            start_lat = float(i[7])
            start_lng = float(i[8])

            endAirport = j[1].strip()
            endIATA = j[5].strip()
            end_lat = float(j[7])
            end_lng = float(j[8])
            # print(startAirport, (start_lat, start_lng))

            geod = Geodesic(6371000, 0)
            line = geod.InverseLine(start_lat, start_lng, end_lat, end_lng)
            distance = line.s13 / 1000  # Convert to kilometers
            print(f"{startAirport}-{endAirport} - Distance: {distance:.4f} km")

            output_list.append(f"{startIATA}, {endIATA},{distance:.4f},{startAirport},{endAirport}\n")

            if distance > dis:
                dis = distance
                _startAirport = startAirport
                _endAirport = endAirport

    with open("The_distance_of_two_airports_for_A380.csv", "w", encoding="utf-8") as f:
        f.writelines(output_list)

    print(f"The most far disance between two airports are {_startAirport}-{_endAirport}, the distance is {dis:.4f} km.")


"""Find my hub's to every airports distance for runway"""


def FMHTEAD(runway: int):

    hubList = [
        ["TPE", 25.07770000000000, 121.2330020000000000],
        ["SIN", 1.35019000000000, 103.9940030000000000],
        ["PER", -31.94029998779290, 115.9670028686520000],
        ["ORD", 41.97860000000000, -87.9048000000000000],
        ["CHC", -43.48939895629880, 172.5319976806640000],
        ["KEF", 63.98500061035200, -22.6056003570560000],
        ["JNB", -26.13920000000000, 28.2460000000000000],
        ["HNL", 21.32062000000000, -157.9242280000000000],
        ["VIE", 48.11029815673800, 16.5697002410890000],
        ["AUH", 24.43300056457510, 54.6511001586914000],
        ["SCL", -33.39300155639640, -70.7857971191406000],
        ["AAP", -16.34110069270000, -71.5830993652000000],
    ]

    url = r"D:/NiceFlight/Airline_Manager/flight_plan.xlsx"
    df = pd.read_excel(url, header=0, sheet_name="airportsData")
    # print(airports)

    selectAirports = []
    for airport in df.iloc:
        if int(airport["Max Runway(ft)"]) >= runway:
            selectAirports.append(airport.tolist())
    # print(len(selectAirports))

    seen_pairs = set()
    output_list = []

    for i in hubList:
        for j_index, j in enumerate(selectAirports):
            if i[0].strip() == j[5].strip():
                continue
            pair = tuple(sorted((i[0].strip(), j[5].strip())))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            # print(seen_pairs)

            startIATA = i[0].strip()
            start_lat = float(i[1])
            start_lng = float(i[2])

            endIATA = j[5].strip()
            end_lat = float(j[7])
            end_lng = float(j[8])
            # print(startAirport, (start_lat, start_lng))

            geod = Geodesic(6371000, 0)
            line = geod.InverseLine(start_lat, start_lng, end_lat, end_lng)
            distance = line.s13 / 1000  # Convert to kilometers
            print(f"{startIATA}-{endIATA} - Distance: {distance:.0f} km")

            output_list.append(f"{startIATA},{endIATA},{distance:.0f}\n")

    with open("The_distance_of_hubs_to_every_airports_for_A380.csv", "w", encoding="utf-8") as f:
        f.writelines(output_list)


"""The most far of two airports"""


def TMFOTA():
    with open("airportsData.json", "r", encoding="utf-8") as f:
        ar_data = json.load(f)
    # print(ar_data)

    startPoint = ""
    desPoint = ""
    dis = 0
    seen_pairs = set()

    _startPoint = ""
    _desPoint = ""

    for i in ar_data:
        for j in ar_data:
            startPoint = i["IATA Code"]
            startLat = float(i["Lat"])
            startLng = float(i["Lng"])
            desPoint = j["IATA Code"]
            desLat = float(j["Lat"])
            desLng = float(j["Lng"])

            pair = tuple(sorted((startPoint.strip(), desPoint.strip())))

            if startPoint == desPoint or pair in seen_pairs:
                continue
            seen_pairs.add(pair)

            geod = Geodesic.WGS84
            line = geod.InverseLine(startLat, startLng, desLat, desLng)
            distance = line.s13 / 1000  # Convert to kilometers

            if distance > dis:
                dis = distance
                _startPoint = startPoint
                _desPoint = desPoint
                _startAirport = i["Name"]
                _desAirport = j["Name"]
                print(f"{_startPoint}-{_desPoint} - {dis:.4f} km.")

    print(f"The Most far of two airports are {_startAirport}({_startPoint}) and {_desAirport}({_desPoint}), the distance is {dis:.4f} km")


if __name__ == "__main__":
    MFOTAs(0)
    FMHTEAD(9680)
    TMFOTA()
