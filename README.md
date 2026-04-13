# NapkinSimilarity
NapkinSimiliarity is a MS2 similarity score than can be explained on a napkin. </br>

picture of napkin


## How does it work?
Even tough it can be explained on a napkin it might not be entire clear from the napkin alone so let's go through it quickly. The similarity score is using the compression distance (Zip It! https://www.youtube.com/watch?v=aLaYgzmRPa8). 
Let's take three sentences:
- (1) Napkins are your best companion while eating Spaghetti
- (2) Napkins are your best companion while eating ice-cream
- (3) Ancient civilisations were already using napkins

(1) and (2) are very similar only Spaghetti and ice-cream differ. This can be compressed efficiently. (1) and (3) are very different and therefore you cannot compress as much.
</br>
The similarity can be calculated by using the length of the compression of two sentence alone compared to the two sentences combined.
```
len(1) + len(2) / len(1 + 2) --> large (similar)
len(1) + len(3) / len(1 + 3) --> small (dissimilar)
```

The same concept can be applied to fragments and losses in tandem mass spectrometry with some small modifications:
- word ==> fragment or loss
- len of compression ==> intensity (matching fragments get (intensity_1 + intensity_2 / 2))
- to be comparable, scale the output from 0 - 1

## How to install?
```
git clone https://github.com/j-a-dietrich/NapkinSimilarity.git

cd NapkinSimilarity

pip install -e .
```

## How to use it?
```
from matchms.importing import load_from_mgf
import NapkinSimilarity

spectra = list(load_from_mgf("pesticides.mgf"))
spec_1 = spectra[0]
spec_2 = spectra[1]

NapkinSimilarity.run(spec_1, spec_2)
```
