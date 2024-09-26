'''
Generate and persist Linked Art representations.
'''

import json
import requests

from argparse import ArgumentParser
from pathlib import Path

from cromulent.model import factory
from rdflib import Graph


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument(
        '-b',
        '--base',
        type=str,
        default='https://example.org/cdkg/'
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str
    )
    args = parser.parse_args()

    if args.output:
        out_path = Path(args.output)
    else:
        package_dir = Path(__file__).parent.parent.parent
        out_path = package_dir / 'data/domain/base/'

    factory.base_url = args.base
    factory.base_dir = str(out_path)
    factory.auto_assign_id = False

    from cdkg.representation import base, extra

    partitions = [
        base.ACTIVITY,
        base.DIGITAL,
        base.EVENT,
        base.GROUP,
        base.PERSON,
        base.PODCAST,
        base.SET,
        base.TEXT,
        base.VISUAL
    ]

    context_cache = None        
    graph = Graph()

    for partition in partitions:
        for representation in partition:
            iri = representation.id
            resource = iri.split(args.base)[-1]

            if resource in extra.EXTRA:
                for extensions in extra.EXTRA[resource]:
                    for extension, obj in extensions.items():
                        setattr(representation, extension, obj)

            factory.toFile(representation, compact=False)
            graph_str = factory.toString(representation, compact=False)
            graph_json = json.loads(graph_str)

            if context_cache is None:
                context_iri = graph_json['@context']
                response = requests.get(context_iri)
                context_cache = response.json()
            else:
                graph_json['@context'] = context_cache

            graph.parse(
                data=json.dumps(graph_json),
                format='json-ld'
            )

    graph_path = out_path / 'base'
    graph.serialize(
        destination=graph_path.with_name('cdkg.ttl'),
        format='longturtle'
    )
