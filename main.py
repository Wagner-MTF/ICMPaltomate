import subprocess
import pandas as pd
import json
import os
import re
import time
import random
import sys
from datetime import datetime

SISTEMA = "ICMPaltomate"

def efeito_hacker(duracao=0.4):
    """Animação visual no terminal antes de cada log."""
    caracteres = "01ABCDEFHIJKLMNOPQRSTUVXYZ#@&*$"
    fim = time.time() + duracao
    while time.time() < fim:
        linha = "".join(random.choice(caracteres) for _ in range(40))
        # Escrita em Verde
        sys.stdout.write(f"\r\033[92m{linha}\033[0m")
        sys.stdout.flush()
        time.sleep(0.04)

def extrair_ms(saida_cmd):
    try:
        # Pega o valor da média ou tempo individual
        busca = re.search(r"(?:media|average)\s*=\s*(\d+)\s*ms", saida_cmd.lower())
        if busca: return busca.group(1)
        busca_indiv = re.search(r"(?:tempo|time)[=<](\d+)\s*ms", saida_cmd.lower())
        if busca_indiv: return busca_indiv.group(1)
        return "0"
    except: return "Erro"

def salvar_no_excel(dados):
    """Força a gravação imediata no arquivo Excel."""
    arquivo = "log_ICMPaltomate.xlsx"
    df_novo = pd.DataFrame([dados])
    
    try:
        if os.path.exists(arquivo):
            df_antigo = pd.read_excel(arquivo)
            df_final = pd.concat([df_antigo, df_novo], ignore_index=True)
        else:
            df_final = df_novo
        
        # O parâmetro index=False é crucial para não sujar a planilha
        df_final.to_excel(arquivo, index=False)
    except Exception as e:
        print(f"\n[!] Erro ao gravar Excel: {e}")

def executar_ciclo_hacker(host, origem):
    # 1. Faz a animação visual
    efeito_hacker()
    
    # 2. Dispara o ping (escondido do usuário)
    comando = ["ping", "-n", "1", host]
    execucao = subprocess.run(comando, capture_output=True, text=True)
    
    status = "Online" if "TTL=" in execucao.stdout else "Offline"
    ms = extrair_ms(execucao.stdout) if status == "Online" else "---"
    
    # 3. Organiza os dados
    dados_registro = {
        "Data_Inicio_Captura": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "Nome_Sistema": SISTEMA,
        "Origem": origem,
        "Destino": host,
        "Milisegundos": ms,
        "Status": status
    }
    
    # 4. ENVIA PARA O EXCEL IMEDIATAMENTE
    salvar_no_excel(dados_registro)
    
    # 5. Mostra confirmação limpa no CMD
    sys.stdout.write(f"\r\033[94m[REGISTRO SALVO]\033[0m {host} -> {ms}ms | {status}      \n")
    return dados_registro

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\033[92m" + "="*45)
    print(f"      {SISTEMA} : MODO HACKER ATIVADO")
    print("="*45 + "\033[0m")
    
    try:
        while True:
            # Carregar configurações
            with open('targets.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            origem = config['nome_origem']
            alvo_principal = config['destinos'][0] # Foca em apenas 1 destino
            duracao_min = config.get('intervalo_minutos', 1)
            
            tempo_limite = time.time() + (duracao_min * 60)
            
            print(f"\033[93mAlvo:\033[0m {alvo_principal} | \033[93mTempo:\033[0m {duracao_min} min\n")

            while time.time() < tempo_limite:
                executar_ciclo_hacker(alvo_principal, origem)
                time.sleep(0.5) # Pausa entre cada ping gravado

            print(f"\n\033[92m✅ CICLO DE {duracao_min} MIN FINALIZADO E LOGADO NO EXCEL!\033[0m")
            
            opcao = input("\nDeseja reiniciar nova sessão? (S/N): ").strip().upper()
            if opcao != 'S':
                print("Finalizando sistema...")
                break

    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro crítico: {e}")