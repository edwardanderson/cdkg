from cromulent.model import (
    Group,
    Person
)
from cromulent.vocab import PrimaryName

from cdkg.representation import (
    santise_label_for_iri_resource,
    SOURCE_METADATA
)


PERSON = []

for row in SOURCE_METADATA:
    speaker_label = row.get('Speaker')
    if not speaker_label:
        continue

    actor_label = speaker_label.replace(' and ', ' & ')
    members_labels = actor_label.split(' & ')
    for member_label in members_labels:
        # Person
        resource = santise_label_for_iri_resource(member_label)
        identifier = 'speaker' + '/' + resource
        person = Person(
            ident=identifier,
            label=member_label
        )

        # Preferred name
        name = PrimaryName(content=member_label)
        person.identified_by = name

        if len(members_labels) > 1:
            # Group membership
            group_resource = santise_label_for_iri_resource(speaker_label)
            group_iri = 'speaker' + '/' + group_resource
            group = Group(
                ident=group_iri,
                label=speaker_label
            )
            person.member_of = group

        PERSON.append(person)
