import subprocess
import pandas as pd
import json
import os
from datetime import datetime

# Nome do sistema para o portfólio
SISTEMA = "ICMPaltomate"

def extrair_latencia(saida_cmd):
    """Extrai o tempo médio (ms) da resposta do comando ping."""
    try:
        # No Windows, buscamos por 'media =' ou 'average ='
        if "media =" in saida_cmd.lower():
            return saida_cmd.lower().split("media =")[-1].replace("ms", "").strip()
        return "N/A"
    except:
        return "Erro"

def disparar_ping(host, origem):
    """Executa o comando no CMD e organiza os dados."""
    print(f"[{SISTEMA}] Verificando: {host}...")
    
    # -n 2 envia dois pacotes para ser rápido mas preciso
    comando = ["ping", "-n", "2", host]
    execucao = subprocess.run(comando, capture_output=True, text=True)
    
    # Se houver 'TTL' na resposta, o destino está online
    status = "Online" if "TTL=" in execucao.stdout else "Offline"
    latencia = extrair_latencia(execucao.stdout) if status == "Online" else "---"
    
    return {
        "Data_Hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "Sistema": SISTEMA,
        "Origem": origem,
        "Destino": host,
        "Status": status,
        "Latencia_ms": latencia
    }

def salvar_no_excel(novos_dados, nome_arquivo="log_ICMPaltomate.xlsx"):
    """Salva os resultados em uma planilha Excel, acumulando os dados."""
    df_novo = pd.DataFrame(novos_dados)
    
    if os.path.exists(nome_arquivo):
        df_antigo = pd.read_excel(nome_arquivo)
        df_final = pd.concat([df_antigo, df_novo], ignore_index=True)
    else:
        df_final = df_novo
        
    df_final.to_excel(nome_arquivo, index=False)
    print(f"✅ Relatório atualizado: {nome_arquivo}")

# --- EXECUÇÃO PRINCIPAL ---
if __name__ == "__main__":
    print(f"--- INICIANDO {SISTEMA} ---")
    
    try:
        # 1. Carregar destinos
        with open('targets.json', 'r') as f:
            config = json.load(f)
        
        # 2. Executar pings
        resultados = []
        for alvo in config['destinos']:
            res = disparar_ping(alvo, config['nome_origem'])
            resultados.append(res)
        
        # 3. Salvar no Excel
        salvar_no_excel(resultados)
        
    except FileNotFoundError:
        print("❌ Erro: O arquivo 'targets.json' não foi encontrado!")
    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado: {e}")