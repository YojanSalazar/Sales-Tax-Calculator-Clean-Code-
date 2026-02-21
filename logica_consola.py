import app_logic



while True:
    opcion = input("MENU  \n\n"
    "Este es el listados de productos disponibles: \n\n"
    "1. Shampoo \n"
    "2. Dolex \n"
    "3. Barra de Chocolate \n"
    "4. Canasta de Huevos \n"
    "5. Whisky \n"
    "6. Cigarrillos \n"
    "7. Cerveza \n"
    "0. Salir \n\n")

    if opcion == "1":
        valor = float(input("Ingrese el precio del shampoo: "))
        tax = 19 / 100
        print (app_logic.calculate_iva(valor, tax))
    elif opcion == "2":
        valor = float(input("Ingrese el precio del Dolex: "))
        tax = 5/ 100
        print (app_logic.calculate_iva(valor, tax))
    elif opcion == "3":
        valor = float(input("Ingrese el precio de la barra de chocolate: "))
        tax = 5 / 100
        print (app_logic.calculate_iva(valor, tax))
    elif opcion == "4":
        valor = float(input("Ingrese el precio de la canasta de huevos: "))
        tax = 0
        print (app_logic.calculate_iva(valor, tax))
    elif opcion == "5":
        valor = float(input("Ingrese el precio del whisky: "))
        tax = 19 / 100
        grado = 40
        volumen = 750
        tarifa = 342
        calular_licor = app_logic.calculate_licores(valor, grado, tarifa, volumen)
        print (app_logic.calculate_iva(calular_licor, tax))
    elif opcion == "6":
        valor = float(input("Ingrese el precio de los cigarrillos: "))
        tax = 0.1
        numero_bolsas = int(input("Ingrese el número de bolsas: "))
        print (app_logic.Calculate_bolsa(valor, tax, numero_bolsas) + app_logic.calculte_impuesto_nacional_consumo(valor, tax))
    elif opcion == "7":
        valor = float(input("Ingrese el precio de la cerveza: "))
        tax = 19 / 100
        grado = 10
        volumen = 650   
        tarifa = 342     
        calular_licor = app_logic.calculate_licores(valor, grado, tarifa, volumen)
        numero_bolsas = int(input("Ingrese el número de bolsas: "))
        print (numero_bolsas + app_logic.calculate_iva(calular_licor, tax))
    elif opcion == "0":
        print("Gracias por usar el programa. ¡Hasta luego!")
        break
 