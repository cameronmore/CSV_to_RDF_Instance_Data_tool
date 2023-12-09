import csv, re, os, uuid
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD, RDFS, NamespaceManager


# Define graph
g = Graph()

# Define common namespaces
ex = Namespace('http://example.org/')
g.bind('ex',ex)
cco = Namespace('http://www.ontologyrepository.com/CommonCoreOntologies/')
g.bind('cco',cco)
obo = Namespace('http://purl.obolibrary.org/obo/')
g.bind('obo',obo)
owl = Namespace('http://www.w3.org/2002/07/owl#')
g.bind('owl',owl)

prefixes = {
    'cco':'http://www.ontologyrepository.com/CommonCoreOntologies/',
    'obo':'http://purl.obolibrary.org/obo/',
    'rdfs':'http://www.w3.org/2000/01/rdf-schema#'
}


def total_mapping_and_generate_data(mapping_file,data_file,uuid_or_hex,prefix_dict=dict):
    """
    Takes a mapping CSV file and data CSV file as input. \n
    This function uses a sligtly different syntax than the other version of this tool, it uses ':' rather than '.' between the prefixes and the identifiers. \n
    Rather than cco.Person, which is RDFLib syntax, one should write cco:Person, which is valid RDF syntax. \n
    Mapping syntax is a simpler version of regular RDFLib syntax. \n
    If uuid_or_hex is False, then the generated triples are generated without hyphens (as hexidecibles, not uuids). If True or None, then regular random uuids will be used. \n
    Native Python modules csv, re, and uuid must be imported. \n
    Dependencies: RDFLib, XSD, and RDF must be imported, a grah must be parsed in RDFLib, the function adds triples to this graph, then serializes and prints the generated data to the terminal. \n
    Known issues: pre-defined namespaces are not definable. For some reason, ns1 or ns2 are being bound to all the IRIs, not cco. \n
    
        
    """
   
    with open(data_file, 'r') as f:
       
        data_reader = csv.DictReader(f)
        for data_row in data_reader:
            

            with open(mapping_file, 'r') as input_file:                
                mapping_reader = csv.DictReader(input_file)
                
                
                #for dict_row in mapping_reader:
                    #for k, v in dict_row.items():

                        #for k, v in prefix_dict.items():
                            #dict_row = dict(((key, value.replace(k,v)) for key, value in dict_row.items()))



                    
            
            
                
                #Impliment a find-and-replace loop here that replaces prefixes in the triples wit the full IRI prefix
                    #Use *args or *kwargs to let user put their own prefixes in, but hard code a bunch of them like obo and cco especially
                    #for cco in mapping_file
                        #replace with http://ontologyrepository...


                for mapping_row in mapping_reader:
                    
                    uuid_str = str(uuid.uuid4())
                    if uuid_or_hex is False:
                        uuid_str = uuid.uuid4().hex
                    
                    #The script iterates both the mapping and the data creating triples based off the kind of relation asserted in the mapping:
                    #Every line is either:
                        # instance to class
                        #instance to datapoint
                    # or
                        # instsnce to instance         

                    #Case 1: Instance to Class
                    if mapping_row['p'] == 'RDF:type' :
                        g.add((URIRef(URIRef(mapping_row['s'])+uuid_str),RDF.type,URIRef(mapping_row['o'])))
                        g.add((URIRef(URIRef(mapping_row['s'])+uuid_str),RDF.type,owl.NamedIdividual))
               
                    #Case 1.5 Instance to something else
                    if mapping_row['p'] != 'RDF:type' :
                        
                        #Case 2: Instance to datapoint
                        if 'datapoint' in mapping_row['o']:
                            split_datapoint_list = mapping_row['o'].split('/')

                            g.add((URIRef(URIRef(mapping_row['s'])+uuid_str),URIRef(mapping_row['p']),Literal(data_row[split_datapoint_list[2]],datatype=URIRef("http://www.w3.org/2001/XMLSchema#" + split_datapoint_list[1]) )  ))
                        
                        #Case 3: Instance to Instance
                        else:
                            g.add(( URIRef(URIRef(mapping_row['s'])+uuid_str),URIRef(mapping_row['p']),URIRef(URIRef(mapping_row['o'])+uuid_str) ))

        print(g.serialize(format="turtle"))


total_mapping_and_generate_data('sample_mapping.csv','sample_data.csv',True,prefix_dict=prefixes)

#Current error: predefined namespaces are not appearing in the generated triples
