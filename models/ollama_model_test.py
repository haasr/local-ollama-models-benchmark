"""
Ollama model benchmark implementation.
"""

import csv
import json
import platform
import socket
import statistics
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

import ollama

from tests.prompts import BENCHMARK_PROMPTS


class OllamaModelTest:
    """
    Runs a standardized benchmark against one Ollama model.

    One instance represents one model test on one computer.
    """

    def __init__(self, model_name: str, results_dir: Path):
        self.model_name = model_name
        self.results_dir = results_dir

        self.hostname = socket.gethostname()

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def run(self):
        self._print_header()

        self._check_ollama()
        self._ensure_model()

        system_info = self._collect_system_info()

        print()
        print("Running benchmark...")
        print()

        results = []

        for index, prompt in enumerate(BENCHMARK_PROMPTS, start=1):
            print(
                f"[{index}/{len(BENCHMARK_PROMPTS)}] "
                f"{prompt['name']}"
            )

            result = self._run_prompt(prompt)

            results.append(result)

            self._print_result(result)

        summary = self._calculate_summary(results)

        self._save_results(
            system_info=system_info,
            results=results,
            summary=summary,
        )

        self._print_summary(summary)

    # ---------------------------------------------------------
    # Setup
    # ---------------------------------------------------------

    def _check_ollama(self):
        print("Checking Ollama...")

        try:
            ollama.list()
        except Exception as exc:
            raise RuntimeError(
                "Could not connect to Ollama. "
                "Make sure Ollama is running."
            ) from exc

        print("Ollama connection OK.")

    def _ensure_model(self):
        print(f"Checking model: {self.model_name}")

        models = ollama.list()

        installed = {
            model["name"]
            for model in models["models"]
        }

        if self.model_name not in installed:
            print()
            print(
                f"Model '{self.model_name}' is not installed."
            )

            answer = input(
                "Download it now? [y/N]: "
            ).strip().lower()

            if answer != "y":
                raise RuntimeError(
                    f"Model '{self.model_name}' is required."
                )

            print()
            print(f"Pulling {self.model_name}...")

            ollama.pull(self.model_name)

        print("Model available.")

    # ---------------------------------------------------------
    # Benchmark
    # ---------------------------------------------------------

    def _run_prompt(self, prompt_definition):
        prompt = prompt_definition["prompt"]

        start_time = time.perf_counter()

        response = ollama.generate(
            model=self.model_name,
            prompt=prompt,
            stream=False,
            options={
                # Keep the test reasonably consistent.
                "temperature": 0,
            },
        )

        elapsed = time.perf_counter() - start_time

        response_text = response["response"]

        eval_count = response.get("eval_count", 0)
        eval_duration_ns = response.get("eval_duration", 0)

        prompt_eval_count = response.get(
            "prompt_eval_count",
            0,
        )

        prompt_eval_duration_ns = response.get(
            "prompt_eval_duration",
            0,
        )

        if eval_duration_ns:
            output_tokens_per_second = (
                eval_count
                / (eval_duration_ns / 1_000_000_000)
            )
        else:
            output_tokens_per_second = 0

        if prompt_eval_duration_ns:
            prompt_tokens_per_second = (
                prompt_eval_count
                / (prompt_eval_duration_ns / 1_000_000_000)
            )
        else:
            prompt_tokens_per_second = 0

        return {
            "prompt_name": prompt_definition["name"],
            "category": prompt_definition["category"],
            "elapsed_seconds": elapsed,
            "eval_count": eval_count,
            "prompt_eval_count": prompt_eval_count,
            "output_tokens_per_second": output_tokens_per_second,
            "prompt_tokens_per_second": prompt_tokens_per_second,
            "response": response_text,
        }

    # ---------------------------------------------------------
    # System information
    # ---------------------------------------------------------

    def _collect_system_info(self):
        return {
            "hostname": self.hostname,
            "timestamp_utc": datetime.now(
                timezone.utc
            ).isoformat(),

            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),

            "python_version": platform.python_version(),

            "ollama_model": self.model_name,
        }

    # ---------------------------------------------------------
    # Results
    # ---------------------------------------------------------

    def _calculate_summary(self, results):
        speeds = [
            r["output_tokens_per_second"]
            for r in results
            if r["output_tokens_per_second"] > 0
        ]

        elapsed = [
            r["elapsed_seconds"]
            for r in results
        ]

        return {
            "average_output_tokens_per_second": (
                statistics.mean(speeds)
                if speeds else 0
            ),

            "median_output_tokens_per_second": (
                statistics.median(speeds)
                if speeds else 0
            ),

            "min_output_tokens_per_second": (
                min(speeds)
                if speeds else 0
            ),

            "max_output_tokens_per_second": (
                max(speeds)
                if speeds else 0
            ),

            "average_elapsed_seconds": (
                statistics.mean(elapsed)
                if elapsed else 0
            ),

            "total_elapsed_seconds": sum(elapsed),

            "num_prompts": len(results),
        }

    def _save_results(
        self,
        system_info,
        results,
        summary,
    ):
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        safe_model = (
            self.model_name
            .replace(":", "_")
            .replace("/", "_")
        )

        base_name = (
            f"{self.hostname}_"
            f"{safe_model}_"
            f"{timestamp}"
        )

        json_path = self.results_dir / (
            f"{base_name}.json"
        )

        csv_path = self.results_dir / (
            f"{base_name}.csv"
        )

        output = {
            "system": system_info,
            "model": self.model_name,
            "summary": summary,
            "prompts": results,
        }

        with open(
            json_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                output,
                file,
                indent=2,
            )

        self._write_csv(csv_path, results)

        print()
        print(f"Results written to:")
        print(f"  {json_path}")
        print(f"  {csv_path}")

    def _write_csv(self, path, results):
        fieldnames = [
            "prompt_name",
            "category",
            "elapsed_seconds",
            "prompt_eval_count",
            "eval_count",
            "prompt_tokens_per_second",
            "output_tokens_per_second",
        ]

        with open(
            path,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames,
            )

            writer.writeheader()

            for result in results:
                writer.writerow({
                    key: result.get(key)
                    for key in fieldnames
                })

    # ---------------------------------------------------------
    # Console output
    # ---------------------------------------------------------

    def _print_header(self):
        print()
        print("=" * 60)
        print(" Ollama Model Benchmark")
        print("=" * 60)
        print()
        print(f"Computer : {self.hostname}")
        print(f"Model    : {self.model_name}")
        print()

    def _print_result(self, result):
        print(
            f"    Time: "
            f"{result['elapsed_seconds']:.2f}s"
        )

        print(
            f"    Output: "
            f"{result['output_tokens_per_second']:.2f} tok/s"
        )

        print()

    def _print_summary(self, summary):
        print()
        print("=" * 60)
        print(" Benchmark Summary")
        print("=" * 60)
        print()

        print(
            "Average output speed : "
            f"{summary['average_output_tokens_per_second']:.2f} tok/s"
        )

        print(
            "Median output speed  : "
            f"{summary['median_output_tokens_per_second']:.2f} tok/s"
        )

        print(
            "Slowest               : "
            f"{summary['min_output_tokens_per_second']:.2f} tok/s"
        )

        print(
            "Fastest               : "
            f"{summary['max_output_tokens_per_second']:.2f} tok/s"
        )

        print(
            "Total test time       : "
            f"{summary['total_elapsed_seconds']:.2f}s"
        )

        print()
