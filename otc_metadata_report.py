"""
Generates various reports on the state of OTC metadata.
"""
import argparse

import otcmetadata


def _print_orphans(type: str, orphans: list) -> None:
    if len(orphans) > 0:
        print(f'Orphaned {type}:')
        for orphan in orphans:
            print(f'  {"<No Label>" if orphan["label"] is None else orphan["label"]}: {orphan["uri"]}')
        print("")


def orphans() -> None:
    """
    Locate items that should be linked to something, but aren't. Such items include:

    Person (should have Assumed Role)
    Organization (should have Person via Assumed Role)
    Funder (should have Funding)
    Sensor (should have Sensor Deployment)
    Instrument (should have Instrument Deployment)
    Platform (should have Platform Deployment)

    Note that this doesn't check for items that should have links that are required (e.g. a Calibration must be
    linked to a Sensor). These will be found in other reports.
    """
    _print_orphans('People', otcmetadata.get_items_without('Person', 'hasHolder'))


######################################################################
# Main script: Parse command line and run the selected report.
_REPORTS_REQUIRING_URI = ['person']

parser = argparse.ArgumentParser(description='Generate reports of OTC metadata')
parser.add_argument('-report', type=str, nargs=1, help='The report to generate', required=True,
                    choices=[
                        'orphans',
                        'person'
                    ])
parser.add_argument('-uri', type=str, help='Item URI (required for some reports)', required=False)

args = parser.parse_args()
report = args.report[0]
if report in _REPORTS_REQUIRING_URI and args.uri is None:
    print('URI required for selected report')

if report == 'orphans':
    orphans()
