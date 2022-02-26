# MODA - Modelowanie Danych

A university class about database modeling using UML.

## Exporter
A script that exports data from an oracle database to custom schemas, builds an XML file, validates it with an XSD schema and sends to a custom backend. 

## Backend (not written by me)
A server written in express that validates the XML file, converts to custom schema and saves it to a mongoDB database.

## Docs (written by the whole team)
The directory contains:
- Concept model
- Logical model
- Relational model
- XML model
- MongoDB model