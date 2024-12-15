import numpy as np
import onnxruntime
from huggingface_hub import hf_hub_download

def predict_phishing_probabilities(urls):
    if not urls:
        return {}
    REPO_ID = "pirocheto/phishing-url-detection"
    FILENAME = "model.onnx"
    model_path = hf_hub_download(repo_id=REPO_ID, filename=FILENAME)

    # Initializing the ONNX Runtime session with the pre-trained model
    sess = onnxruntime.InferenceSession(
        model_path,
        providers=["CPUExecutionProvider"],
    )

    inputs = np.array(urls, dtype="str")

    # Using the ONNX model to make predictions on the input data
    results = sess.run(None, {"inputs": inputs})[1]

    probabilities = {}
    for url, proba in zip(urls, results):
        probabilities[url] = proba[1] * 100

    return probabilities

# Example usage
urls = [
    "https://amzn.com/0132390779",
    "http://www.medicalnewstoday.com/articles/188939.php",
]
probabilities = predict_phishing_probabilities(urls)
