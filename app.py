import streamlit as st
import openpyxl
import pandas as pd
from profiling_class import Profiling
import datetime
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import streamlit.components.v1 as components
import altair as alt

def apply_function(df, selected_weights):
    """
    Applies a series of transformations to the input DataFrame.

    Parameters:
    df (pandas.DataFrame): The input DataFrame.

    Returns:
    pandas.DataFrame: The transformed DataFrame.
    """
    df['colab'] = df['colab'].fillna(-1).astype(int)
    df['lawsuit'] = df['lawsuit'].fillna(-1).astype(int)
    df['revenue'] = df['revenue'].fillna(-1).astype(float)

    profiles = df.apply(lambda x: pd.Series(Profiling(x, selected_weights).create_profile()), axis=1)
    df = pd.concat([
        df, profiles
    ], axis=1)

    return df

def to_excel(df):
    """
    Converts a pandas DataFrame to an Excel file.

    Args:
        df (pandas.DataFrame): The DataFrame to be converted.

    Returns:
        bytes: The processed data in the form of bytes.

    """
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.close()
    processed_data = output.getvalue()
    return processed_data

def bar_chart_perfilamento_colunas(df):
    revenue_count = df['Revenue profile'].value_counts().reset_index().rename(columns={'Revenue profile': 'Perfil', 'count': 'contagem'})
    revenue_count['Métrica'] = 'Receita'
    colab_count = df['Colab profile'].value_counts().reset_index().rename(columns={'Colab profile': 'Perfil', 'count': 'contagem'})
    colab_count['Métrica'] = 'Colaboradores'
    lawsuit_count = df['Lawsuit profile'].value_counts().reset_index().rename(columns={'Lawsuit profile': 'Perfil', 'count': 'contagem'})
    lawsuit_count['Métrica'] = 'Processos'
    
    
    chart = alt.Chart(
        pd.concat([revenue_count, colab_count, lawsuit_count])
    ).mark_bar(opacity=0.6,
        stroke='black',
        strokeWidth=1,
        strokeOpacity=1,
        color = 'grey'
    ).encode(
        y = alt.Y('Perfil').sort(
            ['Sem perfil', 'Mosca', 'Pena', 'Médio', 'Pesado']
        ),

        x = 'contagem',

        column = alt.Column('Métrica').header(labelFontSize = 20, labelFontStyle = 'bold').title(None),

        tooltip = 'contagem'
    ).properties(
        width=250,
        height=300
    ).configure(
        background = 'white'
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        domain=False
    )  

    return components.html(
        chart.to_html(),
        height = 400,
        width = 1000,
    )

def bar_chart_perfilamento_comparativo(df):
    # Count the amount of "Nova" and "Final" values
    nova_count = df['Nova'].value_counts().reset_index().rename(columns={'Nova': 'Perfil', 'count': 'contagem'})
    nova_count['Métrica'] = 'Por peso'

    final_count = df['Final'].value_counts().reset_index().rename(columns={'Final': 'Perfil', 'count': 'contagem'})
    final_count['Métrica'] = 'Por critério de perfilamento'

    # Create the bar chart
    chart = alt.Chart(
        pd.concat([nova_count,final_count])
    ).mark_bar(
        opacity=0.6,
        stroke='black',
        strokeWidth=1,
        strokeOpacity=1,
    ).encode(
        y=alt.Y(
            'Métrica'
        ).title(None).axis(
            labelFontSize = 12, labelFontStyle = 'bold'),

        x=alt.X(
            'contagem'
        ).axis(
            title='Contagem', labelFontSize = 12, labelFontStyle = 'bold'
        ),

        color = alt.Color('Métrica'),

        row = alt.Row(
            'Perfil'
        ).sort(
            ['Sem perfil', 'Mosca', 'Pena', 'Médio', 'Pesado']
        ).header(
            alt.Header(labelAngle=0, labelFontSize = 20, labelFontStyle = 'bold', labelAlign = 'left')
        ).title(None),

        tooltip = 'contagem'

    ).properties(
        width=400,
        height=80
    ).configure(
        background = 'white'
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        domain=False
    )   

    # Display the chart
    return components.html(
        chart.to_html(),
        height = 600,
        width = 900,
    )

def main():
    """
    Main function for the application.
    """
    # Set the title and description
    st.title("Perfilamento de escritórios de advocacia")
    st.write("Faça o upload da planilha e selecione a tabela que deseja perfilar.")
    st.write("A planilha deve estar no formato .xlsx")

    uploaded_file = st.file_uploader("Upload da tabela.", type=['xlsx'])  

    if uploaded_file:
        # Read the uploaded file into a DataFrame
        file_details = {
            "Filename": uploaded_file.name,
            "FileType": uploaded_file.type,
            "FileSize": uploaded_file.size
        }

        wb = openpyxl.load_workbook(uploaded_file)

        ## Show Excel file details
        st.subheader("Detalhes da planilha:")
        st.json(file_details, expanded=False)
        st.markdown("----")

        ## Select sheet
        sheet_selector = st.selectbox("Selecione a tabela:", wb.sheetnames)     
        df = pd.read_excel(uploaded_file, sheet_selector)
        st.markdown(f"### Tabela selecionada: `{sheet_selector}`")
        st.write(df)

        selected_columns = []
        selected_weights = {'lawsuit': 1, 'colab': 1, 'revenue': 1}

        st.markdown("### Selecione as colunas e os pesos para o perfilamento")
        st.markdown("Peso 0 significa que a coluna não será considerada no perfilamento, mas ao menos uma coluna deve ter peso maior que zero")
        st.markdown("#### Número de processos")
        selected_columns.append(
            st.selectbox("Selecione a coluna que corresponde ao número de processos", df.columns)
        )
        selected_weights['lawsuit'] = st.slider("Selecione o peso para o número de processos", 0, 3, 0, 1)

        st.markdown("#### Número de colaboradores")
        selected_columns.append(
            st.selectbox("Selecione a coluna que corresponde ao número de colaboradores", df.columns)
        )
        selected_weights['colab'] = st.slider("Selecione o peso para o número de colaboradores", 0, 3, 0, 1)

        st.markdown("#### Receita de 12 meses")
        selected_columns.append(
            st.selectbox("Selecione a coluna que corresponde a receita de 12 meses", df.columns)
        )
        selected_weights['revenue'] = st.slider("Selecione o peso para a receita de 12 meses", 0, 3, 0, 1)
        
        if sum(selected_weights.values()) == 0:
            st.markdown("##### Selecione ao menos um peso diferente de zero.")

        if len(selected_columns) < 3:
            st.markdown("##### Selecione as três colunas para perfilamento")

        if (len(selected_columns) == 3) and (sum(selected_weights.values()) > 0):
            # Rename the selected columns
            df_aux = df[selected_columns].rename(
                columns={
                    selected_columns[0]: "lawsuit", 
                    selected_columns[1]: "colab", 
                    selected_columns[2]: "revenue"
                }
            )
            
            # Apply function
            df_aux = apply_function(df_aux, selected_weights)

            df = pd.concat([
                df, 
                df_aux.drop(columns=['lawsuit', 'colab', 'revenue'])
            ], axis=1)

            st.markdown('# Resultados do perfilamento')
            
            st.markdown('### Perfilamento de cada coluna')
            bar_chart_perfilamento_colunas(df)  

            st.markdown('### Comparação entre perfilamento por peso e por critério de perfilamento')
            bar_chart_perfilamento_comparativo(df)            

            # Rename the columns back to their original names

            st.markdown('# Tabela perfilada')
            st.write(df_aux)

            # Download the modified DataFrame as an Excel file
            # Generate a timestamp for the file name
            df_xlsx = to_excel(df)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            st.download_button("Download da tabela perfilada", data=df_xlsx, file_name=f"tabela_perfilada_{timestamp}.xlsx")

if __name__ == "__main__":
    main()