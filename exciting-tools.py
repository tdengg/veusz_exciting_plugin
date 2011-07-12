import veusz.plugins as plugins
import veusz.embed as enb
import time
import veusz.plugins.datasetplugin as dataplug
import numpy as np

class BandPlugin(plugins.ToolsPlugin):
    """Plot bandstructure and character"""

    # a tuple of strings building up menu to place plugin on
    menu = ('Bandstructure',)
    # unique name for plugin
    name = 'Bandstructure'

    # name to appear on status tool bar
    description_short = 'Bandstructure plot'
    # text to appear in dialog box
    description_full = 'Bandstructure plot'

    def __init__(self):
        """Make list of fields."""
        self.fields = [ 
            
#            plugins.FieldWidget("widget", descr="Start from widget",
#                                default="/"),
#            plugins.FieldMarker("markersearch", descr="Search for marker"),
#            plugins.FieldMarker("markerreplace", descr="Replace with marker"),
            plugins.FieldBool("character", descr="Plot character of bands")
            ]

    def apply(self, interface, fields):
        """Do the work of the plugin.
        interface: veusz command line interface object (exporting commands)
        fields: dict mapping field names to values
        """
        self.fields = fields
        def walkNodes(node, i, ch):
            """Walk nodes"""
            #if i <1:
            #    print node.name, node.type
            #    try:
            #        print node.settingtype
            #    except:
            #        print ''
            if node.type == 'setting' and node.settingtype == 'dataset-or-floatlist' and not ch:
                if node.name == 'xData':
                    node.val = 'x'
                elif node.name == 'yData':
                    node.val = self.datasets_band[i]
            elif node.type == 'setting' and node.settingtype == 'dataset-or-floatlist' and ch:
                if node.name == 'xData':
                    node.val = 'xchar'
                elif node.name == 'yData':
                    node.val = 'energy'
            #elif node.type == 'setting' and node.name == 'scalePoints' and ch:
            #    print 'done'
            #    node.val = self.datasets_char[i]
            else:
                for c in node.children:
                    walkNodes(c,i,ch)
        
        def walkNodes_2(node, i, ch):

            if node.type == 'setting' and node.name == 'scalePoints' and ch:
                print self.datasets_char[i]
                node.val = self.datasets_char[i]
            else:
                for c in node.children:
                    walkNodes_2(c,i,ch)
                    
        g = interface.Root.fromPath('/page1/graph1')
        #g.Add('xy', marker = 'none')
        
        self.datasets_band = []
        self.datasets_char = []
        self.datasets = interface.GetDatasets()
        for set in self.datasets:
            if set.startswith('band'):
                self.datasets_band.append(set)
            elif set.startswith('char'):
                self.datasets_char.append(set)
                 
        i=0
        for dataset in self.datasets_band:
            if dataset != 'x':
                g.Add('xy', name='band%i'%i, marker = 'none')
                for child in g.children:
                    if child.type == 'widget':
                        lastc = child
                lastc.PlotLine.width.val='1pt'    
                walkNodes(lastc,i,False)
            
            i=i+1
            
        i=0
        if fields['character']:
            for dataset in self.datasets_char:

                if dataset != 'x':
                    
                    g.Add('xy', name='char%i'%i)
                    for child in g.children:
                        if child.type == 'widget':
                            lastc = child
                        
                    walkNodes(lastc,i,True)
                    for child in g.children:
                        if child.type == 'widget':
                            lastc = child
                    walkNodes_2(lastc,i,True)
                    lastc.PlotLine.hide.val = True
                    
                i=i+1
            g['char1'].marker.val = 'circle'
        g['x'].mode.val = 'labels'
        
        g['x'].MajorTicks.number.val = 0
        g['x'].MajorTicks.length.val = '187pt'

        labels = interface.GetData('labels')
        pos = interface.GetData('labels_distance')
        posli=[]
        for p in pos[0]:
            posli.append(float(p))
  
        g['x'].MajorTicks.manualTicks.val = posli
        g['y'].label.val = 'Energy in Hartree'
        i=0
        for l in labels:
            if l == 'GAMMA': l='\Gamma'
            g.Add('label', name = 'label%i'%i)
        
            g['label%i'%i].yPos.val = -2.6
            g['label%i'%i].positioning.val = 'axes'
            g['label%i'%i].xPos.val = posli[i]
            g['label%i'%i].label.val = l
            g['label%i'%i].alignHorz.val = 'centre'
            g['label%i'%i].alignVert.val = 'top'
            
            i=i+1
            
        time.sleep(1)
        
        
        #info = plugins.datasetplugin.DatasetPluginHelper(interface.GetDatasets())
        #print info.datasets1d()
        #widget.Widget.addChild(widgets.graph.Graph)
        # get the Node corresponding to the widget path given
        #fromwidget = interface.Root.fromPath(fields['widget'])
        #search = fields['markersearch']
        #replace = fields['markerreplace']

        # loop over every xy widget including and below fromwidget
        #for node in fromwidget.WalkWidgets(widgettype='xy'):
            # if marker is value given, replace
        #    if node.marker.val == search:
        #        node.marker.val = replace

class DosPlugin(plugins.ToolsPlugin):
    """Plot bandstructure and character"""

    # a tuple of strings building up menu to place plugin on
    menu = ('DOS',)
    # unique name for plugin
    name = 'DOS'

    # name to appear on status tool bar
    description_short = 'DOS plot'
    # text to appear in dialog box
    description_full = 'Desnity of states plot'

    def __init__(self):
        """Make list of fields."""
        self.fields = [ 
            
            #plugins.FieldWidget("widget", descr="Start from widget",
            #                    default="/"),
            #plugins.FieldMarker("markersearch", descr="Search for marker"),
            #plugins.FieldMarker("markerreplace", descr="Replace with marker"),
            #plugins.FieldBool("character", descr="Plot character of bands")
            ]

    def apply(self, interface, fields):
        """Do the work of the plugin.
        interface: veusz command line interface object (exporting commands)
        fields: dict mapping field names to values
        """
        self.fields = fields
        def walkNodes(node, i):
            """Walk nodes"""

            if node.type == 'setting' and node.settingtype == 'dataset-or-floatlist':
                if node.name == 'xData':
                    node.val = 'edos'
                elif node.name == 'yData':
                    node.val = self.datasets_dos[i]

            #elif node.type == 'setting' and node.name == 'scalePoints' and ch:
            #    print 'done'
            #    node.val = self.datasets_char[i]
            else:
                for c in node.children:
                    walkNodes(c,i)
        
       
        g = interface.Root.fromPath('/page1/graph1')
        g.Add('xy', marker = 'none')
        
        self.datasets_dos = []
        self.datasets_total = []
        self.datasets = interface.GetDatasets()
        for set in self.datasets:
            if set.startswith('dos'):
                self.datasets_dos.append(set)
            elif set.startswith('totaldos'):
                self.datasets_total.append(set)
                 
        i=0
        for dataset in self.datasets_dos:
            if dataset != 'x':
                g.Add('xy', name=dataset, marker = 'none')
                for child in g.children:
                    if child.type == 'widget':
                        lastc = child
                lastc.PlotLine.width.val='1pt'    
                walkNodes(lastc,i)
                
                d = dataset.replace('_',' ').replace('[',' =').replace(']',' ').replace("'",' ').replace("dos",'pardos: ')
                dataset.replace('_',' ')
                lastc.key.val = str(d)
                if i !=1:
                    lastc.hide.val = True
            
            i=i+1
            
        g['x'].label.val = 'Energy in Hartree'
        g['y'].label.val = 'DOS'
        energy = interface.GetData('edos')
        g.Add('key')
        for c in g.children:
            
            if c.name == 'key1':
                c.horzPosn.val = 'left'
                c.vertPosn.val = 'top'
        #print min(energy[0])
        #g['x'].min.val = str(min(energy[0]))
        #g['x'].max.val = str(max(energy[0]))
            
        time.sleep(1)

class EOSPlugin(plugins.ToolsPlugin):
    """Plot bandstructure and character"""

    # a tuple of strings building up menu to place plugin on
    menu = ('EOS',)
    # unique name for plugin
    name = 'EOS'

    # name to appear on status tool bar
    description_short = 'EOS plot'
    # text to appear in dialog box
    description_full = 'Equation of states'

    def __init__(self):
        """Make list of fields."""
        self.fields = [ 
            
            #plugins.FieldWidget("widget", descr="Start from widget",
            #                    default="/"),
            #plugins.FieldMarker("markersearch", descr="Search for marker"),
            #plugins.FieldMarker("markerreplace", descr="Replace with marker"),
            #plugins.FieldBool("character", descr="Plot character of bands")
            ]

    def apply(self, interface, fields):
        """Do the work of the plugin.
        interface: veusz command line interface object (exporting commands)
        fields: dict mapping field names to values
        """
        self.fields = fields
        self.hash = []
        self.fite = []
        self.lv = []
        def walkNodes(node, j):
            """Walk nodes"""
            
            if node.name == 'f_'+self.hash[j]: self.xy = 2
            elif node.name == 'p_'+self.hash[j]: 
                self.xy = 1
                node.PlotLine.hide = True
            elif node.name not in ['p_'+self.hash[j],'f_'+self.hash[j]] and node.name.startswith('f_') or node.name.startswith('p_'): self.xy = 0
            
            if node.type == 'setting' and node.settingtype == 'dataset-or-floatlist':
                if node.name == 'xData':
                    print self.xy
                    if self.xy == 1:
                        node.val = 'V_points_%s'%self.hash[j]
                    elif self.xy == 2: node.val = self.lv[j]
                elif node.name == 'yData':
                    if self.xy == 1:
                        node.val = 'E_points_%s'%self.hash[j]
                    elif self.xy == 2: node.val = self.fite[j]

            else:
                for c in node.children:
                    walkNodes(c,j)
        
        def fitev(par, v, ein):
    
            fite = []
            deltasq = []
            res = []
            v0 = par[0]
            b0 = par[1]
            db0 = par[2]
            emin = par[3]
            i=0
            while i < len(v):
                    
                vov = (v0/v[i])**(2./3.)
                fite.append(float(emin + 9. * v0 * b0/16. * ((vov - 1.)**3. * db0 + (vov - 1.)**2. * (6. - 4. * vov))))
                if len(v) == len(ein):
                    deltasq.append((fite[i] - ein[i])**2.)
                    res.append(fite[i] - ein[i])
                #print (emin - ein[i])**2
                i = i+1
            return deltasq, fite, res
    
        self.datasets = interface.GetDatasets()
        n=0
        for set in self.datasets:
            if set.startswith('V_points'): 
                self.hash.append(set.lstrip('V_points'))
                n+=1
        
        
        g = interface.Root.fromPath('/page1/graph1')
        
        self.xy = 0
        for j in range(n):
            print n, j
            try:
                g.Add('xy', name='p_'+self.hash[j], marker = 'circle')
                g.Add('xy', name='f_'+self.hash[j], marker = 'none')
            except:
                print 'Plot exists!'
            V_points = interface.GetData('V_points_%s'%self.hash[j])[0]
            E_points = interface.GetData('E_points_%s'%self.hash[j])[0]
            
            B = interface.GetData('B_%s'%self.hash[j])[0][0]/(2.942104*10**4.)
            V = interface.GetData('V_%s'%self.hash[j])[0][0]
            E = interface.GetData('E_%s'%self.hash[j])[0][0]
            dB = interface.GetData('dB_%s'%self.hash[j])[0][0]
            g['x'].label.val = 'Volume in Bohr^3'
            g['y'].label.val = 'Energy in Hartree'
            par = [V,B,dB,E]
            self.lv.append(np.linspace(min(V_points),max(V_points),100))
            delta, fite, res = fitev(par, self.lv[j], E_points)
            self.fite.append(fite)
            print self.fite
            for child in g.children:
                walkNodes(child, j)
            #print min(energy[0])
            #g['x'].min.val = str(min(energy[0]))
            #g['x'].max.val = str(max(energy[0]))
            #g['xy1'].PlotLine.hide.val = True
        time.sleep(1)

plugins.toolspluginregistry.append(EOSPlugin)
plugins.toolspluginregistry.append(BandPlugin)
plugins.toolspluginregistry.append(DosPlugin)