# The class containing the model
import torch
from PIL import Image
import torchvision
from torchvision import transforms

class MobileNet:
    def __init__(self):
        # Source: https://github.com/Lasagne/Recipes/blob/master/examples/resnet50/imagenet_classes.txt
        with open('imagenet_classes.txt') as f:
            self.classes = [line.strip() for line in f.readlines()]

        # self.model = torch.hub.load('pytorch/vision', 'mobilenet_v2', pretrained=True)
        self.model = torchvision.models.mobilenet_v2(pretrained=True)
        self.model.eval()
    
    def infer(self, image_path):
        input_image = Image.open(image_path)
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        input_tensor = preprocess(input_image)

        # create a mini-batch as expected by the model
        input_batch = input_tensor.unsqueeze(0) 

        # move the input and model to GPU for speed if available
        if torch.cuda.is_available():
            input_batch = input_batch.to('cuda')
            self.model.to('cuda')

        with torch.no_grad():
            output = self.model(input_batch)

        # The output has unnormalized scores. To get probabilities, you can run a softmax on it.
        output = torch.nn.functional.softmax(output[0], dim=0)
        confidence, index = torch.max(output, 0)

        return (self.classes[index.item()], confidence.item())



