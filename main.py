import streamlit as st
import pandas as pd
from datetime import datetime,timedelta

# Carregar o DataFrame a partir do arquivo CSV
df = pd.read_csv('data.csv')

# Função para calcular o período da manhã
def calcular_periodo_manha(entrada, almoco_saida):

    if pd.isnull(entrada) or pd.isnull(almoco_saida) or entrada == '-' or almoco_saida == '-':
        return '-'
    else:
        entrada = datetime.strptime(entrada, "%H:%M")
        almoco_saida = datetime.strptime(almoco_saida, "%H:%M")
        periodo_trabalhado_manha = almoco_saida - entrada
        return str(periodo_trabalhado_manha)

# Função para calcular o período da tarde
def calcular_periodo_tarde(almoco_entrada, saida):

    if pd.isnull(almoco_entrada) or pd.isnull(saida) or almoco_entrada == '-' or saida == '-':
        return '-'
    else:
        almoco_entrada = datetime.strptime(almoco_entrada, "%H:%M")
        saida = datetime.strptime(saida, "%H:%M")
        periodo_periodo_tarde = saida - almoco_entrada
        return str(periodo_periodo_tarde)

# Função para calcular o período de almoço
def calcular_periodo_almoco(almoco_entrada, almoco_saida):
    if pd.isnull(almoco_entrada) or pd.isnull(almoco_saida) or almoco_entrada == '-' or almoco_saida == '-':
        return ''
    else:
        almoco_entrada = datetime.strptime(almoco_entrada, "%H:%M")
        almoco_saida = datetime.strptime(almoco_saida, "%H:%M")
        periodo_almoco =  almoco_entrada - almoco_saida
        return str(periodo_almoco)

# Função para calcular as horas trabalhadas
def calcular_horas_trabalhadas(df_row):

    if pd.isnull(df_row['Relação de Horas Manhã']) or pd.isnull(df_row['Relação de Horas Tarde']) or df_row['Relação de Horas Manhã'] == '-' or df_row['Relação de Horas Tarde'] == '-':
        return '-'

    def calcular_intervalo(manha, tarde):
        total_horas = manha + tarde
        return total_horas

    manha = pd.to_timedelta(df_row['Relação de Horas Manhã'])
    tarde = pd.to_timedelta(df_row['Relação de Horas Tarde'])

    total_horas_trabalhadas = calcular_intervalo(manha, tarde)
    total_horas_formatado = str(total_horas_trabalhadas).split()[-1]  # Extrai apenas HH:MM:SS
    return total_horas_formatado

# Função para calcular o banco de horas para cada dia.
def calcular_banco_de_horas(df_row):
    if pd.isnull(df_row['Relação de Horas Manhã']) or pd.isnull(df_row['Relação de Horas Tarde']) or df_row['Relação de Horas Manhã'] == '-' or df_row['Relação de Horas Tarde'] == '-':
        return '-'
    else:
        total_horas_trabalhadas = pd.to_timedelta(df_row['Horas Trabalhadas'])
        if pd.to_datetime(df_row['Data']).weekday() == 4:
            jornada_diaria = pd.to_timedelta('8:00:00')
        else:
            jornada_diaria = pd.to_timedelta('9:00:00')
        horas_extra = total_horas_trabalhadas.total_seconds() - jornada_diaria.total_seconds()
        minutos = horas_extra / 60
        return int(minutos)



# Função para calcular o total de horas trabalhadas
def calcular_total_minutos_banco(coluna_minutos_banco):
    total_minutos = 0
    
    for minutos_banco in coluna_minutos_banco:
        if pd.isnull(minutos_banco) or minutos_banco == '-':
            minutos_banco = 0
        else:
            minutos_banco = int(minutos_banco)

        total_minutos += minutos_banco

    return total_minutos

def calcular_total_horas_trabalhadas(coluna_hora_trabalhada):
    total_horas = pd.to_timedelta('0:0:0')
    
    for hora_trabalhada in coluna_hora_trabalhada:
        if pd.isnull(hora_trabalhada) or hora_trabalhada == '-':
            hora_trabalhada = pd.to_timedelta('0:0:0')
        else:
            hora_trabalhada = pd.to_timedelta(hora_trabalhada)

        total_horas += hora_trabalhada

    horas = int(total_horas.total_seconds() // 3600)
    minutos = int((total_horas.total_seconds() % 3600) // 60)
    return f'{horas}h {minutos}m'

def formatar_total_minutos(total_minutos):
    sinal = '' if total_minutos >= 0 else '-'
    total_minutos = abs(total_minutos)

    horas = total_minutos // 60
    minutos = total_minutos % 60

    return f'{sinal}{horas}h {minutos}m'
st.title('Segue modelo de tabela 📋')
# Boolean to resize the dataframe, stored as a session state variable
st.checkbox("expandir", value=True, key="use_container_width")
# Exibir o DataFrame como uma tabela no Streamlit
st.dataframe(df, use_container_width = st.session_state.use_container_width)
st.write('Faça o download da tabela.💻')

# Layout do Streamlit
st.title('Relatório de Ponto 🕐')

# Botão de upload para carregar um arquivo CSV
uploaded_file = st.file_uploader("Escolha um arquivo CSV 📄", type=["csv"])

# Se um arquivo CSV for carregado, processá-lo
if uploaded_file is not None:
    # Leitura do DataFrame a partir do arquivo CSV
    df = pd.read_csv(uploaded_file, encoding='utf-8')

    # Adicionar colunas e realizar cálculos
    df['Relação de Horas Manhã'] = df.apply(lambda row: calcular_periodo_manha(row['Entrada'], row['Almoço Saída']), axis=1)
    df['Relação de Horas Tarde'] = df.apply(lambda row: calcular_periodo_tarde(row['Almoço Entrada'], row['Saída']), axis=1)
    df['Horas Trabalhadas'] = df.apply(calcular_horas_trabalhadas, axis=1)
    df['Banco de Minutos'] = df.apply(calcular_banco_de_horas, axis=1)
    # Calcular o total de horas trabalhadas
    total_horas_trabalhadas = calcular_total_horas_trabalhadas(df['Horas Trabalhadas'])
    horas_totais_banco = calcular_total_minutos_banco(df['Banco de Minutos'] )
    # Selecionar as colunas relevantes para a exibição no Streamlit
    relacao_horas_dias = df[['Data','Entrada', 'Almoço Saída', 'Almoço Entrada', 'Saída', 
                             'Relação de Horas Manhã', 'Relação de Horas Tarde',
                             'Horas Trabalhadas', 'Banco de Minutos',
                            ]]

    # Exibir a tabela resultante no Streamlit
    st.data_editor(relacao_horas_dias)

    # Dividir a tela em duas colunas no Streamlit
    col1, col2 = st.columns(2)

    # Exibir métricas no Streamlit
    col1.metric("Total de horas trabalhadas", f'{total_horas_trabalhadas}')
    total_horas = formatar_total_minutos(horas_totais_banco)
    col2.metric("Total de horas banco", f'{total_horas}')

    # Exibir um gráfico de linha no Streamlit
    st.write('## Relação de minutos pelos Dias:')
    st.line_chart(df.set_index('Data')[['Banco de Minutos']])
