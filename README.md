This is a simple script to convert FITS images to stamps.

## Usage

```
usage: fits_to_stamps.py [-h] [--trimsec TRIMSEC] [--fitsext FITSEXT]
                         [--stampsize STAMPSIZE]
                         [--separatorwidth SEPARATORWIDTH]
                         [--fitsglob FITSGLOB] [--workers WORKERS]
                         target

convert a FITS to 3 x 3 stamps.

positional arguments:
  target                path to a single FITS file or a directory of FITS
                        files to convert

optional arguments:
  -h, --help            show this help message and exit
  --trimsec TRIMSEC     the FITS header keys containing the TRIMSEC section.
                        All of the keys in the CSV list provided will be
                        tried. default: TRIMSEC,DATASEC,TRIMSEC0
  --fitsext FITSEXT     the FITS extension number containing the image to work
                        on. default: automatic detection for normal and
                        .fits.fz files
  --stampsize STAMPSIZE
                        the individual stamp size in pixels. default: 256
  --separatorwidth SEPARATORWIDTH
                        the width of the separator lines between stamps in
                        pixels. default: 1
  --fitsglob FITSGLOB   the file glob to use to recognize FITS files in a
                        directory. default: *.fits*
  --workers WORKERS     number of parallel workers to operate on multiple FITS
                        files default: 8
```

## Installation

This requires:

- numpy
- astropy
- Pillow

Install it with pip (preferably in a virtualenv, or use the `--user` flag):

```
pip [--user] install git+https://github.com/waqasbhatti/fits-to-stamps
```

## License

This is provided under the MIT license. See the LICENSE file for the full text.
