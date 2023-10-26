import tkinter as tk
import tkinter.messagebox as messagebox

contacts = []

# Fonction pour trouver le numéro en fonction de l'ID
def trouver_numero_par_id(contact_id):
    for contact in contacts:
        if contact["id"] == contact_id:
            return contact["numero"]
    return "Numéro introuvable"

# Fonction pour trouver le nom en fonction de l'ID
def trouver_nom_par_id(contact_id):
    for contact in contacts:
        if contact["id"] == contact_id:
            return contact["nom"]
    return "Nom introuvable"

# Fonction pour trouver le prénom en fonction de l'ID
def trouver_prenom_par_id(contact_id):
    for contact in contacts:
        if contact["id"] == contact_id:
            return contact["prenom"]
    return "Prénom introuvable"

# Fonction pour afficher le numéro de téléphone dans une boîte de message pop-up
def afficher_numero_telephone():
    selection = liste_contacts.curselection()
    if selection:
        index = selection[0]
        contact_id = liste_contacts.get(index).split(":")[0]  # Récupérer l'ID
        numero = trouver_numero_par_id(contact_id)
        nom = trouver_nom_par_id(contact_id)
        prenom = trouver_prenom_par_id(contact_id)
        messagebox.showinfo("Numéro de téléphone", f"Le numéro de téléphone de {nom} {prenom} : {numero}")

# Fonction pour valider le numéro de téléphone
def valider_numero(numero):
    return len(numero) == 10 and numero[0] == '0' and numero.isdigit()

# Fonction pour ajouter un contact à la liste
def ajouter_contact():
    nom = entry_nom.get()
    prenom = entry_prenom.get()
    numero = entry_numero.get()
    if not valider_numero(numero):
        messagebox.showerror("Erreur", "Le numéro de téléphone doit avoir 10 chiffres et commencer par 0.")
        return
    contact_id = len(contacts) + 1  # ID unique pour chaque contact
    contact = {"id": str(contact_id), "nom": nom, "prenom": prenom, "numero": numero}
    contacts.append(contact)
    liste_contacts.insert(tk.END, f"{contact['id']}:{contact['nom']} {contact['prenom']}")
    entry_nom.delete(0, tk.END)
    entry_prenom.delete(0, tk.END)
    entry_numero.delete(0, tk.END)
    enregistrer_contacts()

# Fonction pour supprimer un contact sélectionné
def supprimer_contact():
    selection = liste_contacts.curselection()
    if selection:
        index = selection[0]
        contact_id = liste_contacts.get(index).split(":")[0]  # Récupérer l'ID
        for contact in contacts:
            if contact["id"] == contact_id:
                contacts.remove(contact)
                break
        liste_contacts.delete(index)
        enregistrer_contacts()
        label_numero.config(text="Numéro :")

# Fonction pour enregistrer les contacts dans un fichier txt
def enregistrer_contacts():
    with open("contacts.txt", "w") as file:
        for contact in contacts:
            file.write(f"{contact['id']}:{contact['nom']} {contact['prenom']} ({contact['numero']})\n")

# Créer la fenêtre principale
root = tk.Tk()
root.title("Gestion de Contacts")
root.geometry("500x500")  # Ajustez la taille de la fenêtre

label_nom = tk.Label(root, text="Nom:")
label_nom.pack()
entry_nom = tk.Entry(root, width=30) 
entry_nom.pack()

label_prenom = tk.Label(root, text="Prénom:")
label_prenom.pack()
entry_prenom = tk.Entry(root, width=30) 
entry_prenom.pack()

label_numero = tk.Label(root, text="Numéro:")
label_numero.pack()

entry_numero = tk.Entry(root, width=30) 
entry_numero.pack()

bouton_ajouter = tk.Button(root, text="Ajouter", command=ajouter_contact, width=30, padx=10, pady=5)
bouton_ajouter.pack()

liste_contacts = tk.Listbox(root, width=30)
liste_contacts.pack()

bouton_supprimer = tk.Button(root, text="Supprimer", command=supprimer_contact, width=30, padx=10, pady=5)
bouton_supprimer.pack()

bouton_enregistrer = tk.Button(root, text="Enregistrer Contacts", command=enregistrer_contacts, width=30, padx=10, pady=5)
bouton_enregistrer.pack()

bouton_afficher_numero = tk.Button(root, text="Afficher le numéro de téléphone", command=afficher_numero_telephone, width=30, padx=10, pady=5)
bouton_afficher_numero.pack()

# Charger les contacts à partir du fichier s'ils existent
try:
    with open("contacts.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(":")
            if len(parts) == 2:
                contact_id, contact_info = parts
                contact_id = contact_id.strip()
                contact_info = contact_info.strip()
                nom_prenom, numero = contact_info.split("(")
                nom_prenom = nom_prenom.strip()
                numero = numero.strip(")")
                contacts.append({"id": contact_id, "nom": nom_prenom.split()[0], "prenom": nom_prenom.split()[1], "numero": numero})
                liste_contacts.insert(tk.END, f"{contact_id}:{nom_prenom}")

except FileNotFoundError:
    pass

# Lancer l'application
root.mainloop()
