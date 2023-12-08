# CSV_to_RDF_Instance_tool
A tool for turning csv into rdf with complex mappings. This tool depends on RDFLib, Pandas, and was built on a Windows machine. This tool works best when used in a self-contained folder.

# Usage
The tool has two functions, the first takes a mapping file and transforms it into RDFLib syntax, and the second maps the csv data to rdf triples.

# Syntax

## Basic Rules
This syntax assumes that you have a full worked-out knowledge graph mapping of your data you can use to construct the mapping file. Every triple in a mapping must be explicitly asserted. Type assertions with `RDF:type` will assume that the subject of the triple is an instance. The mapping file must be a CSV and the first row must be `s,p,o` (subject, predicate, object).

## Example
The following is an example of a simple mapping.

```csv
s,p,o
ex:Person_1,RDF:type,ex:Person
ex:Person_1,RDFS:label,datapoint/string/Name
ex:Person_1,ex:agent_in,ex:Process_1
ex:Process_1,RDF:type,ex:Process
ex:Process_1,RDFS:label,datapoint/string/Activity
```

A corresponding csv of the data would look like this:

```csv
Name,Activity
John,Teaching
Mark,Thinking
Sally,Working
```

```mermaid
flowchart TD;

C{Person};
C -->|designated by| G{Nominal ICE};
C -->|agent in| D{Activity};
D -->|label| E(Datapoint: Activity);
G -->|has text value| H(Datapoint: Name);
```

This is a mapping that takes two datapoints, one which is the `rdfs:label` for the set of people, and another which is the `rdfs:label` for the activities those people are `ex.agent_in`.

To connect a triple to a column in a csv, the following syntax is used:
`datapoint/datatype/column` where `datatype` is a valid `xsd:datatype` and `column` is the name of a column in the csv.

In previous versions, the mapping and data generating happened in two steps. Now it happens in one.
