#!/bin/python -B

from sre_compile import isstring
import xlrd

def sum_str(x, ch = ''):
    res = ""
    for it in x:
        res = res + (ch if res != "" else "") + it
    return res

# Ficheiro de base de dados
loc = ("Base_de_dados_DiD.xls")

# Abrir bloco e folha folha
ws = xlrd.open_workbook(loc)
st = ws.sheet_by_index(0)

data_list = st.col_values(0)
data_list.pop(0)
popl = st.col_values(12)
popl.pop(0)
area = st.col_values(13)
area.pop(0)

for i in range(1, 12):
    c = '      '
    col = st.col_values(i)
    name = col.pop(0).replace(" ", "_")

    data = {}
    areas = []
    
    for n,val,pp,a in zip(data_list, col, popl,area):
        if n[0:3] != c[0:3]:
            c = sum_str(n.split(" ")[0:-1], " ")
            data[c] = []
            data[c + " (pop)"] = []
            areas.append(float(a.split(" ")[0].replace(',','.')))
        data[c].append(val)
        data[c + " (pop)"].append(pp)

    data1 = data.pop("Salvador")
    data2 = data.pop("Santa Maria")
    data_aux = []
    for el1, el2 in zip(data1, data2):
        data_aux.append(el1+el2)
    data1 = data.pop("União das Freguesias de Serpa (Salvador e Santa Maria)  de 30/9 a 31/12 de")
    data1[0] = data1[0] + data_aux[-1]*((365.0 - 92-0)/365.0)
    data_aux = data_aux + data1
    data["União das Freguesias de Serpa (Salvador e Santa Maria)"] = data_aux

    data1 = data.pop("Salvador (pop)")
    data2 = data.pop("Santa Maria (pop)")
    data_aux = []
    for el1, el2 in zip(data1, data2):
        data_aux.append(el1+el2)
    data_aux[-1] = data_aux[-1]/2
    data1 = data.pop("União das Freguesias de Serpa (Salvador e Santa Maria)  de 30/9 a 31/12 de (pop)")
    data_aux = data_aux + data1
    data["União das Freguesias de Serpa (Salvador e Santa Maria) (pop)"] = data_aux

    data1 = data.pop("Vale de Vargo")
    data2 = data.pop("Vila Nova de São Bento")
    data_aux = []
    for el1, el2 in zip(data1, data2):
        data_aux.append(el1+el2)
    data1 = data.pop("União das Freguesias de Vila Nova de São Bento e Vale de Vargo")
    data_aux[-1] = data_aux[-1]*(365.0/(365.0 - 92-0))
    data_aux = data_aux + data1
    data["União das Freguesias de Vila Nova de São Bento e Vale de Vargo"] = data_aux

    data1 = data.pop("Vale de Vargo (pop)")
    data2 = data.pop("Vila Nova de São Bento (pop)")
    data_aux = []
    for el1, el2 in zip(data1, data2):
        data_aux.append(el1+el2)
    data_aux[-1] = data_aux[-1]/2
    data_aux[-2] = data_aux[-2]/2
    data1 = data.pop("União das Freguesias de Vila Nova de São Bento e Vale de Vargo (pop)")
    data_aux = data_aux + data1
    data["União das Freguesias de Vila Nova de São Bento e Vale de Vargo (pop)"] = data_aux
    
    for i in reversed([2,3,5,6]):
        areas.pop(i)
    areas2 = []
    for a in areas:
        areas2.append(a)
        areas2.append(a)

    #for key in data:
    #    print(key + ":" + str(data[key]))
    #input()

    with open("csv/" + name + ".csv", "w") as fp:
        for i in range(2007, 2022):
            fp.write(str(i))
            if i != 2021:
                fp.write(",")
        for key,a in zip(data,areas2):
            if key[-5:] == "(pop)":
                continue
            fp.write("\n" + key + "\n")
            fp.write(("1," if key[0] == "U" else "0,") + str(a) + "\n")
            for el in data[key + " (pop)"]:
                fp.write(str(int(el)))
                fp.write("\n" if el == data[key + " (pop)"][-1] else ",")
            for el in data[key]:
                fp.write(str(round(el,2)))
                fp.write("" if el == data[key][-1] else ",")

