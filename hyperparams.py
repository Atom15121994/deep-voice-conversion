# -*- coding: utf-8 -*-
#/usr/bin/python2
'''
By kyubyong park. kbpark.linguist@gmail.com. 
https://www.github.com/kyubyong/vc
'''


class Hyperparams:
    '''Hyper parameters'''
    # signal processing
    sr = 16000 # Sampling rate.
    frame_shift = 0.005 # seconds
    frame_length = 0.025 # seconds
    hop_length = int(sr*frame_shift) # samples.  This is dependent on the frame_shift.
    n_fft = int(sr*frame_length) # samples. This is dependent on the frame_length.
    win_length = n_fft  # TODO cross check
    n_mfcc = 20
    n_iter = 30 # Number of inversion iterations

    # model
    hidden_units = 256 # alias = E
    encoder_num_banks = 16
    decoder_num_banks = 8
    num_highwaynet_blocks = 4
    norm_type = 'ins'  # a normalizer function. value: bn, ln, ins, or None
    dropout_rate = 0.2

    # training scheme
    lr = 0.0005
    batch_size = 32
    num_epochs = 10000