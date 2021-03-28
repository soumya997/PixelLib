cloned from original [pixellib](https://github.com/ayoolaolafenwa/PixelLib)

```python
augmentation = imgaug.augmenters.Sometimes(0.5, [
iaa.CLAHE(clip_limit=(1, 10)),
imgaug.augmenters.Fliplr(0.5),
iaa.Flipud(0.5),
imgaug.augmenters.GaussianBlur(sigma=(0.0, 5.0))
])
```
