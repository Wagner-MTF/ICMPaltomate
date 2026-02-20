# 🚀 ICMPaltomate - Hacker Edition

O **ICMPaltomate** é uma ferramenta de monitoramento de conectividade ICMP (Ping) com foco em análise de latência e automação de logs. Esta versão apresenta uma interface personalizada estilo "Hacker/Matrix" e salvamento de dados em tempo real em planilhas Excel.



## ✨ Funcionalidades
- **Captura Contínua:** Monitora o alvo pelo tempo exato definido pelo usuário.
- **Modo Hacker:** Interface visual animada em verde (ANSI) com efeito de processamento de dados.
- **Persistência Real-Time:** Cada ping é salvo instantaneamente no Excel (`.xlsx`), evitando perda de dados.
- **Foco em Alvo Único:** Monitoramento dedicado para análise de estabilidade de um host específico.
- **Relatório Completo:** Logs contendo Timestamp, Nome do Sistema, Origem, Destino, Latência (ms) e Status.

## 🛠️ Tecnologias
- **Python 3.x**
- **Pandas** & **Openpyxl** (Tratamento de dados e Excel)
- **Subprocess** (Execução silenciosa de comandos de rede)
- **Regex** (Extração inteligente de latência)

## 🚀 Como Instalar e Rodar

### 1. Clonar o Repositório
Abra o terminal (CMD ou PowerShell) e digite:
```bash
git clone [https://github.com/Wagner-MTF/ICMPaltomate.git](https://github.com/Wagner-MTF/ICMPaltomate.git)
cd ICMPaltomate
```

## 2. Instalar Dependências
Certifique-se de ter o Python instalado. Depois, instale as bibliotecas necessárias:

```
pip install pandas openpyxl
```

## 3. Configurar Alvos
Edite o arquivo targets.json na raiz do projeto:

nome_origem: Nome da sua estação.

intervalo_minutos: Tempo que o scanner deve rodar antes de perguntar se deseja continuar.

destinos: O primeiro IP/Site desta lista será o alvo monitorado.

```
python main.py
```

## 📊 Estrutura do Relatório
O arquivo log_ICMPaltomate.xlsx será gerado com as seguintes colunas:
| Data_Inicio_Captura | Nome_Sistema | Origem | Destino | Milisegundos | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 20/02/2026 10:00:01 | ICMPaltomate | Wagner_PC | 8.8.8.8 | 15 | Online |

Desenvolvido por Wagner Matheus de Faria