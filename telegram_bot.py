# telegram_bot.py
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Configura logs simples (útil para depurar)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# O token será lido de uma variável de ambiente (não ficará no código)
TOKEN = os.getenv("TELEGRAM_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Resposta ao comando /start"""
    await update.message.reply_text("Olá! Eu sou seu bot gratuito no Telegram.")


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Resposta ao comando /ping"""
    await update.message.reply_text("Pong! 🏓")


async def soma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /soma <a> <b> → devolve a soma"""
    try:
        a = int(context.args[0])
        b = int(context.args[1])
        await update.message.reply_text(f"{a} + {b} = {a + b}")
    except (IndexError, ValueError):
        await update.message.reply_text("Uso: /soma <num1> <num2>")


if __name__ == "__main__":
    # Cria a aplicação do bot usando o token da variável de ambiente
    app = ApplicationBuilder().token(TOKEN).build()
    # Registra os comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("soma", soma))

    # Inicia o bot em modo *polling* (Render cuidará do webhook)
    app.run_polling()
