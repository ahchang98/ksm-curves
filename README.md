# ksm-curves
Generates curved lasers for kshootmania chart files (\*.ksh)

## Running the Program
**REQUIRES PYTHON >=3.9**

Run the following for help:

    python curve.py -h

Recommended to save file in KSM editor after opening file with generated curve

## Notes
- Laser locations
  - Normal: *05AFKPUZejo*
  - Fine: *0257ACFHKMPSUXZbehjmo*
  - Very Fine: *0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmno*
- Laser curvature allows positive and negative decimal values, 0.0 = linear
- Note numerator/denominator found in bottom-right of editor

## Warnings
- Curvature behaves badly for values too large
- If getting wide lasers without -w/--wide, there may be an existing wide laser directive in ksh file
- Avoid trying to erase a laser in the middle of a segment; the whole segment could be erased unintentionally
- If the previous laser segment ends in a slam, generating a curve at the slam could erase the previous segment
