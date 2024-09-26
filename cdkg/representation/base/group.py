from cromulent.model import Group
from cromulent.vocab import PrimaryName

from cdkg.representation import (
    santise_label_for_iri_resource,
    SOURCE_METADATA
)


GROUP = []

for row in SOURCE_METADATA:
    speaker_label = row.get('Speaker')
    if not speaker_label:
        continue

    actor_label = speaker_label.replace(' and ', ' & ')
    if ' & ' in actor_label:
        # Group
        resource = santise_label_for_iri_resource(speaker_label)
        identifier = 'speaker' + '/' + resource
        group = Group(
            ident=identifier,
            label=speaker_label
        )

        # Preferred name
        name = PrimaryName(content=speaker_label)
        group.identified_by = name

        GROUP.append(group)
