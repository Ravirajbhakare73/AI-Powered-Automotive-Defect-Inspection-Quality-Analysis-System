import os

from dotenv import load_dotenv
from google import genai

from backend.services.rag import search_knowledge


# Load variables from the project's .env file
load_dotenv()


class AutomotiveDefectAgent:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=api_key
        )

    def analyze(
        self,
        defect: str,
        confidence: float
    ):

        # ------------------------------------------------
        # 1. Retrieve relevant automotive knowledge
        # ------------------------------------------------

        query = f"""
Automotive manufacturing quality analysis.

Detected defect:
{defect}

Confidence:
{confidence}

Find information about:
possible causes,
diagnostic investigation,
fixtures,
tooling,
handling,
contamination,
process variation,
and corrective actions.
"""

        knowledge = search_knowledge(
            query=query,
            top_k=3
        )

        # ------------------------------------------------
        # 2. Prepare RAG context
        # ------------------------------------------------

        if knowledge:

            context = "\n\n".join(
                knowledge
            )

        else:

            context = (
                "No relevant knowledge was retrieved."
            )

        # ------------------------------------------------
        # 3. Gemini prompt
        # ------------------------------------------------

        prompt = f"""
You are an automotive manufacturing
quality-analysis AI assistant.

A computer vision system detected:

Defect:
{defect}

Detection confidence:
{confidence:.2%}

Relevant knowledge retrieved from the
automotive quality knowledge base:

---------------- KNOWLEDGE ----------------

{context}

-------------- END KNOWLEDGE --------------

Analyze the inspection result.

Return the following sections:

1. Detected Defect
2. Observation
3. Likely Root-Cause Candidates
4. Diagnostic Investigation
5. Recommended Corrective Actions
6. Process Improvement Recommendation
7. Priority
8. Additional Investigation Required

Important rules:

- The vision model detects the visible defect.
- Do NOT claim that a root cause is confirmed.
- Treat root causes as hypotheses.
- Recommend physical/process verification.
- Base the analysis primarily on the retrieved knowledge.
- Do not invent manufacturing facts that are not supported
  by the retrieved knowledge.
- Keep the answer practical for an automotive quality
  inspection environment.
"""

        # ------------------------------------------------
        # 4. Generate AI analysis
        # ------------------------------------------------

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        # ------------------------------------------------
        # 5. Return result
        # ------------------------------------------------

        return {
            "defect": defect,
            "confidence": confidence,
            "analysis": response.text,
            "sources": knowledge
        }