import streamlit as st
import openpyxl
import pandas as pd
from profiling_class import Profiling
import datetime
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb

def apply_function(df):
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

    profiles = df.apply(lambda x: pd.Series(Profiling(x).create_profile()), axis=1)
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
        selected_columns.append(
            st.selectbox("Selecione a coluna que corresponde ao número de processos", df.columns)
        )
        
        selected_columns.append(
            st.selectbox("Select a coluna que corresponde ao número de colaboradores", df.columns)
        )
        
        selected_columns.append(
            st.selectbox("Selecione a coluna que corresponde a receita de 12 meses", df.columns)
        )

        if len(selected_columns) == 3:
            # Rename the selected columns
            df_aux = df[selected_columns].rename(
                columns={
                    selected_columns[0]: "lawsuit", 
                    selected_columns[1]: "colab", 
                    selected_columns[2]: "revenue"
                }
            )
            
            # Apply function
            df_aux = apply_function(df_aux)

            # Rename the columns back to their original names

            st.header('Tabela perfilada')
            st.write(df_aux)

            df = pd.concat([
                df, 
                df_aux.drop(columns=['lawsuit', 'colab', 'revenue'])
            ], axis=1)

            # Download the modified DataFrame as an Excel file
            # Generate a timestamp for the file name
            df_xlsx = to_excel(df)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            st.download_button("Download da tabela perfilada", data=df_xlsx, file_name=f"tabela_perfilada_{timestamp}.xlsx")

if __name__ == "__main__":
    main()