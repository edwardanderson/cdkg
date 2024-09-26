import csv
import srt

from pathlib import Path


def santise_label_for_iri_resource(label: str) -> str:
    '''Santise a label string for use in an IRI.'''
    resource = (
        label
        .strip()
        .replace(' ', '-')
        .replace('&', 'and')
        .lower()
    )
    return resource


root = Path(__file__).parent.parent.parent
source_metadata_path = root / 'data/source/cdkg-challenge/Transcripts/Connected Data Knowledge Graph Challenge - Transcript Metadata.csv'
with open (source_metadata_path, 'r') as in_file:
    SOURCE_METADATA = list(csv.DictReader(in_file))

SUBTITLES = {}
for row in SOURCE_METADATA:
    srt_relative_path = row.get('File')
    if not srt_relative_path:
        continue

    srt_path = source_metadata_path.parent.parent / srt_relative_path[1:]
    SUBTITLES[srt_relative_path] = list(srt.parse(srt_path.read_text()))
