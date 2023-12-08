import csv, re, os, uuid
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, XSD, RDFS

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


def total_mapping_and_generate_data(mapping_file,data_file,uuid_or_hex):
    """
    Takes a mapping CSV file and data CSV file as input. \n
    Mapping syntax is a simpler version of regular RDFLib syntax. \n
    If uuid_or_hex is False, then the generated triples are generated without hyphens (as hexidecibles, not uuids). If True or None, then regular random uuids will be used. \n
    Native Python modules csv, re, and uuid must be imported. \n
    Dependencies: RDFLib, XSD, and RDF must be imported, a grah must be parsed in RDFLib, the function adds triples to this graph, then serializes and prints the generated data to the terminal. \n
    
        
    """
    with open(data_file, 'r') as f:
        data_reader = csv.DictReader(f)
        for data_row in data_reader:
            

            with open(mapping_file, 'r') as input_file:
                mapping_reader = csv.DictReader(input_file)

                for mapping_row in mapping_reader:
                    
                    uuid_str = str(uuid.uuid4())
                    if uuid_or_hex is False:
                        uuid_str = uuid.uuid4().hex
                        
                    if mapping_row['p'] == 'RDF.type' :
                        g.add((URIRef(mapping_row['s']+uuid_str),RDF.type,URIRef(mapping_row['o'])))
                        g.add((URIRef(mapping_row['s']+uuid_str),RDF.type,owl.NamedIdividual))
               
                    if mapping_row['p'] != 'RDF.type' :
                        if 'datapoint' in mapping_row['o']:
                            split_datapoint_list = mapping_row['o'].split('/')
                            #This is where we break the datapoint/string/column down to use in the g.add line below
                            g.add((URIRef(mapping_row['s']+uuid_str),RDF.type,Literal(data_row[split_datapoint_list[2]],datatype=XSD.split_datapoint_list[1] )  ))
                            
                            #There are a finite amount of kinds of triples this tool can use:
                            # instance to class
                            # instance to instance
                            # instance to datapoint
                            # It is bad practice to make literals the s in any graph
                            
                            #Each triple combination adds the following to the graph:
                                # if instance , rdf:type , class
                                    #then add uri(instance) rdf:type class
                                    #then add rdf:type owl:NamedIdividual
                                # if instance , objectproperty , instance
                                    #then add uri(instance) , objectproperty , uri(instance)
                                # if instance , object property , datapoint
                                    #then add uri(instance) , object proprty , literal(datapoint)
                            
                            #The decision tree has two points that make it easy to distinguish which case a row is:
                                #Either a row in the mapping has datapoint in it or not.
                                #Either a row in the mapping has rdf:type or not.
                                #These two options are mutually exclusive
                                
                        else:
                            g.add(( URIRef(mapping_row['s']+uuid_str),URIRef(mapping_row['p']),URIRef(mapping_row['o']+uuid_str) ))
        print(g.serialize(format="turtle"))


total_mapping_and_generate_data('sample_mapping.csv','sample_data.csv',True)

#Currently gettinh an error because the mapping file is a csv, and each value of each column is a string, not an RDFLib object
    #Even though cco.Person is an RDF:Lib object in python, the function is reading it as a string in a csv... which it is...
#To change this, the mapping could be rewritten in as a python file or written AS a csv but with a .py extension
#Fixed this problem by just wrapping all the items retrieved from the mapping file with URIRef()
