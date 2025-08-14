from geographiclib.geodesic import Geodesic


"""WGS84"""
geod = Geodesic.WGS84  # type: ignore
line = geod.InverseLine(-16.34110069270000, -71.5830993652000000, 16.04389953613280, 108.1989974975580000)
distance = line.s13 / 1000  # Convert to kilometers
print(f"WGS84 Distance: {distance:.4f} km")

"""GRS80"""
geod = Geodesic(6378137, 1 / 298.257222101)  # type: ignore
# geod = Geodesic.GRS80  # type: ignore
line = geod.InverseLine(-16.34110069270000, -71.5830993652000000, 16.04389953613280, 108.1989974975580000)
distance = line.s13 / 1000  # Convert to kilometers
print(f"GRS80 Distance: {distance:.4f} km")

"""England Airy 1830"""
geod = Geodesic(6377563.396, 1 / 299.3249646)  # type: ignore
line = geod.InverseLine(-16.34110069270000, -71.5830993652000000, 16.04389953613280, 108.1989974975580000)
distance = line.s13 / 1000  # Convert to kilometers
print(f"England Airy 1830 Distance: {distance:.4f} km")

"""International 1924"""
geod = Geodesic(6378388, 1 / 297.0)  # type: ignore
line = geod.InverseLine(-16.34110069270000, -71.5830993652000000, 16.04389953613280, 108.1989974975580000)
distance = line.s13 / 1000  # Convert to kilometers
print(f"International 1924 Distance: {distance:.4f} km")

"""America Clarke 1866"""
geod = Geodesic(6378206.4, 1 / 294.9786982)  # type: ignore
line = geod.InverseLine(-16.34110069270000, -71.5830993652000000, 16.04389953613280, 108.1989974975580000)
distance = line.s13 / 1000  # Convert to kilometers
print(f"America Clarke 1866 Distance: {distance:.4f} km")

"""sphere"""
geod = Geodesic(6371000, 0)  # type: ignore
line = geod.InverseLine(-16.34110069270000, -71.5830993652000000, 16.04389953613280, 108.1989974975580000)
distance = line.s13 / 1000  # Convert to kilometers
print(f"sphere Distance: {distance:.4f} km")

"""sphere"""
geod = Geodesic.SPHERE  # type: ignore  sphere
line = geod.InverseLine(-16.34110069270000, -71.5830993652000000, 16.04389953613280, 108.1989974975580000)
distance = line.s13 / 1000  # Convert to kilometers
print(f"sphere Distance: {distance:.4f} km")
