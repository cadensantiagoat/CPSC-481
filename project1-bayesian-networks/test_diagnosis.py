from diagnostics import Diagnostics

d = Diagnostics()

tests = [
    ("No", "Yes", "Abnormal", "Absent"),
    ("Yes", "No", "Normal", "Absent"),
    ("NA", "Yes", "Abnormal", "Present"),
    ("NA", "NA", "NA", "NA"),
]

for t in tests:
    print(t, "->", d.diagnose(*t))