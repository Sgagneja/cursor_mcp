import asyncio
from dotenv import load_dotenv
from linkup import LinkupClient
from rag import RAGWorkflow
from mcp.server.fastmcp import FastMCP
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

logger.info("Initializing MCP server components...")
mcp = FastMCP('cursor-mcp-server')
client = LinkupClient()
rag_workflow = RAGWorkflow()
logger.info("MCP server components initialized")

@mcp.tool()
def web_search(query: str) -> str:
    """Search the web for the given query."""
    logger.info(f"Received web search query: {query}")
    search_response = client.search(
        query=query,
        depth="standard",  # "standard" or "deep"
        output_type="sourcedAnswer",  # "searchResults" or "sourcedAnswer" or "structured"
        structured_output_schema=None,  # must be filled if output_type is "structured"
    )
    return search_response

@mcp.tool()
async def rag(query: str) -> str:
    """Use a simple RAG workflow to answer queries using documents from data directory about Deep Seek"""
    logger.info(f"Received RAG query: {query}")
    response = await rag_workflow.query(query)
    return str(response)

if __name__ == "__main__":
    logger.info("Starting document ingestion...")
    asyncio.run(rag_workflow.ingest_documents("data"))
    logger.info("Document ingestion complete")
    logger.info("Starting MCP server with stdio transport...")
    mcp.run(transport="stdio")
    logger.info("MCP server started")