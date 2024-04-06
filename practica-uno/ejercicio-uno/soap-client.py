from zeep import Client

client = Client('http://localhost:8000')


result = client.service.Suma(a=10, b=2)
print(result)
result = client.service.Resta(a=10, b=2)
print(result)
result = client.service.Producto(a=10, b=2)
print(result)
result = client.service.Division(a=10, b=2)
print(result)