#!/usr/bin/env python3
import json


def main() -> None:
    print(
        json.dumps(
            {
                "status": "success",
                "answer": "Sample answer from a compliant contest submission.",
                "actions_taken": ["validated_input", "returned_structured_output"],
                "errors_recovered": 0,
                "trace_id": "sample-trace",
            }
        )
    )


if __name__ == "__main__":
    main()
