import torch
from torchvision import transforms
from PIL import Image
from torchvision.models import vgg16
from ai.loaddata import load_data
from model.user import Record
from db_config import  db_init as mr

class ImageClassifier2:
    def __init__(self, model_path='./ai/mushroom_vgg_64_0.0001.mod', img_dir="./mushroom_dataset", batch_size=16, num_classes=10):
        self.model_path = model_path
        self.num_classes = num_classes
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self.load_model()
        self.model.to(self.device)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # VGG-16预训练模型的标准化参数
        ])
        _, _, cls_list = load_data(img_dir, batch_size=batch_size)
        self.cls_idx = {idx: class_name for idx, class_name in enumerate(cls_list)}

    def load_model(self):
        model = vgg16()
        nf = model.classifier[6].in_features
        model.classifier[6] = torch.nn.Linear(nf, self.num_classes)
        model.load_state_dict(torch.load(self.model_path, map_location=self.device))  # 明确指定加载模型的设备
        model.eval()
        return model

    def classify_image(self, img_path,user_id):
        image = Image.open(img_path).convert('RGB')
        image = self.transform(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            output = self.model(image)
            probabilities = torch.nn.functional.softmax(output, dim=1)
            confidence, predicted_class_idx = torch.max(probabilities, dim=1)
            predicted_class_name = self.cls_idx[predicted_class_idx.item()]
            # Save to database

        record = Record(
            user_id=user_id,
            predicted_class=predicted_class_name,
            confidence=str(confidence),
            image_path=img_path
        )
        mr.session.add(record)
        mr.session.commit()

        return predicted_class_name, confidence.item()


