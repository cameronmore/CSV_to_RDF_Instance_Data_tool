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


def process_mapping(mapping_file,uuid_or_hex):
    """
    Iterate through the 
        
    """

    
    #Create a temporary_mapping working file to read and write to
    final_file = 'temporary_mapping'
    with open(os.path.join(os.getcwd(), final_file), 'w') as f:
        f.write('')

    #Change IRIs to RDFLib-readable IRIs to add
    with open(mapping_file, 'r') as input_file, open(final_file, 'w', newline='') as output_file:
        reader = csv.DictReader(input_file)
        writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)
        writer.writeheader()

        for row in reader:
            
            uuid_str = str(uuid.uuid4())
            if uuid_or_hex is False:
                uuid_str = uuid.uuid4().hex
         
            if row['p'] != 'RDF.type' :
                if 'datapoint' in row['o']:
                    g.add((URIRef(row['s']+uuid_str),RDF.type,Literal(    )   ))
                    
                    #Do the adding and iterating in this step here!!
                    
                    #Enumerate the possible triple options:
                        # if instance , rdf:type , class
                            #then x
                        # if instance , objectproperty , instance
                            #then y
                        # if instance , object property , datapoint
                            #then z
                    
                    #todo for long term, add possible pyTransform so literals can be bound as certain iris? too diffcult to do in systematic form?
                    
                    row['s'] = str("URIRef(" + row['s'] + " + uuid_str)")
                elif 'datapoint' in row['s']:
                    row['o'] = str("URIRef(" + row['o'] + " + uuid_str)")   
                else:
                    row['s'] = str("URIRef(" + row['s'] + " + uuid_str)")
                    row['o'] = str("URIRef(" + row['o'] + " + uuid_str)")
            if row['p'] == 'RDF.type':
                row['s'] = str("URIRef(" + row['s'] + " + uuid_str)")           
                new_row = {'s': row['s'], 'p': row['p'], 'o': 'owl.NamedIndividual'}
                writer.writerow(new_row)
                
            writer.writerow(row)

    #Read the mapping file and fill in the datapoints with RDFLib-readable IRIs
    df = pd.read_csv(final_file)

    for index, row in df.iterrows():
        if 'datapoint' in row.iloc[2]:
            my_list = row.iloc[2].split('/')
            new_value = 'Literal(row[' + "'" + my_list[2] + "'" + '], datatype=XSD.' + my_list[1] +')'
            row.iloc[2]=new_value

        if 'datapoint' in row.iloc[0]:
            my_list = row.iloc[0].split('/')
            new_value = 'Literal(row[' + "'" + my_list[2] + "'" + '], datatype=XSD.' + my_list[1] +')'
            row.iloc[0]=new_value

