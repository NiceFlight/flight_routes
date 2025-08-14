import pandas as pd
from geographiclib.geodesic import Geodesic
import time


startTime = time.time()
url = r"D:/NiceFlight/Airline_Manager/flight_plan.xlsx"

df = pd.read_excel(url, header=0, sheet_name="airport")
# print(airports)

selectAirports = []
for airport in df.iloc:
    if int(airport["Max Runway(ft)"]) >= 9680:
        selectAirports.append(airport.tolist())

print(len(selectAirports))

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
_startAirport = ""
_endAirport = ""
dis = 0
output_list = []


"""Most far of two airports"""
# for i_index, i in enumerate(selectAirports):
#     for j_index, j in enumerate(selectAirports):
#         if j_index <= i_index:
#             continue
#         startAirport = i[1].strip()
#         startIATA = i[5].strip()
#         start_lat = float(i[7])
#         start_lng = float(i[8])

#         endAirport = j[1].strip()
#         endIATA = j[5].strip()
#         end_lat = float(j[7])
#         end_lng = float(j[8])
#         # print(startAirport, (start_lat, start_lng))

#         geod = Geodesic.SPHERE  # type: ignore
#         line = geod.InverseLine(start_lat, start_lng, end_lat, end_lng)
#         distance = line.s13 / 1000  # Convert to kilometers
#         print(f"{startAirport}-{endAirport} - Distance: {distance:.4f} km")

#         output_list.append(
#             f"{startIATA}, {endIATA},{distance:.4f},{startAirport},{endAirport}\n"
#         )

#         if distance > dis:
#             dis = distance
#             _startAirport = startAirport
#             _endAirport = endAirport

# # with open("The_distance_of_two_airports_for_A380.csv", "w", encoding="utf-8") as f:
# #     f.writelines(output_list)

# endTime = time.time()

# print(
#     f"The most far disance between two airports are {_startAirport}-{_endAirport}, the distance is {dis:.4f} km, it costs {(endTime - startTime):.2f} seconds calculating"
# )


"""Find my hub's to every airports distance"""
# seen_pairs = set()
# for i in hubList:
#     for j_index, j in enumerate(selectAirports):
#         if i[0].strip() == j[5].strip():
#             continue
#         pair = tuple(sorted((i[0].strip(), j[5].strip())))
#         if pair in seen_pairs:
#             continue
#         seen_pairs.add(pair)
#         # print(seen_pairs)

#         startIATA = i[0].strip()
#         start_lat = float(i[1])
#         start_lng = float(i[2])

#         endIATA = j[5].strip()
#         end_lat = float(j[7])
#         end_lng = float(j[8])
#         # print(startAirport, (start_lat, start_lng))

#         geod = Geodesic(6371000, 0)  # type: ignore
#         line = geod.InverseLine(start_lat, start_lng, end_lat, end_lng)
#         distance = line.s13 / 1000  # Convert to kilometers
#         print(f"{startIATA}-{endIATA} - Distance: {distance:.0f} km")

#         output_list.append(f"{startIATA},{endIATA},{distance:.0f}\n")

# # with open(
# #     "The_distance_of_hubs_to_every_airports_for_A380.csv", "w", encoding="utf-8"
# # ) as f:
# #     f.writelines(output_list)
