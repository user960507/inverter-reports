from reportlab.pdfgen import canvas

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

from reportlab.platypus import PageTemplate, Frame, BaseDocTemplate
from reportlab.platypus import NextPageTemplate, PageBreak, Paragraph, Table, Image

import io
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("darkgrid")
styles = getSampleStyleSheet()


padding = dict(  leftPadding=45,   rightPadding=36,  topPadding=36,  bottomPadding=27)
portrait_frame = Frame(0, 0, *A4, **padding)
landscape_frame = Frame(0, 0, *landscape(A4), **padding)

def on_page(canvas, doc, pagesize=A4):
    page_num = canvas.getPageNumber()
    canvas.drawCentredString(pagesize[0]/2, 50, str(page_num))
    #canvas.drawImage('https://cpng.pikpng.com/pngl/s/203-2033353_huawei-black-logo-huawei-clipart.png', 0, 0)

def on_page_landscape(canvas, doc):
  return on_page(canvas, doc, pagesize=landscape(A4))


portrait_template = PageTemplate(  id='portrait',   frames=portrait_frame,  onPage=on_page,   pagesize=A4)
landscape_template = PageTemplate(  id='landscape',   frames=landscape_frame,   onPage=on_page_landscape,   pagesize=landscape(A4))



class Reporte:
    __story = []

    def __init__(self,datos, base_dir, kind):
        self.datadict = datos
        self.report_type = kind
        if self.report_type == "inspect":
            self.filename = base_dir + "/"  + datos['Device SN'][0] +".pdf"
            self.pdfobject = BaseDocTemplate(  self.filename ,  pageTemplates=[    portrait_template,    landscape_template  ])
            self.rep_inspect()
        else:
            self.filename = base_dir + "/"  + datos[0]['Inverter SN'][0] +"_string.pdf"
            self.pdfobject = BaseDocTemplate(  self.filename ,  pageTemplates=[   landscape_template  ])
            self.rep_string()

    def rep_inspect(self):
        w, h = A4
        self.header()
        self.body_main()
        #self.body_sec()
        self.strings_report()
        self.pdfobject.build(self.__story)
    
    def rep_string(self):
        self.strings_report_detail()
        self.pdfobject.build(self.__story)        

    def header(self):
        self.__story.append(Paragraph('ANÁLISIS DE ESTADO DE INVERSOR:    ', styles['Heading1']))
        self.__story.append(Paragraph('Tipo de dispositivo:    ' + self.datadict['Device type'][0]))
        self.__story.append(Paragraph('Número de serie del dispositivo:    ' + self.datadict['Device SN'][0]))
        self.__story.append(Paragraph('Alias del dispositivo:  ' + self.datadict['Device alias'][0]))
        self.__story.append(Paragraph('Fecha y hora de la prueba:  ' + self.datadict['Test time'][0]))
        self.__story.append(Paragraph('Capacidad nominal del inversor (kW):    ' + self.datadict['Rated inverter capacity (kW)'][0]))
        self.__story.append(Paragraph('Modo de salida:    ' + self.datadict['Output mode'][0]))
        self.__story.append(Paragraph('Código de la red eléctrica actual:    ' + self.datadict['Current grid code'][0]))
        
    def body_main(self):
        self.__story.append(Paragraph('RESULTADOS INSPECCIÓN:    ', styles['Heading2']))

        self.__story.append(Paragraph('Producción energética total (kWh):    ' + self.datadict['Total energy yield (kWh)'][0]))
        self.__story.append(Paragraph('Estado del capacitor del bus:    ' + self.datadict['Bus capacitor status'][0]))
        self.__story.append(Paragraph('Capacitancia de bus positiva (micro-F):    ' + self.datadict['Positive bus capacitance (microF)'][0]))
        self.__story.append(Paragraph('Capacitancia de bus negativa (micro-F):    ' + self.datadict['Negative bus capacitance (microF)'][0]))
        self.__story.append(Paragraph('Impedancia de CC de la red (Ohm):    ' + self.datadict['Grid DC impedance (Ohm)'][0]))
        self.__story.append(Paragraph('Impedancia de CA de la red (Ohm):    ' + self.datadict['Grid AC impedance (Ohm)'][0]))


        stringaux1 = 'Resistencia de aislamiento más baja (MOhm):    ' + self.datadict['Lowest insulation resistance (MOhm)'][0] + ' Fecha:    ' + self.datadict['Lowest insulation resistance occurrence time'][0] 
        self.__story.append(Paragraph(stringaux1))
        stringaux2 = 'Capacitancia parasítica más alta (micro-F):    ' + self.datadict['Highest parasitic capacitance (microF)'][0] + ' Fecha:    ' + self.datadict['Highest parasitic capacitance occurrence time'][0] 
        self.__story.append(Paragraph(stringaux2))
        stringaux2 = 'Capacitancia parasítica más baja (micro-F):    ' + self.datadict['Lowest parasitic capacitance (microF)'][0] +  ' Fecha:    ' + self.datadict['Lowest parasitic capacitance occurrence time'][0] 
        self.__story.append(Paragraph(stringaux2))
        stringaux3 = 'Voltaje de fase más alto de la red (V):    ' + self.datadict['Highest phase voltage of the grid (V)'][0] +  ' Fecha:    ' + self.datadict['Highest grid phase voltage occurrence time'][0] 
        self.__story.append(Paragraph(stringaux3))
        stringaux4 = 'Voltaje de fase más bajo de la red (V):    ' + self.datadict['Lowest phase voltage of the grid (V)'][0] +  ' Fecha:    ' + self.datadict['Lowest grid phase voltage occurrence time'][0] 
        self.__story.append(Paragraph(stringaux4))
        stringaux5 = 'Voltaje de línea más alto de la red (V):    ' + self.datadict['Highest line voltage of the grid (V)'][0] +  ' Fecha:    ' + self.datadict['Highest grid line voltage occurrence time'][0] 
        self.__story.append(Paragraph(stringaux5))
        stringaux6 = 'Voltaje de línea más bajo de la red (V):    ' + self.datadict['Lowest line voltage of the grid (V)'][0] +  ' Fecha:    ' + self.datadict['Lowest grid line voltage occurrence time'][0] 
        self.__story.append(Paragraph(stringaux6))
        stringaux7 = 'Frecuencia más alta de la red (Hz):    ' + self.datadict['Highest grid frequency (Hz)'][0] +  ' Fecha:    ' + self.datadict['Highest grid frequency occurrence time'][0] 
        self.__story.append(Paragraph(stringaux7))
        stringaux8 = 'Frecuencia más baja de la red (Hz):    ' + self.datadict['Lowest grid frequency (Hz)'][0] +  ' Fecha:    ' + self.datadict['Lowest grid frequency occurrence time'][0] 
        self.__story.append(Paragraph(stringaux8))
        stringaux9 = 'Armónico de voltaje más alto (%):    ' + self.datadict['Highest voltage harmonic (%)'][0] +  ' Fecha:    ' + self.datadict['Highest voltage harmonic occurrence time'][0] 
        self.__story.append(Paragraph(stringaux9))

    def body_sec(self):
        self.__story.append(Paragraph('Operación:    ', styles['Heading2']))
        self.__story.append(Paragraph('Tiempo de ejecución del ventilador (hora):    ' + self.datadict['Fan runtime (hour)'][0]))
        self.__story.append(Paragraph('Tiempo de funcionamiento total con conexión a la red eléctrica (h):    ' + self.datadict['Total on-grid runtime (hour)'][0]))
        self.__story.append(Paragraph('Tiempo de inactividad inesperada total (h):    ' + self.datadict['Total unexpected downtime (hour)'][0]))
        self.__story.append(Paragraph('Tiempo total en modo de espera (h):    ' + self.datadict['Total standby duration (hour)'][0]))
        self.__story.append(Paragraph('Tiempo total de inactividad inesperada de la red (hora):    ' + self.datadict['Total unexpected grid downtime (hour)'][0]))
        self.__story.append(Paragraph('Tiempo total de inactividad planificada (hora):    ' + self.datadict['Total planned downtime (hour)'][0]))
        self.__story.append(Paragraph('Duración total de entrada de CC (hora):    ' + self.datadict['Total DC input duration (hour)'][0]))
        self.__story.append(Paragraph('Tiempo de ejecución limitado por la potencia (hora):    ' + self.datadict['Power-limited runtime (hour)'][0]))

    def strings_report(self):
        aqui, nombres = self.get_data_string_index()
        cant = int(self.datadict['Quantity of PV strings'][0])
        self.__story.append(Paragraph('ESTADO STRINGS:    ', styles['Heading2']))
        self.__story.append(Paragraph('Cantidad de cadenas FV:    ' + self.datadict['Quantity of PV strings'][0]))
        self.__story.append(Paragraph('Error de corriente durante el barrido:    ' + self.datadict['Current error during scanning'][0]))
        #self.__story.append(Paragraph('String ,Factor de carga,  Producción energética total (kWh),  Indicador de estado,  Indicador de validez de curva'))
        
        
        auxDic = {"String":[],"Factor de carga":[],"Producción energética total (kWh)":[],"Indicador de estado":[],"Indicador de validez de curva":[],}
        for nombre in nombres:
            for id in range(1,cant+1):
                if ("String" and str(id) )  in nombre:
                    #auxDic = {}
                    if len(nombre) < 10:
                      #auxDic["id"].append(id)
                      auxDic["String"].append(nombre)
                      auxDic["Factor de carga"].append(self.datadict[nombre][0])
                      auxDic["Producción energética total (kWh)"].append(self.datadict[nombre][1])
                      auxDic["Indicador de estado"].append(self.datadict[nombre][2])
                      auxDic["Indicador de validez de curva"].append(self.datadict[nombre][3])
                      #stringui = nombre+ ": " + "\t" + self.datadict[nombre][0] + "\t" + self.datadict[nombre][1] + "\t" + self.datadict[nombre][2] + "\t" + self.datadict[nombre][3] 
                      #df = pd.DataFrame.from_dict(auxDic)
                      #self.__story.append(self.df2table(df))

        #columns=['String ,Factor de carga,  Producción energética total (kWh),  Indicador de estado,  Indicador de validez de curva']
        df = pd.DataFrame.from_dict(auxDic)
        self.__story.append(self.df2table(df))
        self.__story.append(NextPageTemplate('landscape'))

        auxDic2 = {}
        for nombre in nombres:
            for id in range(1,cant+1):
                if ("PV" and str(id) )  in nombre:
                    #auxDic = {}
                    if len(nombre) > 10 and len(nombre) < 20  :
                      auxDic2[nombre] = self.datadict[nombre]
        df2 = pd.DataFrame.from_dict(auxDic2)
        for col in df2.columns:
            df2.loc[df2[col] == "null", col] = 0
            df2[col] = df2[col].astype(float)
            #print(df2[col])
            
        #print(df2.describe())
        line_fig, ax = plt.subplots(dpi=300, figsize=(9, 7))
        legends = []
        for i in range(1,len(df2.columns) +1, 2):
            sns.lineplot(data=df2, x=df2.columns[i-1],y= df2.columns[i], ax=ax, legend='brief', label=str(df2.columns[i][11:15]))
            #legends.append(str())
            #a.set_label = "aaaaaa"
        #plt.tight_layout()
        plt.xlabel("Voltaje (V)")
        plt.ylabel("Corriente (A)")
        plt.title("CURVA IV STRINGS")
        #
        ax.legend(title="String", loc='best')
        #plt.show()
        #for key in auxDic2.keys():
        #    print(key, ": ", len(auxDic2[key]))
        self.__story.append(self.fig2image(line_fig))

    def get_data_string_index(self):
        lista = list(self.datadict.keys())
        inde = lista.index('Current error during scanning')
        #print(lista[inde:])
        return inde, lista[inde:]
    
    def df2table(self, df):
      return Table(
        [[Paragraph(col) for col in df.columns]] + df.values.tolist(), 
        style=[
          ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
          ('LINEBELOW',(0,0), (-1,0), 1, colors.black),
          ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
          ('BOX', (0,0), (-1,-1), 1, colors.black),
          ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.lightgrey, colors.white])],
        hAlign = 'LEFT')
    
    def fig2image(self, f):
        buf = io.BytesIO()
        f.savefig(buf, format='png', dpi=300)
        buf.seek(0)
        x, y = f.get_size_inches()
        return Image(buf, x * inch, y * inch)

    def strings_report_detail(self):
        
        self.__story.append(Paragraph('ANÁLISIS DE CURVA I-V DETALLADO:    ', styles['Heading1']))
        self.__story.append(self.df2table(self.datadict[0]))
        

        df2 = self.datadict[1]
        line_fig, ax = plt.subplots(dpi=300, figsize=(9, 7))
        legends = []
        for i in range(1,len(df2.columns) +1, 2):
            sns.lineplot(data=df2, x=df2.columns[i],y= df2.columns[i-1], ax=ax, legend='brief', label=str(df2.columns[i-1]))
            #legends.append(str())
            #a.set_label = "aaaaaa"
        #plt.tight_layout()
        plt.xlabel("Voltaje (V)")
        plt.ylabel("Corriente (A)")
        plt.title("CURVA IV STRINGS")
        #
        ax.legend(title="String", loc='best')
        #plt.show()
        #for key in auxDic2.keys():
        #    print(key, ": ", len(auxDic2[key]))
        self.__story.append(self.fig2image(line_fig))