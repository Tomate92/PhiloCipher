import unicodedata
import itertools


def supprimer_accents(texte):
    texte_normalise = unicodedata.normalize('NFD', texte)
    texte_sans_accents = ''.join(char for char in texte_normalise if unicodedata.category(char) != 'Mn')
    return texte_sans_accents


class Cipher:
    def __init__(self):
        self.lettres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.nombres = []
        self.clair = []
        self.tuples = []
        self.clef = ""
        self.code = ""
        self.texte = ""

    def trouver_place_lettres(self, lettre):
        try:
            # S'assurer que la lettre est un nombre valide entre 1 et 26
            index = int(lettre) - 1
            if index < 0 or index >= len(self.lettres):
                raise ValueError(f'Index {index + 1} hors de portée.')
            return self.lettres[index]
        except ValueError as e:
            # print(f'Erreur dans \'trouver_place_lettres\': {e}')
            return '?'

    def encoder(self):
        a = supprimer_accents(input("Texte à coder: "))

        for char in a:
            char = char.upper()
            self.nombres.append(format(self.lettres.find(char)+1, '02'))

        while '00' in self.nombres:
            self.nombres.remove('00')

        i = 1
        while len(self.tuples) < len(self.nombres):
            j = str(self.nombres[i-1])
            self.tuples.append((j[0], j[-1]))
            i += 1

        self.clef += ''.join(self.tuples[i][0] for i in range(len(self.tuples)))
        self.code += ''.join(self.tuples[i][-1] for i in range(len(self.tuples)))

        print("Votre phrase codée: " + self.code + "\nAvec comme mot-clef: " + self.clef)

        return self.clef, self.code

    def decoder(self):
        a = input("Texte à décoder: ")
        b = input("Mot-clef: ")

        a = list(a)
        b = list(b)

        self.tuples.extend(zip(b, a))
        self.clair = [''.join([i[0], i[1]]) for i in self.tuples]
        self.clair = [''.join(self.trouver_place_lettres(i)) for i in self.clair]
        self.texte = ''.join(i for i in self.clair)

        print("Votre phrase décodée: " + self.texte)

    def bruteforce(self):
        print("Tentative de brute force...")
        texte_a_decoder = input("Texte codé à cracker: ")
        while texte_a_decoder == '' or texte_a_decoder.isspace():
            print("Ca ne peut pas être vide.")
            texte_a_decoder = input("Texte codé à cracker: ")
        self.mot_ou_phrase_a_retrouver = input("Mot ou phrase à retrouver dans le texte (laisser vide si rien): ")

        longueur_clef = len(texte_a_decoder)
        possibilites = ['0', '1', '2']

        for combinaison in itertools.product(possibilites, repeat=longueur_clef):
            clef_possible = ''.join(combinaison)
            print(f"Tentative de clé: {clef_possible}")
            self.decoder_bruteforce(texte_a_decoder, clef_possible)

    def decoder_bruteforce(self, a, b):
        self.tuples.clear()
        a = list(a)
        b = list(b)

        self.tuples.extend(zip(b, a))
        self.clair = [''.join([i[0], i[1]]) for i in self.tuples]
        self.clair = [''.join(self.trouver_place_lettres(i)) for i in self.clair]
        self.texte = ''.join(i for i in self.clair)


        print(f"Décodé avec la clé '{''.join(b)}' : {self.texte}")


        if self.texte == self.mot_ou_phrase_a_retrouver.upper():
            print(f"\nClé trouvée: {''.join(b)}")
            print(f"Texte décodé: {self.texte}")
            exit()


print("PhiloCipher")
print("1. Encoder")
print("2. Décoder")
print("3. BruteForce")

a = int(input(""))
while a < 1 or a > 3:
    a = int(input("Veuillez entrer un nombre entre 1 et 3 :"))

if a == 1:
    Cipher().encoder()
elif a == 2:
    Cipher().decoder()
else:
    Cipher().bruteforce()

# 254051805102535445
# 011112121221011100
# 3**18