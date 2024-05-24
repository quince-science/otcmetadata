"""
Generates various reports on the state of OTC metadata.
"""
import argparse

import otcmetadata

DEBUG = False


def _print_orphans(type: str, orphans: list) -> None:
    print(f'Orphaned {type}:')
    if len(orphans) > 0:
        for orphan in orphans:
            label = orphan["label"]
            if label is None:
                label = orphan["name"]

            print(f'  {"<No Label>" if label is None else label}: {orphan["uri"]}')
    else:
        print("  No orphans")

    print("")


def orphans() -> None:
    """
    Locate items that should be linked to something, but aren't. Such items include:

    Person (should have Assumed Role)
    xOrganization (should have Person via Assumed Role - Academic Institution and Station only)
    Funder (should have Funding)
    Sensor (should have Sensor Deployment)
    Device (should have Sensor)
    Instrument (should have Instrument Deployment)
    Platform (should have Platform Deployment)

    Note that this doesn't check for items that should have links that are required (e.g. a Calibration must be
    linked to a Sensor). These will be found in other reports.
    """
    _print_orphans('People (no roles)', otcmetadata.get_items_without('Person', 'hasHolder', DEBUG))
    _print_orphans('Devices (no concrete sensor instances)',
                   otcmetadata.get_items_without('Device', 'hasSensor', DEBUG))
    _print_orphans('Sensors (no Sensor Deployment)',
                   otcmetadata.get_items_without('Sensor', 'hasSensorDeployment', DEBUG))
    _print_orphans('Instruments (no Instrument Deployment)',
                   otcmetadata.get_items_without('Instrument', 'hasInstrumentDeployment', DEBUG))
    _print_orphans('Platforms (no Platform Deployment)',
                   otcmetadata.get_items_without('Platform', 'hasPlatformDeployment', DEBUG))
    _print_orphans('Funder (no Funding)',
                   otcmetadata.get_items_without('Funder', 'hasFunding', DEBUG))
    _print_orphans('Academic Institution (no People)',
                   otcmetadata.get_items_without('AcademicInstitution', 'atOrganization', DEBUG))
    _print_orphans('Station (no People)',
                   otcmetadata.get_items_without('Station', 'atOrganization', DEBUG))


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
parser.add_argument('-debug', action="store_true",
                    help='Print debugging information during operation')

args = parser.parse_args()
DEBUG = args.debug
report = args.report[0]
if report in _REPORTS_REQUIRING_URI and args.uri is None:
    print('URI required for selected report')

if report == 'orphans':
    orphans()
