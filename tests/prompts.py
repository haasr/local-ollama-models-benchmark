"""
Standardized benchmark prompts.
"""

BENCHMARK_PROMPTS = [

    {
        "name": "short_answer",
        "category": "general",
        "prompt": """
Explain photosynthesis to a first-year college student
in approximately 150 words. Be clear and concise.
""",
    },

    {
        "name": "reasoning",
        "category": "reasoning",
        "prompt": """
A classroom has 24 students.

Each student shakes hands exactly once with every
other student.

How many handshakes occur?

Explain how you arrive at your answer.
""",
    },

    {
        "name": "summarization",
        "category": "summarization",
        "prompt": """
Summarize the following paragraph in approximately
100 words:

Artificial intelligence systems can process large
amounts of information quickly, but their usefulness
depends heavily on the quality of the information
provided to them. A model can generate fluent and
confident responses while still producing incorrect
information. For this reason, users should treat
generated answers as outputs requiring verification,
particularly when the answers concern technical,
scientific, legal, financial, or medical subjects.
""",
    },

    {
        "name": "coding",
        "category": "coding",
        "prompt": """
Write a Python function called `find_duplicates`
that accepts a list of integers and returns a list
containing the values that occur more than once.

Do not use external libraries.

Include a short explanation of the algorithm.
""",
    },

    {
        "name": "structured_output",
        "category": "structured",
        "prompt": """
Return exactly five fictional university courses.

For each course provide:
- course_code
- course_name
- department
- credits

Return the result as valid JSON.
""",
    },

    {
        "name": "longer_generation",
        "category": "generation",
        "prompt": """
Write approximately 500 words explaining the
advantages and disadvantages of running a large
language model locally on a student's personal
computer rather than using a cloud-based AI service.
""",
    },
]
