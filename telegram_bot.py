# telegram_bot.py
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from tinydb import TinyDB, Query

# Configura logs simples (útil para depurar)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# O token será lido de uma variável de ambiente (não ficará no código)
TOKEN = os.getenv("TELEGRAM_TOKEN")
# Banco de dados local (arquivo JSON dentro do container)
db = TinyDB("tasks.json")
Task = Query()


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
# ---------- COMANDOS DE LISTA DE TAREFAS ----------
async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /add <texto> → salva a tarefa."""
    if not context.args:
        await update.message.reply_text("Uso: /add <tarefa>")
        return
    task_text = " ".join(context.args)
    db.insert({"user_id": update.effective_user.id, "text": task_text})
    await update.message.reply_text(f"Tarefa adicionada: {task_text}")

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /list → lista as tarefas do usuário."""
    user_tasks = db.search(Task.user_id == update.effective_user.id)
    if not user_tasks:
        await update.message.reply_text("Você ainda não tem tarefas.")
        return
    lines = [f"{i+1}. {t['text']}" for i, t in enumerate(user_tasks)]
    await update.message.reply_text("\n".join(lines))

async def del_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /del <número> → remove a tarefa indicada."""
    if not context.args or not context.args[0].isdigit():
        await update.message.reply_text("Uso: /del <número>")
        return
    idx = int(context.args[0]) - 1
    user_tasks = db.search(Task.user_id == update.effective_user.id)
    if idx < 0 or idx >= len(user_tasks):
        await update.message.reply_text("Número inválido.")
        return
    db.remove(doc_ids=[user_tasks[idx].doc_id])
    await update.message.reply_text("Tarefa removida.")


if __name__ == "__main__":
    # Cria a aplicação do bot usando o token da variável de ambiente
    app = ApplicationBuilder().token(TOKEN).build()
    # Registra os comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("soma", soma))
    app.add_handler(CommandHandler("add", add_task))
    app.add_handler(CommandHandler("list", list_tasks))
    app.add_handler(CommandHandler("del", del_task))

    # Inicia o bot em modo *polling* (Render cuidará do webhook)
    app.run_polling()
