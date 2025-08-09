import os
from flask import Flask, request
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# --- Données des plateformes ---
plateformes = {
    "BoursoBank": {
        "lien": "https://www.boursobank.com/affiliation",
        "tuto": [
            "1️⃣ Rendez-vous sur le lien ci-dessus.",
            "2️⃣ Créez un compte.",
            "3️⃣ Copiez votre lien partenaire."
        ]
    },
    "Revolut": {
        "lien": "https://www.revolut.com/referral",
        "tuto": [
            "1️⃣ Ouvrez le lien.",
            "2️⃣ Créez un compte Revolut.",
            "3️⃣ Activez votre carte pour valider."
        ]
    },
    "HelloBank": {
        "lien": "https://www.hellobank.fr/affiliation",
        "tuto": [
            "1️⃣ Cliquez sur le lien.",
            "2️⃣ Remplissez vos infos.",
            "3️⃣ Recevez votre prime."
        ]
    },
    "BankIn": {
        "lien": "https://www.bankin.com/affiliation",
        "tuto": [
            "1️⃣ Inscrivez-vous via le lien.",
            "2️⃣ Connectez vos comptes.",
            "3️⃣ Profitez de vos avantages."
        ]
    },
    "PayPal": {
        "lien": "https://www.paypal.com/referral",
        "tuto": [
            "1️⃣ Connectez-vous à PayPal.",
            "2️⃣ Invitez un ami via le lien.",
            "3️⃣ Recevez votre prime."
        ]
    },
    "Crédit Agricole": {
        "lien": "https://www.credit-agricole.fr/affiliation",
        "tuto": [
            "1️⃣ Ouvrez le lien.",
            "2️⃣ Choisissez votre agence.",
            "3️⃣ Remplissez le formulaire."
        ]
    },
    "Crédit Lyonnais": {
        "lien": "https://www.lcl.fr/affiliation",
        "tuto": [
            "1️⃣ Accédez au lien.",
            "2️⃣ Créez un compte.",
            "3️⃣ Recevez votre prime."
        ]
    },
    "Société Générale": {
        "lien": "https://particuliers.societegenerale.fr/affiliation",
        "tuto": [
            "1️⃣ Cliquez sur le lien.",
            "2️⃣ Ouvrez un compte.",
            "3️⃣ Recevez vos avantages."
        ]
    },
    "BforBank": {
        "lien": "https://www.bforbank.com/affiliation",
        "tuto": [
            "1️⃣ Suivez le lien.",
            "2️⃣ Remplissez vos infos.",
            "3️⃣ Validez pour la prime."
        ]
    },
    "N26": {
        "lien": "https://n26.com/referral",
        "tuto": [
            "1️⃣ Ouvrez un compte via le lien.",
            "2️⃣ Commandez votre carte.",
            "3️⃣ Utilisez-la pour activer la prime."
        ]
    },
    "Fortuneo": {
        "lien": "https://www.fortuneo.fr/affiliation",
        "tuto": [
            "1️⃣ Cliquez sur le lien.",
            "2️⃣ Créez un compte.",
            "3️⃣ Profitez de vos avantages."
        ]
    },
    "CoinBase": {
        "lien": "https://www.coinbase.com/join",
        "tuto": [
            "1️⃣ Ouvrez le lien.",
            "2️⃣ Créez un compte.",
            "3️⃣ Achetez pour activer la prime."
        ]
    },
    "Kraken": {
        "lien": "https://kraken.com/referral",
        "tuto": [
            "1️⃣ Cliquez sur le lien.",
            "2️⃣ Créez un compte.",
            "3️⃣ Commencez à trader."
        ]
    },
    "Deblock": {
        "lien": "https://www.deblock.com/affiliation",
        "tuto": [
            "1️⃣ Inscrivez-vous via le lien.",
            "2️⃣ Vérifiez votre identité.",
            "3️⃣ Recevez la prime."
        ]
    },
    "Robinhood": {
        "lien": "https://robinhood.com/referral",
        "tuto": [
            "1️⃣ Ouvrez un compte via le lien.",
            "2️⃣ Déposez des fonds.",
            "3️⃣ Recevez une action gratuite."
        ]
    }
}

# --- Flask app pour Render ---
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot Telegram Affiliation est actif 🚀"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put_nowait(update)
    return "OK"

# --- Fonctions du bot ---
async def start(update, context):
    keyboard = []
    row = []
    for i, name in enumerate(plateformes.keys(), start=1):
        row.append(InlineKeyboardButton(name, callback_data=name))
        if i % 2 == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("💳 Choisissez la plateforme :", reply_markup=reply_markup)

async def button(update, context):
    query = update.callback_query
    await query.answer()
    plateforme = plateformes[query.data]
    message = f"**{query.data}**\n\n🔗 Lien : {plateforme['lien']}\n\n📋 Tutoriel :\n"
    message += "\n".join(plateforme["tuto"])
    await query.edit_message_text(text=message, parse_mode="Markdown")

# --- Lancer l'application ---
if __name__ == "__main__":
    TOKEN = os.environ.get("
          8274151273:AAGLzb8UVZn7Jqd-49P8CG3CxSMFvlhGcTI
        ")
    PUBLIC_URL = os.environ.get("PUBLIC_URL")

    application = Application.builder().token(TOKEN).build()
    bot = application.bot

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    if PUBLIC_URL:
        bot.set_webhook(f"{PUBLIC_URL}/webhook")

    application.run_polling()
