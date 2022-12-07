from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, connections, Nested


class MoocArticle(Document):
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    body = Text(analyzer='snowball')
    tags = Keyword()
    length = Integer()

    class Index:
        name = 'mooccube'
        settings = {
            "number_of_shards": 2,
        }


class BaiduArticle(Document):
    name = Keyword()
    wiki_abstract = Text(index=False)
    google_translation = Text(index=False)
    properties = Keyword(),
    baidu_snippet_zh = Nested(properties={
        'title': Text(analyzer='ik_max_word'),
        'url': Text(index=False),
        'snippet': Text(index=False),
    })

    class Meta:
        doc_type = "doc"

    class Index:
        name = 'baidu_search_docs'
        using = 'es'


name2model = {
    "MoocArticle": MoocArticle,
    "BaiduArticle": BaiduArticle,
}
