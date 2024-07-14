import torch
from torchvision import transforms
from torchvision.models import alexnet
from PIL import Image
from ai.loaddata import load_data
from db_config import  db_init as mr
from model.user import Record
from datetime import datetime
class ImageClassifier:
    def __init__(self, model_path='./ai/mushroom_alex_32_0.0001.mod', img_dir="./mushroom_dataset", batch_size=16, num_classes=10):
        self.model_path = model_path
        self.num_classes = num_classes
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self.load_model()
        self.model.to(self.device)

        # 使用与训练时相同的预处理步骤
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        _, _, cls_list = load_data(img_dir, batch_size=batch_size)
        self.cls_idx = {idx: class_name for idx, class_name in enumerate(cls_list)}

    def load_model(self):
        # 不使用预训练权重
        model = alexnet(weights=None)
        fc_in = model.classifier[6].in_features
        model.classifier[6] = torch.nn.Linear(fc_in, self.num_classes)
        model.load_state_dict(torch.load(self.model_path, map_location=self.device))
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