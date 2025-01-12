import csv

# Charger les transactions depuis un fichier CSV
def load_transactions(file_path):
    """
    Charge les transactions à partir d'un fichier CSV.
    :param file_path: Chemin vers le fichier CSV.
    :return: Liste des transactions (chaque transaction est une liste d'items).
    """
    transactions = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Sauter l'en-tête
        for row in reader:
            # Considérer tous les items (à partir de la 2e colonne) comme une transaction
            items = row[1:]  # Les items commencent à partir de la 2e colonne
            transactions.append(items)
    return transactions

# Calculer le support d'un itemset
def calculate_support(transactions, itemset):
    """
    Calcule le support d'un itemset dans les transactions.
    :param transactions: Liste des transactions.
    :param itemset: Ensemble d'items à vérifier.
    :return: Nombre de transactions contenant l'itemset.
    """
    count = 0
    for transaction in transactions:
        if set(itemset).issubset(set(transaction)):
            count += 1
    return count

# Générer des candidats de taille k
def generate_candidates(frequent_itemsets, k):
    """
    Génère des candidats de taille k à partir des itemsets fréquents de taille k-1.
    :param frequent_itemsets: Liste des itemsets fréquents de taille k-1.
    :param k: Taille des candidats à générer.
    :return: Liste des candidats de taille k.
    """
    candidates = []
    for i in range(len(frequent_itemsets)):
        for j in range(i + 1, len(frequent_itemsets)):
            candidate = list(set(frequent_itemsets[i]) | set(frequent_itemsets[j]))
            if len(candidate) == k:
                candidate.sort()
                if candidate not in candidates:
                    candidates.append(candidate)
    return candidates

# Algorithme Apriori
def apriori(transactions, minsup):
    """
    Implémente l'algorithme Apriori pour trouver les itemsets fréquents.
    :param transactions: Liste des transactions.
    :param minsup: Seuil minimal de support.
    :return: Dictionnaire des itemsets fréquents par taille.
    """
    # Trouver les itemsets fréquents de taille 1
    unique_items = set(item for transaction in transactions for item in transaction)
    L1 = []
    for item in unique_items:
        support = calculate_support(transactions, [item])
        if support >= minsup:
            L1.append([item])
    frequent_itemsets = L1
    all_frequent_itemsets = {1: frequent_itemsets}

    # Générer les itemsets fréquents pour k >= 2
    k = 2
    while frequent_itemsets:
        candidates = generate_candidates(frequent_itemsets, k)
        frequent_itemsets = []
        for candidate in candidates:
            support = calculate_support(transactions, candidate)
            if support >= minsup:
                frequent_itemsets.append(candidate)
        if frequent_itemsets:
            all_frequent_itemsets[k] = frequent_itemsets
        k += 1

    return all_frequent_itemsets

# Fonction principale
if __name__ == "__main__":
    # Chemin vers le fichier CSV
    file_path = 'transactions.csv'  # Assurez-vous que ce fichier existe dans le même dossier ou spécifiez un chemin complet.

    # Charger les transactions
    try:
        transactions = load_transactions(file_path)
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{file_path}' est introuvable. Assurez-vous qu'il existe.")
        exit()

    # Exécuter l'algorithme Apriori
    minsup = 2  # Seuil minimal de support
    frequent_itemsets = apriori(transactions, minsup)

    # Afficher les résultats
    print("\nItemsets fréquents trouvés :")
    for k, itemsets in frequent_itemsets.items():
        print(f"Taille {k}: {itemsets}")