import requests, json
import os
import pandas as pd
# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Try it out by opening Python and typing
# from geoparse_documents import annotateFile; f=annotateFile(); from googleNLP import parseWithGoogle; parseWithGoogle(f.pdf_words_clean[0:10000], print_input=True, print_output=True)

def parseWithGoogle(text, print_output=False, print_input=False, flatten=True):
    """ Makes request to Google Cloud and returns a df

    Input
        text            String. Do not pass lists, dictionaries, etc. Basic strings only.

    Returns
        Pandas dataframe with each extracted feature
    """
    client = language.LanguageServiceClient()

    if print_input:
        print(text)

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    # PS: HOW DO I ONLY REQUEST LOCATIONS?
    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')
    if print_output:
        for entity in entities:
            print('=' * 20)
            print(u'{:<16}: {}'.format('name', entity.name))
            print(u'{:<16}: {}'.format('type', entity_type[entity.type]))
            print(u'{:<16}: {}'.format('metadata', entity.metadata))
            print(u'{:<16}: {}'.format('salience', entity.salience))
            print(u'{:<16}: {}'.format('wikipedia_url',
                  entity.metadata.get('wikipedia_url', '-')))

    if flatten:
        df = _flatten_into_df(entities)
    else:
        df = pd.DataFrame(entities)
    return df


def _get_api_key():
    key = os.environ.get('googleCloud_key')
    if not key:
        raise PermissionError('No Geoparser IO key found. Request one on www.geoparser.io and set as environment variable.')
    return(key)


def _flatten_into_df(data_to_flatten):
    """ Takes data in list or dict format.

    Input
        data_to_flatten        a dictionary or list containing the data to end up in the dataframe. 
    """
    
    # check if data is a dictionary - if it is, make it into a list
    if isinstance(data_to_flatten, dict):
        data_to_flatten = [data_to_flatten]

    for idx, item in enumerate(data_to_flatten):
        df_element = pd.io.json.json_normalize(item)
        if idx == 0:
            df_temp = df_element
        else:
            df_temp = df_temp.append(df_element)

    return df_temp