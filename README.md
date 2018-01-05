# Surgo ML-platform: accessing funding data
Sandbox to try out different geoparsing methods. There is one example document `usaid_evaluation_example.pdf`, and two attempts at parsing:

* [Geoparser.io](www.geoparser.io)
* [Google Cloud NLP](https://cloud.google.com/natural-language/docs/analyzing-entities)

## Setting up

* Install Python 3.6
* Install requirements
* Get an API key for Google Cloud NLP and save the .json application credentials. Store the path in an environment variable called `GOOGLE_APPLICATION_CREDENTIALS`.
* Get an API key for geoparser.io and store it as string in environment variable `geoparserIO_key`.

## Demo document with geoparser.io and Google NLP
In Python

```
import geoparse_documents
x = geoparse_documents.annotateFile()  # this will download NLTK stopwords
x.parse_with_geoparserIO()
x.parse_with_google_NLP()
```

Each will return a dataframe with extracted locations. Due to request size limitations on geoparser.io we only send 10k chars. 

```
>>> x.parse_with_geoparserIO()
  geometry.coordinates geometry.type       id properties.admin1  \
0         [79.0, 22.0]         Point  1269750                00   

   properties.confidence properties.country properties.name  \
0                    1.0                 IN           India   

                               properties.references  \
0  [[2300, 2305], [2417, 2422], [2738, 2743], [52...   

                properties.type     type  
0  independent political entity  Feature 
```

and Google NLP:

```               name entity_type     salience  \
0        tamil nadu    LOCATION     0.123987   
1             india    LOCATION    0.0883873   
14        districts    LOCATION    0.0147802   
42   apac districts    LOCATION   0.00566704   
52            state    LOCATION   0.00464536   
76            state    LOCATION   0.00220922   
77            state    LOCATION   0.00220922   
82          clinics    LOCATION   0.00195836   
124           areas    LOCATION   0.00123148   
149       districts    LOCATION  0.000857077   
163          states    LOCATION  0.000659028   
164           state    LOCATION  0.000659028   
165           state    LOCATION  0.000659028   

                                wikipedia_url google_knowledge_graph  
0    https://en.wikipedia.org/wiki/Tamil_Nadu               /m/07c98  
1         https://en.wikipedia.org/wiki/India               /m/03rk0  
14                                       None                   None  
42                                       None                   None  
52                                       None                   None  
76                                       None                   None  
77                                       None                   None  
82                                       None                   None  
124                                      None                   None  
149                                      None                   None  
163                                      None                   None  
164                                      None                   None  
165                                      None                   None  


```

Google can also parse a much larger chunk of the document:

`x.parse_with_google_NLP(start_at_char=0, end_at_char=150000)`

which yields >4k entities including many non-geographic locations ('home', 'clinics', 'brothels'). 
