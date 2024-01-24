#n = 7 vaut le 7 diminué et n = 8 vaut le 7 majeur pour la gamme mineure
def nb_suiv(gamme = "Major", n = 1):
	if gamme == "Major":
		if n == 1:
			return rd.choice([2, 3, 4, 5, 6, 7])
		elif n == 2 or n == 4:
			return rd.choice([5, 7])
		elif n == 3:
			return 6
		elif n == 5:
			return 1
		elif n == 6:
			return rd.choice([2, 4])
		elif n == 7:
			return rd.choice([1, 3])
		else:
			print("erreur nb_suivi", gamme, n)
	elif gamme == "Minor":
		if n == 1:
			return rd.choice([2, 3, 4, 5, 6, 7])
		elif n == 2:
			return rd.choice([5, 7])
		elif n == 3:
			return 6
		elif n == 4:
			return rd.choice([5, 7, 8])
		elif n == 5 or n == 7:
			return 1
		elif n == 6:
			return rd.choice([2, 4])
		elif n == 8:
			return 3
		else:
			print("erreur nb_suivi", gamme, n)
	else:
			print("erreur nb_suivi", gamme, n)


def acc_suiv(g_root, g_qual, a_root, a_qual):
	g_n = lettre_nombre(g_root)
	a_n = lettre_nombre(a_root)


n = 1
print(n)
for i in range(1000):
	n = nb_suiv("Major", n)
	print(n)
