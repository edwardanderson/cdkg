from datetime import datetime, timedelta

from cromulent.model import (
    Activity,
    DigitalObject,
    Dimension,
    Event,
    Group,
    LinguisticObject,
    MeasurementUnit,
    Name,
    Person,
    TimeSpan,
    Type,
    Set,
    VisualItem
)
from cromulent.vocab import (
    instances,
    PrimaryName,
    WebPage
)

from cdkg.representation import (
    santise_label_for_iri_resource,
    SOURCE_METADATA,
    SUBTITLES
)


ACTIVITY = []

for index, row in enumerate(SOURCE_METADATA):
    title = row.get('Title').strip()
    if not title:
        continue

    speaker_label = row.get('Speaker', '').strip()
    homepage_url = row.get('Web', '').strip()
    video_url = row.get('Video', '').strip()
    event_label = row.get('Event', '').strip()
    category_label = row.get('Category', '').strip()
    date_label = row.get('Date', '').strip()
    srt_relative_path = row.get('File', '').strip()

    subtitles = SUBTITLES[srt_relative_path]
    total_time = list(subtitles)[-1].end

    # Activity
    resource = santise_label_for_iri_resource(title)
    identifier = 'presentation' + '/' + str(index)
    label = f'Presentation of "{title}"'
    activity = Activity(
        ident=identifier,
        label=label
    )

    # Preferred name
    name = PrimaryName(content=title)
    name.language = instances['english']
    activity.identified_by = name

    # Type
    activity.classified_as = Type(
        ident='https://vocab.getty.edu/aat/300258677',
        label='Presentation'
    )

    actor_name = speaker_label.replace(' and ', ' & ')
    actor_resource = santise_label_for_iri_resource(actor_name)
    actor_identifier = 'speaker' + '/' + actor_resource
    if '&' in actor_name:
            actor = Group(
            ident=actor_identifier,
            label=speaker_label
        )
    else:
        actor = Person(
            ident=actor_identifier,
            label=speaker_label
        )

    activity.carried_out_by = actor

    # Homepage
    webpage = WebPage(label='Homepage')
    webpage.format = 'text/html'
    webpage.access_point = DigitalObject(ident=homepage_url)
    webpage_text = LinguisticObject(
        label=f'Textual content of homepage'
    )
    webpage_text.digitally_carried_by = webpage
    activity.subject_of = webpage_text

    # Part of conference event
    event_resource = santise_label_for_iri_resource(event_label)
    event_identifier = 'programme' + '/' + event_resource
    activity.part_of = Event(
        ident=event_identifier,
        label=event_label
    )

    # Visual work
    visual_work = VisualItem(
        ident=identifier,
        label=f'Visual content of "{title}"'
    )
    activity.representation = visual_work

    # Set.
    set_resource = santise_label_for_iri_resource(category_label)
    set_identifier = 'track/' + set_resource
    activity.member_of = Set(
        ident=set_identifier,
        label=category_label
    )

    # Time-Span
    date_obj = datetime.strptime(date_label, '%d/%m/%Y')
    date_end = date_obj + timedelta(hours=23, minutes=59, seconds=59)
    time_span = TimeSpan()
    time_span.begin_of_the_begin = date_obj.isoformat()
    time_span.end_of_the_end = date_end.isoformat()
    ts_name = Name(content=date_label)
    time_span.identified_by = ts_name
    minutes = total_time.total_seconds() / 60.0
    duration = Dimension(value=round(minutes))
    duration.unit = MeasurementUnit(
         ident='http://vocab.getty.edu/aat/300379240',
         label='Minutes'
    )
    dimension_name = Name(content=f'{round(minutes)} min')
    duration.identified_by = dimension_name
    time_span.duration = duration
    activity.timespan = time_span

    ACTIVITY.append(activity)
