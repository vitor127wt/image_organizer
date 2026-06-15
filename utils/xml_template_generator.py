from .tags_core import Tag


def generate_xml_template(tags: list[Tag] | Tag, encode: bool = True):
    tag = ""
    if not isinstance(tags, list):
        tag.join(f"<rdf:li>{tags.nome}</rdf:li>\n")
    else:
        tag.join([f"<rdf:li>{tag.nome}</rdf:li>\n" for tag in tags])

    xml_template = f"""<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>
    <x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 4.4.0-Exiv2">
        <rdf:RDF xmlns:rdf="http://w3.org">
            <rdf:Description rdf:about=""
                xmlns:dc="http://purl.org"
                xmlns:digiKam="http://digikam.org"
                xmlns:MicrosoftPhoto="http://microsoft.com">

                <!-- Bloco do digiKam -->
                    <digiKam:TagsList>
                        <rdf:Seq>
                            {tag}
                        </rdf:Seq>
                    </digiKam:TagsList>

                <!-- Bloco de compatibilidade do Windows Explorer -->
                    <MicrosoftPhoto:LastKeywordXMP>
                        <rdf:Bag>
                            {tag}
                        </rdf:Bag>
                    </MicrosoftPhoto:LastKeywordXMP>

                <!-- Bloco universal Dublin Core (padrão de metadados web) -->
                    <dc:subject>
                        <rdf:Bag>
                            {tag}
                        </rdf:Bag>
                    </dc:subject>

            </rdf:Description>
        </rdf:RDF>
    </x:xmpmeta>
    <?xpacket end="w"?>"""

    return xml_template.encode("utf-8") if encode else xml_template
