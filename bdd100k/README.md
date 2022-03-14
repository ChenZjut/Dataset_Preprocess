# Dataset_Preprocess

## How to use?

### Bdd100k

#### 1.folder structure

**.**
**├── bddTL2voc.py**
**├── BDDVOC**
**│   ├── Annotations**
**│   │   ├── train**
**│   │   └── val**
**│   └── JPEGImages**
**│       ├── train**
**│       └── val**
**├── counter_labels.py**
**├── Images**
**│   ├── 100k**
**│   │   ├── test**
**│   │   ├── train**
**│   │   └── val**
**│   └── 10k**
**│       ├── test**
**│       ├── train**
**│       └── val**
**├── Labels**
**│   ├── bdd100k_labels_images_train.json**
**│   └── bdd100k_labels_images_val.json**
**├── split_color.py**
**└── voc_label.py**

#### 2.Prepare dataset

**Unzip the dataset to the ``Images`` and ``Labels``folder**

```bash
python bddTL2voc.py
```

**After running this code, a dataset in VOC format will be generated in the folder BDDVOC.**

#### 3.Count the number of labels

```bash
python counter_labels.py
```

**Notes: Remember to modify the path**

```python
save_xmls_path = './BDDVOC/Annotations/train'
```

**The results are as follows:**

```bash
green: 79406
red: 46118
unknown: 57176
yellow: 3417
```

#### 4.Choose the label I want

```bash
python split_yellow.py
```

**I found that the data set has very few labels for a certain category, and I prioritized picking out all of this category.**