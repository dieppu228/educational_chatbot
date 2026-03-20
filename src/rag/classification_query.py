# Classification query

from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Tên model bạn đã upload lên Hugging Face
model_name = "khacdiep2208/phobert-finetuned-query-classification"

# Load tokenizer và model đã fine-tune
tokenizer = AutoTokenizer.from_pretrained(model_name)
model_class = AutoModelForSequenceClassification.from_pretrained(model_name)


# Ví dụ: thử dự đoán
query = "cho câu hỏi trắc nghiệm về an toàn thông tin"
inputs = tokenizer(query, return_tensors="pt")
outputs = model_class(**inputs)

predicted_class = outputs.logits.argmax(dim=-1).item()
print("Predicted class:", predicted_class)
