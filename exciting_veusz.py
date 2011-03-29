from veusz.plugins import *
import lxml.etree as etree
import numpy as np
import veusz.embed as veusz

class ImportPluginExample(ImportPlugin):
 
    name = "exciting/XML"
    author = "tde"
    description = "Reads xml files"
 
    def __init__(self):
        ImportPlugin.__init__(self)
        self.fields = [
            ImportFieldCombo("type", items=("Bandstructure", "DOS","xPath"), editable=False, default="Bandstructure"),
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
                #if params.field_results["character"]:
                    
                #    char0 = tree.xpath("//band[%i]/point/bc[@l='0']/@character"%i)
                #    print char0
                ##    datasets.append(ImportDataset1D("char_l0_band%i"%i, char0))
                #    char1 = tree.xpath("//band[%i]/point/bc[@l='1']/@character"%i)
                #    datasets.append(ImportDataset1D("char_l1_band%i"%i, char1))
                #    char2 = tree.xpath("//band[%i]/point/bc[@l='2']/@character"%i)
                #    datasets.append(ImportDataset1D("char_l2_band%i"%i, char2))
                #    char3 = tree.xpath("//band[%i]/point/bc[@l='3']/@character"%i)
                #    datasets.append(ImportDataset1D("char_l3_band%i"%i, char3))
            if params.field_results["character"]:
                char0_scaled=[]
                char1_scaled=[]
                char2_scaled=[]
                char3_scaled=[]
                
                char0 = tree.xpath("//band/point/bc[@l='0']/@character")
                for e in char0:
                    char0_scaled.append(float(e)*1.)
                datasets.append(ImportDataset1D("char_l0", char0_scaled))
                char1 = tree.xpath("//band/point/bc[@l='1']/@character")
                for e in char1:
                    char1_scaled.append(float(e)*1.)
                datasets.append(ImportDataset1D("char_l1", char1_scaled))
                char2 = tree.xpath("//band/point/bc[@l='2']/@character")
                for e in char2:
                    char2_scaled.append(float(e)*1.)
                datasets.append(ImportDataset1D("char_l2", char2_scaled))
                char3 = tree.xpath("//band/point/bc[@l='3']/@character")
                for e in char3:
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
            ndiag = tree.xpath("count(//diagram)")
            xdata = tree.xpath("//totaldos/diagram[1]/point/@e")
            datasets.append(ImportDataset1D("xdos", xdata))
            for i in range(ndiag):
                i+=1
                ydata = tree.xpath("//totaldos/diagram[%i]/point/@dos"%i)
                datasets.append(ImportDataset1D("dos%i"%i, ydata))


 
        return datasets
 
importpluginregistry.append(ImportPluginExample())