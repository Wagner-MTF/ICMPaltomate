import subprocess
import pandas as pd
import json
import os
import time
from datetime import datetime

SISTEMA = "ICMPaltomate"

def extrair_ms(saida_cmd):
    """Extrai o número de milissegundos de forma robusta."""
    try:
        # Tenta encontrar o padrão de tempo médio no final do ping
        # O Windows costuma usar 'media =' ou 'average ='
        import re
        # Busca por um número seguido de 'ms' logo após 'media =' ou 'average ='
        busca = re.search(r"(?:media|average)\s*=\s*(\d+)\s*ms", saida_cmd.lower())
        if busca:
            return busca.group(1) # Retorna apenas o número
        
        # Se não achou a média, tenta pegar o tempo do primeiro pacote
        busca_individual = re.search(r"(?:tempo|time)[=<](\d+)\s*ms", saida_cmd.lower())
        if busca_individual:
            return busca_individual.group(1)
            
        return "N/A"
    except:
        return "Erro"

def disparar_ping(host, origem):
    # Captura o momento exato do início desta verificação
    data_inicio = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    print(f"[{data_inicio}] {SISTEMA} -> Verificando {host}...")
    
    comando = ["ping", "-n", "2", host]
    execucao = subprocess.run(comando, capture_output=True, text=True)
    
    status = "Online" if "TTL=" in execucao.stdout else "Offline"
    ms = extrair_ms(execucao.stdout) if status == "Online" else "---"
    
    # Montando a estrutura conforme solicitado
    return {
        "Data_Inicio_Captura": data_inicio,
        "Nome_Sistema": SISTEMA,
        "Origem": origem,
        "Destino": host,
        "Milisegundos": ms,
        "Status": status
    }

def salvar_no_excel(novos_dados):
    arquivo = "log_ICMPaltomate.xlsx"
    df_novo = pd.DataFrame(novos_dados)
    if os.path.exists(arquivo):
        df_antigo = pd.read_excel(arquivo)
        df_final = pd.concat([df_antigo, df_novo], ignore_index=True)
    else:
        df_final = df_novo
    df_final.to_excel(arquivo, index=False)

if __name__ == "__main__":
    print(f"=== {SISTEMA} INICIADO ===")
    
    try:
        while True:
            # Carregar configurações
            with open('targets.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            origem = config['nome_origem']
            intervalo_min = config['intervalo_minutos']
            alvos = config['destinos']
            
            resultados_rodada = []
            for alvo in alvos:
                res = disparar_ping(alvo, origem)
                resultados_rodada.append(res)
            
            # Salva no excel
            salvar_no_excel(resultados_rodada)
            
            # MENSAGEM DE CONCLUÍDO (Exatamente no minuto limite)
            print(f"✅ CICLO DE MONITORAMENTO CONCLUÍDO!")
            print(f"Aguardando {intervalo_min} minuto(s) para a próxima rodada...\n")
            
            # Espera o tempo definido
            time.sleep(intervalo_min * 60)

    except KeyboardInterrupt:
        print(f"\n--- {SISTEMA} FINALIZADO ---")
    except Exception as e:
        print(f"❌ Erro crítico: {e}")