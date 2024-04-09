from graspy.tor import struct
from graspy.tor import CoordinateSystem, reference

struct1 = struct(x=0, y=0, z=0, unit="m")
print(struct1)

assert str(struct1) == "struct(x: 0 m, y: 0 m, z: 0 m)"
struct2 = struct(x=0, y=0, z=0)
print(struct2)
assert str(struct2) == "struct(x: 0, y: 0, z: 0)"


cs = CoordinateSystem(
    origin=struct1,
    x_axis=struct2,
    reference=reference("reference"),
    name="test",
)

print(cs)

example_cs = """test  coor_sys  
(
  origin           : struct(x: 0 m, y: 0 m, z: 0 m),
  x_axis           : struct(x: 0, y: 0, z: 0),
  base             : ref(reference)
)"""

print(example_cs)
assert str(cs) == example_cs
