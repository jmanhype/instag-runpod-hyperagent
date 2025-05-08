# 🚀 InsTaG: Full Setup & Usage Guide on RunPod 🚀

This guide provides a comprehensive, step-by-step walkthrough for setting up the InsTaG project on RunPod, using your custom Docker image `batmanosama/instag-runpod:latest`.

## 🌟 Phase 0: RunPod Deployment & Initial Setup

### 1. Log in to RunPod 🔑
   - Navigate to [https://www.runpod.io/console/pods](https://www.runpod.io/console/pods).

### 2. Deploy a New Pod ☁️
   - Click **"+ New Pod"**.
   - **GPU**: Select **RTX 4090 (24 GB)**.
   - **Container Image**: `batmanosama/instag-runpod:latest`.
   - **Disks**: Allocate 50-100GB for Container Disk, and optionally 50-200GB+ for a persistent Volume Disk (e.g., mounted at `/workspace/persistent_storage`).
   - **Overrides**: Configure ports (usually not needed) and environment variables (if any).
   - **Auto Shutdown**: Recommended to set an idle timer (e.g., 1-2 hours).
   - Review and **"Deploy"**.

### 3. Wait for Pod Initialization ⏳
   - Status will change to "Running".

### 4. Connect via SSH 💻
   - In pod details -> **"Connect"** tab, find the SSH command: `ssh root@<region>.ssh.runpod.io -p <PORT_NUMBER>`.
   - Connect from your local terminal.

### 5. Initial Navigation & Environment Activation ✅
   - In RunPod SSH session:
     ```bash
     cd /workspace/instag_project
     conda activate instag
     nvidia-smi # Verify GPU
     ```

## 🛠️ Phase 1: InsTaG Project Setup (Post-Docker Deployment)

### 1. Initialize Git Submodules (Good Practice)
   ```bash
   git submodule update --init --recursive
   ```

### 2. Download Pre-trained Models & Tools for InsTaG 🧩
   ```bash
   bash scripts/prepare.sh
   ```

## 🗿 Phase 2: Mandatory Dependency - Basel Face Model (BFM) 2009

### 1. Download BFM 2009 Locally (on your computer)
   - Go to [BFM Download Page](https://faces.dmi.unibas.ch/bfm/main.php?nav=1-2&id=downloads).
   - Register and download `01_MorphableModel.mat` (often in `Basel Face Model 2009.zip`).

### 2. Upload BFM to RunPod via SCP ⬆️
   - On your local terminal:
     ```bash
     # Replace <PORT_NUMBER>, <PATH_TO_LOCAL_BFM_FILE>, and <region>
     scp -P <PORT_NUMBER> <PATH_TO_LOCAL_BFM_FILE>/01_MorphableModel.mat root@<region>.ssh.runpod.io:/workspace/instag_project/data_utils/face_tracking/3DMM/
     ```
   - On RunPod (if directory doesn't exist):
     ```bash
     mkdir -p /workspace/instag_project/data_utils/face_tracking/3DMM
     ```

### 3. Run BFM Conversion Script 🔄
   - In RunPod SSH session:
     ```bash
     cd /workspace/instag_project/data_utils/face_tracking
     python convert_BFM.py
     cd /workspace/instag_project # Back to project root
     ```

## ✨ Phase 3: Optional Tools Setup

### 1. Set Up EasyPortrait (for Tooth Masks) 🦷
   ```bash
   # These might already be installed by your Dockerfile or environment.yml
   pip install -U openmim
   mim install mmcv-full==1.7.1 prettytable

   mkdir -p /workspace/instag_project/data_utils/easyportrait
   wget "https://rndml-team-cv.obs.ru-moscow-1.hc.sbercloud.ru/datasets/easyportrait/experiments/models/fpn-fp-512.pth" -O /workspace/instag_project/data_utils/easyportrait/fpn-fp-512.pth
   ```

### 2. Set Up Sapiens (for Geometry Priors in Adaptation) 📐
   - Needed for adaptation, not pre-training.
   ```bash
   bash scripts/prepare_sapiens.sh # This creates 'sapiens_lite' conda env
   # Remember to switch back: conda activate instag
   ```

## 🎬 Phase 4: Data Preparation for Pre-training

Choose **Option A** or **Option B**.

### Option A: Using Talking Gaussian Dataset Videos 🗣️
   - Assumes `macron.mp4` and `may.mp4` are in `/workspace/instag_project/CelebV-HQ/talking_gaussian_dataset/`.
   ```bash
   cd /workspace/instag_project
   mkdir -p data/pretrain/may data/pretrain/macron
   cp CelebV-HQ/talking_gaussian_dataset/may.mp4 data/pretrain/may/may.mp4
   cp CelebV-HQ/talking_gaussian_dataset/macron.mp4 data/pretrain/macron/macron.mp4
   echo "Talking Gaussian videos organized."
   ```

### Option B: Using CelebV-HQ Dataset Videos 🌟
   1. **Install Dependencies (if not in Docker)**:
      ```bash
      # pip install yt-dlp opencv-python # Should be in your image
      ```
   2. **Download Videos**:
      ```bash
      cd /workspace/instag_project/CelebV-HQ
      python download_and_process.py # Downloads ~10 videos by default
      ```
   3. **Organize Videos for InsTaG**:
      ```bash
      cd /workspace/instag_project
      # Example for one video (repeat for all):
      # VIDEO_ID="M2Ohb0FAaJU_1" # Replace with actual video ID
      # mkdir -p data/pretrain/${VIDEO_ID}
      # cp CelebV-HQ/downloaded_celebvhq/processed/${VIDEO_ID}.mp4 data/pretrain/${VIDEO_ID}/${VIDEO_ID}.mp4
      echo "CelebV-HQ videos need to be manually organized into data/pretrain/<VIDEO_ID>/<VIDEO_ID>.mp4"
      ```

## ⚙️ Phase 5: Video Preprocessing for InsTaG

For *each* video in `data/pretrain/<VIDEO_ID>/<VIDEO_ID>.mp4`:

### 1. Run InsTaG's `process.py` Script 🎞️
   ```bash
   cd /workspace/instag_project
   # Example for 'may'
   python data_utils/process.py data/pretrain/may/may.mp4
   # Example for 'macron'
   python data_utils/process.py data/pretrain/macron/macron.mp4
   # Repeat for all other videos
   ```

### 2. Optional: Split Video for Evaluation (`split.py`) ✂️
   ```bash
   python data_utils/split.py data/pretrain/may/may.mp4
   # Repeat for other videos if desired
   ```

## 🤔 Phase 6: Action Unit (AU) Extraction using OpenFace

This is often the most challenging external dependency.

### 1. Ensure OpenFace is Usable 🧐
   - If not in your Docker image, this requires manual effort.
   - Try `FeatureExtraction -h` in the pod. If not found, proceed to "If OpenFace is NOT in the pod".

### 2. Extract AUs:
   - **If OpenFace is NOT in the pod (Likely)**:
     1. Run OpenFace on your local machine on the *original, unprocessed* MP4s.
     2. Rename the output CSV for each video to `au.csv`.
     3. Upload each `au.csv` to RunPod using `scp`:
        ```bash
        # On your local machine:
        # scp -P <PORT_NUMBER> <PATH_TO_LOCAL_AU.CSV> root@<region>.ssh.runpod.io:/workspace/instag_project/data/pretrain/<VIDEO_ID>/au.csv
        ```
        *Example for `may`*: `scp -P 12345 ~/OpenFace_Output/may_au.csv root@us-east-1.ssh.runpod.io:/workspace/instag_project/data/pretrain/may/au.csv`

## 👄 Phase 7: Generate Tooth Masks using EasyPortrait

### 1. Set `PYTHONPATH`  PATH
   ```bash
   export PYTHONPATH=/workspace/instag_project/data_utils/easyportrait:$PYTHONPATH
   ```

### 2. Run `create_teeth_mask.py` 😷
   ```bash
   cd /workspace/instag_project
   # Example for 'may'
   python data_utils/easyportrait/create_teeth_mask.py data/pretrain/may
   # Example for 'macron'
   python data_utils/easyportrait/create_teeth_mask.py data/pretrain/macron
   # Repeat for all video IDs
   ```

## 🔊 Phase 8: Audio Feature Extraction

Choose one method. Assumes `.wav` files exist from `data_utils/process.py`.

### 1. Navigate to Project Root
   ```bash
   cd /workspace/instag_project
   ```

### 2. Choose an Audio Extractor:

   - **DeepSpeech (Paper's evaluation choice)** 🎤:
     ```bash
     python data_utils/deepspeech_features/extract_ds_features.py --input data/pretrain/may/may.wav # Output: may.npy
     # Repeat for all videos
     ```
   - **Wav2Vec (Often performs well)** 🌊:
     ```bash
     python data_utils/wav2vec.py --wav data/pretrain/may/may.wav --save_feats # Output: may_eo.npy
     # Repeat for all videos
     ```
   - **HuBERT (Good for non-English, may need longer videos)** 🗣️:
     ```bash
     python data_utils/hubert.py --wav data/pretrain/may/may.wav # Output: may_hu.npy
     # Repeat for all videos
     ```

## 🏋️ Phase 9: Pre-training the InsTaG Model

### 1. Check Environment & Directory ✅
   ```bash
   cd /workspace/instag_project
   conda activate instag
   ```

### 2. Configure and Start Pre-training 🚀
   - **Edit `pretrain_face.py` and `pretrain_mouth.py`**: Update the `video_ids` list in these files (around line 30) to include the IDs of the videos you have prepared (e.g., `video_ids = ["may", "macron"]`).
     ```bash
     nano pretrain_face.py
     nano pretrain_mouth.py
     ```
   - **Create Output Directory**:
     ```bash
     mkdir -p output/my_instag_pretrain_run1
     ```
   - **Run Pre-training Script**:
     ```bash
     # Args: <data_dir> <output_dir> <gpu_id>
     bash scripts/pretrain_con.sh data/pretrain output/my_instag_pretrain_run1 0
     ```

### 3. Monitor Training 📊
   - **Logs**: `tail -f output/my_instag_pretrain_run1/train.log`
   - **GPU**: `watch -n 1 nvidia-smi`
   - **`tmux` or `screen` (Highly Recommended for long runs)**:
     ```bash
     tmux new -s instag_training
     # Run training command inside tmux
     # Detach: Ctrl+b then d
     # Reattach: tmux attach -t instag_training
     ```
   - Pre-training can take many hours or days!

## 🧑‍🎓 Phase 10: Adaptation to a New Identity (After Pre-training)

### 1. Prepare Data for the New Identity 🖼️
   - Follow **Phases 4 through 8** for the new person's video (e.g., in `data/new_person_id`).

### 2. Generate Geometry Priors using Sapiens (if not done in Phase 3)
   ```bash
   conda activate sapiens_lite
   bash /workspace/instag_project/data_utils/sapiens/run.sh /workspace/instag_project/data/new_person_id
   conda activate instag # Switch back
   ```

### 3. Run Adaptation Script 🧬
   - Modify `scripts/train_xx_few.sh` to load your pre-trained model from `output/my_instag_pretrain_run1`.
   ```bash
   # Example:
   bash scripts/train_xx_few.sh data/new_person_id output/adapted_new_person_model 0
   ```

## 🧪 Phase 11: Testing and Inference

### 1. Render a Test Clip (Using Test Set Poses/Audio) 🎥
   ```bash
   cd /workspace/instag_project
   # Example using an adapted model
   python synthesize_fuse.py -S data/new_person_id -M output/adapted_new_person_model --eval
   # Renders in: output/adapted_new_person_model/test/ours_None/renders/
   ```

### 2. Inference with Specified Driving Audio 🗣️➡️👤
   1. Extract features from your custom audio (e.g., `my_speech.wav` -> `my_speech_features.npy` via DeepSpeech):
      ```bash
      python data_utils/deepspeech_features/extract_ds_features.py --input my_speech.wav --output_name my_speech_features.npy
      ```
   2. Run synthesis:
      ```bash
      python synthesize_fuse.py \
          -S data/new_person_id \
          -M output/adapted_new_person_model \
          --audio my_speech_features.npy \
          --audio_extractor deepspeech \
          --dilate \
          --use_train
      ```

## 💾 Phase 12: Downloading Results from RunPod

### 1. Use `scp` from Your Local Machine ⬇️
   ```bash
   # Download a directory (e.g., generated videos)
   # scp -P <PORT_NUMBER> -r root@<region>.ssh.runpod.io:/workspace/instag_project/output/adapted_new_person_model/test/ours_None/renders/ ./my_local_instag_videos/

   # Download a model checkpoint
   # scp -P <PORT_NUMBER> root@<region>.ssh.runpod.io:/workspace/instag_project/output/my_instag_pretrain_run1/checkpoints/model_epoch_10.pth ./my_local_models/
   ```

## 💰 Phase 13: Managing RunPod Resources

- **STOP Your Pod**: When not actively training/inferencing, stop it from the RunPod console to save costs! 🛑
- **Delete Your Pod**: If completely done, delete the pod to stop all charges.

---

Good luck with your InsTaG project! This detailed guide should help you navigate the complexities. 🎉
