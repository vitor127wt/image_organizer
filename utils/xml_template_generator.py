import textwrap as tw

from .tags_core import Tag


def generate_xml_template(tags: list[Tag] | Tag, encode: bool = True):
    if not isinstance(tags, list):
        tag = "".join(f"<rdf:li>{tags.nome}</rdf:li>")
    else:
        tag = "\n".join([f"<rdf:li>{tag.nome}</rdf:li>" for tag in tags])

    def generate_indent(indent: int):
        return "    " * indent

    xml_template = f"""<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>
    <x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 4.4.0-Exiv2">
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
            <rdf:Description rdf:about=""
                xmlns:dc="http://purl.org/dc/elements/1.1/"
                xmlns:digiKam="http://www.digikam.org/ns/1.0/"
                xmlns:MicrosoftPhoto="http://ns.microsoft.com/photo/1.0/">
                <digiKam:TagsList>
                    <rdf:Seq>
{tw.indent(tag, f"{generate_indent(6)}")}
                    </rdf:Seq>
                </digiKam:TagsList>
                <MicrosoftPhoto:LastKeywordXMP>
                    <rdf:Bag>
{tw.indent(tag, f"{generate_indent(6)}")}
                    </rdf:Bag>
                </MicrosoftPhoto:LastKeywordXMP>
                <dc:subject>
                    <rdf:Bag>
{tw.indent(tag, f"{generate_indent(6)}")}
                    </rdf:Bag>
                </dc:subject>
            </rdf:Description>
        </rdf:RDF>
    </x:xmpmeta>
    <?xpacket end="w"?>"""

    if encode:
        return xml_template.encode("utf-8")
    return xml_template
