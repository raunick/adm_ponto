import streamlit as st
import pandas as pd
from datetime import datetime ,timedelta

df = pd.read_csv('data.csv')
data_atual = datetime.now()
formato_br = "%d/%m/%Y %H:%M:%S"
data_formatada_br = data_atual.strftime(formato_br)


st.table(df)
'''
# Relatorio do seu ponto da data atual:
'''




st.write(f'Data atual: {data_formatada_br}')


def calcular_periodo_manha(entrada, almoco_saida):
    if pd.isnull(entrada) or pd.isnull(almoco_saida) or entrada == '-' or almoco_saida == '-':
        return ''
    else:
        entrada = datetime.strptime(entrada, "%H:%M")
        almoco_saida = datetime.strptime(almoco_saida, "%H:%M")
        periodo_trabalhado_manha = almoco_saida - entrada
        return str(periodo_trabalhado_manha)
def calcular_periodo_tarde(almoco_entrada,saida):
    if pd.isnull(almoco_entrada) or pd.isnull(saida) or almoco_entrada == '-' or saida == '-':
        return ''
    else:

        almoco_entrada = datetime.strptime(almoco_entrada, "%H:%M")
        saida = datetime.strptime(saida, "%H:%M")
        periodo_periodo_tarde = saida - almoco_entrada
        return str(periodo_periodo_tarde)
def calcular_periodo_almoco(almoco_entrada, almoco_saida):
    if pd.isnull(almoco_entrada) or pd.isnull(almoco_saida) or almoco_entrada == '-' or almoco_saida == '-':
        return ''
    else:
        almoco_entrada = datetime.strptime(almoco_entrada, "%H:%M")
        almoco_saida = datetime.strptime(almoco_saida, "%H:%M")
        periodo_almoco =  almoco_entrada - almoco_saida
        return str(periodo_almoco)
    
def calcular_horas_trabalhadas(df_row):
    if pd.isnull(df_row['Relação de Horas Manhã']) or pd.isnull(df_row['Relação de Horas Tarde']) or pd.isnull(df_row['Relação de Horas Almoço']):
        return ''
    else:
        manha = pd.to_timedelta(df_row['Relação de Horas Manhã'])
        almoco = pd.to_timedelta(df_row['Relação de Horas Almoço'])
        tarde = pd.to_timedelta(df_row['Relação de Horas Tarde'])
        total_horas_trabalhadas = manha + tarde + almoco
        delta = pd.to_timedelta(total_horas_trabalhadas)
        # Converter para um objeto datetime
        delta_datetime = datetime(1, 1, 1) + delta

        # Imprimir apenas horas e minutos
        formato = "%H:%M:%S"
        total_horas_trabalhadas_formatado = delta_datetime.strftime(formato)
        return str(total_horas_trabalhadas_formatado)


def calcular_banco_de_horas(df_row):
    if pd.isnull(df_row['Horas Trabalhadas']):
        return '', ''
    else:
        total_horas_trabalhadas = pd.to_timedelta(df_row['Horas Trabalhadas'])
        
        # Verifica se é sexta-feira (o método weekday() retorna 4 para sexta-feira)
        if pd.to_datetime(df_row['Data']).weekday() == 4:
            jornada_diaria = pd.to_timedelta('7:00:00')
        # Verifica se é sábado (o método weekday() retorna 5 para sábado)
        elif pd.to_datetime(df_row['Data']).weekday() == 5:
            jornada_diaria = pd.to_timedelta('00:00:00')  # Jornada de trabalho zero
        # Verifica se é domingo (o método weekday() retorna 6 para domingo)
        elif pd.to_datetime(df_row['Data']).weekday() == 6:
            jornada_diaria = pd.to_timedelta('00:00:00')  # Jornada de trabalho zero
        else:
            jornada_diaria = pd.to_timedelta('8:00:00')

        banco_de_horas = total_horas_trabalhadas - jornada_diaria
        return str(banco_de_horas)

    
df['Relação de Horas Manhã'] = df.apply(lambda row: calcular_periodo_manha(row['Entrada'], row['Almoço Saída']), axis=1)
df['Relação de Horas Tarde'] = df.apply(lambda row: calcular_periodo_manha(row['Almoço Entrada'], row['Saída']), axis=1)
df['Relação de Horas Almoço'] = df.apply(lambda row: calcular_periodo_almoco(row['Almoço Entrada'], row['Almoço Saída']), axis=1)
df['Horas Trabalhadas'] = df.apply(calcular_horas_trabalhadas, axis=1)
df['Banco de Horas'] = df.apply(calcular_banco_de_horas, axis=1)
# Exiba o DataFrame original e a "Relação de Horas Manhã"
st.table(df[['Data', 'Entrada', 'Almoço Saída', 'Almoço Entrada','Saída' ,'Relação de Horas Manhã', 'Relação de Horas Tarde', 'Relação de Horas Almoço', 'Total de Horas Trabalhadas', 'Banco de Horas']])