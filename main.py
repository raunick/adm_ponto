import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Carregar o DataFrame a partir do arquivo CSV
df = pd.read_csv('data.csv')
st.title('Segue modelo de tabela')
# Boolean to resize the dataframe, stored as a session state variable
st.checkbox("expandir", value=True, key="use_container_width")
# Exibir o DataFrame como uma tabela no Streamlit
st.dataframe(df,use_container_width=st.session_state.use_container_width)
st.write('Faça o download da tabela.')

# Função para calcular o período da manhã
def calcular_periodo_manha(entrada, almoco_saida):
    """
    Calcula o período trabalhado na parte da manhã.
    """
    if pd.isnull(entrada) or pd.isnull(almoco_saida) or entrada == '-' or almoco_saida == '-':
        return ''
    else:
        entrada = datetime.strptime(entrada, "%H:%M")
        almoco_saida = datetime.strptime(almoco_saida, "%H:%M")
        periodo_trabalhado_manha = almoco_saida - entrada
        return str(periodo_trabalhado_manha)

# Função para calcular o período da tarde
def calcular_periodo_tarde(almoco_entrada, saida):
    """
    Calcula o período trabalhado na parte da tarde.
    """
    if pd.isnull(almoco_entrada) or pd.isnull(saida) or almoco_entrada == '-' or saida == '-':
        return ''
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
    """
    Calcula o total de horas trabalhadas.
    """
    if pd.isnull(df_row['Relação de Horas Manhã']) or pd.isnull(df_row['Relação de Horas Tarde']) or pd.isnull(df_row['Relação de Horas Almoço']):
        return ''
    else:
        manha = pd.to_timedelta(df_row['Relação de Horas Manhã'])
        almoco = pd.to_timedelta(df_row['Relação de Horas Almoço'])
        tarde = pd.to_timedelta(df_row['Relação de Horas Tarde'])
        total_horas_trabalhadas = manha + tarde + almoco
        delta = pd.to_timedelta(total_horas_trabalhadas)
        delta_datetime = datetime(1, 1, 1) + delta
        formato = "%H:%M:%S"
        total_horas_trabalhadas_formatado = delta_datetime.strftime(formato)
        return str(total_horas_trabalhadas_formatado)

# Função para calcular o banco de horas
def calcular_banco_de_horas(df_row):
    """
    Calcula o banco de horas para cada dia.
    """
    if pd.isnull(df_row['Horas Trabalhadas']):
        return '', ''
    else:
        total_horas_trabalhadas = pd.to_timedelta(df_row['Horas Trabalhadas'])
        if pd.to_datetime(df_row['Data']).weekday() == 4:
            jornada_diaria = pd.to_timedelta('9:00:00')
        elif pd.to_datetime(df_row['Data']).weekday() == 5:
            jornada_diaria = pd.to_timedelta('00:00:00')
        elif pd.to_datetime(df_row['Data']).weekday() == 6:
            jornada_diaria = pd.to_timedelta('00:00:00')
        elif df_row['Dia da Semana'] == 'Feriado':
            jornada_diaria = pd.to_timedelta('00:00:00')
        else:
            jornada_diaria = pd.to_timedelta('8:00:00')
        banco_de_horas_timedelta = total_horas_trabalhadas - jornada_diaria
        horas = int(banco_de_horas_timedelta.total_seconds() // 3600)
        minutos = int((banco_de_horas_timedelta.total_seconds() % 3600) // 60)
        return f'{horas}:{minutos}'

# Função para calcular o total de horas trabalhadas
def calcular_total_horas_banco(coluna_horas):
    """
    Calcula o total de horas no banco de horas.
    """
    total_horas_trabalhadas = pd.to_timedelta('00:00:00')

    for horas_str in coluna_horas:
        if pd.notnull(horas_str):
            horas, minutos = map(int, horas_str.split(':'))
            total_horas_trabalhadas += pd.to_timedelta(f'{horas}:{minutos}:00')

    horas = int(total_horas_trabalhadas.total_seconds() // 3600)
    minutos = int((total_horas_trabalhadas.total_seconds() % 3600) // 60)

    return f'{horas}h{minutos}m'

# Função para calcular as horas positivas
def calcular_horas_positivas(coluna_horas):
    """
    Calcula e imprime as horas positivas.
    """
    total_horas_trabalhadas = pd.to_timedelta('00:00:00')

    for horas_str in coluna_horas:
        if pd.notnull(horas_str):
            horas, minutos = map(int, horas_str.split(':'))
            total_horas_trabalhadas += pd.to_timedelta(f'{horas}:{minutos}:00')

    horas = int(total_horas_trabalhadas.total_seconds() // 3600)
    minutos = int((total_horas_trabalhadas.total_seconds() % 3600) // 60)

    print(f'{horas}:{minutos}')

# Função para calcular o total de horas trabalhadas
def calcular_total_horas_trabalhadas(coluna_hora_trabalhada):
    """
    Calcula o total de horas trabalhadas.
    """
    coluna_hora_trabalhada = pd.to_timedelta(df['Horas Trabalhadas'])
    total_horas = coluna_hora_trabalhada.sum()
    horas = int(total_horas.total_seconds() // 3600)
    minutos = int((total_horas.total_seconds() % 3600) // 60)
    return f'{horas}h{minutos}m'

# Calcular e adicionar colunas ao DataFrame
df['Relação de Horas Manhã'] = df.apply(lambda row: calcular_periodo_manha(row['Entrada'], row['Almoço Saída']), axis=1)
df['Relação de Horas Tarde'] = df.apply(lambda row: calcular_periodo_tarde(row['Almoço Entrada'], row['Saída']), axis=1)
df['Relação de Horas Almoço'] = df.apply(lambda row: calcular_periodo_almoco(row['Almoço Entrada'], row['Almoço Saída']), axis=1)
df['Horas Trabalhadas'] = df.apply(calcular_horas_trabalhadas, axis=1)
df['Banco de Horas'] = df.apply(calcular_banco_de_horas, axis=1)

# Selecionar as colunas relevantes para a exibição no Streamlit
relacao_horas_dias = df[['Data', 'Entrada', 'Almoço Saída', 'Almoço Entrada', 'Saída', 'Relação de Horas Manhã', 'Relação de Horas Tarde', 'Relação de Horas Almoço', 'Horas Trabalhadas', 'Banco de Horas']]

# Exibir a tabela resultante no Streamlit
# st.table(df[['Data', 'Entrada', 'Almoço Saída', 'Almoço Entrada', 'Saída', 'Relação de Horas Manhã', 'Relação de Horas Tarde', 'Relação de Horas Almoço', 'Horas Trabalhadas', 'Banco de Horas']])

# Card com o dia de maior banco de horas
dia_max_banco_horas = df.loc[df['Banco de Horas'].idxmax()]

# Card com o dia de menor banco de horas usando st.metric
dia_min_banco_horas = df.loc[df['Banco de Horas'].idxmin()]

# Calcular o total de horas no banco de horas e de trabalho
horas_totais_banco = calcular_total_horas_banco(df['Banco de Horas'])
horas_totais_trabalho = calcular_total_horas_trabalhadas(df['Horas Trabalhadas'])
# Layout do Streamlit
st.title('Relatório de Ponto')

# Botão de upload para carregar um arquivo CSV
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type=["csv"])

# Se um arquivo CSV for carregado, processá-lo
if uploaded_file is not None:
    # Leitura do DataFrame a partir do arquivo CSV
    df = pd.read_csv(uploaded_file)

    # Adicionar colunas e realizar cálculos
    df['Relação de Horas Manhã'] = df.apply(lambda row: calcular_periodo_manha(row['Entrada'], row['Almoço Saída']), axis=1)
    df['Relação de Horas Tarde'] = df.apply(lambda row: calcular_periodo_tarde(row['Almoço Entrada'], row['Saída']), axis=1)
    df['Relação de Horas Almoço'] = df.apply(lambda row: calcular_periodo_almoco(row['Almoço Entrada'], row['Almoço Saída']), axis=1)
    df['Horas Trabalhadas'] = df.apply(calcular_horas_trabalhadas, axis=1)
    df['Banco de Horas'] = df.apply(calcular_banco_de_horas, axis=1)

    # Selecionar as colunas relevantes para a exibição no Streamlit
    relacao_horas_dias = df[['Data', 'Entrada', 'Almoço Saída', 'Almoço Entrada', 'Saída', 'Relação de Horas Manhã', 'Relação de Horas Tarde', 'Relação de Horas Almoço', 'Horas Trabalhadas', 'Banco de Horas']]

    # Exibir a tabela resultante no Streamlit
    st.dataframe(df[['Data', 'Entrada', 'Almoço Saída', 'Almoço Entrada', 'Saída', 'Relação de Horas Manhã', 'Relação de Horas Tarde', 'Relação de Horas Almoço', 'Horas Trabalhadas', 'Banco de Horas']])

    # Card com o dia de maior banco de horas
    dia_max_banco_horas = df.loc[df['Banco de Horas'].idxmax()]

    # Card com o dia de menor banco de horas usando st.metric
    dia_min_banco_horas = df.loc[df['Banco de Horas'].idxmin()]

    # Calcular o total de horas no banco de horas e de trabalho
    horas_totais_banco = calcular_total_horas_banco(df['Banco de Horas'])
    horas_totais_trabalho = calcular_total_horas_trabalhadas(df['Horas Trabalhadas'])

    # Dividir a tela em duas colunas no Streamlit
    col1, col2 = st.columns(2)

    # Exibir métricas no Streamlit
    col1.metric("Total de horas trabalhadas", f'{horas_totais_trabalho}')
    col2.metric("Total de horas banco", f'{horas_totais_banco}')

    # Exibir um gráfico de linha no Streamlit
    st.write('## Relação de Horas pelos Dias:')
    st.line_chart(df.set_index('Data')[['Banco de Horas']])
