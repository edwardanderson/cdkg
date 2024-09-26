from cromulent.model import (
    Activity,
    Creation,
    DigitalObject,
    VisualItem
)

from cdkg.representation import (
    santise_label_for_iri_resource,
    SOURCE_METADATA
)


VISUAL = []

for index, row in enumerate(SOURCE_METADATA):
    title_label = row.get('Title').strip()
    if not title_label:
        continue

    video_url = row.get('Video').strip()
    parent = row.get('Event')

    # Visual work
    resource = santise_label_for_iri_resource(title_label)
    identifier = 'presentation' + '/' + str(index)
    label = f'Visual content of "{title_label}"'
    visual_work = VisualItem(ident=identifier, label=label)

    # Creation
    activity_label = f'Presentation of "{title_label}"'
    creation = Creation(ident=identifier)
    creation.caused_by = Activity(
        ident=identifier,
        label=activity_label
    )
    visual_work.created_by = creation

    # Recording
    recording_identifier = 'recording' + '/' + str(index)
    recording_label = f'Recording of "{title_label}"'
    recording = DigitalObject(
        ident=recording_identifier,
        label=recording_label
    )
    visual_work.digitally_shown_by = recording

    VISUAL.append(visual_work)
