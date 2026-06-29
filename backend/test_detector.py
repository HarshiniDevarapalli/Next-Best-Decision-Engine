from backend.services.weak_signal.llm_detector import LLMWeakSignalDetector

detector = LLMWeakSignalDetector()

transcript = """
Customer said they are considering Salesforce.

Budget has been reduced by 25%.

Renewal is in 18 days.

Product adoption has been declining.

Customer requested executive involvement.
"""

report = detector.predict(transcript)

print(report.model_dump_json(indent=4))