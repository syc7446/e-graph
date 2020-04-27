import networkx as nx
import pydot as pd

def plot(buchi,filename, path1=None, path2=None):
    '''
    visualize a graph and a colored path (option)
    '''
    filename = './'+ filename +'_dot.txt'
    graph = nx.nx_pydot.to_pydot(buchi)

    if path1 is not None:
        # "write_dot" may fail to encode nodes.
        for i in range(len(path1[0])-1):
            e = graph.get_edge(repr(repr(path1[0][i])),
                               repr(repr(path1[0][i+1])))[0]
            e.set_color('blue')
            n = graph.get_node(repr(repr(path1[0][i])))[0]
            n.set_color('blue')
            n = graph.get_node(repr(repr(path1[0][i+1])))[0]
            n.set_color('blue')
    if path2 is not None:    
        for i in range(len(path2[0])-1):
            e = graph.get_edge(repr(repr(path2[0][i])),
                               repr(repr(path2[0][i+1])))[0]
            if e.get_color() == 'blue' or e.get_color() == 'green':
                e.set_color('green')
            else:
                e.set_color('red')
            n = graph.get_node(repr(repr(path2[0][i])))[0]
            if n.get_color() == 'blue' or n.get_color() == 'green':
                n.set_color('green')
            else:
                n.set_color('red')
            n = graph.get_node(repr(repr(path2[0][i+1])))[0]
            if n.get_color() == 'blue' or n.get_color() == 'green':
                n.set_color('green')
            else:
                n.set_color('red')
        ## from IPython import embed; embed(); sys.exit()
            
    #graph = graph.pop()
    pdfname = filename.replace('.txt','.pdf')
    graph.write_pdf(pdfname)
    graph.write_png(pdfname.replace('pdf','png'))
    
    print 'Graph Successfully Plotted'

    
