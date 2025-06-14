# Generation Output

After running the main jobs:

	bash generate_all.sh

in the root directory the generated motions will be saved in generation/batch_motions/

# MoMask: Generative Masked Modeling of 3D Human Motions (CVPR 2024)
### [[Project Page]](https://ericguo5513.github.io/momask) [[Paper]](https://arxiv.org/abs/2312.00063) [[Huggingface Demo]](https://huggingface.co/spaces/MeYourHint/MoMask) [[Colab Demo]](https://github.com/camenduru/MoMask-colab)
![teaser_image](https://ericguo5513.github.io/momask/static/images/teaser.png)

If you find our code or paper helpful, please consider starring our repository and citing:
```
@inproceedings{guo2024momask,
  title={Momask: Generative masked modeling of 3d human motions},
  author={Guo, Chuan and Mu, Yuxuan and Javed, Muhammad Gohar and Wang, Sen and Cheng, Li},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  pages={1900--1910},
  year={2024}
}
```

## :postbox: News
📢 **2024-08-02** --- The [WebUI demo 🤗](https://huggingface.co/spaces/MeYourHint/MoMask) is now running smoothly on a CPU. No GPU is required to use MoMask.

📢 **2024-02-26** --- 🔥🔥🔥 Congrats! MoMask is accepted to CVPR 2024.

📢 **2024-01-12** --- Now you can use MoMask in Blender as an add-on. Thanks to [@makeinufilm](https://twitter.com/makeinufilm) for sharing the [tutorial](https://medium.com/@makeinufilm/notes-on-how-to-set-up-the-momask-environment-and-how-to-use-blenderaddon-6563f1abdbfa).

📢 **2023-12-30** --- For easy WebUI BVH visulization, you could try this website [bvh2vrma](https://vrm-c.github.io/bvh2vrma/) from this [github](https://github.com/vrm-c/bvh2vrma?tab=readme-ov-file).

📢 **2023-12-29** --- Thanks to Camenduru for supporting the [🤗Colab](https://github.com/camenduru/MoMask-colab) demo.

📢 **2023-12-27** --- Release WebUI demo. Try now on [🤗HuggingFace](https://huggingface.co/spaces/MeYourHint/MoMask)!

📢 **2023-12-19** --- Release scripts for temporal inpainting.

📢 **2023-12-15** --- Release codes and models for momask. Including training/eval/generation scripts.

📢 **2023-11-29** --- Initialized the webpage and git project.  


## :round_pushpin: Get You Ready

<details>
  
### 1. Conda Environment
```
conda env create -f environment.yml
conda activate momask
pip install git+https://github.com/openai/CLIP.git
```
We test our code on Python 3.7.13 and PyTorch 1.7.1

#### Alternative: Pip Installation
<details>
We provide an alternative pip installation in case you encounter difficulties setting up the conda environment.

```
pip install -r requirements.txt
```
We test this installation on Python 3.10

</details>

### 2. Models and Dependencies

#### Download Pre-trained Models
```
bash prepare/download_models.sh
```

#### Download Evaluation Models and Gloves
For evaluation only.
```
bash prepare/download_evaluator.sh
bash prepare/download_glove.sh
```

#### Troubleshooting
To address the download error related to gdown: "Cannot retrieve the public link of the file. You may need to change the permission to 'Anyone with the link', or have had many accesses". A potential solution is to run `pip install --upgrade --no-cache-dir gdown`, as suggested on https://github.com/wkentaro/gdown/issues/43. This should help resolve the issue.

#### (Optional) Download Manually
Visit [[Google Drive]](https://drive.google.com/drive/folders/1sHajltuE2xgHh91H9pFpMAYAkHaX9o57?usp=drive_link) to download the models and evaluators mannually.

### 3. Get Data

You have two options here:
* **Skip getting data**, if you just want to generate motions using *own* descriptions.
* **Get full data**, if you want to *re-train* and *evaluate* the model.

**(a). Full data (text + motion)**

**HumanML3D** - Follow the instruction in [HumanML3D](https://github.com/EricGuo5513/HumanML3D.git), then copy the result dataset to our repository:
```
cp -r ../HumanML3D/HumanML3D ./dataset/HumanML3D
```
**KIT**-Download from [HumanML3D](https://github.com/EricGuo5513/HumanML3D.git), then place result in `./dataset/KIT-ML`

#### 

</details>

## :rocket: Demo
<details>

### (a) Generate from a single prompt
```
python gen_t2m.py --gpu_id 1 --ext exp1 --text_prompt "A person is running on a treadmill."
```
### (b) Generate from a prompt file
An example of prompt file is given in `./assets/text_prompt.txt`. Please follow the format of `<text description>#<motion length>` at each line. Motion length indicates the number of poses, which must be integeter and will be rounded by 4. In our work, motion is in 20 fps.

If you write `<text description>#NA`, our model will determine a length. Note once there is **one** NA, all the others will be **NA** automatically.

```
python gen_t2m.py --gpu_id 1 --ext exp2 --text_path ./assets/text_prompt.txt
```


A few more parameters you may be interested:
* `--repeat_times`: number of replications for generation, default `1`.
* `--motion_length`: specify the number of poses for generation, only applicable in (a).

The output files are stored under folder `./generation/<ext>/`. They are
* `numpy files`: generated motions with shape of (nframe, 22, 3), under subfolder `./joints`.
* `video files`: stick figure animation in mp4 format, under subfolder `./animation`.
* `bvh files`: bvh files of the generated motion, under subfolder `./animation`.

We also apply naive foot ik to the generated motions, see files with suffix `_ik`. It sometimes works well, but sometimes will fail.
  
</details>

## :dancers: Visualization
<details>

All the animations are manually rendered in blender. We use the characters from [mixamo](https://www.mixamo.com/#/). You need to download the characters in T-Pose with skeleton.

### Retargeting
For retargeting, we found rokoko usually leads to large error on foot. On the other hand, [keemap.rig.transfer](https://github.com/nkeeline/Keemap-Blender-Rig-ReTargeting-Addon/releases) shows more precise retargetting. You could watch the [tutorial](https://www.youtube.com/watch?v=EG-VCMkVpxg) here.

Following these steps:
* Download keemap.rig.transfer from the github, and install it in blender.
* Import both the motion files (.bvh) and character files (.fbx) in blender.
* `Shift + Select` the both source and target skeleton. (Do not need to be Rest Position)
* Switch to `Pose Mode`, then unfold the `KeeMapRig` tool at the top-right corner of the view window.
* For `bone mapping file`, direct to `./assets/mapping.json`(or `mapping6.json` if it doesn't work), and click `Read In Bone Mapping File`. This file is manually made by us. It works for most characters in mixamo.
* (Optional) You could manually fill in the bone mapping and adjust the rotations by your own, for your own character. `Save Bone Mapping File` can save the mapping configuration in local file, as specified by the mapping file path.
* Adjust the `Number of Samples`, `Source Rig`, `Destination Rig Name`.
* Clik `Transfer Animation from Source Destination`, wait a few seconds.

We didn't tried other retargetting tools. Welcome to comment if you find others are more useful.

### Scene

We use this [scene](https://drive.google.com/file/d/16SbrnG9JsJ2w7UwCFmh10PcBdl6HxlrA/view?usp=drive_link) for animation.


</details>

## :clapper: Temporal Inpainting
<details>
We conduct mask-based editing in the m-transformer stage, followed by the regeneration of residual tokens for the entire sequence. To load your own motion, provide the path through `--source_motion`. Utilize `-msec` to specify the mask section, supporting either ratio or frame index. For instance, `-msec 0.3,0.6` with `max_motion_length=196` is equivalent to `-msec 59,118`, indicating the editing of the frame section [59, 118]. 

```
python edit_t2m.py --gpu_id 1 --ext exp3 --use_res_model -msec 0.4,0.7 --text_prompt "A man picks something from the ground using his right hand."
```

Note: Presently, the source motion must adhere to the format of a HumanML3D dim-263 feature vector. An example motion vector data from the HumanML3D test set is available in `example_data/000612.npy`. To process your own motion data, you can utilize the `process_file` function from `utils/motion_process.py`.

</details>

## :space_invader: Train Your Own Models
<details>


**Note**: You have to train RVQ **BEFORE** training masked/residual transformers. The latter two can be trained simultaneously.

### Train RVQ
You may also need to download evaluation models to run the scripts.
```
python train_vq.py --name rvq_name --gpu_id 1 --dataset_name t2m --batch_size 256 --num_quantizers 6  --max_epoch 50 --quantize_dropout_prob 0.2 --gamma 0.05
```

### Train Masked Transformer
```
python train_t2m_transformer.py --name mtrans_name --gpu_id 2 --dataset_name t2m --batch_size 64 --vq_name rvq_name
```

### Train Residual Transformer
```
python train_res_transformer.py --name rtrans_name  --gpu_id 2 --dataset_name t2m --batch_size 64 --vq_name rvq_name --cond_drop_prob 0.2 --share_weight
```

* `--dataset_name`: motion dataset, `t2m` for HumanML3D and `kit` for KIT-ML.  
* `--name`: name your model. This will create to model space as `./checkpoints/<dataset_name>/<name>`
* `--gpu_id`: GPU id.
* `--batch_size`: we use `512` for rvq training. For masked/residual transformer, we use `64` on HumanML3D and `16` for KIT-ML.
* `--num_quantizers`: number of quantization layers, `6` is used in our case.
* `--quantize_drop_prob`: quantization dropout ratio, `0.2` is used.
* `--vq_name`: when training masked/residual transformer, you need to specify the name of rvq model for tokenization.
* `--cond_drop_prob`: condition drop ratio, for classifier-free guidance. `0.2` is used.
* `--share_weight`: whether to share the projection/embedding weights in residual transformer.

All the pre-trained models and intermediate results will be saved in space `./checkpoints/<dataset_name>/<name>`.
</details>

## :book: Evaluation
<details>

### Evaluate RVQ Reconstruction:
HumanML3D:
```
python eval_t2m_vq.py --gpu_id 0 --name rvq_nq6_dc512_nc512_noshare_qdp0.2 --dataset_name t2m --ext rvq_nq6

```
KIT-ML:
```
python eval_t2m_vq.py --gpu_id 0 --name rvq_nq6_dc512_nc512_noshare_qdp0.2_k --dataset_name kit --ext rvq_nq6
```

### Evaluate Text2motion Generation:
HumanML3D:
```
python eval_t2m_trans_res.py --res_name tres_nlayer8_ld384_ff1024_rvq6ns_cdp0.2_sw --dataset_name t2m --name t2m_nlayer8_nhead6_ld384_ff1024_cdp0.1_rvq6ns --gpu_id 1 --cond_scale 4 --time_steps 10 --ext evaluation
```
KIT-ML:
```
python eval_t2m_trans_res.py --res_name tres_nlayer8_ld384_ff1024_rvq6ns_cdp0.2_sw_k --dataset_name kit --name t2m_nlayer8_nhead6_ld384_ff1024_cdp0.1_rvq6ns_k --gpu_id 0 --cond_scale 2 --time_steps 10 --ext evaluation
```

* `--res_name`: model name of `residual transformer`.  
* `--name`: model name of `masked transformer`.  
* `--cond_scale`: scale of classifer-free guidance.
* `--time_steps`: number of iterations for inference.
* `--ext`: filename for saving evaluation results.
* `--which_epoch`: checkpoint name of `masked transformer`.

The final evaluation results will be saved in `./checkpoints/<dataset_name>/<name>/eval/<ext>.log`

</details>

## Acknowlegements

We sincerely thank the open-sourcing of these works where our code is based on: 

[deep-motion-editing](https://github.com/DeepMotionEditing/deep-motion-editing), [Muse](https://github.com/lucidrains/muse-maskgit-pytorch), [vector-quantize-pytorch](https://github.com/lucidrains/vector-quantize-pytorch), [T2M-GPT](https://github.com/Mael-zys/T2M-GPT), [MDM](https://github.com/GuyTevet/motion-diffusion-model/tree/main) and [MLD](https://github.com/ChenFengYe/motion-latent-diffusion/tree/main)

## License
This code is distributed under an [MIT LICENSE](https://github.com/EricGuo5513/momask-codes/tree/main?tab=MIT-1-ov-file#readme).

Note that our code depends on other libraries, including SMPL, SMPL-X, PyTorch3D, and uses datasets which each have their own respective licenses that must also be followed.

### Misc
Contact cguo2@ualberta.ca for further questions.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=EricGuo5513/momask-codes&type=Date)](https://star-history.com/#EricGuo5513/momask-codes&Date)
