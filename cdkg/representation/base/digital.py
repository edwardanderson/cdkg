from cromulent.model import (
    DigitalObject,
    LinguisticObject,
    Type,
    VisualItem
)

from cdkg.representation import (
    santise_label_for_iri_resource,
    SOURCE_METADATA
)


DIGITAL = []

for index, row in enumerate(SOURCE_METADATA):
    title_label = row.get('Title').strip()
    if not title_label:
        continue

    video_url = row.get('Video', '').strip()
    srt_relative_path = row.get('File').strip()

    # Digital object
    resource = santise_label_for_iri_resource(title_label)
    identifier = 'recording' + '/' + str(index)
    label = f'Recording of "{title_label}"'
    digital_obj = DigitalObject(
        ident=identifier,
        label=label
    )

    presentation_identifier = 'presentation' + '/' + str(index)

    # Visual work
    visual_work_label = f'Visual content of "{title_label}"'
    visual_work = VisualItem(
        ident=presentation_identifier,
        label=visual_work_label
    )
    digital_obj.digitally_shows = visual_work

    # Textual work
    textual_work_label = f'Textual content of "{title_label}"'
    textual_work = LinguisticObject(
        ident=presentation_identifier,
        label=textual_work_label
    )
    digital_obj.digitally_carries = textual_work

    # Type
    digital_obj.classified_as = Type(
        ident='https://vocab.getty.edu/aat/300028682',
        label='Video recording'
    )

    # Recording
    recording = DigitalObject(ident=video_url)
    digital_obj.access_point = recording

    DIGITAL.append(digital_obj)

    # for n2, item in enumerate(subtitles):
    #     resource_fragment = str(n) + '#' + str(n2)
    #     part_iri = BASE + PATH + resource_fragment
    #     part = LinguisticObject(ident=part_iri)
    #     part.content = item.content.replace('\n', ' ')
    #     part.part_of = LinguisticObject(ident=iri)
    #     digital_part_iri = BASE + PATH + str(n) + '#' + str(n2)
    #     digital_part = DigitalObject(ident=digital_part_iri)
    #     part.digitally_carried_by = digital_part
