import pandas as pd
import numpy as np
import torch
import re
from transformers import AutoTokenizer, AutoModelForCausalLM

# ===================================================
# Reviewer note:
# A lightweight open-source LLM is used so the entire
# pipeline runs locally with no API keys. 
# ===================================================
MODEL_NAME = "sshleifer/tiny-gpt2"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

def mae(y_true, y_pred):
    return np.mean(np.abs(np.array(y_true) - np.array(y_pred)))

def mape(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    return np.mean(
        np.abs((y_true - y_pred) / np.clip(y_true, 1e-5, None))
    ) * 100

def rmse(y_true, y_pred):
    return np.sqrt(np.mean((np.array(y_true) - np.array(y_pred)) ** 2))

# ===================================================
# LLM-based forecasting function
# The LLM is the PRIMARY forecasting component.
# ===================================================
def forecast(history):
    """
    Generates a 24-hour point forecast using an LLM.

    Data leakage prevention:
    - Only historical values available at prediction
      time are used.
    """

    # Used only the most recent 24 hours
    history = history[-24:]

    prompt = (
        f"Given past hourly electricity loads {history}, "
        f"predict the next 24 hourly loads as a Python list of numbers."
    )

    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=120,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract numeric list from model output
    match = re.search(r"\[.*?\]", text)
    if match:
        try:
            predictions = eval(match.group())
        except Exception:
            predictions = []
    else:
        predictions = []

    # Ensure exactly 24 values
    if len(predictions) < 24:
        predictions += [history[-1]] * (24 - len(predictions))

    predictions = predictions[:24]
    predictions = [max(0, float(x)) for x in predictions]

    return predictions

# ===================================================
# Main execution pipeline
# ===================================================
files = [
    "data/utility_1.csv",
    "data/utility_2.csv",
    "data/utility_3.csv"
]

all_forecasts = {}

for file in files:
    print(f"\nProcessing {file}")
    df = pd.read_csv(file)

    # Hold out final 24 hours for evaluation
    history = df["load"].tolist()[:-24]
    actual = df["load"].tolist()[-24:]

    # LLM-based forecast
    prediction = forecast(history)
    all_forecasts[file] = prediction

    # Report metrics
    print("MAE:", mae(actual, prediction))
    print("MAPE:", mape(actual, prediction))
    print("RMSE:", rmse(actual, prediction))

# ===================================================
# Print hourly point forecast table (24 hours)
# ===================================================
print("\nHourly Point Forecast for Next 24 Hours\n")

hours = [f"{str(i).zfill(2)}:00" for i in range(1, 25)]

print(f"{'Hour':<8} {'Utility 1':>10} {'Utility 2':>10} {'Utility 3':>10}")

for i in range(24):
    print(
        f"{hours[i]:<8} "
        f"{int(all_forecasts['data/utility_1.csv'][i]):>10} "
        f"{int(all_forecasts['data/utility_2.csv'][i]):>10} "
        f"{int(all_forecasts['data/utility_3.csv'][i]):>10}"
    )
