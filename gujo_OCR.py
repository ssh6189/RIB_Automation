# CODE : Recognition Gujo Plan's text by Naver-OCR (ResNet-Attn)
# DATE : 2021-03-09 (by SH)
# INPUT : Gujo Plan's text crop img (JPG)
# OUTPUT : result txt file

import string
import argparse
import cv2

import torch
import torch.backends.cudnn as cudnn
import torch.utils.data
import torch.nn.functional as F

from OCR_utils import CTCLabelConverter, AttnLabelConverter
from OCR_dataset import RawDataset, AlignCollate
from OCR_model import Model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

'''
0. 작성자 : 유승환

1. input 
 (1-1) weights_gujo_oc : OCR model's dir
 (1-2) txt_gujo_path : OCR results(txt)'s dir
 (1-3) image_folder_path, tmp_image_folder_pat : crop text img's dir

2. output 
 (2-1) ocr_result.txt : OCR results (txt)

3. algorithm : recognition txt by ResNet-Attn

'''
def demo_gujo(weights_gujo_ocr, txt_gujo_path, tmp_image_folder_path, image_folder_path):
    ### input parameter ########################################################
    batch_size_ocr = 32
    img_height_ocr = 32
    img_width_ocr = 100
    batch_max_length_ocr = 25
    rgb = None
    num_fiducial = 20
    input_channel = 1
    output_channel = 2048
    hidden_size = 256

    character = "0123456789abcdefghijklmnopqrstuvwxyz;',/~@=구조평면도층지하옥탑붕보대근크기측상부늑단주외건축치수중앙내호벽"
    Trans = "None"
    Feat = "ResNet"
    Seq = "None"
    Predict = "Attn"
    ############################################################################

    """ model configuration """
    if 'CTC' in Predict:
        converter = CTCLabelConverter(character)
    else:
        converter = AttnLabelConverter(character)
    num_class = len(converter.character)

    if rgb:
        input_channel = 3

    model = Model(Trans, Feat, Seq, Predict, input_channel, output_channel, hidden_size, num_class, batch_max_length_ocr)
    model = torch.nn.DataParallel(model).to(device)

    # load model
    print('loading pretrained model from %s' % weights_gujo_ocr)
    model.load_state_dict(torch.load(weights_gujo_ocr, map_location=device))

    # prepare data. two demo images from https://github.com/bgshih/crnn#run-demo
    AlignCollate_demo = AlignCollate(imgH=img_height_ocr, imgW=img_width_ocr, keep_ratio_with_pad=False)
    demo_data = RawDataset(root=image_folder_path, rgb=rgb)  # use RawDataset
    demo_loader = torch.utils.data.DataLoader(
        demo_data, batch_size=batch_size_ocr,
        shuffle=False,
        num_workers=int(4),
        collate_fn=AlignCollate_demo, pin_memory=True)

    # predict
    model.eval()
    with torch.no_grad():
        for image_tensors, image_path_list in demo_loader:
            batch_size = image_tensors.size(0)
            image = image_tensors.to(device)
            # For max length prediction
            length_for_pred = torch.IntTensor([batch_max_length_ocr] * batch_size).to(device)
            text_for_pred = torch.LongTensor(batch_size, batch_max_length_ocr + 1).fill_(0).to(device)

            if 'CTC' in Predict:
                preds = model(image, text_for_pred)

                # Select max probabilty (greedy decoding) then decode index to character
                preds_size = torch.IntTensor([preds.size(1)] * batch_size)
                _, preds_index = preds.max(2)
                # preds_index = preds_index.view(-1)
                preds_str = converter.decode(preds_index, preds_size)

            else:
                preds = model(image, text_for_pred, is_train=False)

                # select max probabilty (greedy decoding) then decode index to character
                _, preds_index = preds.max(2)
                preds_str = converter.decode(preds_index, length_for_pred)


            log = open(f'./log_demo_result.txt', 'a')
            dashed_line = '-' * 80
            head = f'{"image_path":25s}\t{"predicted_labels":25s}\tconfidence score'
            
            log.write(f'{dashed_line}\n{head}\n{dashed_line}\n')

            preds_prob = F.softmax(preds, dim=2)
            preds_max_prob, _ = preds_prob.max(dim=2)

            for img_name, pred, pred_max_prob in zip(image_path_list, preds_str, preds_max_prob):
                if 'Attn' in Predict:
                    pred_EOS = pred.find('[s]')
                    pred = pred[:pred_EOS]  # prune after "end of sentence" token ([s])
                    pred_max_prob = pred_max_prob[:pred_EOS]

                # calculate confidence score (= multiply of pred_max_prob)
                confidence_score = pred_max_prob.cumprod(dim=0)[-1]

                with open(txt_gujo_path + 'ocr_result.txt', 'a') as f:
                    f.write(('%s \n') % (pred))

            log.close()