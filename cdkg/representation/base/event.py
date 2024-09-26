from cromulent.model import Event
from cromulent.vocab import (
    instances,
    PrimaryName
)

from cdkg.representation import (
    santise_label_for_iri_resource,
    SOURCE_METADATA
)


EVENT = []

events = set()
for row in SOURCE_METADATA:
    event_label = row.get('Event')
    if not event_label:
        continue

    events.add(event_label)

for event_label in events:
    # Conference event
    resource = santise_label_for_iri_resource(event_label)
    identifier = 'programme' + '/' + resource
    event = Event(ident=identifier)

    # Preferred name
    name = PrimaryName(content=event_label)
    name.language = instances['english']
    event.identified_by = name

    EVENT.append(event)
