from cromulent.model import Set
from cromulent.vocab import (
    instances,
    PrimaryName
)

from cdkg.representation import (
    santise_label_for_iri_resource,
    SOURCE_METADATA
)


SET = []

concepts = set()
for row in SOURCE_METADATA:
    category_label = row.get('Category').strip()
    if not category_label:
        continue

    concepts.add(category_label)

for set_label in concepts:
    # Set
    resource = santise_label_for_iri_resource(set_label)
    identifier = 'track' + '/' + resource
    set_ = Set(
        ident=identifier,
        label=set_label
    )

    # Preferred name
    name = PrimaryName(content=set_label)
    name.language = instances['english']
    set_.identified_by = name

    SET.append(set_)
