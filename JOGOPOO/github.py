#10/03/2026
import os

print("✉️ configurando email....")
comando_email = "git config user.email \"lucashenriquesilva0809@gmail.com\" "
os.system(comando_email)

print("🆕 Adicionando modificaçôes...")
comando01 = "git add *"
os.system(comando01)

mensagem = input("💬Mensagem do commit: ")

while(len(mensagem) < 5):
    print("❗Mensagem muito pequena, detalhe mais...")
    mensagem = input("💬Mensagem do commit: ")

print("✅ Registrando alterações...")
comando02 = f"git commit -m \"{mensagem}\" "
os.system(comando02)

print("🔁Enviando projeto ao GitHub")
comando03 = "git push"
os.system(comando03)

