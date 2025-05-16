import torch
from torchvision import models, transforms
from PIL import Image
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def load_model(model_path, num_classes=196):
    model = models.resnet18(weights=None)
    model.fc = torch.nn.Linear(model.fc.in_features, num_classes)

    if os.path.exists(model_path):
        model.load_state_dict(torch.load(model_path, map_location=device))
    else:
        raise FileNotFoundError(f"Model file not found at {model_path}")

    return model.to(device).eval()


model = load_model(r'AI\car_model.pth')
class_names = sorted([d.name for d in os.scandir('AI/path_car') if d.is_dir()])

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])


def found_car_by_photo(photo_name):
    image_path = os.path.join('image', photo_name)

    try:
        image = Image.open(image_path).convert('RGB')
    except IOError as e:
        raise ValueError(f"Error opening image {photo_name}: {str(e)}")

    input_tensor = transform(image).unsqueeze(0).to(device)

    # Исправленный блок с autocast
    with torch.no_grad(), torch.amp.autocast(
            device_type=device.type,
            enabled=device.type == 'cuda'
    ):
        output = model(input_tensor)

    predicted_class = output.argmax().item()
    return class_names[predicted_class]