nombres = ["Eduardo Herdocia","Andrea Zavala", "Gabriel Pocurrull", "Jhocabed Barrera",
           "Gabriel Jimenez", "Stephany Herrera", "Steven Hernandez", "Hilly Oporta", "William Martinez"
           , "Luz Galarza", "Laura Rodriguez", "Juan Marenco", "Cynthia West", "Jharet Herrera", "Viktor Miranda",
           "Manuel Hernandez", "Cristiana Espinoza", "Sharon Cadenas", "Sharon Calvo", "Lester Pereira"
           , "Fernando Torrez", "Rodrigo Rodriguez", "Andrea Nuñez", "Maria Escorcia", "Kenneth Lopez", "Josue Lopez",
           "Yamil Moreno", "Guadalupe Torrez", "Lucia Acosta", "Meriyen Palacios", "Mariam Urbina", "Jose Jose",
           "Clifford Lacayo", "Eduardo Quant", "Anna Reyes", "Osvaldo Rodriguez", "Elieta Parajon", ""]
correos = []
values = []
id = 1
for name in nombres:
    separado = name.split()
    correo = f"{separado[0].lower()}.{separado[1].lower()}@student.edu"
    correos.append(correo)


nombres_sorted = sorted(nombres)
for name in nombres_sorted:
    value = (f"(student_id, image_name, student_picture) "
             f"values ({id}, 'Normal', LOAD_FILE('D:/Clases KU/fall 24/foto alumnos/{name}.jfif')),")
    print(value)
    id += 1

print(len(correos))





