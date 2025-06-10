# main.py
from ElasticGraph_fromDir import build_directory_network
#from Classic_DirGrpah import make_Dirgraph


#make_Dirgraph('C:/Users/Email/Desktop/CAM')

root_directory = 'C:/Users/Email/Desktop/CAM'
build_directory_network(root_directory, output_file='directory_tree.html')
