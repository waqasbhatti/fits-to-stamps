#!/usr/bin/env python

'''
fits_to_stamps.py - Waqas Bhatti (wbhatti@astro.princeton.edu) - Sep 2018.
License: MIT. See the LICENSE file for the full text.

'''

import os
import os.path
import argparse
import sys
import glob

import multiprocessing as mp

import numpy as np
from PIL import Image
from astropy.io import fits as pyfits
from astropy.visualization import ZScaleInterval



def read_fits(fits_file,ext=0):
    '''
    Shortcut function to get the header and data from a fits file and a given
    extension.

    '''

    hdulist = pyfits.open(fits_file)
    img_header = hdulist[ext].header
    img_data = hdulist[ext].data
    hdulist.close()

    return img_data, img_header



def compressed_fits_ext(fits_file):
    '''
    Check if a fits file is a compressed FITS file. Return the extension numbers
    of the compressed image as a list if these exist, otherwise, return None.

    '''

    hdulist = pyfits.open(fits_file)

    compressed_img_exts = []

    for i, ext in enumerate(hdulist):
        if isinstance(ext,pyfits.hdu.compressed.CompImageHDU):
            compressed_img_exts.append(i)

    hdulist.close()

    if len(compressed_img_exts) < 1:
        return None
    else:
        return compressed_img_exts



def read_fits_header(fits_file, ext=0):
    '''
    Shortcut function to just read the header of the FITS file and return it.

    '''
    hdulist = pyfits.open(fits_file)
    img_header = hdulist[ext].header
    hdulist.close()

    return img_header



def trim_image(fits_img,
               fits_hdr,
               trimkeys=('TRIMSEC','DATASEC','TRIMSEC0'),
               custombox=None):
    '''
    Returns a trimmed image using the TRIMSEC header of the image header.

    custombox is a string of the form [Xlo:Xhi,Ylo:Yhi] and will trim the image
    to a custom size.

    '''

    if custombox:

        trimsec = custombox

    else:

        trimsec = None

        for h in trimkeys:
            if h in fits_hdr:
                trimsec = fits_hdr[h]
                break
        else:
            if custombox is None:
                print('no DATASEC or TRIMSEC in image header')
                return

    if trimsec and trimsec != '[0:0,0:0]':

        datasec = trimsec.strip('[]').split(',')

        try:
            datasec_y = [int(x) for x in datasec[0].split(':')]
            datasec_x = [int(x) for x in datasec[1].split(':')]

            trimmed_img = fits_img[datasec_x[0]-1:datasec_x[1],
                                   datasec_y[0]-1:datasec_y[1]]
        except ValueError as e:
            print('datasec/trimsec not correctly set in FITS header, '
                  ' not trimming')
            trimmed_img = fits_img

    else:
        print('datasec/trimsec not correctly set in FITS header, '
              ' not trimming')
        trimmed_img = fits_img

    return trimmed_img



def clipped_linscale_img(img_array,
                         lo, hi,
                         cap=255.0):
    '''
    This clips the image between the values:

    [median(img_array) - lo, median(img_array) + hi]

    and returns a linearly scaled image using the cap given.

    '''

    img_med = np.median(img_array)
    clipped_linear_img = np.clip(img_array,
                                 img_med-lo,
                                 img_med+hi)
    return cap*clipped_linear_img/(img_med+hi)



def img_to_stamps(img,
                  stampsize=256):
    '''
    Generate stamps for an image of size imgsizex x imgsize y. Stamps not in the
    center of the image will be generated for the edges of the image. This
    generates 3 x 3 stamps for each image.

    top_left_corner = img[:xstampsize,:ystampsize]
    bottom_right_corner = img[-xstampsize:,-ystampsize:]

    top_right_corner = img[imgsizex-xstampsize:,:ystampsize]
    bottom_left_corner = img[:xstampsize,imgsizey-ystampsize:]

    top_center = img[
                   imgsizex/2-xstampsize/2:imgsizex/2+xstampsize/2,:ystampsize
                 ]
    bottom_center = img[imgsizex/2-xstampsize/2:imgsizex/2+xstampsize/2,
                        imgsizey-ystampsize:]

    center = img[imgsizex/2-xstampsize/2:imgsizex/2+xstampsize/2,
                 imgsizey/2-ystampsize/2:imgsizey/2+ystampsize/2]

    right_center = img[imgsizex-xstampsize:,
                       imgsizey/2-ystampsize/2:imgsizey/2+ystampsize/2]
    left_center = img[
                    :xstampsize,imgsizey/2-ystampsize/2:imgsizey/2+ystampsize/2
                  ]


    '''

    imgsizex, imgsizey = img.shape
    xstampsize, ystampsize = stampsize, stampsize

    # get the total number of possible stamps
    n_possible_xstamps = imgsizex/float(xstampsize)
    n_possible_ystamps = imgsizey/float(ystampsize)


    # if we can actually make stamps, then go ahead
    if (n_possible_xstamps >= 3) and (n_possible_ystamps >= 3):

        topleft = img[:xstampsize,:ystampsize]
        topcenter = img[
            int(imgsizex/2-xstampsize/2):int(imgsizex/2+xstampsize/2),
            :ystampsize
        ]
        topright = img[imgsizex-xstampsize:,:ystampsize]
        midleft = img[
            :xstampsize,
            int(imgsizey/2-ystampsize/2):int(imgsizey/2+ystampsize/2)
        ]
        midcenter = img[
            int(imgsizex/2-xstampsize/2):int(imgsizex/2+xstampsize/2),
            int(imgsizey/2-ystampsize/2):int(imgsizey/2+ystampsize/2)
        ]
        midright = img[
            imgsizex-xstampsize:,
            int(imgsizey/2-ystampsize/2):int(imgsizey/2+ystampsize/2)
        ]
        bottomleft = img[:xstampsize,imgsizey-ystampsize:]
        bottomcenter = img[
            int(imgsizex/2-xstampsize/2):int(imgsizex/2+xstampsize/2),
            imgsizey-ystampsize:
        ]
        bottomright = img[-xstampsize:,-ystampsize:]

        return {
            'topleft':topleft,
            'topcenter':topcenter,
            'topright':topright,
            'midleft':midleft,
            'midcenter':midcenter,
            'midright':midright,
            'bottomleft':bottomleft,
            'bottomcenter':bottomcenter,
            'bottomright':bottomright
        }

    else:
        print('stampsize is too large for this image')
        return None



def zscale_image(imgarr):
    '''
    This zscales an image.

    '''

    zscaler = ZScaleInterval()
    scaled_vals = zscaler.get_limits(imgarr)
    return clipped_linscale_img(imgarr, scaled_vals[0], scaled_vals[1])



def fits_to_zscaled_stamps(fits_image,
                           outfile,
                           fits_extension=None,
                           trimkeys='TRIMSEC,DATASEC,TRIMSEC0',
                           stampsize=256,
                           separatorwidth=1):
    '''
    This turns an FITS image into a zscaled image, stamps it, and returns a PNG.

    '''

    compressed_ext = compressed_fits_ext(fits_image)

    if fits_extension is None and compressed_ext:
        img, hdr = read_fits(fits_image,
                             ext=compressed_ext[0])
    elif (fits_extension is not None):
        img, hdr = read_fits(fits_image, ext=fits_extension)
    else:
        img, hdr = read_fits(fits_image)

    trimmed_img = trim_image(img, hdr, trimkeys.split(','))
    scaled_img = zscale_image(trimmed_img)
    image_stamps = img_to_stamps(scaled_img, stampsize=stampsize)

    toprow_xsize, toprow_ysize = image_stamps['topright'].shape
    toprow_separr = np.array([[255.0]*separatorwidth]*toprow_ysize)

    # build stacks

    topleft = image_stamps['topleft']
    midleft = image_stamps['midleft']
    bottomleft = image_stamps['bottomleft']

    topcenter = image_stamps['topcenter']
    midcenter = image_stamps['midcenter']
    bottomcenter = image_stamps['bottomcenter']

    topright = image_stamps['topright']
    midright = image_stamps['midright']
    bottomright = image_stamps['bottomright']

    toprow_stamp = np.hstack((topleft,
                              toprow_separr,
                              midleft,
                              toprow_separr,
                              bottomleft))

    midrow_xsize, midrow_ysize = midright.shape
    midrow_separr = np.array([[255.0]*separatorwidth]*midrow_ysize)

    # similarly, these should be midleft, midcenter, midright
    midrow_stamp = np.hstack((topcenter,
                              midrow_separr,
                              midcenter,
                              midrow_separr,
                              bottomcenter))

    bottomrow_xsize, bottomrow_ysize = bottomright.shape
    bottomrow_ysize = bottomright.shape[1]
    bottomrow_separr = np.array([[255.0]*separatorwidth]*bottomrow_ysize)

    # similarly, these should be bottomleft, bottomcenter, bottomright
    bottomrow_stamp = np.hstack((topright,
                                 bottomrow_separr,
                                 midright,
                                 bottomrow_separr,
                                 bottomright))

    full_stamp = np.vstack(
        (toprow_stamp,
         np.array([255.0]*(toprow_xsize*3 + separatorwidth*2)),
         midrow_stamp,
         np.array([255.0]*(midrow_xsize*3 + separatorwidth*2)),
         bottomrow_stamp)
    )

    full_stamp = np.flipud(full_stamp)
    pillow_image = Image.fromarray(full_stamp)
    pillow_image = pillow_image.convert('L')
    pillow_image.save(outfile)

    return outfile



def parallel_fits_worker(task):
    '''
    This is a parallel worker for the FITS to stamps process.

    '''

    fits, options = task

    try:

        outpng = os.path.splitext(os.path.basename(fits))[0] + '.png'
        outpngpath = os.path.join(os.path.dirname(fits), outpng)
        donepng = fits_to_zscaled_stamps(
            fits,
            outpngpath,
            **options
        )

        print('%s -> %s OK' % (fits, outpng))
        return donepng

    except Exception as e:
        print('could not convert %s to stamp PNG: %s, error was: %r' %
              (fits, e))
        return None



def main():
    '''
    This is the main function.

    '''

    aparser = argparse.ArgumentParser(
        description='convert a FITS to 3 x 3 stamps.'
    )

    aparser.add_argument(
        'target',
        action='store',
        type=str,
        help=("path to a single FITS file or "
              "a directory of FITS files to convert")
    )

    aparser.add_argument(
        '--trimsec',
        action='store',
        type=str,
        default='TRIMSEC,DATASEC,TRIMSEC0',
        help=('the FITS header keys containing '
              'the TRIMSEC section. All of the keys '
              'in the CSV list provided will be tried. default: %(default)s')
    )

    aparser.add_argument(
        '--fitsext',
        action='store',
        type=str,
        default=None,
        help=('the FITS extension number containing '
              'the image to work on. default: automatic detection '
              'for normal and .fits.fz files')
    )

    aparser.add_argument(
        '--stampsize',
        action='store',
        type=int,
        default=256,
        help=('the individual stamp size in pixels. default: %(default)s')
    )

    aparser.add_argument(
        '--separatorwidth',
        action='store',
        type=int,
        default=1,
        help=('the width of the separator lines '
              'between stamps in pixels. default: %(default)s')
    )

    aparser.add_argument(
        '--fitsglob',
        action='store',
        type=str,
        default='*.fits*',
        help=('the file glob to use to '
              'recognize FITS files in a directory. default: %(default)s')
    )

    aparser.add_argument(
        '--workers',
        action='store',
        type=int,
        default=mp.cpu_count(),
        help=('number of parallel workers to operate on multiple FITS files'
              ' default: %(default)s')
    )


    args = aparser.parse_args()

    if os.path.exists(args.target) and os.path.isdir(args.target):

        fits = glob.glob(os.path.join(args.target, args.fitsglob))
        manyfits = True

    elif os.path.exists(args.target) and os.path.isfile(args.target):
        fits = args.target
        manyfits = False

    else:
        print("the target file or directory: %s does not exist." % args.target)
        sys.exit(1)


    if not manyfits:

        # if there's a single file, process it
        outpng = os.path.splitext(os.path.basename(args.target))[0] + '.png'
        outpngpath = os.path.join(os.path.dirname(args.target), outpng)

        try:

            donepng = fits_to_zscaled_stamps(
                fits,
                outpngpath,
                stampsize=args.stampsize,
                trimkeys=args.trimsec,
                separatorwidth=args.separatorwidth,
                fits_extension=args.fitsext,
            )

            print('%s -> %s OK' % (fits, donepng))
            sys.exit(0)


        except Exception as e:
            print('failed to make a stamp for %s' % fits)
            raise

    # if there are many fits, we'll launch multiple processes
    else:

        tasks = [(x, {'fits_extension':args.fitsext,
                      'trimkeys':args.trimsec,
                      'stampsize':args.stampsize,
                      'separatorwidth':args.separatorwidth}) for x in
                 fits]

        pool = mp.Pool(args.workers)
        pool.map(parallel_fits_worker, tasks)
        pool.close()
        pool.join()

        sys.exit(0)


if __name__ == '__main__':
    main()
