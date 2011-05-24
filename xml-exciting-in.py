from veusz.plugins import *
import lxml.etree as etree
import numpy as np
import veusz.embed as veusz
import os

class ImportPluginExample(ImportPlugin):
 
    name = "exciting/XML"
    author = "tde"
    description = "Reads Exciting specific xml files and general XPath expressions."
 
    def __init__(self):
        ImportPlugin.__init__(self)
        self.fields = [
            ImportFieldCombo("type", items=("Bandstructure", "DOS","xPath","Convergence"), editable=False, default="Bandstructure"),
            ImportFieldText("name", descr="Dataset name", default="name"),
            ImportFieldText("xPath", descr="xPath", default="xPath expression"),
            ImportFieldCheck("character", descr="Character of Bandstructure")
            ]


    def doImport(self, params):
        """Actually import data
        params is a ImportPluginParams object.
        Return a list of ImportDataset1D, ImportDataset2D objects
        """
        f = params.openFileWithEncoding()
        tree = etree.parse(f)
        data = []
        datasets = []
        

        if params.field_results["type"] == "Bandstructure":
            nbands = tree.xpath("count(//band)")
            xdata = tree.xpath("//band[1]/point/@distance")
            datasets.append(ImportDataset1D("x", xdata))
            for i in range(nbands):
                i+=1
                ydata = tree.xpath("//band[%i]/point/@eval"%i)
                datasets.append(ImportDataset1D("band%i"%i, ydata))
            datasets.append(ImportDatasetText("labels", tree.xpath("//vertex/@label")))
            datasets.append(ImportDataset1D("labels_distance", tree.xpath("//vertex/@distance")))

            if params.field_results["character"]:
                char0_scaled=[]
                char1_scaled=[]
                char2_scaled=[]
                char3_scaled=[]
                
                char0 = tree.xpath("//band/point/bc[@l='0']/@character")
                for e in char0:
                    if float(e) == 0. or float(e) < 10**(-26): e="1.0E-26"
                    char0_scaled.append(float(e)*1.)
                datasets.append(ImportDataset1D("char_l0", char0_scaled))
                
                char1 = tree.xpath("//band/point/bc[@l='1']/@character")
                for e in char1:
                    if float(e) == 0. or float(e) < 10**(-26): e="1.0E-26"
                    char1_scaled.append(float(e)*1.)
                datasets.append(ImportDataset1D("char_l1", char1_scaled))
                
                char2 = tree.xpath("//band/point/bc[@l='2']/@character")
                for e in char2:
                    if float(e) == 0. or float(e) < 10**(-26): e="1.0E-26"
                    char2_scaled.append(float(e)*1.)
                datasets.append(ImportDataset1D("char_l2", char2_scaled))
                
                char3 = tree.xpath("//band/point/bc[@l='3']/@character")
                for e in char3:
                    if float(e) == 0. or float(e) < 10**(-26): e="1.0E-26"
                    char3_scaled.append(float(e)*1.)
                datasets.append(ImportDataset1D("char_l3", char3_scaled))
                
                energy = tree.xpath("//band/point/@eval")
                datasets.append(ImportDataset1D("energy", energy))
                xchar = tree.xpath("//band/point/@distance")
                datasets.append(ImportDataset1D("xchar", xchar))
                
        elif params.field_results["type"] == "xPath":
            
            xpath = str(params.field_results["xPath"])
            data = tree.xpath(xpath)
            datasets.append(ImportDataset1D(params.field_results["name"], data))
        elif params.field_results["type"] == "DOS":
            natom = tree.xpath("count(//partialdos)")
            ndiag = tree.xpath("count(//partialdos/diagram)")
            xdata = tree.xpath("//totaldos/diagram[1]/point/@e")
            datasets.append(ImportDataset1D("edos", xdata))
            totaldos = tree.xpath("//totaldos/diagram[1]/point/@dos")
            datasets.append(ImportDataset1D("totaldos", totaldos))
            for i in range(natom):
                i+=1
                for j in range(ndiag):
                    j+=1
                    n = tree.xpath("//partialdos[%(i)s]/diagram[%(j)s]/@nspin"%{'i':i,'j':j})
                    l = tree.xpath("//partialdos[%(i)s]/diagram[%(j)s]/@l"%{'i':i,'j':j})
                    m = tree.xpath("//partialdos[%(i)s]/diagram[%(j)s]/@m"%{'i':i,'j':j})
                    ydata = tree.xpath("//partialdos[%(i)s]/diagram[%(j)s]/point/@dos"%{'i':i,'j':j})
                    datasets.append(ImportDataset1D("dos_atom%(i)s_n%(n)s_l%(l)s_m%(m)s"%{'i':i,'n':n,'l':l,'m':m}, ydata))
        elif params.field_results["type"] == "Convergence":
            pars = ['rgkmax','ngridk','swidth']
            for par in pars:
                valstack = []
                energy = tree.xpath("//conv[@par='%s']/@energy"%par)
                
                B = tree.xpath("//conv[@par='%s']/@B"%par)
                V = tree.xpath("//conv[@par='%s']/@V"%par)
                val = tree.xpath("//conv[@par='%s']/@parval"%par)
                
                i=0
                for vlues in val:
                    if len(eval(vlues)[par]) > 1:
                        valstack.append(float(str(eval(vlues)[par][i]).rstrip()))
                        if i<3: i+=1
                        else: i=0
                    else:
                        valstack.append(float(str(eval(vlues)[par][0]).rstrip()))
                     
                datasets.append(ImportDataset1D("%s_B"%par,B))
                datasets.append(ImportDataset1D("%s_V"%par,V))
                datasets.append(ImportDataset1D("%s_energy"%par,energy))
                datasets.append(ImportDataset1D(par,valstack))
            

 
        return datasets
 
importpluginregistry.append(ImportPluginExample())