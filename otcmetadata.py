"""
Methods for extracting information from the ICOS OTC metadata system.
"""
from icoscp_core.icos import meta

_OTC_STATION_URI_BASE = 'http://meta.icos-cp.eu/resources/otcmeta/'
_OTC_CLASS_URI_BASE = 'http://meta.icos-cp.eu/ontologies/otcmeta/'

_CP_QUERY_PREFIX = """prefix cpmeta: <http://meta.icos-cp.eu/ontologies/cpmeta/>
                 prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>"""

_OTC_QUERY_PREFIX = """prefix otcmeta: <http://meta.icos-cp.eu/ontologies/otcmeta/>
                    prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    """


def get_items_without(item_class: str, relationship: str, print_query: bool = False) -> list:
    query = f"""{_OTC_QUERY_PREFIX}
            select ?uri ?label ?name where {{
            ?uri rdf:type otcmeta:{item_class} .
            OPTIONAL {{?uri rdfs:label ?label}} .
            OPTIONAL {{?uri otcmeta:hasName ?name}} .
            bind(coalesce(?label, ?name, ?uri) as ?sortLabel)
            FILTER NOT EXISTS {{[] otcmeta:{relationship} ?uri}}
            }}
            ORDER BY ASC(?sortLabel)
    """
    if print_query:
        print(query)
    query_result = meta.sparql_select(query)
    result = []

    for record in query_result.bindings:
        result.append({
            'uri': record['uri'].uri,
            'label': record['label'].value if 'label' in record else None,
            'name': record['name'].value if 'name' in record else None
        })

    return result


def get_otc_station_for_core_station(core_station_uri: str) -> str | None:
    """
    Retrieve the OTC metadata URI for a station from its core metadata URI. Returns None if the URI isn't found.
    :param core_station_uri: The station's URI in the core metadata.
    :return: The OTC metadata URI.
    """
    query = f"""{_CP_QUERY_PREFIX}
    select * where {{
      <{core_station_uri}> cpmeta:hasOtcId ?otcId
    }}
    """
    query_result = meta.sparql_select(query)
    if len(query_result.bindings) == 0:
        return None
    else:
        return f'{_OTC_STATION_URI_BASE}{query_result.bindings[0]['otcId'].value}'
