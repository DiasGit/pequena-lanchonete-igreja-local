import streamlit as st
import pandas as pd

def calcular_lucros(df):
    df['lucro_do_produto'] = (df['total_de_vendas'] * df['preco_de_venda'] * (1 - df['desconto'] / 100)) - (df['total_de_vendas'] * df['custo_de_producao'])
    lucro_total_por_produto = df.groupby('nome_do_produto')['lucro_do_produto'].sum().reset_index()
    lucro_total_de_vendas = df['lucro_do_produto'].sum()
    return lucro_total_por_produto, lucro_total_de_vendas

st.title("Projeto Vendinha da Igreja")

if 'dados_de_vendas' not in st.session_state:
    st.session_state.dados_de_vendas = pd.DataFrame(columns=['nome_do_produto', 'total_de_vendas', 'custo_de_producao', 'preco_de_venda', 'desconto'])

with st.form("entrada_de_dados"):
    nome_do_produto = st.text_input("Insira o nome do produto vendido")
    total_de_vendas = st.number_input("Total de Vendas", min_value=0)
    custo_de_producao = st.number_input("Custo de Produção", min_value=0.0, format="%.2f")
    preco_de_venda = st.number_input("Preço de Venda", min_value=0.0, format="%.2f")
    desconto = st.number_input("Desconto (%)", min_value=0.0, format="%.2f")

    submitted = st.form_submit_button("Adicionar produto")

    if submitted:
        if nome_do_produto and total_de_vendas > 0 and custo_de_producao >= 0 and preco_de_venda >= 0:
            novo_dado = pd.DataFrame({
                'nome_do_produto': [nome_do_produto],
                'total_de_vendas': [total_de_vendas],
                'custo_de_producao': [custo_de_producao],
                'preco_de_venda': [preco_de_venda],
                'desconto': [desconto]
            })
            if not novo_dado.empty:
                st.session_state.dados_de_vendas = pd.concat([st.session_state.dados_de_vendas, novo_dado], ignore_index=True)
                st.success("Produto adicionado com sucesso!")
        else:
            st.warning("Por favor, preencha todos os campos corretamente.")

st.subheader("Produtos adicionados")
st.dataframe(st.session_state.dados_de_vendas)

if not st.session_state.dados_de_vendas.empty:
    produto_a_remover = st.selectbox("Remover produto:", st.session_state.dados_de_vendas['nome_do_produto'].tolist())
    if st.button("Remover"):
        st.session_state.dados_de_vendas = st.session_state.dados_de_vendas[st.session_state.dados_de_vendas['nome_do_produto'] != produto_a_remover]
        st.success(f"Produto '{produto_a_remover}' removido com sucesso!")

st.subheader("Produtos adicionados atualizados")
st.dataframe(st.session_state.dados_de_vendas)

if not st.session_state.dados_de_vendas.empty:
    lucro_total_por_produto, lucro_total_de_vendas = calcular_lucros(st.session_state.dados_de_vendas)

    st.subheader("Lucro por produto")
    st.dataframe(lucro_total_por_produto)

    st.subheader("Lucro Total de Vendas")
    st.write(lucro_total_de_vendas)
