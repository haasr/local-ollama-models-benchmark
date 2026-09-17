# Ollama Local LLM Benchmark

**Disclaimer**: 100% ChatGPT vibed repo. Just need trying to do a quick & dirty lab benchmark.

A small, repeatable benchmark harness for testing local Large Language Models (LLMs) using [Ollama](https://ollama.com/).

The benchmark is designed for running the **same test suite on multiple computers in parallel**. Each computer can select a different model, allowing us to compare model performance while reducing the effects of machine-to-machine variation.

---

## Project Structure

```text
ollama-benchmark/
│
├── driver.py
├── run.ps1
│
├── models/
│   ├── __init__.py
│   └── ollama_model_test.py
│
├── tests/
│   ├── __init__.py
│   └── prompts.py
│
└── results/
```

### `driver.py`

The main benchmark launcher.

It provides a menu for selecting which model to test and then hands the test off to the appropriate benchmark class.

### `run.ps1`

The recommended entry point on Windows.

It:

1. Checks that Python is installed.
2. Creates `.venv` if necessary.
3. Makes sure `pip` is available.
4. Installs the Python `ollama` package if necessary.
5. Launches `driver.py`.

### `models/`

Contains the model-specific benchmark implementations.

### `tests/`

Contains the standardized prompts used by the benchmark.

### `results/`

Benchmark results are saved here as both JSON and CSV files.

---

# Requirements

## Hardware

The benchmark is intended primarily for testing computers capable of running local LLMs.

The initial target hardware is:

- Dell OptiPlex 5090
- 11th-generation Intel Core i7
- 16 GB DDR4 RAM

The benchmark can also be used on personal Windows PCs, gaming laptops, and Macs running Ollama.

---

## Software

You will need:

- Python 3.10 or newer
- Ollama
- At least one Ollama model

Ollama must be installed separately from this Python project.

The Python `ollama` package is only the Python client used to communicate with the local Ollama installation.

---

# Running the Benchmark

## Windows

Open PowerShell in the project directory and run:

```powershell
.\run.ps1
```

The first run may take a little longer because the script creates the Python virtual environment and installs the required Python package.

After that, running the script should be quick.

You should see a menu similar to:

```text
============================================================
 Ollama Local LLM Benchmark
============================================================

Select the model to test:

  1. Llama 3.2 3B             llama3.2:3b
  2. Qwen 3 4B                qwen3:4b
  3. Qwen 3 8B                qwen3:8b
  4. Llama 3.1 8B             llama3.1:8b
  5. Gemma 3 4B               gemma3:4b

  Q. Quit

Selection:
```

Select the model you want to benchmark.

If the selected model is not installed, the benchmark will offer to download it.

---

# Running Multiple Computers

The benchmark is specifically designed to make parallel testing easy.

For example, suppose you have five OptiPlex computers:

```text
OPT-01 → llama3.2:3b
OPT-02 → qwen3:4b
OPT-03 → qwen3:8b
OPT-04 → llama3.1:8b
OPT-05 → gemma3:4b
```

Run the benchmark on each computer and select the appropriate model.

Each computer will run the same standardized prompt suite and save its results locally.

This is preferable to running all models sequentially on one computer because loading and unloading multiple models can affect available RAM and system state.

---

# What Is Being Measured?

The benchmark records several performance measurements for each prompt.

### Generation speed

The primary measurement is **output tokens per second**.

This represents how quickly the model generates its response after processing the prompt.

### Prompt processing speed

The benchmark also records the number of prompt tokens processed and the time required to process them.

### Total response time

The complete elapsed time for the request is recorded as well.

### Model output

The generated response is saved in the JSON results file.

This makes it possible to inspect the actual responses later rather than relying solely on numerical performance measurements.

---

# Benchmark Tasks

The initial benchmark contains several different workloads:

| Test | Purpose |
|---|---|
| Short Answer | General conversational generation |
| Reasoning | Basic multi-step reasoning |
| Summarization | Processing and condensing supplied text |
| Coding | Python code generation |
| Structured Output | Generating structured JSON |
| Longer Generation | Sustained text generation |

The same prompts are used for every model so that results can be compared more consistently.

---

# Results

Each benchmark run creates two files in `results/`.

For example:

```text
OPT-03_qwen3_8b_20260917_143512.json
OPT-03_qwen3_8b_20260917_143512.csv
```

## CSV

The CSV contains the numerical benchmark results and is intended for later analysis in Excel, Python, or another data-analysis tool.

## JSON

The JSON contains:

- Computer information
- Model information
- Benchmark summary
- Individual prompt results
- Generated responses

The JSON file is therefore useful when we want to inspect **what the model actually produced**, rather than just how quickly it produced it.

---

# Important: Keep the Machines Idle

For meaningful benchmark results, try to keep the test computer otherwise idle.

Avoid running:

- Web browsers with many tabs
- Other AI applications
- Large software builds
- Video editing
- Games
- Other CPU/GPU-intensive programs

The goal is to measure the LLM workload rather than competition from unrelated applications.

---

# Experimental Design

This benchmark is intended to answer questions such as:

> How much faster/slower is an 8B model than a 4B model on our lab hardware?

and:

> At what model size does the student experience become noticeably slow?

The benchmark should therefore be run under reasonably consistent conditions.

When possible:

1. Use the same hardware configuration.
2. Use the same model version.
3. Use the same benchmark prompts.
4. Run only one benchmark at a time on each computer.
5. Keep background applications to a minimum.
6. Record any unusual conditions.

Results from different hardware configurations should not automatically be treated as directly equivalent.

---

# Adding a Model

Models are currently defined in `driver.py`.

Add a new entry to the `MODELS` dictionary:

```python
MODELS = {
    "1": {
        "name": "llama3.2:3b",
        "description": "Llama 3.2 3B",
    },

    "2": {
        "name": "qwen3:4b",
        "description": "Qwen 3 4B",
    },

    # Add another model here.
}
```

The `name` must match the model name recognized by Ollama.

For example:

```bash
ollama list
```

can be used to see the models currently installed on a computer.

---

# Adding Benchmark Tasks

Benchmark prompts are defined in:

```text
tests/prompts.py
```

A new task can be added to `BENCHMARK_PROMPTS`:

```python
{
    "name": "my_test",
    "category": "coding",
    "prompt": """
    Your standardized benchmark prompt goes here.
    """,
},
```

Try to keep benchmark prompts deterministic and reasonably representative of the workloads we actually care about.

---

# Future Improvements

The benchmark is intentionally structured so that additional measurements can be added without changing the basic workflow.

Potential future measurements include:

- Peak RAM usage
- CPU utilization
- CPU temperature
- GPU utilization
- GPU memory usage
- Model loading time
- Time to first token
- Generation speed over time
- Context-length performance
- Power consumption
- Automated response-quality evaluation

These measurements will allow us to distinguish between:

**"The computer can technically run the model."**

and

**"The computer provides a useful interactive experience with the model."**

The second question is ultimately the more important one for determining which models to recommend to students.