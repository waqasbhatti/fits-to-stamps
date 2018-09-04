This is a simple script to convert FITS images to stamps.

## Usage

```
usage: fits-to-stamps [-h] [--trimsec TRIMSEC] [--fitsext FITSEXT]
                      [--stampsize STAMPSIZE]
                      [--separatorwidth SEPARATORWIDTH] [--fitsglob FITSGLOB]
                      [--workers WORKERS]
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

Install it with pip from [PyPI](https://pypi.org/project/fits-to-stamps)
(preferably in a virtualenv, or use the `--user` flag):

```
pip [--user] install fits-to-stamps
```

Or to install the latest version.

```
pip [--user] install git+https://github.com/waqasbhatti/fits-to-stamps
```

Once the installation is done, you'll be able to execute the script as
`fits-to-stamps` if the virtualenv is active (or `~/.local/bin` for `pip --user`
installs is in your $PATH).

To use it without needing the virtualenv active all the time, add an alias to
your `~/.bashrc`:

```
alias fits-to-stamps="/path/to/your/virtualenv/bin/fits-to-stamps"
```

That should make it run with the correct Python interpreter in the virtualenv.


## License

This is provided under the MIT license. See the LICENSE file for the full text.
