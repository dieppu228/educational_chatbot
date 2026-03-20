from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Tên model bạn đã upload lên Hugging Face
model_name = "khacdiep2208/phobert-finetuned-query-classification"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)




def routing_query(
    query: str,
    tokenizer_obj=None,
    model_obj=None,
    device: str = None,
    max_length: int = 128
) -> int:
    """
    Routing query bằng model classification đã fine-tune.

    Args:
        query (str): câu query của user
        tokenizer_obj: tokenizer từ HuggingFace (sử dụng global nếu None)
        model_obj: AutoModelForSequenceClassification (sử dụng global nếu None)
        device (str, optional): 'cpu' hoặc 'cuda'
        max_length (int): max token length

    Returns:
        int: nhãn dự đoán (0, 1, hoặc 2)
    """
    
    # Sử dụng global model/tokenizer nếu không truyền vào
    _tokenizer = tokenizer_obj if tokenizer_obj is not None else globals()['tokenizer']
    _model = model_obj if model_obj is not None else globals()['model']

    # Tự động chọn device nếu không truyền vào
    device = "cuda" if torch.cuda.is_available() else "cpu"
    _model = _model.to(device)
    _model.eval()

    # Tokenize
    inputs = _tokenizer(
        query,
        padding=True,
        truncation=True,
        max_length=max_length,
        return_tensors="pt"
    )

    # Đưa input lên device
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Inference
    with torch.no_grad():
        outputs = _model(**inputs)
        logits = outputs.logits
        predicted_label = torch.argmax(logits, dim=-1).item()

    return predicted_label
