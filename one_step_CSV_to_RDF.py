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

#Call process_mapping('yourdata.csv') with your data.
#process_mapping('mapp.csv')

#Function 1

def process_mapping(mapping_file):
    """
    This function takes a mapping file and generates a new file called post_processed_mapping.txt
    The lines from this fie should be pasted into the body of the function map_data()
    This function takes a very specific syntax with the following criteria:
        The mapping file must be a .csv
        The first line must be 's,p,o'
        Every triple in the mapping must be explicitly asserted, with type assertions being done with RDF.type
    The triples produces have hyphens in them. In future versions, an option to use hex will be available. (hex=true or false)
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
            
            if row['p'] != 'RDF.type' :
                if 'datapoint' in row['o']:
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


    df.to_csv(final_file, index=False, header=False)


    with open(final_file, 'r+') as f:
        data = f.read()
        new_data = re.sub(r'"', '', data)
        f.seek(0)
        f.write(new_data)
        f.truncate()

    #Create final mapped file 
    filename = 'post_processed_mapping.py'
    with open(os.path.join(os.getcwd(), filename), 'w') as f:
        f.write('')

    #Migrate working csv file to final mapped txt file, delete temporary_mapping working file
    with open(final_file, newline='') as f_input, open('post_processed_mapping.py', 'w') as f_output:
        csv_input = csv.reader(f_input)
        for row in csv_input:
            f_output.write(','.join(row) + '\n')
            
    os.remove('temporary_mapping')
            

    #Add g.add(()) to every line
    with open('post_processed_mapping.py', 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.truncate()
        for line in lines:
            new_line = 'g.add((' + line.strip() + '))\n'
            f.write(new_line)


#Function 2


def map_data(instance_data):
    """
    This function must be updated with the mapping triples produced by the function process_mapping()
    """
    with open(instance_data, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            
            # Generate UUID for each row
            uuid_str = str(uuid.uuid4())

            # Add post-processed mapping
            
            """
            Either paste the lines of RDFLib from "post_processed_mapping.py" here or let this function call that file
            """
            exec(open("post_processed_mapping.py").read())
            
            


    # Serialize graph to RDF/XML format
    print(g.serialize(format='ttl'))

def process_and_generate_data(mapping,data):
    """
    This function generates the proper RDFLib syntax mapping and generates triples using that mapping in one step.
    """
    #Process mapping
    process_mapping(mapping)
    
    #Map data
    map_data(data)

#Usage:
#process_mapping('sample_mapping.csv')

#Call the second function
#map_data('sample_data.csv')

#Or call both at the same time
process_and_generate_data('sample_mapping.csv','sample_data.csv')

