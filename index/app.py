from flask import Flask, render_template, request
from llama_index import StorageContext, load_index_from_storage
from llama_index.query_engine import CitationQueryEngine
from llama_index.vector_stores.types import ExactMatchFilter, MetadataFilters

print("index: loading storage context")
storage_context = StorageContext.from_defaults(persist_dir="_data/index_store")

print("index: loading index from storage")
index = load_index_from_storage(storage_context)

print("index: done loading")

app = Flask(__name__)


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
                "citation_no": i,
                "file_name": cit.metadata["file_name"],
                "course_id": cit.metadata["course_id"],
                "page_number": cit.metadata["page_label"],
                "source_window": cit.metadata["window"],
            }
            for i, cit in enumerate(response.source_nodes)
        ],
    }
