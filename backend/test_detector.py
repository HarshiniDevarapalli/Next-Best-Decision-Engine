from services.weak_signal.llm_detector import LLMWeakSignalDetector

detector = LLMWeakSignalDetector()

transcript = """
Customer said they are evaluating Salesforce.
They also mentioned budget cuts next quarter.
Usage has been declining.
Renewal is in three weeks.
"""

report = detector.predict(transcript)

print(report.model_dump_json(indent=4))