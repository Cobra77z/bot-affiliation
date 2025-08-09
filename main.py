import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# Variables d'environnement
BOT_TOKEN = os.getenv("8274151273:AAGLzb8UVZn7Jqd-49P8CG3CxSMFvlhGcTI")
PUBLIC_URL = os.getenv("https://bot-affiliation.onrender.com")

if not BOT_TOKEN or not PUBLIC_URL:
    raise ValueError("⚠️ BOT_TOKEN et PUBLIC_URL doivent être définis dans Render Environment Variables")

# Flask app
app = Flask(__name__)

# Plateformes et tutoriels détaillés
platforms = {
    "BoursoBank": (
        "https://bourso.com/affiliation",
        "📋 **Tuto BoursoBank :**\n"
        "1️⃣ Clique sur le lien ci-dessus.\n"
        "2️⃣ Remplis le formulaire d'ouverture de compte.\n"
        "3️⃣ Fournis tes justificatifs d'identité et de domicile.\n"
        "4️⃣ Effectue un premier versement (montant minimum indiqué sur le site).\n"
        "5️⃣ Ta prime sera créditée après validation du compte."
    ),
    "Revolut": (
        "https://revolut.com/referral",
        "📋 **Tuto Revolut :**\n"
        "1️⃣ Ouvre le lien et télécharge l'application.\n"
        "2️⃣ Crée ton compte et valide ton identité.\n"
        "3️⃣ Commande ta carte bancaire gratuite.\n"
        "4️⃣ Effectue un paiement avec ta carte.\n"
        "5️⃣ Prime reçue sous 24h."
    ),
    "HelloBank": (
        "https://hellobank.fr/parrainage",
        "📋 **Tuto HelloBank :**\n"
        "1️⃣ Clique sur le lien.\n"
        "2️⃣ Remplis le formulaire d'inscription.\n"
        "3️⃣ Envoie tes justificatifs.\n"
        "4️⃣ Effectue un premier versement.\n"
        "5️⃣ Prime créditée après validation."
    ),
    "BankIn": (
        "https://bankin.com/parrainage",
        "📋 **Tuto BankIn :**\n"
        "1️⃣ Télécharge l'application via le lien.\n"
        "2️⃣ Crée ton compte.\n"
        "3️⃣ Connecte au moins un compte bancaire.\n"
        "4️⃣ Profite des fonctionnalités premium offertes."
    ),
    "PayPal": (
        "https://paypal.com/referral",
        "📋 **Tuto PayPal :**\n"
        "1️⃣ Connecte-toi ou crée un compte via le lien.\n"
        "2️⃣ Ajoute un compte bancaire ou une carte.\n"
        "3️⃣ Envoie ou reçois de l'argent pour activer la prime."
    ),
    "Crédit Agricole": (
        "https://credit-agricole.fr/offre",
        "📋 **Tuto Crédit Agricole :**\n"
        "1️⃣ Clique sur le lien et choisis ton agence.\n"
        "2️⃣ Ouvre un compte en ligne.\n"
        "3️⃣ Dépose le montant minimum requis.\n"
        "4️⃣ Reçois ta prime."
    ),
    "Crédit Lyonnais": (
        "https://lcl.fr/parrainage",
        "📋 **Tuto LCL :**\n"
        "1️⃣ Ouvre le lien et remplis le formulaire.\n"
        "2️⃣ Fournis tes justificatifs.\n"
        "3️⃣ Effectue ton premier versement.\n"
        "4️⃣ Prime créditée sous quelques jours."
    ),
    "Société Générale": (
        "https://societegenerale.fr/parrainage",
        "📋 **Tuto Société Générale :**\n"
        "1️⃣ Clique sur le lien et choisis ton offre.\n"
        "2️⃣ Ouvre ton compte.\n"
        "3️⃣ Fournis les pièces justificatives.\n"
        "4️⃣ Prime versée après validation."
    ),
    "BforBank": (
        "https://bforbank.com/parrainage",
        "📋 **Tuto BforBank :**\n"
        "1️⃣ Ouvre le lien.\n"
        "2️⃣ Crée un compte avec tes informations.\n"
        "3️⃣ Envoie tes justificatifs.\n"
        "4️⃣ Effectue un dépôt initial.\n"
        "5️⃣ Prime versée après activation."
    ),
    "N26": (
        "https://n26.com/referral",
        "📋 **Tuto N26 :**\n"
        "1️⃣ Clique sur le lien et télécharge l'application.\n"
        "2️⃣ Crée un compte et valide ton identité.\n"
        "3️⃣ Commande ta carte.\n"
        "4️⃣ Effectue un paiement pour déclencher la prime."
    ),
    "Fortuneo": (
        "https://fortuneo.fr/parrainage",
        "📋 **Tuto Fortuneo :**\n"
        "1️⃣ Ouvre le lien et choisis ton type de compte.\n"
        "2️⃣ Remplis le formulaire d'inscription.\n"
        "3️⃣ Envoie tes justificatifs.\n"
        "4️⃣ Prime versée après dépôt initial."
    ),
    "CoinBase": (
        "https://coinbase.com/join",
        "📋 **Tuto Coinbase :**\n"
        "1️⃣ Inscris-toi via le lien.\n"
        "2️⃣ Vérifie ton identité.\n"
        "3️⃣ Achète ou vends l'équivalent de 100€ en crypto.\n"
        "4️⃣ Prime créditée automatiquement."
    ),
    "Kraken": (
        "https://kraken.com/referral",
        "📋 **Tuto Kraken :**\n"
        "1️⃣ Clique sur le lien.\n"
        "2️⃣ Crée un compte et valide ton identité.\n"
        "3️⃣ Dépose un montant minimum.\n"
        "4️⃣ Prime versée après ton premier trade."
    ),
    "Deblock": (
        "https://deblock.com/parrainage",
        "📋 **Tuto Deblock :**\n"
        "1️⃣ Ouvre le lien.\n"
        "2️⃣ Crée un compte et valide ton email.\n"
        "3️⃣ Active ton profil.\n"
        "4️⃣ Prime reçue après ton premier transfert."
    ),
    "Robinhood": (
        "https://robinhood.com/referral",
        "📋 **Tuto Robinhood :**\n"
        "1️⃣ Ouvre le lien.\n"
        "2️⃣ Crée un compte.\n"
        "3️⃣ Dépose des fonds.\n"
        "4️⃣ Reçois des actions gratuites."
    )
}

# Bot
application = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, callback_data=name)] for name in platforms.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Bienvenue ! Choisis une plateforme pour voir le lien et le tutoriel :", reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    name = query.data
    link, tuto = platforms[name]
    await query.edit_message_text(f"🔗 **Lien :** {link}\n\n{tuto}", parse_mode="Markdown")

application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_click))

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put(update)
    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!", 200

@app.before_first_request
def set_webhook():
    webhook_url = f"{PUBLIC_URL}/{BOT_TOKEN}"
    application.bot.set_webhook(url=webhook_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
