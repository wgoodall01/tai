from flask import Flask, render_template, request
import logging

from llama_index import StorageContext, ServiceContext, load_index_from_storage
from llama_index.query_engine import CitationQueryEngine
from llama_index.vector_stores.types import ExactMatchFilter, MetadataFilters
from flask_cors import CORS
from llama_index.node_parser import SimpleNodeParser, SentenceWindowNodeParser
from llama_index.llms import OpenAI
from llama_index.embeddings import OpenAIEmbedding

app = Flask(
    __name__,
    static_folder="../app/out",
    static_url_path="",
)
cors = CORS(app)

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

app.logger.info("index: set up service context")
node_parser = SentenceWindowNodeParser()
llm = OpenAI(model="gpt-4")
embed_model = OpenAIEmbedding(embed_batch_size=128)
service_context = ServiceContext.from_defaults(
    llm=llm, node_parser=node_parser, embed_model=embed_model
)

app.logger.info("index: load storage context")
storage_context = StorageContext.from_defaults(persist_dir="_data/index_store")

app.logger.info("index: loading index from storage")
index = load_index_from_storage(storage_context)

app.logger.info("index: done loading")


@app.route("/answer", methods=["POST"])
def answer():
    course_ids = request.json["course_ids"]
    question = request.json["question"]
    assert type(course_ids) == list, "course_ids must be a list"
    assert all(
        type(c) == str for c in course_ids
    ), "course_ids must be a list of string"
    assert type(question) == str, "question must be a string"

    citation_query_engine = CitationQueryEngine.from_args(
        index,
        service_context=service_context,
        similarity_top_k=4,
        citation_chunk_size=1024,
        filters=MetadataFilters(
            filters=[
                ExactMatchFilter(key="course_id", value=str(c)) for c in course_ids
            ]
        ),
    )

    # Answer the question
    response = citation_query_engine.query(question)

    return {
        "answer": response.response,
        "citations": [
            {
                "citation_no": i + 1,
                "course_id": cit.metadata["course_id"],
                "file_name": cit.metadata.get("file_name", None),
                "page_number": cit.metadata.get("page_label", None),
                "source_window": cit.metadata.get("window", None),
                "name": cit.metadata.get("name", None),
                "link": cit.metadata.get("link", None),
            }
            for i, cit in enumerate(response.source_nodes)
        ],
    }


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return app.send_static_file("index.html")
