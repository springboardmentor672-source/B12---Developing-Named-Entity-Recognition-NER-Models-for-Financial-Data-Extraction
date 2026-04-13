import os
import textwrap
from pathlib import Path
import langextract as lx
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env")
API_KEY = os.getenv("LANGEXTRACT_API_KEY")

PROMPT = textwrap.dedent("""\
    Extract financial entities and key information in order of appearance.
    Use exact text for extractions. Do not paraphrase or overlap entities.
    Provide meaningful attributes for each entity to add context.""")

EXAMPLES = [
    lx.data.ExampleData(
        text="Apple Inc. reported a quarterly revenue of $117.9 billion, up 11% from the previous year.",
        extractions=[
            lx.data.Extraction(
                extraction_class="organization",
                extraction_text="Apple Inc.",
                attributes={"type": "technology company"}
            ),
            lx.data.Extraction(
                extraction_class="financial_metric",
                extraction_text="$117.9 billion",
                attributes={"metric_type": "quarterly revenue", "trend": "positive"}
            ),
            lx.data.Extraction(
                extraction_class="growth_rate",
                extraction_text="up 11%",
                attributes={"period": "year-over-year", "direction": "increase"}
            ),
        ]
    )
]
def extract_financial_info(
    text: str,
    model_id: str = "gemini-3-flash-preview",
    extraction_passes: int = 1,
    max_workers: int = 5,
    save_results: bool = False,
    output_name: str = "finance_extraction_results",
    output_dir: str = str(BASE_DIR)
) -> dict:
    """
    Extract structured financial information from text using LangExtract + Gemini AI.

    Args:
        text (str): Input financial text or document URL.
        model_id (str): Gemini model to use (default: gemini-3-flash-preview).
        extraction_passes (int): Number of extraction passes for better recall.
        max_workers (int): Parallel workers for large documents.
        save_results (bool): Save results to JSONL file.
        output_name (str): Output file name (without extension).
        output_dir (str): Directory to save results.

    Returns:
        dict: Extracted entities with class, text, attributes, and positions.
    """
    result = lx.extract(
        text_or_documents=text,
        prompt_description=PROMPT,
        examples=EXAMPLES,
        model_id=model_id,
        api_key=API_KEY,
        extraction_passes=extraction_passes,
        max_workers=max_workers,
    )
 # Optionally save results to JSONL
    if save_results:
        lx.io.save_annotated_documents(
            [result],
            output_name=output_name,
            output_dir=output_dir
        )
        print(f"Results saved to {output_dir}/{output_name}.jsonl")

    entities = []
    if hasattr(result, "extractions"):
        for extraction in result.extractions:
            entities.append({
                "class": extraction.extraction_class,
                "text": extraction.extraction_text,
                "attributes": extraction.attributes if extraction.attributes else {}
            })

    return {
        "total_entities": len(entities),
        "entities": entities
    }


def generate_visualization(jsonl_path: str, output_html: str = "visualization.html"):
    """
    Generate an interactive HTML visualization from a JSONL results file.

    Args:
        jsonl_path (str): Path to the JSONL results file.
        output_html (str): Output HTML file name.
    """
    html_content = lx.visualize(jsonl_path)
    with open(output_html, "w") as f:
        if hasattr(html_content, "data"):
            f.write(html_content.data) 
        else:
            f.write(html_content)
    print(f"Visualization saved to {output_html}")

if __name__ == "__main__":
    sample_text = """
    Apple Inc. reported a quarterly revenue of $117.9 billion, up 11% from the previous year.
    The company's stock price surged to $150 per share following the announcement.
    Meanwhile, Tesla's market capitalization reached $600 billion after unveiling its new electric vehicle model.
    Investors are closely watching the Federal Reserve's interest rate decisions,
    which could impact bond yields and inflation rates.
    In other news, JPMorgan Chase & Co. acquired a fintech startup for $1.2 billion
    to enhance its digital banking services.
    """

    results = extract_financial_info(
        text=sample_text,
        model_id="gemini-3-flash-preview",
        save_results=True,            
        output_name="finance_results",
        output_dir=str(BASE_DIR)
    )

    print(f"\nTotal Entities Found: {results['total_entities']}")
    print("-" * 50)
    for entity in results["entities"]:
        print(f"Class     : {entity['class']}")
        print(f"Text      : {entity['text']}")
        print(f"Attributes: {entity['attributes']}")
        print("-" * 50)

    # Generate HTML visualization (uncomment to use)
    generate_visualization("finance_results", "finance_visualization.html")