import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_email(receiver_email, email_content):
    """
    Fonction pour envoyer un email (à personnaliser avec vos propres paramètres SMTP)
    """
    try:
        # Configuration du serveur SMTP (à remplacer avec vos propres paramètres)
        smtp_server = "smtp.gmail.com"
        port = 587
        sender_email = "votre_email@gmail.com"
        password = "votre_mot_de_passe_app"

        # Créer le message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "Nouveau Contact ONA Entreprises"
        message.attach(MIMEText(email_content, "plain"))

        # Établir la connexion SMTP et envoyer l'email
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        
        return True
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
                # Préparer le contenu de l'email
                email_content = f"""Bonjour jeune frérot, 

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
                # Envoi de l'email
                if send_email(mail_receveur, email_content):
                    st.success("C'est bien Léna, tu es bien dressée 👍")
                    # Vous pouvez ajouter ici une logique supplémentaire si nécessaire
                else:
                    st.error("Problème lors de l'envoi de l'email")

if __name__ == "__main__":
    main()

# Note importante : 
# 1. Remplacez 'votre_email@gmail.com' et 'votre_mot_de_passe_app' 
#    par vos propres identifiants SMTP
# 2. Pour un mot de passe d'application, utilisez les paramètres 
#    de sécurité de votre compte Gmail
# 3. Installez les dépendances : streamlit
