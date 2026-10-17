"""
Evaluation script for Task 3 - runs a larger test set, reports accuracy,
and explicitly lists failure cases (as required by the task).
"""

from qa_engine import SmartFAQBot

TEST_CASES = [
    ("last date for paying fees", "semester fee deadline"),
    ("how do I see my attendance %", "ERP portal"),
    ("min attendance needed for exams", "75%"),
    ("library open and close time", "9 AM to 6 PM"),
    ("how to get bonafide letter", "bonafide certificate"),
    ("forgot my erp password", "Forgot Password"),
    ("documents for hostel", "admission letter"),
    ("dress code rules", "Formal attire"),
    ("how to join coding club", "coding club"),
    ("process for duplicate id card", "duplicate ID card"),
    ("letter proving I am a student here", "bonafide certificate"),  # known failure case
    ("", None),  # empty input -> error handling test
]


def main():
    bot = SmartFAQBot()
    correct, failures = 0, []

    for query, expected in TEST_CASES:
        result = bot.get_answer(query)
        if expected is None:
            # this is an edge-case / error-handling test, not an accuracy test
            print(f"[EDGE CASE] Query: {query!r} -> Status: {result['status']}, Answer: {result['answer']}")
            continue

        passed = expected.lower() in result["answer"].lower()
        correct += int(passed)
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] '{query}' -> {result['answer']} (score {result['score']})")
        if not passed:
            failures.append((query, expected, result["answer"], result["score"]))

    accuracy_cases = [t for t in TEST_CASES if t[1] is not None]
    accuracy = (correct / len(accuracy_cases)) * 100
    print(f"\nTop-1 Accuracy: {accuracy:.1f}% ({correct}/{len(accuracy_cases)})")

    print("\nFailure Cases:")
    if not failures:
        print("  None")
    else:
        for q, expected, got, score in failures:
            print(f"  Query: {q!r} | Expected: {expected} | Got: {got} | Score: {score}")


if __name__ == "__main__":
    main()
