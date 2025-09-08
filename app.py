import streamlit as st
import smtplib
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ID de la feuille Google Sheets
SHEET_ID = "1wO1wsN1Jlof5yL4AOuRqnYQu3OAcX29WWwXPZ1UPxSI"

def sauvegarder_dans_sheets(donnees):
    """
    Sauvegarde les données du formulaire dans un Google Sheet
    """
    try:
        # Configuration pour l'accès à Google Sheets
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # Utiliser les credentials stockés dans Streamlit Secrets
        creds_dict = st.secrets["google_credentials"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        
        # Authentification et accès au Google Sheet
        client = gspread.authorize(creds)
        
        # Ouvrir la première feuille du document
        sheet = client.open_by_key(SHEET_ID).sheet1
        
        # Préparer les données à enregistrer
        row_data = [
            datetime.now().strftime("%d/%m/%Y"),  # Date
            donnees["etape"],                     # Étape
            donnees["telephone_client"],          # Téléphone client
            donnees["mail_client"],               # Mail client
            donnees["type_contact"],              # Type contact
            donnees["activite"],                  # Activité
            donnees["nom_client"],                # Nom complet du client
            donnees["ref_bien"],                  # Réf bien
            donnees["source"],                    # Source
            donnees["mail_receveur"],             # Adresse mail du receveur
            donnees["commentaire"]                # Commentaire
        ]
        
        # Ajouter une nouvelle ligne dans la feuille
        sheet.append_row(row_data)
        
        return True
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde dans Google Sheets : {e}")
        return False

def send_email(receiver_email, email_content):
    """
    Fonction pour envoyer un email avec gestion sécurisée des identifiants
    """
    try:
        # Configuration du serveur SMTP
        smtp_server = "smtp.gmail.com"
        port = 587
        sender_email = "contactpro.skdigital@gmail.com"
        password = "yzqy wmpw oulb qqvo"

        # Créer le message
        message = MIMEMultipart()
        message["From"] = f"Transmission Contact ONA <{sender_email}>"
        message["To"] = receiver_email
        message["Subject"] = "Nouveau Contact ONA Entreprises"
        message.attach(MIMEText(email_content, "plain"))

        # Établir la connexion SMTP et envoyer l'email
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        
        return True
    except smtplib.SMTPAuthenticationError:
        st.error("Erreur d'authentification. Vérifiez vos identifiants.")
        return False
    except Exception as e:
        st.error(f"Erreur lors de l'envoi de l'email : {e}")
        return False

def main():
    # Configuration de la page
    st.set_page_config(page_title="Transmission Contact ONA", page_icon=":telephone:")
    
    # Titre principal
    st.title("Transmission contact ONA Entreprises by Orpi PRO")
    st.subheader("Contacts entrants")
    
    # Date du jour automatique
    date_aujourd_hui = datetime.now().strftime("%d/%m/%Y")
    st.write(f"**Date :** {date_aujourd_hui}")
    
    # Formulaire de saisie
    with st.form(key='formulaire_contact'):
        # Étape avec valeur par défaut
        etape = st.selectbox("Étape", 
                             options=["Appel à faire", "Appel en cours", "Appel terminé"],
                             index=0)
        
        # Téléphone client (obligatoire)
        telephone_client = st.text_input("Téléphone client *", placeholder="Numéro de téléphone")
        
        # Mail client (optionnel)
        mail_client = st.text_input("Mail client", placeholder="Email du client (optionnel)")
        
        # Type de contact
        type_contact = st.selectbox("Type contact", 
                                    options=["Demandeur", "Vendeur/Bailleur", "Estimation"])
        
        # Activité (optionnel)
        activite = st.text_input("Activité", placeholder="Activité (optionnel)")
        
        # Nom complet du client (obligatoire)
        nom_client = st.text_input("Nom complet du client *", placeholder="Nom et prénom")
        
        # Référence bien (optionnel)
        ref_bien = st.text_input("Réf bien", placeholder="Référence du bien (optionnel)")
        
        # Source
        source = st.text_input("Source", placeholder="Origine du contact")
        
        # Adresse mail du receveur (obligatoire)
        mail_receveur = st.text_input("Adresse mail du receveur *", placeholder="Email du commercial")
        
        # Commentaire
        commentaire = st.text_area("Commentaire", placeholder="Détails supplémentaires")
        
        # Bouton de validation
        submitted = st.form_submit_button("Je valide")
        
        # Validation du formulaire
        if submitted:
            # Vérification des champs obligatoires
            if not telephone_client or not nom_client or not mail_receveur:
                st.error("Merci de remplir tous les champs obligatoires (*)")
            else:
                # Préparer un dictionnaire avec les données
                donnees = {
                    "etape": etape,
                    "telephone_client": telephone_client,
                    "mail_client": mail_client,
                    "type_contact": type_contact,
                    "activite": activite,
                    "nom_client": nom_client,
                    "ref_bien": ref_bien,
                    "source": source,
                    "mail_receveur": mail_receveur,
                    "commentaire": commentaire
                }
                
                # Préparer le contenu de l'email
                email_content = f"""Bonjour, 

Nouveau contact {type_contact}, sa demande a été faite le {date_aujourd_hui}.

Voici ses coordonnées : 

{nom_client}
{mail_client}
{telephone_client}

Ce contact provient de {source}. 
Référence : {ref_bien}

Commentaire de Léna : {commentaire}

Bon appel de vente,
"""
                # Sauvegarder dans Google Sheets
                if sauvegarder_dans_sheets(donnees):
                    # Envoi de l'email
                    if send_email(mail_receveur, email_content):
                        st.success("Validé")
                    else:
                        st.error("Problème lors de l'envoi de l'email")
                else:
                    st.error("Problème lors de la sauvegarde des données")

if __name__ == "__main__":
    main()
