from processingUtils import list_datafiles_from_dir, get_data_from_inspection_results, process_data_from_inspection_results, get_table_from_excel
from reportUtils import Reporte

data_dir = "./data_inspect"
strg_dir = "./data_strings"
repr_dir = "./reportes"

if __name__ == "__main__":
    files = list_datafiles_from_dir(datadir=data_dir)
    for datos in files:
        basefile = data_dir + "/" + datos
        processed = process_data_from_inspection_results(get_data_from_inspection_results(basefile))
        
        #for key in processed.keys():
        #    print(key)
        #    print(processed[key])
        #    print()
        rep = Reporte(processed, repr_dir, "inspect")
        
        
    files_excel = list_datafiles_from_dir(datadir=strg_dir)
    for datos in files_excel:
        basefile = strg_dir + "/" + datos
        processed = get_table_from_excel(basefile)
        print(processed)
        #df = processed[0]
        rep = Reporte(processed, repr_dir, "string")
        #import matplotlib.pyplot as plt
        #df.plot(x="PV1-V", y="PV1-C")
        #df.plot(x="PV2-V", y="PV2-C")
        #plt.show()

