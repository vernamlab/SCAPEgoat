from __future__ import annotations

import chipwhisperer as cw
import cwtvla.ktp
import numpy as np
from WPI_SCA_LIBRARY.FileFormat import *
import os
import tqdm as tqdm


class CWScope:

    def __init__(self, firmware_name, gain=25, num_samples=5000, offset=0, target_type=cw.targets.SimpleSerial):
        """
        Initializes a CW scope object
        :param firmware_name: The name of the compiled firmware that will be loaded on the CW device.
        :param gain: The gain of the CW scope
        :param num_samples: The number of samples to collect for each trace on the CW scope
        :param offset: The offset of the trace collection
        """
        # setup scope
        self.scope = cw.scope()
        self.scope.default_setup()
        self.target = cw.target(self.scope, target_type)

        # configure scope parameters
        self.scope.gain.db = gain
        self.scope.adc.samples = num_samples
        self.scope.offset = offset

        # upload encryption algorithm firmware to the board
        cw.program_target(self.scope, cw.programmers.STM32FProgrammer,
                          os.path.dirname(os.path.abspath(__file__)) + "\\firmware\\{}".format(
                              firmware_name))

    def disconnect(self):
        """Disconnect CW Scope and Target"""
        self.scope.dis()
        self.target.dis()

    def standard_capture_traces(self, num_traces: int,
                                experiment_keys: list | np.ndarray = None,
                                experiment_texts: list | np.ndarray = None,
                                fixed_key: bool = False,
                                fixed_pt: bool = False) -> (np.ndarray, np.ndarray, np.ndarray, np.ndarray):
        """
        Capture procedure for ChipWhisperer devices. Will return a specified number of traces and the data associated
        with the collection.

        :param num_traces: The number of traces to capture
        :type num_traces: int
        :param experiment_keys: A collection of keys to use for the capture of each trace. If not specified, the procedure
                                will use the cw basic key generation `key = cw.ktp.Basic()[0]`
        :type experiment_keys: list or np.ndarray
        :param experiment_texts: A collection of texts to use for the capture of each trace. If not specified, the procedure
                                will use the cw basic plaintext generation `text = cw.ktp.Basic()[1]`
        :type experiment_texts: list or np.ndarray
        :param fixed_key: Whether to use a fixed key for cw.ktp key generation. Ignored if a collection of keys are supplied.
        :type fixed_key: bool
        :param fixed_pt: Whether to use a fixed plaintext for cw.ktp text generation. Ignored if a collection of texts are supplied.
        :type fixed_pt: bool
        :return: a tuple containing the power traces, keys, plaintexts, and ciphertexts for the experiment
        :rtype: tuple(np.ndarray, np.ndarray, np.ndarray, np.ndarray)
        :raises TypeError: if the length of the specified experiment keys and experiment texts are not equal to each other or the number of traces
                            to be collected.
        :Authors: Samuel Karkache (swkarkache@wpi.edu)
        """

        # reject bad params
        if experiment_texts is not None and len(experiment_texts) != num_traces:
            raise TypeError("The collection of plaintext must be the same length as the number of traces to be collected")
        if experiment_keys is not None and len(experiment_keys) != num_traces:
            raise TypeError("The collections of keys must be the same length as the number of traces to be collected")
        if experiment_texts is not None and experiment_keys is not None:
            if len(experiment_texts) != len(experiment_keys):
                raise TypeError("The length of the collection keys is not equal to the length of the collection of texts")

        # init return values
        traces = np.empty([num_traces], dtype=object)
        keys = np.empty([num_traces], dtype=object)
        texts = np.empty([num_traces], dtype=object)
        ciphertexts = np.empty([num_traces], dtype=object)

        # standard ktp setup, can be bypassed if keys or texts array are None type
        ktp = cw.ktp.Basic()
        ktp.fixed_key = fixed_key
        ktp.fixed_text = fixed_pt

        for i in tqdm.tqdm(range(num_traces), desc="Capturing {} Traces".format(num_traces)):

            if experiment_keys is None:
                key = ktp.next()[0]
            else:
                key = experiment_keys[i]
            if experiment_texts is None:
                text = ktp.next()[1]
            else:
                text = experiment_texts[i]

            # capture trace
            trace = cw.capture_trace(self.scope, self.target, text, key)

            # append arrays if trace successfully captured
            if trace is None:
                continue

            traces[i] = trace.wave
            keys[i] = trace.key
            texts[i] = trace.textin
            ciphertexts[i] = trace.textout

        return traces, keys, texts, ciphertexts

    def capture_traces_tvla(self, num_traces: int, ktp: any = cwtvla.ktp.FixedVRandomText()) -> (np.ndarray, np.ndarray):
        """
        Captures fixed and random trace set needed for TVLA
        :param num_traces: the number of traces to capture for each set
        :param ktp: the key text pair algorithm, defaults to cwtvla.ktp.FixedVRandomText(). To use a custom ktp, you would
                    need to provide a class that has methods named `next_group_A()` that specifies the fixed text/key and
                    a method named `next_group_B()` that specifies
        :return: (fixed_traces, random_traces)
        """
        rand_traces = np.empty([num_traces], dtype=object)
        fixed_traces = np.empty([num_traces], dtype=object)

        for i in tqdm.tqdm(range(num_traces), desc='Capturing Fixed and Random Trace Sets'):
            # capture trace from fixed group
            key, pt = ktp.next_group_A()
            trace = cw.capture_trace(self.scope, self.target, pt, key)
            if trace is not None:
                fixed_traces[i] = trace.wave

            # capture trace from random group
            key, pt = ktp.next_group_B()
            trace = cw.capture_trace(self.scope, self.target, pt, key)
            if trace is not None:
                rand_traces[i] = trace.wave

        return fixed_traces, rand_traces
