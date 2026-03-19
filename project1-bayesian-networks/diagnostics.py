import json
import urllib.request
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE")

class Diagnostics:

    def __init__(self):
        self.system_prompt = """You are a Bayesian network inference engine. Given the following evidence, compute the most likely disease using the Asia Bayesian Network below.

CONDITIONAL PROBABILITY TABLES:
- P(Asia=True) = 0.01
- P(Smoking=True) = 0.5
- P(TB=True | Asia=True) = 0.05, P(TB=True | Asia=False) = 0.01
- P(Cancer=True | Smoking=True) = 0.10, P(Cancer=True | Smoking=False) = 0.01
- P(Bronchitis=True | Smoking=True) = 0.60, P(Bronchitis=True | Smoking=False) = 0.30
- P(TBorC=True | TB=True OR Cancer=True) = 1.0, P(TBorC=True | TB=False AND Cancer=False) = 0.0
- P(Xray=True | TBorC=True) = 0.99, P(Xray=True | TBorC=False) = 0.05
- P(Dyspnea=True | TBorC=True, Bronchitis=True) = 0.9
- P(Dyspnea=True | TBorC=True, Bronchitis=False) = 0.7
- P(Dyspnea=True | TBorC=False, Bronchitis=True) = 0.8
- P(Dyspnea=True | TBorC=False, Bronchitis=False) = 0.1

Return ONLY a JSON object, nothing else:
{"disease": "TB" or "Cancer" or "Bronchitis", "probability": <float between 0 and 1>}

The disease field must be exactly "TB", "Cancer", or "Bronchitis" — the one with the highest posterior probability."""

    def diagnose(self, asia, smoking, xray, dyspnea):
        # helper function to convert strings to boolean or None
        def translate(value):
            match value:
                case "Yes" | "Abnormal" | "Present":
                    return True
                case "No" | "Normal" | "Absent":
                    return False
                case "NA":
                    return None

        # Translating inputs
        asia_val = translate(asia)
        smoking_val = translate(smoking)
        xray_val = translate(xray)
        dyspnea_val = translate(dyspnea)

        # Creating evidence dictionary
        evidence = {}
        if asia_val is not None:
            evidence['Asia'] = asia_val
        if smoking_val is not None:
            evidence['Smoking'] = smoking_val
        if xray_val is not None:
            evidence['Xray'] = xray_val
        if dyspnea_val is not None:
            evidence['Dyspnea'] = dyspnea_val

        print(f"Evidence dict: {evidence}")

        # Build the prompt
        prompt = self.system_prompt + f"\n\nEVIDENCE: {evidence}\n\nReturn ONLY the JSON object."

        # Call the Gemini API
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key={API_KEY}"

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req) as response:
                response_data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
            raise

        raw_text = response_data["candidates"][0]["content"]["parts"][0]["text"].strip()
        print(f"Gemini response: {raw_text}")

        # Strip markdown fences if present
        if raw_text.startswith("```"):
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]
            raw_text = raw_text.strip()

        # Parse result
        result = json.loads(raw_text)
        best_disease = result["disease"]
        best_prob = float(result["probability"])

        print(f"Diagnosis: {best_disease} with probability {best_prob:.4f}")

        return [best_disease, best_prob]