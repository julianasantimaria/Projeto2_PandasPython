import pandas as pd
from datetime import datetime

customers_df = pd.read_csv('customers.csv')
sales_df = pd.read_csv('sales.csv')
products_df = pd.read_csv('products.csv')

sales_df['Unit Price'] = sales_df['Unit Price'].str.replace(",", "").astype(float)


#Pergunta 2
customers_df['date_of_birth'] = pd.to_datetime(customers_df['date_of_birth'], format='%Y-%m-%d')
#print(customers_df.head())

#arrumando a data e achando a idade
data_atual = datetime.now()
customers_df['Idade'] = (data_atual - customers_df['date_of_birth']).dt.days // 365
#print(customers_df.head())

#juntando customers com sales
joined_df = pd.merge(customers_df, sales_df, left_on='user_id', right_on='_CustomerID')
#media de idade por IDproduto
media_idade_df = joined_df.groupby('_ProductID')['Idade'].mean().reset_index()
media_idade_df = pd.merge(media_idade_df, products_df, left_on='_ProductID', right_on='product_id')
#print(media_idade_df.head())


#Pergunta3
#contagem de vendas por mes
sales_df['OrderDate'] = pd.to_datetime(sales_df['OrderDate'], format='%d/%m/%y')
sales_df['TotalPedido'] = sales_df['Order Quantity'] * sales_df['Unit Price']
vendas_mes_df = sales_df.resample('M', on='OrderDate')['Order Quantity'].count().reset_index()

#valor total de vendas/mes
valor_total_mes = sales_df.resample('M', on='OrderDate')['TotalPedido'].sum().reset_index()
vendas_mes_df['valor_total_mes'] = valor_total_mes['TotalPedido']
#print(vendas_mes_df.head())


#Pergunta 4
#contagem de vendas por mes
scustomers_df = pd.read_csv('customers.csv')
sales_df = pd.read_csv('sales.csv')
products_df = pd.read_csv('products.csv')

sales_df['OrderDate'] = pd.to_datetime(sales_df['OrderDate'], format='%d/%m/%y')
sales_df['MesAnoPedido'] = sales_df['OrderDate'].dt.strftime('%Y-%m')
result = sales_df.groupby(['MesAnoPedido', 'Sales Channel']).size().reset_index()
result['Quantidade'] = result[0]
print(result)
result = result.pivot(index='MesAnoPedido', columns='Sales Channel', values='Quantidade')
print(result)

'''
customers_df = pd.read_csv('customers.csv')
sales_df = pd.read_csv('sales.csv')
products_df = pd.read_csv('products.csv')

sales_df['OrderDate'] = pd.to_datetime(sales_df['OrderDate'], format='%d/%m/%y')

# def agrupar_por_canal_vendas(agrupado_por_mes):
#     return agrupado_por_mes.groupby('Sales Channel').size()

result = sales_df.set_index('OrderDate').resample('M')\
    .apply(lambda agrupado_por_mes: agrupado_por_mes.groupby('Sales Channel').size())\
    .reset_index()
result['Online>InStore'] = result['Online'] > result['In-Store']
print(result)

'''



