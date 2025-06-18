import os
import pandas as pd


def list_datafiles_from_dir(datadir):
    return os.listdir(datadir)

def get_data_from_inspection_results(filename):
    with  open(file=filename,mode="r", encoding='utf-8') as fili:
        data = fili.readlines()
        return data
    
def process_data_from_inspection_results(data):
    data_dict = {}
    for line in data[1:]:
        for k in ['","', ',"']:   #"','",
            if k in line:
                line = line.replace(k,";")
        for k in [',']:   #"','",
            if k in line:
                line = line.replace(k,"")

        try:
            aux = line.split(";")
            for i in range(0, len(aux)):
                for j in ['\n','\t', "'", '"', "\n       "]:
                    aux[i] = aux[i].replace(j,"")
            #print(aux)
            if len(aux)> 0:
                data_dict[aux[0]] = aux[1:]
        except:
            print("Passed line: ")
            print(line)
            print("\n")
    return data_dict

def get_table_from_excel(excelfile):
        tables_list = []
        # Define the ranges to check
        ranges = [
            ('B:O', 0, 7),   # range B1:O3 para sheet 1
            ('B:EA', 0, 10),   # range B1:EA5 para sheet 2
            ]
        
        xls = pd.ExcelFile(excelfile, engine='openpyxl')
        nstrings = 0
        for i in range(0, len(xls.sheet_names)):
            sheet_name = xls.sheet_names[i]  # Using the first sheet name
            print(sheet_name)
            tupla =  ranges[i]
            col_range = tupla[0]
            skip_rows = tupla[1]
            if nstrings > 0:
                n_rows = nstrings * 2 + 1
            else:
                n_rows = tupla[2]  
            temp_df = pd.read_excel(excelfile, sheet_name=sheet_name, usecols=col_range, skiprows=skip_rows, nrows=n_rows, engine='openpyxl')
            if "Version number" in temp_df.columns:
                temp_df.drop(columns=["Version number"], inplace=True)
                nstrings = temp_df["String"].count()
                print(nstrings)

            if 'Data Details' in temp_df.columns:
                temp_df.drop(columns=['Data Details'], inplace=True)
                temp_df = temp_df.T.iloc[1:]
                temp_df = temp_df.iloc[::-1]
                #temp_df.rename(columns={ 0:"PV1-C", 1:"PV1-V", 2:"PV2-C", 3:"PV2-V",}, inplace=True)
                
                dick = {}
                count = 1
                for i in range(1, len(temp_df.columns)+ 1,2):
                    #print(i)
                    #print(temp_df.columns)
                    dick[i-1] = "PV" + str(count) + "-C" 
                    dick[i]  = "PV" + str(count) + "-V"
                    count = count + 1 
                temp_df.rename(columns=dick, inplace=True)
                

                print(temp_df.columns)   
            if not temp_df.empty:
                    tables_list.append(temp_df)

        #print(len(tables_list))
        return tables_list


