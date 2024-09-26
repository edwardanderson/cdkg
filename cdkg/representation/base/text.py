from cromulent.model import (
    Activity,
    Creation,
    DigitalObject,
    LinguisticObject,
    Type
)
from cromulent.vocab import instances

from cdkg.representation import (
    santise_label_for_iri_resource,
    SOURCE_METADATA,
    SUBTITLES
)


TEXT = []

for index, row in enumerate(SOURCE_METADATA):
    title_label = row.get('Title').strip()
    if not title_label:
        continue

    srt_relative_path = row.get('File')

    # Textual work
    resource = santise_label_for_iri_resource(title_label)
    identifier = 'presentation' + '/' + str(index)
    text_label = f'Textual content of "{title_label}"'
    subtitles = SUBTITLES[srt_relative_path]
    content = ' '.join(
        [
            fragment.content.replace('\n', ' ')
            for fragment in subtitles
        ]
    )
    text = LinguisticObject(
        ident=identifier,
        label=text_label,
        content=content
    )
    text.classified_as = Type(
        ident='http://vocab.getty.edu/aat/300027388',
        label='Transcript',
    )
    text.language = instances['english']

    # Creation
    event_label = f'Presentation of "{title_label}"'
    creation = Creation(ident=identifier)
    creation.caused_by = Activity(
        ident=identifier,
        label=event_label
    )
    text.created_by = creation

    # Recording
    digital_iri = 'recording' + '/' + str(index)
    digital_label = f'Recording of "{title_label}"'
    digital_obj = DigitalObject(
        ident=digital_iri,
        label=digital_label
    )
    text.digitally_carried_by = digital_obj

    TEXT.append(text)

    # TODO: Break text into fragments. Consider thematic divisions over timecodes.
    # for n2, item in enumerate(subtitles):
    #     resource_fragment = str(n) + '#' + str(n2)
    #     part_iri = BASE + PATH + resource_fragment
    #     part = LinguisticObject(ident=part_iri)
    #     part.content = item.content.replace('\n', ' ')
    #     part.part_of = LinguisticObject(ident=iri)
    #     digital_part_iri = BASE + 'digital/' + str(n) + '#' + str(n2)
    #     digital_part = DigitalObject(ident=digital_part_iri)
    #     part.digitally_carried_by = digital_part
