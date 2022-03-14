# Dataset_Preprocess

## How to use?

### LISA

#### 1.folder structure

```bash
.
├── Annotations
│   └── Annotations
│       ├── daySequence1
│       ├── daySequence2
│       ├── dayTrain
│       │   ├── dayClip1
│       │   ├── dayClip10
│       │   ├── dayClip11
│       │   ├── dayClip12
│       │   ├── dayClip13
│       │   ├── dayClip2
│       │   ├── dayClip3
│       │   ├── dayClip4
│       │   ├── dayClip5
│       │   ├── dayClip6
│       │   ├── dayClip7
│       │   ├── dayClip8
│       │   └── dayClip9
│       ├── nightSequence1
│       ├── nightSequence2
│       └── nightTrain
│           ├── nightClip1
│           ├── nightClip2
│           ├── nightClip3
│           ├── nightClip4
│           └── nightClip5
├── daySequence1
│   └── daySequence1
│       └── frames
├── daySequence2
│   └── daySequence2
│       └── frames
├── dayTrain
│   └── dayTrain
│       ├── dayClip1
│       │   └── frames
│       ├── dayClip10
│       │   └── frames
│       ├── dayClip11
│       │   └── frames
│       ├── dayClip12
│       │   └── frames
│       ├── dayClip13
│       │   └── frames
│       ├── dayClip2
│       │   └── frames
│       ├── dayClip3
│       │   └── frames
│       ├── dayClip4
│       │   └── frames
│       ├── dayClip5
│       │   └── frames
│       ├── dayClip6
│       │   └── frames
│       ├── dayClip7
│       │   └── frames
│       ├── dayClip8
│       │   └── frames
│       └── dayClip9
│           └── frames
├── LISA
│   ├── Annotations
│   └── JPEGImages
├── LISAVOC
│   ├── Annotations
│   └── JPEGImages
├── nightSequence1
│   └── nightSequence1
│       └── frames
├── nightSequence2
│   └── nightSequence2
│       └── frames
├── nightTrain
│   └── nightTrain
│       ├── nightClip1
│       │   └── frames
│       ├── nightClip2
│       │   └── frames
│       ├── nightClip3
│       │   └── frames
│       ├── nightClip4
│       │   └── frames
│       └── nightClip5
│           └── frames
├── sample-dayClip6
│   └── sample-dayClip6
│       └── frames
└── sample-nightClip1
    └── sample-nightClip1
        └── frames
```



#### 2.Prepare dataset

**Unzip the dataset to the ``Images`` and ``Labels``folder**

```bash
python lisa2voc.py
```

**After running this code, a dataset in VOC format will be generated in the folder BDDVOC.**

#### 3.Count the number of labels

```bash
python counter_labels.py
```

**Notes: Remember to modify the path**

```python
save_xmls_path = 'LISA/Annotations/'
```

**The results are as follows:**

```bash
yellow: 1258
red: 4222
green: 9426
```

#### 4.Choose the label I want

```bash
python split_color.py
```

**I found that the data set has very few labels for a certain category, and I prioritized picking out all of this category.**

#### 5.Convert directly to yolo's training format

```
python lisa2yolo.py
```

#### 6.Show the Ground Truth in the  xml files

```bash
python show_labels.py
```