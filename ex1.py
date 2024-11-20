def calcul_amende_et_retrait(taux_alcoolemie):
    amende = 0
    retrait_permis = 0

    if 0.5 <= taux_alcoolemie <= 0.8:
        amende = 200 * (taux_alcoolemie - 0.5) + 135
        retrait_permis = 6
    elif 0.8 < taux_alcoolemie <= 1.0:
        amende = 300 * (taux_alcoolemie - 0.5) + 135
        retrait_permis = 24
    elif taux_alcoolemie > 1.0:
        amende = 5000
        retrait_permis = "Permis à repasser"
    else:
        return "Aucune infraction détectée"

    return amende, retrait_permis


taux_alcoolemie = float(input("Entrez le taux d'alcoolémie en g/L : "))

resultat = calcul_amende_et_retrait(taux_alcoolemie)

if isinstance(resultat, tuple):
    amende, retrait_permis = resultat
    print(f"Amende à payer : {amende} euros")
    if retrait_permis == "Permis à repasser":
        print("Vous devez repasser le permis.")
    else:
        print(f"Durée de retrait de permis : {retrait_permis} mois")
else:
    print(resultat)
