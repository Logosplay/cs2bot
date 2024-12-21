lowFloats = {
    #Fracture
    ("Galil AR | Connexion"): lambda x: 0.15 < x < 0.20,
    ("MP5-SD | Kitbash"): lambda x: 0.15 < x < 0.20,
    ("Tec-9 | Brother"): lambda x: 0.15 < x < 0.20,
    ("MAG-7 | Monster Call"): lambda x: 0.15 < x < 0.20,
    ("MAC-10 | Allure"): lambda x: 0.15 < x < 0.20,

    #Kilowatt
    ("Sawed-Off | Analog Input"): lambda x: 0.07 < x < 0.10,
    ("M4A4 | Etch Lord"): lambda x: 0.07 < x < 0.10,
    ("MP7 | Just Smile"): lambda x: 0.07 < x < 0.10,
    ("Five-SeveN | Hybrid"): lambda x: 0.07 < x < 0.10,

    #Revolution
    ("P2000 | Wicked Sick"): lambda x: 0.15 < x < 0.1875,
    ("UMP-45 | Wild Child"): lambda x: 0.15 < x < 0.1875,

    #Prisma
    ("XM1014 | Incinegator"): lambda x: 0.15 < x < 0.1875,

    #Glove
    ("G3SG1 | Stinger"): lambda x: 0.07 < x < 0.0933,
    ("Nova | Gila"): lambda x: 0.07 < x < 0.0933,
}

def main():
    name = "Nova | Gila"
    float = 0.08

    if lowFloats[name](float):
        print("SIM!")
    else: print("gozo")

main()

    

