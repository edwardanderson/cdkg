from lxml import etree
from requests import Session

from cromulent.model import (
    Creation,
    DigitalObject,
    Group,
    LinguisticObject,
    Person,
    Type,
)
from cromulent.vocab import WebPage

from cdkg.representation import (
    santise_label_for_iri_resource,
    SOURCE_METADATA
)


def get_podcast_page_content(url: str) -> str:
    response = session.get(url)
    htmlparser = etree.HTMLParser()
    tree = etree.fromstring(response.text, htmlparser)
    text = tree.xpath('/html/head/meta[@name="description"]/@content')[0]
    return text


PODCAST = []

session = Session()

for index, row in enumerate(SOURCE_METADATA):
    podcast_url = row.get('Podcast').strip()
    speaker = row.get('Speaker').strip()
    if not podcast_url:
        continue

    # Textual work
    identifier = 'podcast' + '/' + str(index)
    label = podcast_url.split('/')[-1].replace('-', ' ').title()
    podcast = LinguisticObject(
        ident=identifier,
        label=label
    )
    podcast.classified_as = Type(
        ident='http://vocab.getty.edu/aat/300310137',
        label='Podcast'
    )

    # Creation
    actor_name = speaker.replace(' and ', ' & ')
    actor_resource = santise_label_for_iri_resource(speaker)
    actor_identifier = 'speaker' + '/' + actor_resource
    if '&' in actor_name:
        actor = Group(
            ident=actor_identifier,
            label=speaker
        )
    else:
        actor = Person(
            ident=actor_identifier,
            label=speaker
        )

    creation = Creation()
    creation.carried_out_by = actor
    podcast.created_by = creation

    # Homepage
    webpage = WebPage(label='Homepage')
    webpage.format = 'text/html'
    webpage.access_point = DigitalObject(ident=podcast_url)
    podcast_webpage_identifier = '/'.join([identifier, 'page', str(index)])
    webpage_text = LinguisticObject(
        ident=podcast_webpage_identifier,
        label=f'Textual content of homepage'
    )
    # webpage_text.content = get_podcast_page_content(podcast_url)
    webpage_text.digitally_carried_by = webpage
    podcast.subject_of = webpage_text

    PODCAST.append(podcast)
