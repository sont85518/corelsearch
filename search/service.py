from sklearn.metrics.pairwise import cosine_similarity
import pickle
import numpy
from PIL import Image
from torchvision.models import *
import torch
import torchvision.transforms as transforms

npy_name = 'static/resnet50.npy'


class ImageEmbeddings:
    def __init__(self, model_name='resnet50'):
        instance = globals()[model_name]
        self.model = instance(pretrained=True)
        self.model = torch.nn.Sequential(*list(self.model.children())[:-1])
        self.model.eval()
        self.scaler = transforms.Resize((224, 224))
        self.normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        self.to_tensor = transforms.ToTensor()

    def emb_path(self, im):
        im = Image.open(im)
        im = self.normalize(self.to_tensor(self.scaler(im))).unsqueeze(0)
        val = self.model(im)
        val = val.view(val.size(1)).detach().numpy()
        return val

    def emb_im(self, im):
        im = self.normalize(self.to_tensor(self.scaler(im))).unsqueeze(0)
        val = self.model(im)
        val = val.view(val.size(1)).detach().numpy()
        return val


with open(npy_name, 'rb') as handle:
    image_database = pickle.load(handle)


model = ImageEmbeddings()


def search(image_dir, t=0.65):
    im_vec = model.emb_path(image_dir)
    cos_metric = cosine_similarity([im_vec], image_database['vecs'])
    top_idx = list(numpy.where(cos_metric[0] >= t))[0]
    dict_results = dict()

    # sort results
    for idx in top_idx:
        dict_results[image_database['indexes'][idx]] = cos_metric[0][idx]

    # return [
    #     ('/media/food-101/01.png', 0.99999994),
    #     ('/media/food-101/02.png', 0.89795125),
    #     ('/media/food-101/01.png', 0.99999994),
    #     ('/media/food-101/02.png', 0.89795125),
    #     ('/media/food-101/01.png', 0.99999994),
    #     ('/media/food-101/02.png', 0.89795125),
    #     ('/media/food-101/01.png', 0.99999994),
    #     ('/media/food-101/02.png', 0.89795125),
    #     ('/media/food-101/01.png', 0.99999994),
    #     ('/media/food-101/02.png', 0.89795125),
    #     ('/media/food-101/01.png', 0.99999994),
    #     ('/media/food-101/02.png', 0.89795125),
    #     ('/media/food-101/01.png', 0.99999994),
    #     ('/media/food-101/02.png', 0.89795125),
    #     ('/media/food-101/01.png', 0.99999994),
    #     ('/media/food-101/02.png', 0.89795125),
    #     ('/media/food-101/01.png', 0.99999994),
    #     ('/media/food-101/02.png', 0.89795125),
    # ]
    return sorted(dict_results.items(), key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    values = search('test.jpg', t=0.65)
    print(values)
