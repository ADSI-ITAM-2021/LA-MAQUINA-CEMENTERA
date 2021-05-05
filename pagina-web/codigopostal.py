import pgeocode

nomi = pgeocode.Nominatim('mx')
df = nomi.query_postal_code("52784")
print(df.latitude)
print(df.longitude)